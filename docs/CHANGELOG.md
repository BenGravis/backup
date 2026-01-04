# Changelog

**Last Updated**: 2026-01-04
**Auto-generated**: From git commits and session logs

---

## v1.2.0 - Optimization Infrastructure Improvements (Jan 4, 2026)

### Real-Time Best Parameters Tracking
- ✨ **Auto-updating best_params.json**: File updates immediately when new best trial found
  - Located in `ftmo_analysis_output/TPE/best_params.json` (or NSGA for multi-objective)
  - Contains trial number, best score, and all parameters
  - Updated via progress callback during optimization
  - Visible even while optimization is running

### Fresh Optimization Start
- ✨ **Clean database with warm-start**: Started fresh with run009 baseline
  - Database: `regime_adaptive_v2_clean_warm.db`
  - Trial #0: Baseline parameters (TP 0.6R/1.2R/2.0R, partial_exit disabled, risk 0.65%)
  - Previous trials archived to `optuna_backups/` with timestamps
  - Warm-start ensures baseline is evaluated before exploration

### Bug Fixes
- ✅ **Import error fixed**: `DEFAULT_STRATEGY_PARAMS` → `PARAMETER_DEFAULTS`
  - Was causing crashes when saving best_params.json
  - Progress callback now works reliably
  - File location: `ftmo_challenge_analyzer.py` line 2147

### Optimization Settings
- Training Period: 2023-01-01 to 2024-09-30 (in-sample)
- Validation Period: 2024-10-01 to 2025-12-26 (out-of-sample)
- Target: 50 trials with TPE single-objective
- Warm-start: run009 baseline (proven 48.6% WR across 12 years)

---

## v1.1.0 - Live Bot Enhancements (Dec 31, 2025)

### Live Bot Features
- ✨ **Daily Close Scanning**: Scan only at 22:05 UTC (after NY close)
  - Ensures complete daily candles, matches backtest exactly
  - No more 4-hour interval scanning with partial candles
  
- ✨ **Spread Monitoring**: Every 10 min for signals awaiting better spread
  - Fresh signals saved to `awaiting_spread.json` if spread too wide
  - When spread improves → Execute with MARKET ORDER immediately
  - Signals expire after 12 hours
  
- ✨ **Spread-Only Entry Filter**: No session filter needed
  - All signals check spread quality only
  - Spread OK → Execute immediately
  - Spread wide → Save for retry every 10 min
  
- ✨ **3-Tier Graduated Risk Management**:
  | Tier | Daily DD | Action |
  |------|----------|--------|
  | 1 | ≥2.0% | Reduce risk: 0.6% → 0.4% |
  | 2 | ≥3.5% | Cancel all pending orders |
  | 3 | ≥4.5% | Emergency close positions |

### Live Bot Sync with TPE Optimizer
- ✅ **Quality Factors**: Now uses `max(1, confluence_score // 3)` (identical to backtest)
- ✅ **Volatile Asset Boost**: Applied via `apply_volatile_asset_boost()` for XAU_USD, NAS100_USD, GBP_JPY, BTC_USD
- ✅ **Active Status Check**: Uses boosted scores with `min_quality_for_active = max(1, min_quality_factors - 1)`

### Multi-Broker Support
- ✨ **Forex.com Demo** ($50K): For testing before 5ers live
- ✨ **5ers Live** ($60K): Production trading
- ✨ **broker_config.py**: New multi-broker configuration
- ✨ **symbol_mapping.py**: Fixed index symbols (SPX500, NAS100, UK100 for Forex.com)

### Bug Fixes
- ✅ **Symbol mapping**: Fixed Forex.com indices (was US500 → now SPX500)
- ✅ **Excluded symbols**: JPY pairs and XAG_USD removed from Forex.com demo (min lot issues)
- ✅ **Session filter**: Only applies to intraday data, not daily backtests

---

## v1.0.0 - Production Release (Dec 31, 2025)

### Highlights
- Finalized 0.6% risk parameters; synced `best_params.json` and `params/current_params.json`.
- 12-year robustness validation (2014-2025): +2,766.3R, $995K, ~48.6% WR.
- FTMO compliance: daily DD <3.8% (limit 5%), total DD <3% (limit 10%).
- 5ers challenge speed: Step 1 (8%) in 18 dagen; Step 2 (5%) in 10 dagen; total 28 dagen.

### Parameters (Dec 31, 2025)
- Risk 0.6% per trade; min_confluence/score 2; min_quality_factors 3.
- ADX trend/range: 22 / 11; trend_min_confluence 6; range_min_confluence 2.
- ATR/trail: trail_activation_r 0.8; atr_trail_multiplier 1.6; atr_min_percentile 42; atr_volatility_ratio 0.95.
- TP ladder: 1.7R / 2.6R / 5.4R with closes 38% / 16% / 30%; partial_exit_at_1r true; partial_exit_pct 0.7.
- DD guards: daily_loss_halt_pct 3.8; max_total_dd_warning 7.9; consecutive_loss_halt 10.
- Filters baseline: HTF/structure/confirmation/fib/displacement/candle_rejection disabled.

---

## Previous Changes (Dec 30, 2025)

### New Features
- **NSGA-II Directory Structure**: Added dedicated output directories for multi-objective optimization
  - `ftmo_analysis_output/NSGA/` - NSGA-II optimization results
  - `ftmo_analysis_output/VALIDATE_NSGA/` - NSGA-II parameter validation
  - Automatic mode detection: `--multi` flag routes to NSGA directories

### Documentation
- Added `ftmo_analysis_output/NSGA/README.md` - NSGA-II optimization guide
- Added `ftmo_analysis_output/VALIDATE_NSGA/README.md` - NSGA-II validation guide  
- Added `ftmo_analysis_output/DIRECTORY_GUIDE.md` - Complete directory structure reference

---

## Previous Changes (Dec 29, 2025)

### New Features
- **Validation Mode**: Test existing parameters on different date ranges without running optimization
  ```bash
  python ftmo_challenge_analyzer.py --validate --start 2020-01-01 --end 2022-12-31 --params-file best_params.json
  ```

### Bug Fixes
- **CRITICAL**: Fixed parameter saving bug - ALL 30+ Optuna parameters now saved correctly
- **CRITICAL**: Fixed date handling in validation mode (datetime vs date objects)
- **Archive improvements**: Added missing files to history archives

---

## Previous Changes (Dec 28, 2025)

### New Features
- **FTMOComplianceTracker**: Compliance tracking with daily DD (4.5%), total DD (9%), streak halt
- **Parameter expansion**: 25+ optimizable parameters (TP scaling, 6 filter toggles, ADX regime)
- **TP scaling**: tp1/2/3_r_multiple (1.0-6.0R) and tp1/2/3_close_pct (0.15-0.40)
- **Filter toggles**: 6 new filters (HTF, structure, Fibonacci, confirmation, displacement, candle rejection)

### Critical Bug Fixes
- **0-trade bug**: Fixed aggressive filters/compliance penalties causing 0 trades
- **params_loader.py**: Removed obsolete `liquidity_sweep_lookback` parameter
- **Metric calculations**: Fixed win_rate (4700%→47%), Calmar ratio, total_return units
- **Optimization logs**: Fixed R=0.0 display bug for losing trials
- **Trade exports**: All 34 symbols now appear in CSV outputs
