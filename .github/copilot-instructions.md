# AI Assistant Instructions - 5ers Trading Bot

## Project Overview

Automated MetaTrader 5 trading bot for **5ers 60K High Stakes** Challenge accounts.

### Current State (January 6, 2026)
- **Status**: ✅ Production Ready
- **Final Simulation**: $948,629 from $60K (+1,481% over 3 years)
- **5ers Compliance**: Max TDD 2.17%, Max DDD 4.16% (both within limits)
- **Exit System**: 3 Take Profit levels with partial closes
- **Entry Queue**: Signals wait for 0.3R proximity before placing limit orders

---

## Architecture

```
┌─────────────────────────────────┐     ┌────────────────────────────────┐
│   OPTIMIZER (Any Platform)      │     │  LIVE BOT (Windows VM + MT5)   │
│                                  │     │                                 │
│  ftmo_challenge_analyzer.py      │────▶│  main_live_bot.py              │
│  - Optuna TPE / NSGA-II          │     │  - Loads params/current*.json  │
│  - Backtesting 2003-2025         │     │  - Entry queue system          │
│  - H1 realistic validation       │     │  - 3-TP partial close          │
│                                  │     │  - Dynamic lot sizing          │
│                                  │     │  - DDD/TDD safety              │
└─────────────────────────────────┘     └────────────────────────────────┘
```

---

## Key Modules

| File | Purpose |
|------|---------|
| `strategy_core.py` | Trading strategy - signals, `simulate_trades()` |
| `ftmo_challenge_analyzer.py` | Optimization & validation engine |
| `main_live_bot.py` | Live MT5 trading with entry queue & dynamic lot sizing |
| `challenge_risk_manager.py` | DDD/TDD enforcement, AccountSnapshot |
| `ftmo_config.py` | 5ers challenge configuration |
| `scripts/simulate_main_live_bot.py` | Full live bot simulation on H1 data |
| `scripts/test_equivalence_v2.py` | Verify live bot = TPE backtest |
| `params/current_params.json` | Active optimized parameters |

---

## 3-TP Exit System

The strategy uses **3 Take Profit levels** with partial closes:

| Level | R-Multiple | Close % | SL Action |
|-------|------------|---------|-----------|
| TP1 | 0.6R | 35% | Move to breakeven |
| TP2 | 1.2R | 30% | Trail to TP1+0.5R |
| TP3 | 2.0R | 35% | Close remaining |

---

## Entry Queue System (NEW)

Signals don't immediately place orders. They wait in a queue:

1. **Signal Generated**: Daily scan at 00:10 server time
2. **Queue Check**: Every 5 minutes
3. **Proximity Check**: If price within **0.3R** of entry → place limit order
4. **Expiry**: Remove signal if waiting > 5 days or price > 1.5R away
5. **Fill**: Limit order fills when H1 bar touches entry price

**Impact**: ~47% of signals execute (better quality trades)

---

## DDD Safety System (3-Tier)

The live bot implements Daily DrawDown protection:

| Tier | Daily DD | Action |
|------|----------|--------|
| Warning | ≥2.0% | Log warning only |
| Reduce | ≥3.0% | Reduce risk: 0.6% → 0.4% |
| Halt | ≥3.5% | Close all positions, stop trading until next day |

**5ers Rules**:
- 5ers DOES track daily drawdown (5% limit)
- TDD is STATIC from initial balance (not trailing like FTMO)
- $60K account → stop-out at $54K (regardless of peak equity)

---

## Validated Performance (January 6, 2026)

### Final Live Bot Simulation (2023-2025)

```json
{
  "starting_balance": 60000,
  "final_balance": 948629,
  "net_return_pct": 1481,
  "total_trades": 943,
  "win_rate": 66.1,
  "max_total_dd_pct": 2.17,
  "max_daily_dd_pct": 4.16,
  "ddd_halt_events": 2,
  "total_commissions": 9391
}
```

### 5ers Compliance

| Rule | Limit | Achieved | Status |
|------|-------|----------|--------|
| Max TDD | 10% | 2.17% | ✅ |
| Max DDD | 5% | 4.16% | ✅ |
| Profit Target | 8% | +1481% | ✅ |

---

## Commands

### Full Live Bot Simulation (RECOMMENDED)
```bash
python scripts/simulate_main_live_bot.py
```

### TPE Validation (signal generation only)
```bash
python ftmo_challenge_analyzer.py --validate --start 2023-01-01 --end 2025-12-31
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

### Lot Sizing - At FILL Moment
```python
# Lot size calculated when order FILLS, not when signal generated
# This enables proper compounding
lot_size = calculate_lot_size(
    balance=current_balance,  # Current, not signal-time balance
    risk_pct=0.6,
    entry=fill_price,
    stop_loss=sl,
)
```

---

## StrategyParams Key Fields

```python
@dataclass
class StrategyParams:
    # Confluence
    min_confluence: int = 2
    min_quality_factors: int = 3
    
    # TP R-Multiples (3 levels)
    tp1_r_multiple: float = 0.6
    tp2_r_multiple: float = 1.2
    tp3_r_multiple: float = 2.0
    
    # Close Percentages (3 levels)
    tp1_close_pct: float = 0.35
    tp2_close_pct: float = 0.30
    tp3_close_pct: float = 0.35
    
    # Risk
    risk_per_trade_pct: float = 0.6
```

---

## FIVEERS_CONFIG Key Fields

```python
class FIVEERS_CONFIG:
    starting_balance = 60000
    profit_target_step1_pct = 0.08    # 8% = $4,800
    profit_target_step2_pct = 0.05    # 5% = $3,000
    max_total_dd_pct = 0.10           # 10% = $6,000
    max_daily_dd_pct = 0.05           # 5% = $3,000
    daily_loss_warning_pct = 0.020    # 2.0%
    daily_loss_reduce_pct = 0.030     # 3.0%
    daily_loss_halt_pct = 0.035       # 3.5%
    limit_order_proximity_r = 0.3     # Entry queue proximity
    max_pending_orders = 100
```

---

## 5ers Challenge Rules

| Rule | Limit |
|------|-------|
| Account Size | $60,000 |
| Max Total DD | 10% below start ($54K stop-out) - STATIC |
| Max Daily DD | 5% from day start ($3K max daily loss) |
| Step 1 Target | 8% = $4,800 |
| Step 2 Target | 5% = $3,000 |
| Min Profitable Days | 3 |

**Key Difference from FTMO**: TDD is STATIC from initial balance, NOT trailing.

---

## File Structure

```
botcreativehub/
├── strategy_core.py              # Trading strategy, signals
├── ftmo_challenge_analyzer.py    # Optimization & validation
├── main_live_bot.py              # Live MT5 trading + entry queue
├── challenge_risk_manager.py     # DDD/TDD enforcement
├── ftmo_config.py                # 5ers configuration
├── params/
│   ├── current_params.json       # Active parameters
│   ├── defaults.py               # Default values
│   └── params_loader.py          # Load utilities
├── scripts/
│   ├── simulate_main_live_bot.py # Full H1 simulation
│   ├── test_equivalence_v2.py    # Equivalence test
│   └── download_h1_required.py   # H1 data downloader
├── data/ohlcv/                   # Historical data (D1 + H1)
├── ftmo_analysis_output/
│   ├── VALIDATE/                 # TPE validation results
│   └── FINAL_SIMULATION_JAN06_2026/  # Final simulation results
└── docs/                         # Documentation
```

---

## What NOT to Do

1. ❌ **Never hardcode parameters** - use params_loader
2. ❌ **Never change exit logic** without full simulation
3. ❌ **Never use look-ahead bias** - always slice HTF data
4. ❌ **Never use trailing TDD** - 5ers uses STATIC TDD
5. ❌ **Never ignore DDD** - 5ers tracks daily drawdown (5% limit)
6. ❌ **Never calculate lot size at signal time** - use fill time balance

---

## Recent History

### January 6, 2026
- **Final Simulation**: $948,629 final balance (+1,481% return)
- **Entry Queue**: Implemented and validated (0.3R proximity)
- **Lot Size Fix**: Now calculates at FILL moment for proper compounding
- **5ers Compliance**: Max TDD 2.17%, Max DDD 4.16% ✅
- **Created**: `scripts/simulate_main_live_bot.py` - definitive simulation tool

### January 5, 2026
- **Equivalence Test**: 97.6% match between TPE and live bot
- **DDD Settings**: Finalized at 3.5%/3.0%/2.0% (halt/reduce/warning)
- **Bug Fixes**: AccountSnapshot fields added

### January 4, 2026
- Changed from 5-TP to 3-TP system
- Added H1 realistic validation

---

## Session Archives

- `ftmo_analysis_output/FINAL_SIMULATION_JAN06_2026/` - Definitive simulation results
- `docs/SESSION_LOG_JAN04_2026.md` - System update session

---

**Last Updated**: January 6, 2026
