# PROJECT OVERVIEW - FTMO 200K Trading Bot

**START HERE** - This is the first file to read to understand the entire project.

---

## 1. Project Summary

This is an automated **MetaTrader 5 Trading Bot** designed specifically for **FTMO 200K Challenge accounts**, paired with a **Walk-Forward Optimization System**.

- **Account Size**: $200,000 USD
- **Platform**: MetaTrader 5 (MT5)
- **Strategy**: 7 Confluence Pillars (multi-timeframe analysis)
- **Optimization**: Self-optimizing using 2024 historical data

---

## 2. Two Main Components

### A. `main_live_bot.py` - Live Trading Bot
**Runs on: Windows VM with MetaTrader 5**

The primary live trading bot that:
- Executes trades 24/7 using the "7 Confluence Pillars" strategy
- Connects directly to MT5 for order execution
- Includes comprehensive FTMO-compliant risk management
- Supports 34 assets (Forex, Metals, Crypto, Indices)
- Manages pending orders, partial take-profits, and trailing stops

```bash
# Run on Windows VM with MT5 installed
python main_live_bot.py
```

### B. `ftmo_challenge_analyzer.py` - Walk-Forward Optimizer
**Runs on: Replit (no MT5 required)**

The optimization engine that:
- Backtests the strategy using 2024 historical OHLCV data
- Training Period: Jan-Sep 2024
- Validation Period: Oct-Dec 2024
- Runs multiple optimization iterations
- **Automatically updates** `main_live_bot.py`, `ftmo_config.py`, and `strategy_core.py` with best-performing parameters
- Generates detailed performance reports and trade logs

```bash
# Run on Replit
python ftmo_challenge_analyzer.py
```

---

## 3. How They Work Together

```
┌─────────────────────────────────────────────────────────────────┐
│                        REPLIT                                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           ftmo_challenge_analyzer.py                      │   │
│  │                                                           │   │
│  │   1. Load historical data (data/ohlcv/2024)               │   │
│  │   2. Run backtests with different parameters              │   │
│  │   3. Score results (win rate, R-multiple, drawdown)       │   │
│  │   4. Find optimal parameters                              │   │
│  │   5. AUTO-UPDATE these files:                             │   │
│  │      - main_live_bot.py (MIN_CONFLUENCE)                  │   │
│  │      - ftmo_config.py (risk_per_trade_pct, etc.)          │   │
│  │      - strategy_core.py (min_confluence, min_quality)     │   │
│  │   6. Save backups to ftmo_optimization_backups/           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Git sync / manual copy
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      WINDOWS VM                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              main_live_bot.py                             │   │
│  │                                                           │   │
│  │   1. Connect to MT5 broker (FTMO)                         │   │
│  │   2. Scan 34 assets every 4 hours                         │   │
│  │   3. Use OPTIMIZED parameters from analyzer               │   │
│  │   4. Place pending orders when setup detected             │   │
│  │   5. Manage positions (partial TPs, trailing SL)          │   │
│  │   6. Enforce FTMO risk rules                              │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Key Parameter Flow:**
- `min_confluence` - Minimum confluence score required (currently 5-6)
- `risk_per_trade_pct` - Risk per trade (0.5-1.0% = $1,000-$2,000)
- `min_quality_factors` - Minimum quality factors required
- TP levels (tp1_r_multiple, tp2_r_multiple, etc.)

---

## 4. Trading Strategy Overview

### The 7 Confluence Pillars

Each trade setup is scored 0-7 based on how many pillars align:

| # | Pillar | Description |
|---|--------|-------------|
| 1 | **HTF Bias** | Monthly/Weekly/Daily trend alignment |
| 2 | **Location** | Price at significant S/R zones |
| 3 | **Fibonacci** | Price in Golden Pocket (0.382-0.886 retracement) |
| 4 | **Liquidity** | Sweep of equal highs/lows (liquidity grab) |
| 5 | **Structure** | Break of Structure (BOS) or Change of Character (CHoCH) |
| 6 | **Confirmation** | 4H candle pattern confirmation |
| 7 | **Risk:Reward** | Minimum 1:1 R:R ratio |

**Trade Entry Requirement**: Minimum 5/7 confluence (configurable via optimizer)

### Multi-Timeframe Analysis

- **Monthly (MN)**: Long-term bias
- **Weekly (W1)**: Intermediate bias  
- **Daily (D1)**: Primary trend direction
- **4-Hour (H4)**: Entry timeframe

### 5 Take-Profit Levels with Partial Closes

| Level | R-Multiple | Close % |
|-------|------------|---------|
| TP1 | 1.5R | 25% |
| TP2 | 3.0R | 25% |
| TP3 | 5.0R | 20% |
| TP4 | 7.0R | 15% |
| TP5 | 10.0R | 15% |

---

## 5. Key Files Reference

### Core Trading Files
| File | Purpose |
|------|---------|
| `main_live_bot.py` | Live trading bot (runs on Windows VM with MT5) |
| `ftmo_challenge_analyzer.py` | Walk-forward optimizer (runs on Replit) |
| `strategy_core.py` | Core strategy logic (7 Confluence Pillars) |
| `ftmo_config.py` | FTMO-specific configuration and risk parameters |

### Data Files
| Directory/File | Purpose |
|----------------|---------|
| `data/ohlcv/` | Historical OHLCV data (2023-2024) for 34 assets |
| `tradr/mt5/client.py` | MT5 connection and order execution |
| `tradr/risk/manager.py` | Risk management logic |
| `tradr/risk/position_sizing.py` | Lot size calculations |
| `tradr/data/oanda.py` | OANDA API data fetching |

### Output Files
| Directory/File | Purpose |
|----------------|---------|
| `ftmo_analysis_output/` | Analysis results and trade logs |
| `ftmo_analysis_output/all_trades_jan_dec_2024.csv` | Complete trade history with all details |
| `ftmo_analysis_output/monthly_performance.csv` | Monthly breakdown |
| `ftmo_analysis_output/symbol_performance.csv` | Per-symbol performance |
| `ftmo_optimization_backups/` | Backup copies of each optimization iteration |

### Configuration Files
| File | Purpose |
|------|---------|
| `config.py` | General configuration and asset lists |
| `challenge_rules.py` | FTMO challenge rule definitions |
| `symbol_mapping.py` | Symbol format conversion (OANDA ↔ FTMO/MT5) |

---

## 6. Position Sizing

### Account Parameters
- **Account Size**: $200,000 USD
- **Risk Per Trade**: 0.5-1.0% ($1,000-$2,000 per trade)
- **Max Daily Loss**: 5% ($10,000)
- **Max Total Drawdown**: 10% ($20,000)

### Lot Size Calculation

The formula (from `tradr/risk/position_sizing.py`):

```
lot_size = risk_usd / (stop_pips × pip_value_per_lot)
```

**Example Calculations:**

| Asset | Risk | Stop Pips | Pip Value | Lot Size |
|-------|------|-----------|-----------|----------|
| EURUSD | $1,000 | 50 pips | $10/lot | 2.0 lots |
| GBPJPY | $1,000 | 80 pips | $6.67/lot | 1.87 lots |
| XAUUSD | $1,500 | 300 pips | $1/lot | 5.0 lots |

**Typical Lot Ranges**: 0.5 - 5.0 lots depending on:
- Stop loss distance (larger stop = smaller lot)
- Current risk mode (Aggressive/Normal/Conservative)
- Number of existing positions

### Contract Specifications

```python
CONTRACT_SPECS = {
    "EURUSD": {"pip_value": 0.0001, "contract_size": 100000},  # $10/pip/lot
    "USDJPY": {"pip_value": 0.01, "contract_size": 100000},    # ~$6.67/pip/lot
    "XAUUSD": {"pip_value": 0.01, "contract_size": 100},       # $1/pip/lot
    "BTCUSD": {"pip_value": 1.0, "contract_size": 1},          # $1/point
}
```

---

## 7. How to Use

### Run the Optimizer (Replit)
```bash
python ftmo_challenge_analyzer.py
```
This will:
1. Load 2024 historical data
2. Run backtests with various parameter combinations
3. Output results to `ftmo_analysis_output/`
4. Auto-update strategy files with optimal parameters
5. Save backups to `ftmo_optimization_backups/`

### Run the Live Bot (Windows VM)
```bash
python main_live_bot.py
```
Requires:
- MetaTrader 5 installed and running
- `.env` file with credentials:
```
MT5_SERVER=FTMO-Demo
MT5_LOGIN=your_account_number
MT5_PASSWORD=your_password
```

### View Status (Replit Web Server)
```bash
python main.py
```
Runs a web server showing bot status and performance.

---

## 8. For New Replit Projects

### Getting Started Checklist

1. **Read this file first** (PROJECT_OVERVIEW.md)

2. **Check current parameters** in `ftmo_config.py`:
   - `min_confluence_score`: Currently 6
   - `risk_per_trade_pct`: Currently 0.5%
   - `max_concurrent_trades`: Currently 7

3. **Review recent backtest results**:
   - `ftmo_analysis_output/all_trades_jan_dec_2024.csv` - All trades with details
   - `ftmo_analysis_output/monthly_performance.csv` - Monthly breakdown

4. **Understand the optimization history**:
   - Check `ftmo_optimization_backups/` for previous iterations
   - Each backup is timestamped (e.g., `ftmo_config_iter1_20251214_222402.py`)

5. **Key metrics to monitor**:
   - Win Rate: Target 80%+
   - Average R-Multiple: Target 1.5R+
   - Max Drawdown: Must stay under 10%
   - Challenge Pass Rate: Target 85%+

### Environment Variables Required

```bash
# OANDA API (for data fetching on Replit)
OANDA_API_KEY=your_oanda_key
OANDA_ACCOUNT_ID=your_account_id

# MT5 (for live trading on Windows VM)
MT5_SERVER=FTMO-Demo
MT5_LOGIN=your_account_number
MT5_PASSWORD=your_password
```

---

## 9. FTMO Challenge Rules Summary

| Rule | Phase 1 | Phase 2 | Funded |
|------|---------|---------|--------|
| Profit Target | 10% ($20,000) | 5% ($10,000) | N/A |
| Max Daily Loss | 5% ($10,000) | 5% ($10,000) | 5% |
| Max Total DD | 10% ($20,000) | 10% ($20,000) | 10% |
| Min Trading Days | 4 | 4 | N/A |
| Time Limit | Unlimited | Unlimited | N/A |

---

## 10. Supported Assets (34 Total)

### Forex Majors (7)
EUR_USD, GBP_USD, USD_JPY, USD_CHF, USD_CAD, AUD_USD, NZD_USD

### Forex Crosses (21)
EUR_GBP, EUR_JPY, EUR_CHF, EUR_AUD, EUR_CAD, EUR_NZD,
GBP_JPY, GBP_CHF, GBP_AUD, GBP_CAD, GBP_NZD,
AUD_JPY, AUD_CHF, AUD_CAD, AUD_NZD,
NZD_JPY, NZD_CHF, NZD_CAD,
CAD_JPY, CAD_CHF, CHF_JPY

### Metals (2)
XAU_USD (Gold), XAG_USD (Silver)

### Indices (2)
SPX500_USD (S&P 500), NAS100_USD (Nasdaq 100)

### Crypto (2)
BTC_USD (Bitcoin), ETH_USD (Ethereum)

---

## Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│                    QUICK COMMANDS                          │
├────────────────────────────────────────────────────────────┤
│ Optimize parameters:    python ftmo_challenge_analyzer.py  │
│ Run live bot:           python main_live_bot.py            │
│ View web status:        python main.py                     │
├────────────────────────────────────────────────────────────┤
│                    KEY PARAMETERS                          │
├────────────────────────────────────────────────────────────┤
│ Min Confluence:         5-6 (out of 7)                     │
│ Risk Per Trade:         0.5-1.0% ($1,000-$2,000)           │
│ Max Concurrent Trades:  7                                  │
│ Take Profits:           1.5R, 3R, 5R, 7R, 10R              │
├────────────────────────────────────────────────────────────┤
│                    KEY FILES                               │
├────────────────────────────────────────────────────────────┤
│ Strategy Logic:         strategy_core.py                   │
│ FTMO Config:            ftmo_config.py                     │
│ Trade Results:          ftmo_analysis_output/              │
│ Historical Data:        data/ohlcv/                        │
└────────────────────────────────────────────────────────────┘
```

---

*Last Updated: December 2024*
