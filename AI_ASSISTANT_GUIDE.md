# AI Assistant Quick Start Guide

**Purpose**: This file helps AI assistants (GitHub Copilot, ChatGPT, Claude, etc.) quickly understand the 5ers 60K Trading Bot project.

**Last Updated**: 2026-01-04

---

## 🎯 Project Summary in 30 Seconds

**What**: Automated MetaTrader 5 trading bot for 5ers 60K High Stakes Challenge  
**Strategy**: 6-Pillar Confluence System with multi-timeframe analysis  
**Optimization**: Optuna (TPE/NSGA-II) with 25+ parameters, real-time best_params.json  
**Training Period**: 2023-01-01 to 2024-09-30 (21 months)
**Validation Period**: 2024-10-01 to 2025-12-26 (15 months)
**Deployment**: Windows VM (live bot) + Linux (optimizer)  
**Current Status**: Fresh TPE optimization running (50 trials, warm-start with run009 baseline)  
**Performance**: ~48% win rate, +2,766R over 12 years (2014-2025)

---

## 📁 Essential Files (Read These First)

### 1. Core Trading Logic
- **`strategy_core.py`** (3000+ lines) - Complete trading strategy implementation
  - `compute_confluence()` - Main entry signal logic (6 pillars)
  - `simulate_trades()` - Backtest engine
  - `generate_signals()` - Signal generation for optimization
  - `apply_volatile_asset_boost()` - Boost for XAU, NAS100, GBP_JPY, BTC

### 2. Optimization Engine
- **`ftmo_challenge_analyzer.py`** (3900 lines) - Parameter optimization & backtesting
  - Dual-mode: TPE (fast) or NSGA-II (multi-objective)
  - 25+ parameter search space
  - Training/Validation/Full-period backtests
  - Saves results to `ftmo_analysis_output/TPE/` or `NSGA/`

### 3. Live Trading Bot
- **`main_live_bot.py`** (2000+ lines) - Production MT5 execution
  - Loads params from `params/current_params.json`
  - Scans at 22:05 UTC (daily close only)
  - Spread-only entry filter (no session filter)
  - Spread monitoring every 10 min
  - 3-tier graduated risk management

### 4. Multi-Broker Support
- **`broker_config.py`** - Forex.com Demo / 5ers Live configuration
- **`symbol_mapping.py`** - OANDA ↔ broker symbol conversion

### 5. Configuration
- **`params/current_params.json`** - Active strategy parameters
- **`params/optimization_config.json`** - Optimization settings
- **`config.py`** - Contract specs (pip values for 34 assets)
- **`ftmo_config.py`** - 5ers challenge rules & limits

---

## 🗂️ Directory Structure

```
ftmotrial/
├── Core Files
│   ├── strategy_core.py           # Trading strategy (6 pillars)
│   ├── ftmo_challenge_analyzer.py # Optimization engine
│   ├── main_live_bot.py           # Live MT5 bot (Windows)
│   ├── broker_config.py           # Multi-broker configuration
│   ├── symbol_mapping.py          # Symbol conversion
│   ├── config.py                  # Contract specs, symbols
│   └── ftmo_config.py             # 5ers rules
│
├── params/ (PARAMETER MANAGEMENT)
│   ├── current_params.json        # Active params (loaded by bot)
│   ├── optimization_config.json   # Optimization settings
│   └── params_loader.py           # Load/save utilities
│
├── tradr/ (MODULES)
│   ├── mt5/client.py              # MT5 API wrapper
│   └── risk/manager.py            # Risk management
│
├── data/ (HISTORICAL DATA)
│   ├── ohlcv/                     # OHLCV CSV files (2003-2025)
│   └── sr_levels/                 # S/R levels (not integrated)
│
├── ftmo_analysis_output/ (RESULTS)
│   ├── TPE/                       # Single-objective runs
│   ├── NSGA/                      # Multi-objective runs
│   └── VALIDATE/                  # Validation runs
│
└── docs/ (DOCUMENTATION)
```

---

## 🔑 Key Concepts for AI Understanding

### 1. Optimization Infrastructure (Jan 4, 2026)

**Real-Time Best Parameters Tracking**:
- `ftmo_analysis_output/TPE/best_params.json` auto-updates during optimization
- Updates immediately when new best trial found
- Contains trial number, score, and all parameters
- Monitor with: `watch -n 5 cat ftmo_analysis_output/TPE/best_params.json`

**Warm-Start from Baseline**:
- Trial #0: run009 baseline (0.6R/1.2R/2.0R, partial_exit disabled, 0.65% risk)
- Proven performance: 48.6% WR across 12 years (2014-2025)
- Parameter space exploration starts after baseline evaluation

**Database Management**:
- Current: `regime_adaptive_v2_clean_warm.db`
- Old trials archived to `optuna_backups/` with timestamps
- Resume support: optimization continues from last trial

### 2. Live Bot Features (Dec 31, 2025)

**Daily Close Scanning**:
- Scan only at 22:05 UTC (after NY close)
- Ensures complete daily candles
- Matches backtest exactly

**Spread-Only Entry Filter (No Session Filter)**:
- Fresh signals saved to `awaiting_spread.json` if spread too wide
- Every 10 min: check if spread improved
- Good spread → MARKET ORDER immediately
- Signals expire after 12 hours

**3-Tier Graduated Risk**:
| Tier | Daily DD | Action |
|------|----------|--------|
| 1 | ≥2.0% | Reduce risk: 0.6% → 0.4% |
| 2 | ≥3.5% | Cancel all pending orders |
| 3 | ≥4.5% | Emergency close positions |

### 3. Live Bot Synced with TPE Optimizer

**CRITICAL**: Both use IDENTICAL logic:
```python
# Quality factors calculation (BOTH):
quality_factors = max(1, confluence_score // 3)

# Volatile asset boost (BOTH):
boosted_confluence, boosted_quality = apply_volatile_asset_boost(
    symbol, confluence_score, quality_factors, params.volatile_asset_boost
)

# Active status check (BOTH):
min_quality_for_active = max(1, params.min_quality_factors - 1)
if boosted_confluence >= MIN_CONFLUENCE and boosted_quality >= min_quality_for_active:
    is_active = True
```

### 4. Parameters - NEVER Hardcode

**Correct**:
```python
from params.params_loader import load_strategy_params
params = load_strategy_params()
```

**Wrong**:
```python
MIN_CONFLUENCE = 5  # Don't hardcode!
```

**Parameter Loading Pitfall** (Fixed Jan 4, 2026):
```python
# ❌ WRONG: This import doesn't exist
from params.defaults import DEFAULT_STRATEGY_PARAMS

# ✅ CORRECT: Use this import
from params.defaults import PARAMETER_DEFAULTS
```

### 5. Multi-Broker Symbol Mapping

```python
from symbol_mapping import get_broker_symbol

# Forex.com examples:
get_broker_symbol("EUR_USD", "forexcom")    # → "EURUSD"
get_broker_symbol("SPX500_USD", "forexcom") # → "SPX500"
get_broker_symbol("NAS100_USD", "forexcom") # → "NAS100"
```

### 5. Historical SR Data

**NOT INTEGRATED**: Both TPE optimizer and live bot pass `historical_sr=None`.
SR files exist in `data/sr_levels/` but are not used.

### 6. Data Requirements

The strategy uses MAXIMUM:
- Monthly: 21 candles (MT5 provides 24)
- Weekly: 21 candles (MT5 provides 104)
- Daily: 50 candles (MT5 provides 500)

**MT5 data is SUFFICIENT** for all strategy requirements.

---

## 💻 Development Commands

### Run Optimization
```bash
./run_optimization.sh --single --trials 100  # TPE
./run_optimization.sh --multi --trials 100   # NSGA-II
python ftmo_challenge_analyzer.py --status   # Check progress
```

### Run Live Bot (Windows VM)
```bash
python main_live_bot.py
```

### Update VM After Code Changes
```cmd
cd C:\Users\Administrator\ftmotrial
git pull
schtasks /End /TN "FTMO_Live_Bot"
schtasks /Run /TN "FTMO_Live_Bot"
```

---

## 📁 Persistence Files

| File | Purpose |
|------|---------|
| `pending_setups.json` | Pending limit orders |
| `awaiting_spread.json` | Signals waiting for better spread |
| `challenge_state.json` | Risk manager state |
| `trading_days.json` | Profitable days tracking |

---

## 🎯 5ers Challenge Rules

| Rule | Limit | Bot Behavior |
|------|-------|--------------|
| Max Daily Loss | 5% | Halt at 4.2% |
| Max Total DD | 10% | Emergency at 7% |
| Step 1 Target | 8% | ~18 days expected |
| Step 2 Target | 5% | ~10 days expected |
| Min Profitable Days | 3 | ~68 trades/month |
| Risk per Trade | 0.6% | $360 per R (60K) |

---

**Last Updated**: 2025-12-31
