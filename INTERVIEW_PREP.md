# AgentX Hackathon 2026 — Master Interview & Technical Q&A Defense Guide

**Team**: Team Aqvyn (Team Code: `884BC4`)  
**Track**: PS-02 · Agentic Trading Bot (Paper Trading)  
**Panel**: Panel 3 | **Slot**: 12 Nov 2026, 12:00 PM – 12:10 PM IST (10 Minutes Total)  
**Meeting Link**: [https://meet.google.com/dhr-iutc-ngk](https://meet.google.com/dhr-iutc-ngk)  
**Submission Status**: ✅ **SUBMITTED** (Portal: [Hack4Hack Workspace Submission](https://hack4hack.com/workspace/6adcdbcf4f5a8ca17dbb87c4?tab=submission))

---

## 📌 Verified Official Submission Links (Keep Open in Tabs)

| Deliverable | Live Verified URL | Purpose during Interview |
|---|---|---|
| 🌐 **Live Web Demo** | [https://teamaqvyn-frontend.vercel.app](https://teamaqvyn-frontend.vercel.app) | Primary screen-share browser tab for the 5-min demo |
| 💻 **GitHub Repository** | [https://github.com/rugvedjavheri06-dev/Team_Aqvyn](https://github.com/rugvedjavheri06-dev/Team_Aqvyn) | Public repo tab to show code & README to judges |
| 🐍 **Backend API Service** | [https://team-aqvyn.onrender.com](https://team-aqvyn.onrender.com) | FastAPI / HTTP SSE backend endpoint |
| 📊 **Presentation Deck** | [Google Drive Presentation](https://drive.google.com/file/d/1rV4e1K_grsY6Pz2GzKMNPqtnXCD85aC8/view?usp=sharing) | Backup slides if judges ask for presentation overview |
| 🎥 **Demo Video** | [Google Drive Demo Video](https://drive.google.com/file/d/1wfJMJkuz2eXX0SU-QFlUk6z8VkM4E0NO/view?usp=sharing) | 2:36 video submitted on portal |

---

## ⏱️ The 10-Minute Winning Breakdown

```
[0:00 - 0:45]  The Killer Hook & Thesis ("The LLM proposes; deterministic code disposes")
[0:45 - 3:00]  Live UI Demo (Left: Model Tools, Middle: Trade Journal, Right: Code Gatekeeper)
[3:00 - 3:45]  Kill Switch Demo (Engage switch, show immediate entry rejection & flattening)
[3:45 - 5:00]  Honest Robustness & Engineering Resilience (30-market Monte Carlo, circuit breaker)
[5:00 - 10:00] Technical Q&A with Panel 3 Judges
```

### Golden Rules for the Interview
1. **Never claim "Our AI beats the market every day."** Hackathon judges hate exaggerated financial claims. Instead, pitch: *"We built an autonomous paper trader with deterministic risk control that guarantees safety, eliminates hallucinations, and protects capital in bear markets."*
2. **Keep the Live Vercel Demo and VS Code open side-by-side**. When asked about a feature, immediately switch to the exact file and line number.
3. **Keep answers to 30–45 seconds**. Leave room for judges to ask more follow-up questions.

---

## 🎬 5-Minute Live Pitch & Screen-Share Demo Script

### Minute 0:00 – 0:45 | The Opening Hook & Problem Statement
> *"Hello judges, we are Team Aqvyn, presenting AgentX for Problem Statement 02: The Agentic Paper-Trading Bot.*  
> *Every AI trading bot on the internet tries to impress you with how much money it allegedly made. **Ours shows you what the model was NOT allowed to do.***  
> *The fundamental flaw with LLMs in finance is that language models hallucinate, miscalculate numbers, and suffer from FOMO. Giving an LLM direct API access to place trades is catastrophic.*  
> *Our core design thesis is: **The LLM proposes; deterministic code disposes.** The model can analyze news, backtest candidate strategies itself, and explain its thesis in plain English, but it has ZERO execution authority. Position sizing, stop-losses, daily loss limits, and a human kill switch live in immutable Python code that no model prompt can ever bypass."*

### Minute 0:45 – 3:00 | 3-Column Live Dashboard Walkthrough
> *(Screen share browser at [https://teamaqvyn-frontend.vercel.app](https://teamaqvyn-frontend.vercel.app) or local `http://localhost:8765`)*  
> 1. *"Notice the three decoupled columns on our trading terminal:*  
> 2. ***Left Column (ReAct Agent & Tool Calls)**: Here you see the model's transparent reasoning trace. Every 20 days, it calls `get_market_overview` to gauge volatility, and runs trailing-window backtests on candidates (`sma_crossover`, `rsi_mean_reversion`, `breakout`) using `run_backtest`. When an entry signal appears, it calls `get_news` to read sentiment. If news is bad, it issues a veto.*  
> 3. ***Middle Column (Plain-Language Journal)**: Every trade execution and skipped trade is written in plain English. It logs the entry reason, the exact stop-loss price, and the maximum worst-case dollar loss.*  
> 4. ***Right Column ('Code Decides' Risk Gatekeeper)**: This is the part the model cannot touch. Four hard mathematical caps govern every trade: a 1% risk budget per trade, a 20% single position cap, an 80% gross exposure cap (keeping 20% cash reserve), and a 2% daily loss limit."*

### Minute 3:00 – 3:45 | The Human Kill Switch Demonstration
> *(Point to the Kill Switch on screen)*  
> *"Now watch our **Human Kill Switch**. I tick 'Also sell everything' and click **Kill Switch**.*  
> *(Button turns red)*  
> *Observe what happens: pending buy orders are cancelled instantly. When we step forward, the gatekeeper blocks all entries with the reason: 'Human kill switch engaged: no new entries'. Crucially, exits and stop-losses are still allowed to run, and existing positions are liquidated at the open, because closing positions reduces portfolio risk."*

### Minute 3:45 – 5:00 | Honest Numbers & Engineering Resilience
> *"We didn't cherry-pick one lucky market seed. In `agentx/robustness.py`, we evaluated across 30 independent synthetic markets. In falling markets, our agent lost only **-1.2%** while Buy-and-Hold dropped **-11.7%**, cutting maximum drawdown by nearly two-thirds.*  
> *Finally, our system is engineered for enterprise reliability: if the external LLM gateway fails 3 times, an automated circuit breaker trips and falls back to deterministic rule-based trading at half size so the bot never crashes. We have 26 passing unit tests. We are ready for your questions."*

---

## 🎯 High-Probability Technical Q&A Defense

---

### Category A: Institutional Risk & Wall Street Standards (Judge Ishwar Jha / JPMorgan Chase Alignment)

#### Q1: "How does your architecture align with real-world financial regulations (e.g., FINRA 15c3-5, SEBI, or SEC algorithmic trading rules)?"
* **30-Second Answer**:  
  "Under **FINRA Rule 15c3-5 (Market Access Rule)** and institutional risk standards, all pre-trade risk checks must be independent, hard-coded, and immune to algorithmic or model bypass.  
  AgentX implements this exact separation:
  1. The LLM sits strictly in the **Analyst layer** (`agent.py`) with read-only tools. It cannot invoke order placement.
  2. The **Deterministic Gatekeeper** (`risk.py`) enforces pre-trade compliance: 1% risk cap, 20% single position limit, 80% gross exposure cap, 2% daily loss limit, and a hardware/software kill switch.
  3. Under **Model Risk Management guidelines (SR 11-7)**, our plain-language journal (`journal.md` and `journal.jsonl`) produces a complete audit trail explaining why every trade was executed or rejected."
* **Code Reference**: [`agentx/risk.py` Lines 110–128](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/risk.py#L110-L128) & [`agentx/journal.py` Lines 13–39](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/journal.py#L13-L39).

#### Q2: "What prevents the LLM from hallucinating an order, inventing a ticker, or buying 1,000,000 shares?"
* **30-Second Answer**:  
  "The LLM has zero execution capability. The agent only outputs a qualitative `decision` ('confirm' or 'veto') and a `conviction` float between 0.0 and 1.0.  
  1. In `risk.py`, our `RiskGatekeeper` clamps conviction (`min(max(conviction, 0.0), 1.0)`). Conviction can only **shrink** position size, never enlarge it.  
  2. The actual share quantity is mathematically calculated as the minimum of four hard caps. If the result is under 1 share, it is rejected.  
  3. In our test suite, `test_llm_cannot_enlarge_or_bypass_risk` runs a deliberately hostile model demanding 100x leverage and confirms all limits hold."
* **Code Reference**: [`agentx/risk.py` Lines 113–121](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/risk.py#L113-L121) and [`tests/test_core.py` Line 154](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/tests/test_core.py#L154).

---

### Category B: Distributed Systems, Failures & Reliability

#### Q3: "What happens if your LLM gateway times out, rate-limits, or crashes during a live trading session?"
* **30-Second Answer**:  
  "We have a dual-layer resilience architecture:
  1. **Graceful Fallback**: In `session.py`, if an LLM call throws `LLMError` or fails JSON parsing, the system immediately falls back to deterministic rule-based trading at **half size** (conviction = 0.5) and records the incident in `journal.md`.
  2. **Circuit Breaker**: In `agent.py`, if 3 consecutive failures occur (`fail_limit = 3`), the circuit breaker opens (`self.offline = True`). The bot stops waiting on the remote API and continues running smoothly without hanging."
* **Code Reference**: [`agentx/agent.py` Lines 97–101](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/agent.py#L97-L101) & [`agentx/session.py` Lines 247–251](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/session.py#L247-L251).

#### Q4: "When the LLM takes 5–10 seconds to generate a response, does the dashboard freeze? Can a user still hit the kill switch?"
* **30-Second Answer**:  
  "No, the UI stays completely responsive. In `dashboard.py`, trading steps run on a dedicated background worker daemon thread (`app.loop`).  
  Endpoints like `/api/state` and `/api/kill` return immediately in `< 10ms` from a thread-safe in-memory cache. A user can hit the Kill Switch instantly even while the LLM is mid-thought. We verified this with a dedicated unit test, `test_state_and_kill_switch_never_wait_on_the_llm`."
* **Code Reference**: [`agentx/dashboard.py` Lines 48–75](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/dashboard.py#L48-L75) and [`tests/test_dashboard.py` Line 31](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/tests/test_dashboard.py#L31).

#### Q5: "What stops the model from being lazy and claiming 'no news' without actually calling the tool?"
* **30-Second Answer**:  
  "During real model testing with Gemini, we caught the model occasionally skipping tools and hallucinating 'no news'. We fixed this by introducing **Required Tool Enforcement** in `agent.py`.  
  The agent tracks invoked tools in `called`. If the model attempts to return a final answer before invoking required tools (`get_news:<symbol>` for signals, or `run_backtest:<strategy>` for strategy selection), the agent bounces the response with a corrective nudge. If it fails again, it falls back to rules."
* **Code Reference**: [`agentx/agent.py` Lines 121–130](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/agent.py#L121-L130) and [`tests/test_core.py` Line 182](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/tests/test_core.py#L182).

---

### Category C: Financial Realism & Backtest Integrity

#### Q6: "How did you eliminate Lookahead Bias in your simulation?"
* **30-Second Answer**:  
  "We enforce strict chronological time-stepping in `session.py`:
  1. All strategy signals and agent decisions are calculated at the **Close of day $t$** using data strictly up to index $t$.
  2. Orders are placed in a pending queue and fill at the **Open price of day $t+1$**.
  3. Stop-losses are evaluated against day $t+1$'s **Low price**. If the market gaps down below the stop, it executes at the worse open price.
  4. The backtester and the live paper trader share the exact same `TradingSession` class, ensuring backtests reflect true execution."
* **Code Reference**: [`agentx/session.py` Lines 101–126](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/session.py#L101-L126) and Lines 166–175.

#### Q7: "Do you model transaction friction, or are your returns zero-cost paper figures?"
* **30-Second Answer**:  
  "Every order in `PaperBroker` includes realistic market friction:
  - **Slippage**: 5 basis points ($0.05\%$) applied adversely to fills (buys fill at $Open \times 1.0005$, sells fill at $Open \times 0.9995$).
  - **Exchange Fees**: 2 basis points ($0.02\%$) deducted from cash upon fill.
  Because the backtest engine shares this broker, backtests cannot be more optimistic than live runs."
* **Code Reference**: [`agentx/broker.py` Lines 38–43](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/broker.py#L38-L43) and Lines 49 & 64.

#### Q8: "If multiple buy signals trigger on the same day, could the bot overspend cash or exceed portfolio exposure?"
* **30-Second Answer**:  
  "No. We implemented a dynamic projection method called `_projected()` in `session.py`.  
  When evaluating the second or third signal on the same day, `_projected()` computes what cash and positions *will be* after earlier approved orders fill. Sizing is always evaluated against projected state, preventing accidental overdrafts or exposure breaches."
* **Code Reference**: [`agentx/session.py` Lines 231–239](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/session.py#L231-L239).

#### Q9: "Did your agent beat Buy-and-Hold? What were your actual numbers?"
* **30-Second Answer (Judges love this honesty)**:  
  "We ran a 30-market Monte Carlo simulation across different synthetic market regimes (`agentx/robustness.py`).
  - Across 30 markets, the agent beat buy-and-hold in **9 out of 30**.
  - In strong bull markets, it intentionally lags ($+4.5\%$ vs $+24.2\%$) because we mandate keeping $\ge 20\%$ in cash and enforce strict position caps.
  - In falling/bear markets, it preserves capital drastically: **$-1.2\%$ loss vs $-11.7\%$ for buy-and-hold**.
  - Mean maximum drawdown was cut to a third ($-5.6\%$ vs $-15.6\%$).
  Our value proposition is **capital preservation, drawdown mitigation, and disciplined risk**, not speculative market-beating."
* **Code Reference**: [`sample_output/robustness.txt`](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/sample_output/robustness.txt) and [`agentx/robustness.py` Lines 21–41](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/robustness.py#L21-L41).

---

### Category D: Memory, Explainability & Multi-Step Planning

#### Q10: "How does the agent's memory work across trading sessions?"
* **30-Second Answer**:  
  "In `memory.py`, whenever a trade is closed, the realised P&L percentage, symbol, date, and strategy are persisted to disk.  
  The `get_memory` tool aggregates win-rates and average P&L per strategy. During strategy selection every 20 days, the prompt explicitly instructs the LLM to 'distrust strategies with poor realised results in memory', creating an autonomous feedback loop."
* **Code Reference**: [`agentx/memory.py` Lines 9–35](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/memory.py#L9-L35) & [`agentx/session.py` Lines 190–192](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/session.py#L190-L192).

#### Q11: "Does this work with real LLMs or only the offline stub?"
* **30-Second Answer**:  
  "Both! We built `HttpLLM` in `llm.py`, which supports any OpenAI-compatible `/v1/chat/completions` endpoint (DeepSeek, Gemini, Groq, local Ollama).  
  In fact, our Windows launcher [`RUN_LIVE_DEMO.bat`](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/RUN_LIVE_DEMO.bat) and [`check_llm.py`](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/check_llm.py) test the real model connection, list available models, and run real strategy selection before launching."
* **Code Reference**: [`agentx/llm.py` Lines 10–55](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/agentx/llm.py#L10-L55) and [`RUN_LIVE_DEMO.bat`](file:///c:/Users/rugve/OneDrive/Desktop/chatAPP/AgentX/agentx-prototype/RUN_LIVE_DEMO.bat).

---

## 📂 Codebase Reference Cheat Sheet (Keep Open During Q&A)

| Topic | File | Line Numbers | Key Function / Symbol |
|---|---|---|---|
| **Architecture Philosophy** | `README.md` | L19 | *"The LLM proposes, deterministic code disposes"* |
| **ReAct Loop & JSON Parser** | `agentx/agent.py` | L25–56, L103–153 | `extract_json()`, `Agent._run()` |
| **Required Tools Enforcement** | `agentx/agent.py` | L121–130 | Bounces model if tool was skipped |
| **LLM Circuit Breaker** | `agentx/agent.py` | L97–101 | Trips after 3 failures (`fail_limit`) |
| **4 Sizing Caps** | `agentx/risk.py` | L113–121 | Risk budget (1%), 20% pos, 80% expo, cash |
| **Human Kill Switch** | `agentx/risk.py` | L45–70, L89–90 | Software flag & `KILL_SWITCH` file |
| **Daily Loss Limit (-2%)** | `agentx/risk.py` | L20, L91–92 | Halts entries when day down 2% |
| **Paper Broker Friction** | `agentx/broker.py` | L38–43, L49, L64 | 5 bps slippage, 2 bps fee |
| **Gap-Down Stop Execution** | `agentx/session.py` | L166–175 | Fills at open if market gapped below stop |
| **Dynamic Projection Sizing** | `agentx/session.py` | L231–239 | `_projected()` method prevents overspend |
| **Non-Blocking UI Thread** | `agentx/dashboard.py` | L48–67 | Background worker loop |
| **Unit Tests (26 total)** | `tests/test_core.py` | L154, L171, L182 | Adversarial, dead LLM, and tool skip tests |
| **Monte Carlo Robustness** | `agentx/robustness.py` | L21–41 | 30 synthetic market comparison |
