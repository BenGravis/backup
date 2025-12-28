# config.py
"""
Configuration for the trading bot

SYMBOL FORMATS:
- All symbols in this file use OANDA format (with underscores)
- Examples: EUR_USD, XAU_USD, SPX500_USD
- These are converted to broker format (EURUSD, XAUUSD, US500.cash) via symbol_mapping.py
- Conversion happens automatically in main_live_bot.py using the symbol_map

DATA SOURCES:
- Forex pairs: OANDA Practice API (68 pairs available)
- Metals, Indices, Crypto: Yahoo Finance (yfinance) - FREE, no API key
  - See scripts/download_yahoo_data.py for historical data download
"""

import os
from pathlib import Path

# Load environment variables from .env file (for Windows VM or local dev)
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(env_file, override=True)
        print(f"[config] ✓ Loaded environment from {env_file}")
    else:
        print(f"[config] WARNING: .env file not found at {env_file}")
        print(f"[config] Looking in: {Path(__file__).parent.absolute()}")
except ImportError:
    print("[config] ERROR: python-dotenv not installed!")
    print("[config] Install it with: pip install python-dotenv")
except Exception as e:
    print(f"[config] ERROR loading .env: {e}")

from challenge_rules import FIVERS_10K_RULES


# ==== FTMO Challenge Risk Model ====
# All challenge rules are centralized in challenge_rules.py
# These values are exported for backward compatibility

ACCOUNT_CURRENCY = FIVERS_10K_RULES.account_currency
ACCOUNT_SIZE = FIVERS_10K_RULES.account_size  # 200,000 USD (FTMO 200K)
MAX_DAILY_LOSS_PCT = FIVERS_10K_RULES.max_daily_loss_pct / 100  # 0.05 (5%)
MAX_TOTAL_LOSS_PCT = FIVERS_10K_RULES.max_total_drawdown_pct / 100  # 0.10 (10%)
RISK_PER_TRADE_PCT = FIVERS_10K_RULES.risk_per_trade_pct / 100  # 0.01 (1%)
MAX_OPEN_RISK_PCT = FIVERS_10K_RULES.max_open_risk_pct / 100  # 0.03 (3%)
MIN_WITHDRAWAL_USD = 150

# Challenge-specific constants (FTMO)
STEP1_PROFIT_TARGET_PCT = FIVERS_10K_RULES.step1_profit_target_pct  # 10% (FTMO Challenge)
STEP2_PROFIT_TARGET_PCT = FIVERS_10K_RULES.step2_profit_target_pct  # 5% (Verification)
MIN_PROFITABLE_DAYS = FIVERS_10K_RULES.min_profitable_days  # 0 (no minimum for FTMO)
PROFITABLE_DAY_THRESHOLD_PCT = FIVERS_10K_RULES.profitable_day_threshold_pct  # 0 (N/A for FTMO)

CONTRACT_SPECS = {
    "EUR_USD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "GBP_USD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "USD_JPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "USD_CHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "USD_CAD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "AUD_USD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "NZD_USD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "EUR_GBP": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "EUR_JPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "EUR_CHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "EUR_AUD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "EUR_CAD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "EUR_NZD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "GBP_JPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "GBP_CHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "GBP_AUD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "GBP_CAD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "GBP_NZD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "AUD_JPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "AUD_CHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "AUD_CAD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "AUD_NZD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "NZD_JPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "NZD_CHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "NZD_CAD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "CAD_JPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "CAD_CHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "CHF_JPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    
    # === Metals (data from Yahoo Finance) ===
    "XAU_USD": {"pip_value": 0.01, "contract_size": 100, "pip_location": 2},     # Gold: $0.01 per pip, 100 oz contract
    "XAG_USD": {"pip_value": 0.001, "contract_size": 5000, "pip_location": 3},   # Silver: $0.001 per pip, 5000 oz contract
    
    # === Indices (data from Yahoo Finance) ===
    "SPX500_USD": {"pip_value": 0.1, "contract_size": 1, "pip_location": 1},     # S&P 500: 0.1 point = 1 pip
    "NAS100_USD": {"pip_value": 0.1, "contract_size": 1, "pip_location": 1},     # Nasdaq 100: 0.1 point = 1 pip
    
    # === Crypto (data from Yahoo Finance) ===
    "BTC_USD": {"pip_value": 1.0, "contract_size": 1, "pip_location": 0},        # Bitcoin: $1 = 1 pip
    "ETH_USD": {"pip_value": 0.01, "contract_size": 1, "pip_location": 2},       # Ethereum: $0.01 = 1 pip
}


# How strict the confluence engine is.
# "standard"  = balanced trades and quality (recommended for live trading)
# "aggressive" = more trades, looser filters (for experimentation/backtesting)
# Set SIGNAL_MODE environment variable to override, e.g., SIGNAL_MODE=aggressive
SIGNAL_MODE = os.getenv("SIGNAL_MODE", "standard")

# Confluence thresholds for each mode
MIN_CONFLUENCE_STANDARD = 4  # 4/7 confluence for standard mode
MIN_CONFLUENCE_AGGRESSIVE = 2  # 2/7 confluence for aggressive mode


# ==== Data source: OANDA (practice) ====

OANDA_API_KEY = os.getenv("OANDA_API_KEY")          # set in Replit secrets
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")    # set in Replit secrets
OANDA_API_URL = "https://api-fxpractice.oanda.com"  # practice endpoint

# Granularity mapping for OANDA
GRANULARITY_MAP = {
    "M": "M",      # Monthly
    "W": "W",      # Weekly
    "D": "D",      # Daily
    "H4": "H4",    # 4-hour
}


# ==== Instruments & groups ====
# All available OANDA Practice instruments (68 forex pairs)
# Note: OANDA Practice only has CURRENCY pairs - no metals, indices, or crypto

FOREX_PAIRS = [
    # === G10 Majors ===
    "EUR_USD", "GBP_USD", "USD_JPY", "USD_CHF", "USD_CAD", "AUD_USD", "NZD_USD",
    
    # === EUR Crosses ===
    "EUR_AUD", "EUR_CAD", "EUR_CHF", "EUR_CZK", "EUR_DKK", "EUR_GBP", "EUR_HKD",
    "EUR_HUF", "EUR_JPY", "EUR_NOK", "EUR_NZD", "EUR_PLN", "EUR_SEK", "EUR_SGD",
    "EUR_TRY", "EUR_ZAR",
    
    # === GBP Crosses ===
    "GBP_AUD", "GBP_CAD", "GBP_CHF", "GBP_HKD", "GBP_JPY", "GBP_NZD", "GBP_PLN",
    "GBP_SGD", "GBP_ZAR",
    
    # === AUD Crosses ===
    "AUD_CAD", "AUD_CHF", "AUD_HKD", "AUD_JPY", "AUD_NZD", "AUD_SGD",
    
    # === NZD Crosses ===
    "NZD_CAD", "NZD_CHF", "NZD_HKD", "NZD_JPY", "NZD_SGD",
    
    # === CAD Crosses ===
    "CAD_CHF", "CAD_HKD", "CAD_JPY", "CAD_SGD",
    
    # === CHF Crosses ===
    "CHF_HKD", "CHF_JPY", "CHF_ZAR",
    
    # === USD Exotic Crosses ===
    "USD_CNH", "USD_CZK", "USD_DKK", "USD_HKD", "USD_HUF", "USD_MXN", "USD_NOK",
    "USD_PLN", "USD_SEK", "USD_SGD", "USD_THB", "USD_TRY", "USD_ZAR",
    
    # === Other Exotic Crosses ===
    "HKD_JPY", "SGD_CHF", "SGD_JPY", "TRY_JPY", "ZAR_JPY",
]

# === NON-FOREX ASSETS (data from Yahoo Finance, not OANDA) ===
# These use Yahoo Finance for historical data and live quotes

# Metals - using futures data from Yahoo Finance
METALS = [
    "XAU_USD",  # Gold (GC=F futures on Yahoo)
    "XAG_USD",  # Silver (SI=F futures on Yahoo)
]

# Indices - using E-mini futures from Yahoo Finance
INDICES = [
    "SPX500_USD",  # S&P 500 E-mini (ES=F on Yahoo)
    "NAS100_USD",  # Nasdaq 100 E-mini (NQ=F on Yahoo)
]

# Crypto - from Yahoo Finance
CRYPTO_ASSETS = [
    "BTC_USD",  # Bitcoin (BTC-USD on Yahoo)
    "ETH_USD",  # Ethereum (ETH-USD on Yahoo)
]

# Convenience groups

def all_market_instruments() -> list[str]:
    """All instruments Blueprint can scan (OANDA format)."""
    return sorted(set(
        FOREX_PAIRS + METALS + INDICES + CRYPTO_ASSETS
    ))