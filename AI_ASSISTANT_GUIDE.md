# AI Assistant Guide - 5ers Trading Bot

## Project Overview

This is a **production-ready automated trading bot** for **5ers 60K High Stakes** Challenge accounts. 

### Key Facts
- **Platform**: MetaTrader 5 (MT5)
- **Account Size**: $60,000
- **Strategy**: 5-TP Confluence System with multi-timeframe analysis
- **Validated**: H1 realistic simulation confirms +1,834% return (2023-2025)

---

## Current State (January 2026)

### ✅ Working System
The system is fully functional with the following validated results:

```
H1 REALISTIC SIMULATION (2023-2025):
- Starting Balance: $60,000
- Final Balance: $1,160,462
- Return: +1,834%
- Win Rate: 71.8%
- Total DD Breached: NO ✅
```

### 5-TP Exit System
The strategy uses **5 Take Profit levels** (NOT 3):

| Level | R-Multiple | Close % |
|-------|------------|---------|
| TP1 | 0.6R | 10% |
| TP2 | 1.2R | 10% |
| TP3 | 2.0R | 15% |
| TP4 | 2.5R | 20% |
| TP5 | 3.5R | 45% |

> ⚠️ **CRITICAL**: Never reduce to 3 TPs - it breaks the exit logic!

---

## Core Files

### Primary Files
| File | Lines | Purpose |
|------|-------|---------|
| `strategy_core.py` | ~3,100 | Trading strategy - signals, 5-TP exits, simulate_trades() |
| `ftmo_challenge_analyzer.py` | ~2,900 | Optimization, validation, backtesting |
| `main_live_bot.py` | ~1,500 | Live MT5 trading |

### Parameters
| File | Purpose |
|------|---------|
| `params/current_params.json` | Active optimized parameters |
| `params/defaults.py` | Default values (includes tp4/tp5) |
| `params/params_loader.py` | Load/merge parameters |

### H1 Validation
| File | Purpose |
|------|---------|
| `scripts/validate_h1_realistic.py` | Simulates exact live bot behavior |
| `tradr/backtest/h1_trade_simulator.py` | H1 trade simulation engine |

---

## Key Functions

### strategy_core.py

```python
# Generate trading signals
signals = generate_signals(candles, symbol, params, monthly_candles, weekly_candles, h4_candles)

# Simulate trades through historical data
trades = simulate_trades(candles, symbol, params, monthly_candles, weekly_candles, h4_candles)

# Compute trade levels (entry, SL, TP1-TP5)
note, is_valid, entry, sl, tp1, tp2, tp3 = compute_trade_levels(daily_candles, direction, params)
```

### ftmo_challenge_analyzer.py

```python
# Run validation on date range
python ftmo_challenge_analyzer.py --validate --start 2023-01-01 --end 2025-12-31

# Run optimization
python ftmo_challenge_analyzer.py --single --trials 100
```

### validate_h1_realistic.py

```python
# Run H1 simulation
python scripts/validate_h1_realistic.py --trades path/to/trades.csv --balance 60000
```

---

## StrategyParams Dataclass

Key parameters in `strategy_core.py`:

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
    
    # Trailing Stop
    trail_activation_r: float = 0.65
    
    # Risk
    risk_per_trade_pct: float = 0.6
```

---

## Data Structure

### OHLCV Data
Located in `data/ohlcv/`:
```
{SYMBOL}_{TIMEFRAME}_{START}_{END}.csv
Examples:
- EUR_USD_D1_2003_2025.csv
- SPX500USD_H1_2023_2025.csv
```

### Output Structure
```
ftmo_analysis_output/
├── VALIDATE/
│   ├── history/
│   │   └── val_2023_2025_007/     # Latest validation
│   │       ├── best_trades_final.csv
│   │       └── analysis_summary.txt
│   └── best_params.json
├── hourly_validator/
│   └── best_trades_final_realistic_summary.json
├── TPE/                           # TPE optimization results
└── NSGA/                          # NSGA-II optimization results
```

---

## Important Conventions

### Symbol Format
- **Internal/Data**: OANDA format (`EUR_USD`, `XAU_USD`)
- **MT5 Execution**: Broker format (`EURUSD`, `XAUUSD`)
- Always use `symbol_mapping.py` for conversions

### Parameters - Never Hardcode
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
# Slice HTF data to reference timestamp
htf_candles = _slice_htf_by_timestamp(weekly_candles, current_daily_dt)
```

---

## Common Tasks

### Run Validation
```bash
python ftmo_challenge_analyzer.py --validate --start 2023-01-01 --end 2025-12-31
```

### Run H1 Simulation
```bash
python scripts/validate_h1_realistic.py --trades ftmo_analysis_output/VALIDATE/best_trades_final.csv --balance 60000
```

### Run Optimization
```bash
python ftmo_challenge_analyzer.py --single --trials 100
```

### Check Status
```bash
python ftmo_challenge_analyzer.py --status
```

---

## 5ers Challenge Rules

| Rule | Limit |
|------|-------|
| Max Total Drawdown | 10% below starting balance |
| Daily Drawdown | None (5ers doesn't track) |
| Step 1 Target | 8% |
| Step 2 Target | 5% |
| Min Profitable Days | 3 |

---

## Recent History

### January 4, 2026
- **REVERTED** to 5-TP system (3-TP removal broke exit logic)
- H1 realistic validator added
- Validation confirmed: +696R (D1), +274R (H1 realistic)

### What NOT to Do
1. ❌ Remove TP4/TP5 - breaks exit calculations
2. ❌ Change exit logic without full validation
3. ❌ Hardcode parameters in source files
4. ❌ Use outdated `atr_tp_multiplier` naming (use actual field names)

---

## Quick Reference

### Validation Run: val_2023_2025_007
- D1 Backtest: 1,779 trades, +696.03R, 45.5% WR
- H1 Realistic: 1,673 trades, +274.71R, 71.8% WR, $1.16M final

### Key Commits
- `61bdcac` - REVERT: Restore 5-TP system
- `2d1979c` - H1 validator results added

---

**Last Updated**: January 4, 2026
