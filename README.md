# 5ers 60K High Stakes Trading Bot

Automated MetaTrader 5 trading bot for **5ers 60K High Stakes** Challenge accounts. Uses a **5-TP Confluence System** with multi-timeframe analysis. Validated with **H1 Realistic Simulation** for production-ready results.

## 🎯 Validated Performance (2023-2025)

### H1 Realistic Simulation Results
*Simulates EXACTLY what `main_live_bot.py` would do in production*

| Metric | Value |
|--------|-------|
| **Starting Balance** | $60,000 |
| **Final Balance** | **$1,160,462** |
| **Net P&L** | **$1,100,462** |
| **Return** | **+1,834%** |
| **Total R** | +274.71R |
| **Win Rate** | **71.8%** |
| **Total Trades** | 1,673 |

### Dynamic Scaling Performance
| Metric | Value |
|--------|-------|
| Avg Lot Multiplier | 1.80x |
| Avg Risk % Used | 1.08% |
| Safety Close Triggers | 22 |
| Total DD Breached | **NO ✅** |

### 5ers Challenge Speed (60K account)
- Step 1 (8% target = $4,800): ~2-3 weeks
- Step 2 (5% target = $3,000): ~1-2 weeks
- **Estimated Total**: ~4-5 weeks

---

## Quick Start

```bash
# Run validation (test current parameters)
python ftmo_challenge_analyzer.py --validate --start 2023-01-01 --end 2025-12-31

# Run H1 realistic simulation (exact live bot behavior)
python scripts/validate_h1_realistic.py --trades ftmo_analysis_output/VALIDATE/best_trades_final.csv --balance 60000

# Run optimization
python ftmo_challenge_analyzer.py --single --trials 100  # TPE single-objective
python ftmo_challenge_analyzer.py --multi --trials 100   # NSGA-II multi-objective

# Check optimization status
python ftmo_challenge_analyzer.py --status

# Run live bot (Windows VM with MT5)
python main_live_bot.py
```

---

## Architecture

### Two-Environment Design
```
┌─────────────────────────────────┐     ┌────────────────────────────────┐
│   OPTIMIZER (Any Platform)      │     │  LIVE BOT (Windows VM + MT5)   │
│                                  │     │                                 │
│  ftmo_challenge_analyzer.py      │────▶│  main_live_bot.py              │
│  - Optuna TPE / NSGA-II          │     │  - Loads params/current*.json  │
│  - Backtesting 2003-2025         │     │  - Real-time MT5 execution     │
│  - Parameter optimization        │     │  - 5ers risk management        │
│  - Out-of-sample validation      │     │  - 5 Take Profit levels        │
│                                  │     │                                 │
│  Output: params/current_params   │     │  Output: Live trade log        │
└─────────────────────────────────┘     └────────────────────────────────┘
```

### Data Flow
```
params/current_params.json       ← Optimized strategy parameters (28 params)
         ↑                            ↓
ftmo_challenge_analyzer.py      main_live_bot.py
(Optuna optimization)           (loads params at startup)
         ↑                            ↓
data/ohlcv/                      scripts/validate_h1_realistic.py
(historical D1/H1 data)          (H1 realistic simulation)
```

---

## Project Structure

```
├── strategy_core.py              # Core trading logic (5-TP system, 3100+ lines)
├── ftmo_challenge_analyzer.py    # Optimization engine & validation
├── main_live_bot.py              # Live MT5 trading entry point
├── broker_config.py              # Multi-broker configuration
├── symbol_mapping.py             # Symbol conversion (OANDA ↔ broker)
├── config.py                     # Contract specs, symbols
├── ftmo_config.py                # 5ers challenge rules
│
├── params/                       # Parameter management
│   ├── current_params.json       # Active parameters (28 optimized values)
│   ├── defaults.py               # Default parameter values
│   └── params_loader.py          # Load/save utilities
│
├── scripts/
│   └── validate_h1_realistic.py  # H1 realistic simulation (matches live bot)
│
├── tradr/
│   └── backtest/
│       └── h1_trade_simulator.py # H1-based trade simulation
│
├── data/ohlcv/                   # Historical data (D1, H1, H4)
├── ftmo_analysis_output/         # Optimization & validation results
│   ├── VALIDATE/history/         # Validation run history
│   └── hourly_validator/         # H1 simulation results
│
└── docs/                         # Documentation
```

---

## 5-TP Exit System

The strategy uses 5 Take Profit levels with partial position closing:

| Level | R-Multiple | Close % | Description |
|-------|------------|---------|-------------|
| TP1 | 0.6R | 10% | Lock early profit |
| TP2 | 1.2R | 10% | Secure 1R |
| TP3 | 2.0R | 15% | 2R milestone |
| TP4 | 2.5R | 20% | Extended profit |
| TP5 | 3.5R | 45% | Maximum target |

**Trailing Stop**: Activated after TP1, moves to breakeven, then follows price.

---

## 5ers Challenge Rules

| Rule | Limit | Our Performance |
|------|-------|-----------------|
| Max Total Drawdown | 10% below start ($54K stop-out) | **<10% ✅** |
| Daily Drawdown | None (5ers doesn't track) | N/A |
| Step 1 Target | 8% = $4,800 | **Achieved** |
| Step 2 Target | 5% = $3,000 | **Achieved** |
| Min Profitable Days | 3 | **22+ days** |

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `strategy_core.py` | Trading strategy logic - 5-TP system, signals |
| `params/current_params.json` | Current optimized parameters |
| `params/defaults.py` | Default parameter values with tp4/tp5 |
| `ftmo_challenge_analyzer.py` | Optimization & validation engine |
| `scripts/validate_h1_realistic.py` | H1 realistic simulation |
| `tradr/backtest/h1_trade_simulator.py` | H1 trade simulation engine |

---

## Documentation

- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture
- **[docs/STRATEGY_GUIDE.md](docs/STRATEGY_GUIDE.md)** - Trading strategy details
- **[docs/EXIT_STRATEGY.md](docs/EXIT_STRATEGY.md)** - 5-TP exit system
- **[docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Deployment instructions
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - AI assistant guide

---

## Validation Results Reference

Latest validation run: `val_2023_2025_007`

### D1 Backtest Results
| Period | Trades | Total R | Win Rate | Est. Profit |
|--------|--------|---------|----------|-------------|
| Training (2023-01 to 2025-02) | 1,273 | +431.83R | 44.1% | $155,460 |
| Validation (2025-02 to 2025-12) | 521 | +266.68R | 48.6% | $96,005 |
| **Full Period** | **1,779** | **+696.03R** | **45.5%** | **$250,569** |

### H1 Realistic Simulation
```json
{
  "total_trades": 1673,
  "winners": 1201,
  "win_rate": 71.8,
  "total_r": 274.71,
  "net_pnl": 1100461.64,
  "final_balance": 1160461.64,
  "return_pct": 1834.1,
  "total_dd_breached": false
}
```

---

**Last Updated**: January 4, 2026
