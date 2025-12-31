# 5ers 60K High Stakes Trading Bot - AI Agent Instructions

## Project Overview
Automated MetaTrader 5 trading bot for **5ers 60K High Stakes** Challenge accounts. Two-environment architecture:
- **Live Bot** (`main_live_bot.py`): Runs on Windows VM with MT5 installed
- **Optimizer** (`ftmo_challenge_analyzer.py`): Runs anywhere (Replit/local) - no MT5 required

### Multi-Broker Support
The bot now supports multiple brokers for testing and production:
- **Forex.com Demo** ($50K): For testing before 5ers live
- **5ers Live** ($60K): Production trading

Set `BROKER_TYPE=forexcom_demo` or `BROKER_TYPE=fiveers_live` in `.env`

## Architecture & Data Flow

```
broker_config.py                 ← Multi-broker configuration (Forex.com, 5ers)
params/optimization_config.json  ← Optimization mode settings (multi-obj, ADX, etc.)
params/current_params.json       ← Optimized strategy parameters
         ↑                            ↓
ftmo_challenge_analyzer.py      main_live_bot.py
(Optuna optimization)           (loads params at startup)
         ↑
data/ohlcv/{SYMBOL}_{TF}_2003_2025.csv  (historical data)
```

### Key Modules
| File | Purpose |
|------|---------|
| `strategy_core.py` | Trading strategy logic - 7 Confluence Pillars, regime detection |
| `broker_config.py` | Multi-broker configuration (Forex.com, 5ers) |
| `params/params_loader.py` | Load/save optimized parameters from JSON |
| `params/optimization_config.py` | Unified optimization config (DB path, mode toggles) |
| `config.py` | Account settings, CONTRACT_SPECS (pip values), tradable symbols |
| `ftmo_config.py` | 5ers challenge rules, risk limits, TP/SL settings |
| `symbol_mapping.py` | Multi-broker symbol conversion (`EUR_USD` → broker-specific) |
| `tradr/mt5/client.py` | MT5 API wrapper (Windows only) |
| `tradr/risk/manager.py` | 5ers drawdown tracking, pre-trade risk checks |

## Live Bot Features (Dec 31, 2025)

### Daily Close Scanning
- **Scan Time**: Only at 22:05 UTC (after NY close)
- **Why**: Ensures complete daily candles, matches backtest exactly
- **Benefit**: No partial candle analysis, consistent with TPE optimizer

### Spread Monitoring (After Daily Close)
- Fresh signals saved to `awaiting_spread.json` if spread too wide
- Every 10 minutes: check if spread improved
- Good spread → Execute with **MARKET ORDER** immediately
- Signals expire after 12 hours

### Session Filter
- Orders only placed during London/NY hours (08:00-22:00 UTC)
- Exception: Fresh signals with tight spread can execute after daily close
- Spread requirement for off-hours: 25% tighter than normal max

### Graduated Risk Management (3-Tier)
| Tier | Daily DD | Action |
|------|----------|--------|
| 1 | ≥2.0% | Reduce risk: 0.6% → 0.4% |
| 2 | ≥3.5% | Cancel all pending orders |
| 3 | ≥4.5% | Emergency close positions |

### Partial Take Profits (Market Orders)
- **TP1**: Close 45% at 0.8-1R, move SL to BE+buffer
- **TP2**: Close 30% at 2R
- **TP3**: Close 25% at 3-4R
- All closes use `TRADE_ACTION_DEAL` (market order)
- Checked every 30 seconds

## Critical Conventions

### Live Bot Synced with TPE Optimizer (Dec 31, 2025)
**Quality factors calculation now IDENTICAL:**
```python
# BOTH use this formula (strategy_core.py generate_signals):
quality_factors = max(1, confluence_score // 3)

# BOTH apply volatile asset boost:
boosted_confluence, boosted_quality = apply_volatile_asset_boost(
    symbol, confluence_score, quality_factors, params.volatile_asset_boost
)

# BOTH use same active threshold:
min_quality_for_active = max(1, params.min_quality_factors - 1)
if boosted_confluence >= MIN_CONFLUENCE and boosted_quality >= min_quality_for_active:
    is_active = True
```

### Multi-Broker Symbol Mapping
Symbol mapping is broker-aware:
```python
from symbol_mapping import get_broker_symbol, get_internal_symbol

# Convert internal -> broker
broker_sym = get_broker_symbol("EUR_USD", "forexcom")  # -> "EURUSD"
broker_sym = get_broker_symbol("SPX500_USD", "fiveers")  # -> "US500.cash"
broker_sym = get_broker_symbol("SPX500_USD", "forexcom")  # -> "SPX500"
```

### Symbol Format
- **Config/data files**: OANDA format with underscores (`EUR_USD`, `XAU_USD`)
- **MT5 execution**: Broker-specific format (`EURUSD`, `XAUUSD`, `SPX500`)
- Always use `symbol_mapping.py` for conversions

### Parameters - NEVER Hardcode
```python
# ✅ CORRECT: Load from params loader
from params.params_loader import load_strategy_params
params = load_strategy_params()

# ❌ WRONG: Hardcoding in source files
MIN_CONFLUENCE = 5  # Don't do this
```

### Historical SR Data
- **TPE optimizer**: Does NOT use historical_sr (passes `None`)
- **Live bot**: Does NOT use historical_sr (fallback to empty dict)
- **Both are IDENTICAL** - no sync issue here
- SR files exist in `data/sr_levels/` but are not integrated

### Data Requirements
The strategy uses MAXIMUM:
- Monthly: 21 candles (MT5 provides 24)
- Weekly: 21 candles (MT5 provides 104)
- Daily: 50 candles (MT5 provides 500)
- **MT5 data is SUFFICIENT for all strategy requirements**

## Development Commands

### Run Optimization (resumable)

**Recommended: Use helper script for background runs**
```bash
./run_optimization.sh --single --trials 100  # TPE (logs to ftmo_analysis_output/TPE/run.log)
./run_optimization.sh --multi --trials 100   # NSGA-II (logs to ftmo_analysis_output/NSGA/run.log)
tail -f ftmo_analysis_output/TPE/run.log     # Monitor complete output
```

**Direct Python execution**
```bash
python ftmo_challenge_analyzer.py             # Run/resume optimization
python ftmo_challenge_analyzer.py --status    # Check progress
python ftmo_challenge_analyzer.py --config    # Show current configuration
python ftmo_challenge_analyzer.py --trials 100  # Set trial count
python ftmo_challenge_analyzer.py --multi     # Use NSGA-II multi-objective
python ftmo_challenge_analyzer.py --single    # Use TPE single-objective
python ftmo_challenge_analyzer.py --adx       # Enable ADX regime filtering
```

### Run Live Bot (Windows VM only)
```bash
# Requires .env with MT5_SERVER, MT5_LOGIN, MT5_PASSWORD
python main_live_bot.py
```

## 5ers Challenge Rules (hardcoded limits)
- Max daily loss: **5%** (halt at 4.2%)
- Max total drawdown: **10%** (emergency at 7%)
- Step 1 target: **8%**, Step 2: **5%**
- Min profitable days: **3**
- Risk per trade: 0.6% = $360 per R (on 60K account)

## File Locations
- Historical data: `data/ohlcv/{SYMBOL}_{TF}_2003_2025.csv`
- SR levels (unused): `data/sr_levels/{SYMBOL}_{TF}_sr.json`
- Optimized params: `params/current_params.json`
- Backtest output: `ftmo_analysis_output/`
- Logs: `logs/tradr_live.log`
- Pending setups: `pending_setups.json`
- Awaiting spread: `awaiting_spread.json`
- Documentation: `docs/`

## Testing Strategy Changes
1. Modify `strategy_core.py` (contains `compute_confluence()`, `simulate_trades()`)
2. Run optimizer: `python ftmo_challenge_analyzer.py --trials 50`
3. Check `ftmo_analysis_output/` for trade CSVs and performance metrics
4. Verify OOS (out-of-sample) performance matches training period

## Common Patterns

### Adding a New Indicator Filter
```python
# In strategy_core.py StrategyParams dataclass
use_my_filter: bool = False
my_threshold: float = 0.5

# In compute_confluence() function
if params.use_my_filter and my_indicator < params.my_threshold:
    return Signal(...)  # Skip or adjust
```

### Adding to Optimization
```python
# In ftmo_challenge_analyzer.py objective function
my_param = trial.suggest_float("my_param", 0.1, 2.0)
```
