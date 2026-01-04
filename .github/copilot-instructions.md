# AI Assistant Instructions - 5ers Trading Bot

## Project Overview

Automated MetaTrader 5 trading bot for **5ers 60K High Stakes** Challenge accounts.

### Current State (January 2026)
- **Status**: ✅ Production Ready
- **Validation**: H1 realistic simulation confirms +1,834% return (2023-2025)
- **Exit System**: 5 Take Profit levels (NOT 3)

---

## Architecture

```
┌─────────────────────────────────┐     ┌────────────────────────────────┐
│   OPTIMIZER (Any Platform)      │     │  LIVE BOT (Windows VM + MT5)   │
│                                  │     │                                 │
│  ftmo_challenge_analyzer.py      │────▶│  main_live_bot.py              │
│  - Optuna TPE / NSGA-II          │     │  - Loads params/current*.json  │
│  - Backtesting 2003-2025         │     │  - Real-time MT5 execution     │
│  - H1 realistic validation       │     │  - 5 Take Profit levels        │
└─────────────────────────────────┘     └────────────────────────────────┘
```

---

## Key Modules

| File | Purpose |
|------|---------|
| `strategy_core.py` | Trading strategy - 5-TP system, signals, simulate_trades() |
| `ftmo_challenge_analyzer.py` | Optimization & validation engine |
| `main_live_bot.py` | Live MT5 trading |
| `scripts/validate_h1_realistic.py` | H1 realistic simulation (matches live bot) |
| `tradr/backtest/h1_trade_simulator.py` | H1 trade simulation engine |
| `params/current_params.json` | Active optimized parameters |
| `params/defaults.py` | Default parameter values (includes tp4/tp5) |

---

## 5-TP Exit System (CRITICAL)

The strategy uses **5 Take Profit levels**. This is critical - DO NOT reduce to 3 TPs.

| Level | R-Multiple | Close % |
|-------|------------|---------|
| TP1 | 0.6R | 10% |
| TP2 | 1.2R | 10% |
| TP3 | 2.0R | 15% |
| TP4 | 2.5R | 20% |
| TP5 | 3.5R | 45% |

**Trailing Stop**:
- Activated after TP1 hit
- Moves to breakeven after TP1
- After TP2+: `trailing_sl = previous_tp + 0.5 * risk`

---

## Validated Performance (2023-2025)

### H1 Realistic Simulation Results
```json
{
  "starting_balance": 60000,
  "final_balance": 1160461.64,
  "net_pnl": 1100461.64,
  "return_pct": 1834.1,
  "total_trades": 1673,
  "winners": 1201,
  "win_rate": 71.8,
  "total_r": 274.71,
  "total_dd_breached": false
}
```

---

## Commands

### Validation
```bash
python ftmo_challenge_analyzer.py --validate --start 2023-01-01 --end 2025-12-31
```

### H1 Realistic Simulation
```bash
python scripts/validate_h1_realistic.py --trades ftmo_analysis_output/VALIDATE/best_trades_final.csv --balance 60000
```

### Optimization
```bash
python ftmo_challenge_analyzer.py --single --trials 100  # TPE
python ftmo_challenge_analyzer.py --multi --trials 100   # NSGA-II
```

### Status
```bash
python ftmo_challenge_analyzer.py --status
```

---

## Critical Conventions

### Symbol Format
- **Internal/Data**: OANDA format with underscores (`EUR_USD`, `XAU_USD`)
- **MT5 Execution**: Broker format (`EURUSD`, `XAUUSD`)
- Use `symbol_mapping.py` for conversions

### Parameters - NEVER Hardcode
```python
# ✅ CORRECT
from params.params_loader import load_strategy_params
params = load_strategy_params()

# ❌ WRONG
MIN_CONFLUENCE = 5  # Don't hardcode
```

### Multi-Timeframe Data
Always prevent look-ahead bias:
```python
htf_candles = _slice_htf_by_timestamp(weekly_candles, current_daily_dt)
```

---

## StrategyParams Key Fields

```python
@dataclass
class StrategyParams:
    # Confluence
    min_confluence: int = 5
    min_quality_factors: int = 3
    
    # TP R-Multiples (5 levels)
    atr_tp1_multiplier: float = 0.6
    atr_tp2_multiplier: float = 1.2
    atr_tp3_multiplier: float = 2.0
    atr_tp4_multiplier: float = 2.5
    atr_tp5_multiplier: float = 3.5
    
    # Close Percentages (5 levels)
    tp1_close_pct: float = 0.10
    tp2_close_pct: float = 0.10
    tp3_close_pct: float = 0.15
    tp4_close_pct: float = 0.20
    tp5_close_pct: float = 0.45
    
    # Risk
    risk_per_trade_pct: float = 0.6
    trail_activation_r: float = 0.65
```

---

## 5ers Challenge Rules

| Rule | Limit |
|------|-------|
| Account Size | $60,000 |
| Max Total DD | 10% below start ($54K stop-out) |
| Daily DD | None (5ers doesn't track) |
| Step 1 Target | 8% = $4,800 |
| Step 2 Target | 5% = $3,000 |
| Min Profitable Days | 3 |

---

## File Structure

```
botcreativehub/
├── strategy_core.py              # 5-TP system, signals
├── ftmo_challenge_analyzer.py    # Optimization & validation
├── main_live_bot.py              # Live MT5 trading
├── params/
│   ├── current_params.json       # Active parameters
│   ├── defaults.py               # Default values (tp1-tp5)
│   └── params_loader.py          # Load utilities
├── scripts/
│   └── validate_h1_realistic.py  # H1 simulation
├── tradr/backtest/
│   └── h1_trade_simulator.py     # H1 trade engine
├── data/ohlcv/                   # Historical data
└── ftmo_analysis_output/         # Results
```

---

## What NOT to Do

1. ❌ **Never reduce from 5 TPs to 3 TPs** - breaks exit logic
2. ❌ **Never hardcode parameters** - use params_loader
3. ❌ **Never change exit logic** without full H1 validation
4. ❌ **Never use look-ahead bias** - always slice HTF data

---

## Recent History

### January 4, 2026
- REVERTED to 5-TP system (3-TP removal broke exit logic)
- Added H1 realistic validation
- Confirmed +1,834% return over 2023-2025

### Key Commits
- `61bdcac` - REVERT: Restore 5-TP system
- `2d1979c` - Add H1 validator results

---

**Last Updated**: January 4, 2026
