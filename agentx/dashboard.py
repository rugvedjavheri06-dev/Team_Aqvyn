"""Live dashboard (stdlib only):  python -m agentx.dashboard [--llm stub|http|none]  then open http://localhost:8765"""
from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .agent import Agent
from .config import LLMConfig
from .data import synthetic_market
from .journal import Journal
from .llm import HttpLLM
from .memory import Memory
from .risk import KillSwitch
from .session import TradingSession
from .stub_llm import StubLLM


class App:
    def __init__(self, llm_kind: str, seed: int = 7, days: int = 360):
        self.llm_kind, self.seed, self.days = llm_kind, seed, days
        self.lock = threading.RLock()
        self.running, self.interval = False, 0.6
        self.queued, self.busy, self._cache = 0, False, None
        self.reset()

    def reset(self, seed=None) -> None:
        with self.lock:
            if seed is not None:
                self.seed = seed
            self.running = False
            market = synthetic_market(days=self.days, seed=self.seed)
            self.agent = None if self.llm_kind == "none" else Agent(HttpLLM(LLMConfig.from_env()) if self.llm_kind == "http" else StubLLM())
            self.kill = KillSwitch("KILL_SWITCH")
            self.session = TradingSession(market, agent=self.agent, journal=Journal(), memory=Memory(),
                                          kill_switch=self.kill, start_idx=60)
            self.queued = 0
            self.session.step()  # first mark so the chart has a point
            self._cache = self._snapshot()

    def step(self, n: int = 1) -> None:
        """Queue n days; the worker thread runs them so HTTP requests never wait on a slow LLM."""
        self.queued += n

    def loop(self) -> None:
        last = 0.0
        while True:
            time.sleep(0.05)
            go = self.queued > 0 or (self.running and time.time() - last >= self.interval)
            if not go:
                continue
            with self.lock:
                if self.session.done:
                    self.running, self.queued = False, 0
                    continue
                self.busy = True
                try:
                    self.session.step()
                finally:
                    self.busy = False
                self.queued = max(0, self.queued - 1)
                self._cache = self._snapshot()
            last = time.time()

    def state(self) -> dict:
        """Lock-free read of the last snapshot, with the live kill-switch status overlaid."""
        d = dict(self._cache or {})
        d["busy"] = self.busy
        d["running"] = self.running
        d["risk"] = {**d.get("risk", {}), "kill": self.kill.is_engaged(), "kill_reason": self.kill.reason}
        return d

    def _snapshot(self) -> dict:
        with self.lock:
            s = self.session
            c = s.gatekeeper.cfg
            closes = s.last_closes
            eq, bench = s.current_equity, (s.bench[-1] if s.bench else s.initial_cash)
            rep = s.report()
            positions = [{"symbol": sym, "qty": p.qty, "avg": round(p.avg_price, 2), "last": round(closes.get(sym, p.avg_price), 2),
                          "pnl_pct": round((closes.get(sym, p.avg_price) / p.avg_price - 1) * 100, 2),
                          "stop": round(p.stop, 2) if p.stop else None, "strategy": p.strategy}
                         for sym, p in s.broker.positions.items()]
            return {
                "date": s.date, "day": s.t - s.start_idx + 1, "total_days": len(s.market) - s.start_idx,
                "done": s.done, "running": self.running, "interval": self.interval,
                "llm": {"kind": self.llm_kind, "offline": bool(self.agent and self.agent.offline),
                        "model": getattr(getattr(getattr(self.agent, "llm", None), "cfg", None), "model", "") if self.llm_kind == "http" else "",
                        "last_error": self.agent.last_error if self.agent else ""},
                "curve": {"dates": s.dates, "agent": [round(x, 2) for x in s.equity], "bench": [round(x, 2) for x in s.bench]},
                "equity": round(eq, 2), "bench_equity": round(bench, 2), "cash": round(s.broker.cash, 2),
                "day_pnl_pct": round(s.day_pnl * 100, 2),
                "max_dd": rep["agent"]["max_drawdown_pct"], "bench_max_dd": rep["buy_and_hold"]["max_drawdown_pct"],
                "strategy": s.strategy, "positions": positions,
                "risk": {"kill": s.kill.is_engaged(), "kill_reason": s.kill.reason, "daily_limit": c.daily_loss_limit_pct * 100,
                         "risk_per_trade": c.risk_per_trade_pct * 100, "max_pos": c.max_position_pct * 100,
                         "max_open": c.max_open_positions, "gross_pct": round(100 * s.exposure[-1], 1) if s.exposure else 0,
                         "max_gross": c.max_gross_exposure_pct * 100,
                         "halted_today": s.day_pnl <= -c.daily_loss_limit_pct},
                "stats": s.stats, "trades": rep["trades"],
                "journal": s.journal.latest(40), "traces": list(reversed(s.traces[-6:])),
            }


class Handler(BaseHTTPRequestHandler):
    app: App
    wbufsize = 65536  # one packet per response (avoids Nagle/delayed-ACK stalls on Windows)

    def log_message(self, *a):  # quiet
        pass

    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(204, b"", "text/plain")

    def do_GET(self):
        if self.path == "/api/state":
            self._send(200, json.dumps(self.app.state(), default=float).encode(), "application/json")
        elif self.path in ("/", "/index.html"):
            self._send(200, PAGE.encode("utf-8"), "text/html; charset=utf-8")
        else:
            self._send(404, b"not found", "text/plain")

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(n) or b"{}") if n else {}
        a, p = self.app, self.path
        if p == "/api/step":
            a.step(int(body.get("n", 1)))
        elif p == "/api/play":
            a.running = True
        elif p == "/api/pause":
            a.running = False
        elif p == "/api/speed":
            a.interval = max(0.05, min(3.0, float(body.get("interval", 0.6))))
        elif p == "/api/kill":  # deliberately lock-free: the kill switch must never wait on the LLM
            a.kill.engage("human pressed the kill switch", flatten=bool(body.get("flatten")))
        elif p == "/api/release":
            a.kill.release()
        elif p == "/api/reset":
            a.reset(body.get("seed"))
        elif p == "/api/llm-reset" and a.agent:
            a.agent.reset()
        else:
            return self._send(404, b"not found", "text/plain")
        self._send(200, b"{}", "application/json")


def main(argv=None) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--llm", choices=["stub", "http", "none"], default="stub")
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8765)))
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args(argv)
    app = App(a.llm, a.seed)
    Handler.app = app
    threading.Thread(target=app.loop, daemon=True).start()
    srv = ThreadingHTTPServer(("0.0.0.0", a.port), Handler)
    print(f"AgentX paper-trading dashboard: http://0.0.0.0:{a.port}  (llm={a.llm}, paper trading + synthetic data)  Ctrl+C to stop")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


# The page lives in ui.html (the same file is deployed as frontend/index.html on Vercel).
PAGE = (Path(__file__).with_name("ui.html")).read_text(encoding="utf-8")


if __name__ == "__main__":
    main()
