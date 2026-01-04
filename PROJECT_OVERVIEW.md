# Project Overview - 5ers 60K High Stakes Trading Bot

## What This Project Does

This is an **automated trading bot** that trades forex, indices, and commodities on MetaTrader 5 (MT5) for the **5ers 60K High Stakes** prop firm challenge.

### Key Results (Validated 2023-2025)

If this bot ran from January 2023 to December 2025:

| Metric | Result |
|--------|--------|
| **Starting Balance** | $60,000 |
| **Final Balance** | $1,160,462 |
| **Total Profit** | $1,100,462 |
| **Return** | +1,834% |
| **Win Rate** | 71.8% |

---

## How It Works

### 1. Signal Generation
The bot scans 34 trading instruments daily at 22:05 UTC (after NY close) looking for high-probability setups based on:
- Multi-timeframe trend alignment (Monthly → Weekly → Daily → H4)
- Support/Resistance levels
- Fibonacci retracements
- Price action patterns

### 2. Trade Entry
When a setup has enough "confluence" (multiple factors aligning), the bot:
- Calculates entry price, stop loss, and 5 take profit levels
- Places a pending order or enters immediately
- Sizes position based on 0.6% account risk per trade

### 3. Trade Management (5-TP System)
The bot uses 5 take profit levels with partial exits:

| Level | Target | Close % | What Happens |
|-------|--------|---------|--------------|
| TP1 | 0.6R | 10% | Close 10%, move SL to breakeven |
| TP2 | 1.2R | 10% | Close 10%, trail SL |
| TP3 | 2.0R | 15% | Close 15%, trail SL |
| TP4 | 2.5R | 20% | Close 20%, trail SL |
| TP5 | 3.5R | 45% | Close remaining 45% |

### 4. Risk Management
- **Base Risk**: 0.6% per trade ($360 on 60K)
- **Dynamic Scaling**: Adjusts size based on win/loss streaks and equity curve
- **Safety Mechanism**: Closes all trades if daily DD exceeds 4.2%

---

## Core Files

### Trading Logic
| File | Purpose |
|------|---------|
| `strategy_core.py` | All trading logic: signals, entries, exits |
| `main_live_bot.py` | Live trading on MT5 |

### Optimization & Validation
| File | Purpose |
|------|---------|
| `ftmo_challenge_analyzer.py` | Optimize and validate parameters |
| `scripts/validate_h1_realistic.py` | Simulate exact live bot behavior |

### Parameters
| File | Purpose |
|------|---------|
| `params/current_params.json` | Active trading parameters |
| `params/defaults.py` | Default parameter values |

---

## How to Run

### Validate Current Parameters
```bash
python ftmo_challenge_analyzer.py --validate --start 2023-01-01 --end 2025-12-31
```

### Run H1 Realistic Simulation
```bash
python scripts/validate_h1_realistic.py --trades ftmo_analysis_output/VALIDATE/best_trades_final.csv --balance 60000
```

### Run Live Bot (Windows with MT5)
```bash
python main_live_bot.py
```

---

## 5ers Challenge Rules

| Rule | Requirement |
|------|-------------|
| Account Size | $60,000 |
| Step 1 Target | 8% = $4,800 |
| Step 2 Target | 5% = $3,000 |
| Max Total Drawdown | 10% = $6,000 (stop-out at $54,000) |
| Min Profitable Days | 3 |

---

## Expected Performance

Based on H1 realistic simulation:

| Timeframe | Expected Return |
|-----------|-----------------|
| Per Month | ~$38,000 profit |
| Step 1 (8%) | 2-3 weeks |
| Step 2 (5%) | 1-2 weeks |
| Total Challenge | 4-5 weeks |

---

## Key Technical Details

### Data
- Historical data in `data/ohlcv/` (D1, H1 timeframes)
- 34 trading instruments (forex pairs, gold, indices)
- Data range: 2003-2025

### Output
- Validation results: `ftmo_analysis_output/VALIDATE/`
- H1 simulation: `ftmo_analysis_output/hourly_validator/`
- Optimization: `ftmo_analysis_output/TPE/` or `NSGA/`

---

## Important Notes

### The 5-TP System is Critical
The strategy uses 5 take profit levels. Attempts to simplify to 3 TPs broke the exit calculations. Always maintain all 5 levels:
- `atr_tp1_multiplier` through `atr_tp5_multiplier`
- `tp1_close_pct` through `tp5_close_pct`

### H1 Simulation = Live Bot Behavior
The `validate_h1_realistic.py` script simulates exactly what the live bot would do:
- Dynamic lot sizing
- Commission deduction
- Safety mechanisms
- Hour-by-hour price simulation

---

**Last Updated**: January 4, 2026
