# 5ers 60K High Stakes Trading Bot

Automated MetaTrader 5 trading bot for **5ers 60K High Stakes** Challenge accounts. Uses a 6-Pillar Confluence system with multi-timeframe analysis. Validated on 12 years (2014-2025) and production-ready.

## Quick Start

```bash
# Run optimization (recommended: use helper script for background runs)
./run_optimization.sh --single --trials 100  # TPE (auto-logs to ftmo_analysis_output/TPE/run.log)
./run_optimization.sh --multi --trials 100   # NSGA-II (auto-logs to ftmo_analysis_output/NSGA/run.log)

# Or run directly
python ftmo_challenge_analyzer.py --single --trials 100  # TPE single-objective (recommended)
python ftmo_challenge_analyzer.py --multi --trials 100   # NSGA-II multi-objective

# Monitor live progress
tail -f ftmo_analysis_output/TPE/run.log          # Complete output
tail -f ftmo_analysis_output/TPE/optimization.log # Trial results only
cat ftmo_analysis_output/TPE/best_params.json     # Current best parameters (auto-updates!)

# Check optimization status
python ftmo_challenge_analyzer.py --status

# Show current configuration
python ftmo_challenge_analyzer.py --config

# Run live bot (Windows VM with MT5)
python main_live_bot.py
```

## Final Results (Dec 31, 2025)

### 12-Year Robustness (2014-2025)
| Period | Total R | Profit (60K) | Win Rate |
|--------|---------|--------------|----------|
| 2014-2016 | +672.7R | $242,166 | 48.7% |
| 2017-2019 | +679.2R | $244,500 | 48.7% |
| 2020-2022 | +662.4R | $238,476 | 48.3% |
| 2023-2025 | +752.0R | $270,720 | 48.8% |
| **Total** | **+2,766.3R** | **$995,862** | **~48.6%** |

### 5ers Challenge Speed (60K account)
- Step 1 (8% target = $4,800): ~18 dagen
- Step 2 (5% target = $3,000): ~10 dagen
- **Totaal**: ~28 dagen

### Compliance Metrics
- Max daily DD <3.8% (limit 5%)
- Max total DD <3% (limit 10%)
- Risk per trade: 0.6% = $360 per R
- Min profitable days: 3 (5ers requirement)

## Latest Updates (Jan 4, 2026)

### Optimization Infrastructure
- ✨ **Real-time Best Params**: `best_params.json` auto-updates during optimization
- ✨ **Fresh Start**: Clean database with warm-start from run009 baseline (0.6R/1.2R/2.0R)
- ✨ **Import Fix**: Fixed `DEFAULT_STRATEGY_PARAMS` → `PARAMETER_DEFAULTS` bug
- ✨ **Progress Tracking**: Visible best trial parameters while optimization runs
- ✨ **Database Archiving**: Old trials archived to `optuna_backups/` with timestamps

### Previous Updates (Dec 31, 2025)

#### Live Bot Enhancements
- ✨ **Daily Close Scanning**: Scan only at 22:05 UTC (after NY close) - matches backtest exactly
- ✨ **Spread-Only Entry Filter**: No session filter, just check spread quality
- ✨ **Spread Monitoring**: Every 10 min, check if spread improved for pending signals
- ✨ **Signal Expiry**: Signals expire after 12 hours if spread never improves
- ✨ **3-Tier Graduated Risk**: 2% DD → reduce risk, 3.5% → cancel pending, 4.5% → emergency close

### Live Bot Synced with TPE Optimizer
- ✅ **Quality Factors**: Now uses `max(1, confluence_score // 3)` (identical to backtest)
- ✅ **Volatile Asset Boost**: Applied for XAU_USD, NAS100_USD, GBP_JPY, BTC_USD
- ✅ **Active Status Check**: Uses boosted scores with `min_quality_for_active = max(1, min_quality_factors - 1)`

### Multi-Broker Support
- ✨ **Forex.com Demo** ($50K): For testing before 5ers live
- ✨ **5ers Live** ($60K): Production trading
- ✨ **Symbol Mapping**: Automatic conversion (SPX500_USD → SPX500 for Forex.com)

### Previous Updates (Dec 28-30, 2025)
- ✅ **Validation Mode**: Test parameters on different date ranges
- ✅ **Parameter saving fix**: ALL 30+ Optuna parameters now saved correctly
- ✅ **12-year validation**: Confirmed robustness across 2014-2025
- ✅ **NSGA-II directories**: Separate output for multi-objective runs

---

## Project Structure

```
├── strategy_core.py          # Core trading logic (6 Confluence Pillars)
├── ftmo_challenge_analyzer.py # Optuna optimization & backtesting
├── main_live_bot.py          # Live MT5 trading entry point
├── broker_config.py          # Multi-broker configuration (Forex.com, 5ers)
├── symbol_mapping.py         # Symbol conversion (OANDA ↔ broker format)
├── config.py                 # Account settings, CONTRACT_SPECS
├── ftmo_config.py            # 5ers challenge rules & risk limits
├── docs/                     # Documentation (system guide, strategy analysis)
├── scripts/                  # Utility scripts (monitoring, debugging)
├── params/                   # Optimized parameters (current_params.json)
└── data/ohlcv/               # Historical OHLCV data (2003-2025)
```

## Optimization & Backtesting

The optimizer uses professional quant best practices:

- **TRAINING PERIOD**: January 1, 2023 – September 30, 2024 (21 months in-sample)
- **VALIDATION PERIOD**: October 1, 2024 – December 26, 2025 (15 months out-of-sample)
- **FINAL BACKTEST**: Full year 2024 (December fully open for trading)
- **ADX > 25 trend-strength filter** applied to avoid ranging markets.

All trades from the final backtest are exported to:
`ftmo_analysis_output/all_trades_2024_full.csv`

Parameters are saved to `params/current_params.json`

Optimization is resumable and can be checked with: `python ftmo_challenge_analyzer.py --status`


## Documentation

### Core Documentation
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Complete system architecture & data flow
- **[STRATEGY_GUIDE.md](docs/STRATEGY_GUIDE.md)** - Trading strategy deep dive with current parameters
- **[API_REFERENCE.md](docs/API_REFERENCE.md)** - Complete API documentation for all modules
- **[DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)** - Installation, deployment & troubleshooting
- **[OPTIMIZATION_FLOW.md](docs/OPTIMIZATION_FLOW.md)** - 4-phase optimization process
- **[BASELINE_ANALYSIS.md](docs/BASELINE_ANALYSIS.md)** - Comprehensive performance analysis & roadmap
- **[CHANGELOG.md](docs/CHANGELOG.md)** - Version history & recent changes

### Quick References
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - AI assistant context & commands

---

**Last Documentation Update**: 2025-12-31
