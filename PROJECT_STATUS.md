# 5ers 60K High Stakes Trading Bot - Project Status Report
**Date**: 2026-01-04  
**Status**: ✅ **PRODUCTION READY** - Live optimization & Windows VM deployment

---

## 📊 Executive Summary

The trading bot is a **professional-grade automated trading system** for **5ers 60K High Stakes** Challenge accounts. Full 12-year validation (2014-2025) confirms production readiness with **~48.6% win rate** and strict compliance.

### ✅ Latest Achievements (Jan 4, 2026)

#### Optimization Infrastructure Improvements
- **Real-time Best Params Tracking**: Auto-updating `best_params.json` during optimization
  - Updates immediately when new best trial found
  - Located in `ftmo_analysis_output/TPE/best_params.json`
  - Contains trial number, score, and all parameters
- **Fresh Optimization Start**: Clean database with warm-start from run009 baseline
  - Baseline parameters: TP 0.6R/1.2R/2.0R, partial_exit disabled, risk 0.65%
  - Trial #0 scores baseline first, then explores parameter space
  - Previous trials archived to `optuna_backups/` for reference
- **Import Bug Fix**: Fixed `DEFAULT_STRATEGY_PARAMS` → `PARAMETER_DEFAULTS` error
  - Prevented crashes during best_params.json saving
  - Progress callback now works reliably
- **Training Period**: 2023-01-01 to 2024-09-30 (21 months in-sample)
- **Validation Period**: 2024-10-01 to 2025-12-26 (15 months out-of-sample)
- **Target**: 50 trials with TPE single-objective optimization

### ✅ Previous Achievements (Dec 31, 2025)

#### Live Bot Enhancements
- **Daily Close Scanning**: Only at 22:05 UTC (matches backtest exactly)
- **Spread-Only Entry Filter**: No session filter, just spread quality check
- **Spread Monitoring**: Every 10 min, execute when spread improves
- **Signal Expiry**: 12 hours after creation if spread never improves
- **3-Tier Graduated Risk**: 2% → reduce risk, 3.5% → cancel pending, 4.5% → emergency close
- **Synced with TPE**: Quality factors now identical (`max(1, confluence_score // 3)`)

#### Multi-Broker Deployment
- **Forex.com Demo**: $50K account for testing (currently deployed)
- **5ers Live**: $60K account for production (next step)
- **Symbol Mapping**: Fixed for Forex.com indices (SPX500, NAS100, UK100)
- **Windows VM**: Task Scheduler configured for 24/7 operation

### ✅ Previous Achievements (Dec 28-30, 2025)
- **12-year robustness**: +2,766.3R total, ~48.6% WR across 4 periods
  - 2014-2016: +672.7R, $242,166 (60K), 48.7% WR
  - 2017-2019: +679.2R, $244,500 (60K), 48.7% WR
  - 2020-2022: +662.4R, $238,476 (60K), 48.3% WR
  - 2023-2025: +752.0R, $270,720 (60K), 48.8% WR
- **5ers speed**: Step 1 (8% = $4,800) in ~18 dagen; Step 2 (5% = $3,000) in ~10 dagen
- **Compliance**: Daily DD <3.8% (limit 5%); Total DD <3% (limit 10%)

---

## 🏗️ Architecture Overview

### Two-Environment Design
```
┌─────────────────────────────────┐     ┌────────────────────────────────┐
│   OPTIMIZER (Any Platform)      │     │  LIVE BOT (Windows VM + MT5)   │
│                                  │     │                                 │
│  ftmo_challenge_analyzer.py      │────▶│  main_live_bot.py              │
│  - Optuna TPE / NSGA-II          │     │  - Loads params/current*.json  │
│  - Backtesting 2003-2025         │     │  - Real-time MT5 execution     │
│  - Parameter optimization        │     │  - 5ers risk management        │
│  - Out-of-sample validation      │     │  - Partial TPs (market orders) │
│                                  │     │                                 │
│  Output: params/current_params   │     │  Output: Live trade log        │
└─────────────────────────────────┘     └────────────────────────────────┘
```

### Data Flow
```
broker_config.py                 ← Multi-broker configuration (Forex.com, 5ers)
params/optimization_config.json  ← Optimization settings (ADX, multi-obj)
params/current_params.json       ← Optimized strategy parameters
         ↑                            ↓
ftmo_challenge_analyzer.py      main_live_bot.py
(Optuna optimization)           (loads params at startup)
    ↓    ↑
    │    └──── data/ohlcv/{SYMBOL}_{TF}_2003_2025.csv  (historical data)
    │
    └─ ftmo_analysis_output/TPE/best_params.json  (real-time best trial)
```

---

## 📁 Project Structure

### Root Level
```
ftmotrial/
├── main_live_bot.py              # Live MT5 bot (Windows VM)
├── ftmo_challenge_analyzer.py    # Optimization engine
├── strategy_core.py              # Trading strategy (6 pillars)
├── broker_config.py              # Multi-broker configuration
├── symbol_mapping.py             # Symbol conversion (OANDA ↔ broker)
├── config.py                     # Contract specs, symbols
├── ftmo_config.py                # 5ers challenge rules
│
├── params/                       # Parameter management
│   ├── current_params.json       # Active parameters
│   ├── optimization_config.json  # Optimization settings
│   └── params_loader.py          # Load/save utilities
│
├── tradr/                        # Core modules
│   ├── mt5/client.py             # MT5 API wrapper
│   └── risk/manager.py           # Risk management
│
├── data/                         # Historical data
│   ├── ohlcv/                    # OHLCV CSV files (2003-2025)
│   └── sr_levels/                # S/R levels (not integrated)
│
├── ftmo_analysis_output/         # Optimization results
│   ├── TPE/                      # Single-objective runs
│   ├── NSGA/                     # Multi-objective runs
│   └── VALIDATE/                 # Validation runs
│
└── docs/                         # Documentation
```

---

## 🔧 Live Bot Configuration

### Current Deployment
| Setting | Value |
|---------|-------|
| **Broker** | Forex.com Demo |
| **Account Size** | $50,000 |
| **Risk per Trade** | 0.6% = $300 |
| **Symbols** | 25 (JPY pairs + XAG excluded) |
| **Session Hours** | 08:00-22:00 UTC |
| **Scan Time** | 22:05 UTC (daily close) |

### Live Bot Features
| Feature | Description |
|---------|-------------|
| **Daily Close Scan** | Only at 22:05 UTC (complete candles) |
| **Spread Monitoring** | Every 10 min, execute when spread OK |
| **Session Filter** | London/NY hours only (08:00-22:00 UTC) |
| **Graduated Risk** | 3-tier protection (2%/3.5%/4.5%) |
| **Partial TPs** | Market orders at TP1/TP2/TP3 |
| **BE + Buffer** | Move SL after TP1 hit |

### Persistence Files
| File | Purpose |
|------|---------|
| `pending_setups.json` | Pending limit orders |
| `awaiting_spread.json` | Signals waiting for spread |
| `challenge_state.json` | Risk manager state |
| `trading_days.json` | Profitable days tracking |

---

## 🎯 Next Steps

1. **Monitor Forex.com Demo**: Wait for first trades (market opens Jan 2, 2025)
2. **Validate Performance**: Compare live results with backtest expectations
3. **Switch to 5ers Live**: After successful demo period
4. **Complete 5ers Challenge**: Step 1 (8%) + Step 2 (5%) in ~28 days

---

## 📚 Documentation

- [README.md](README.md) - Quick start guide
- [docs/CHANGELOG.md](docs/CHANGELOG.md) - Version history
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
- [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) - Deployment instructions
- [.github/copilot-instructions.md](.github/copilot-instructions.md) - AI assistant guide

---

**Last Updated**: 2025-12-31
