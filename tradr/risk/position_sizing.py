"""
Position Sizing for FTMO Challenge Account.

Calculates lot sizes based on risk parameters and contract specifications.
"""

from typing import Dict, Optional


CONTRACT_SPECS = {
    "EURUSD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "GBPUSD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "USDJPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "USDCHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "USDCAD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "AUDUSD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "NZDUSD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "EURJPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "GBPJPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "EURGBP": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "EURCHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "EURAUD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "EURCAD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "EURNZD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "GBPCHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "GBPAUD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "GBPCAD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "GBPNZD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "AUDJPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "AUDCHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "AUDCAD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "AUDNZD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "NZDJPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "NZDCHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "NZDCAD": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "CADJPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "CADCHF": {"pip_value": 0.0001, "contract_size": 100000, "pip_location": 4},
    "CHFJPY": {"pip_value": 0.01, "contract_size": 100000, "pip_location": 2},
    "XAUUSD": {"pip_value": 1.0, "contract_size": 100, "pip_location": 0},  # Forex.com quotes in cents
    "XAGUSD": {"pip_value": 1.0, "contract_size": 5000, "pip_location": 0},  # Forex.com quotes in cents
    "US30": {"pip_value": 1.0, "contract_size": 1, "pip_location": 0},
    "US100": {"pip_value": 1.0, "contract_size": 1, "pip_location": 0},
    "US500": {"pip_value": 1.0, "contract_size": 1, "pip_location": 0},
    "SPX500USD": {"pip_value": 0.1, "contract_size": 1, "pip_location": 1},
    "NAS100USD": {"pip_value": 0.1, "contract_size": 1, "pip_location": 1},
    "BTCUSD": {"pip_value": 1.0, "contract_size": 1, "pip_location": 0},
    "ETHUSD": {"pip_value": 0.01, "contract_size": 1, "pip_location": 2},
}


def normalize_symbol(symbol: str) -> str:
    """Normalize symbol format (remove underscores, dots, etc)."""
    return symbol.replace("_", "").replace(".", "").replace("/", "").upper()


def get_contract_specs(symbol: str) -> Dict:
    """Get contract specifications for a symbol."""
    normalized = normalize_symbol(symbol)
    return CONTRACT_SPECS.get(normalized, {
        "pip_value": 0.0001,
        "contract_size": 100000,
        "pip_location": 4
    })


def get_pip_value(symbol: str, current_price: float = None) -> float:
    """
    Get pip value per standard lot in USD.
    
    Args:
        symbol: Trading symbol
        current_price: Current price (for quote currency conversion)
        
    Returns:
        Pip value in USD per standard lot
    """
    specs = get_contract_specs(symbol)
    pip_size = specs.get("pip_value", 0.0001)
    contract_size = specs.get("contract_size", 100000)
    
    normalized = normalize_symbol(symbol)
    
    if normalized.endswith("USD"):
        return pip_size * contract_size
    elif normalized.startswith("USD") and current_price and current_price > 0:
        return (pip_size / current_price) * contract_size
    elif normalized.startswith("USD"):
        if "JPY" in normalized:
            return (pip_size / 150.0) * contract_size
        else:
            return (pip_size / 1.0) * contract_size
    else:
        return pip_size * contract_size


def calculate_lot_size(
    symbol: str,
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_loss_price: float,
    max_lot: float = 10.0,
    min_lot: float = 0.01,
    existing_positions: int = 0,
) -> Dict:
    """
    Calculate position size for a trade.
    
    Args:
        symbol: Trading symbol
        account_balance: Current account balance in USD
        risk_percent: Risk per trade as decimal (e.g., 0.0075 for 0.75%)
        entry_price: Entry price level
        stop_loss_price: Stop loss price level
        max_lot: Maximum lot size allowed
        min_lot: Minimum lot size
        existing_positions: Number of open positions (for lot reduction)
        
    Returns:
        Dict with lot_size, risk_usd, stop_pips, actual_risk_pct
    """
    if entry_price is None or stop_loss_price is None:
        return {
            "lot_size": 0.0,
            "risk_usd": 0.0,
            "stop_pips": 0.0,
            "actual_risk_pct": 0.0,
            "error": "Invalid entry or stop loss"
        }
    
    specs = get_contract_specs(symbol)
    pip_value_unit = specs.get("pip_value", 0.0001)
    pip_location = specs.get("pip_location", 4)
    
    stop_distance = abs(entry_price - stop_loss_price)
    
    if pip_location == 0:
        stop_pips = stop_distance
    else:
        stop_pips = stop_distance / pip_value_unit
    
    if stop_pips <= 0:
        return {
            "lot_size": 0.0,
            "risk_usd": 0.0,
            "stop_pips": 0.0,
            "actual_risk_pct": 0.0,
            "error": "Stop loss too close to entry"
        }
    
    risk_usd = account_balance * risk_percent
    
    pip_value_per_lot = get_pip_value(symbol, entry_price)
    
    if pip_value_per_lot <= 0:
        return {
            "lot_size": min_lot,
            "risk_usd": risk_usd,
            "stop_pips": stop_pips,
            "actual_risk_pct": risk_percent,
            "error": "Could not calculate pip value"
        }
    
    lot_size = risk_usd / (stop_pips * pip_value_per_lot)
    
    if existing_positions > 0:
        reduction_factor = 1.0 / (existing_positions + 1)
        lot_size = lot_size * reduction_factor
    
    lot_size = round(lot_size, 2)
    lot_size = max(min_lot, min(max_lot, lot_size))
    
    actual_risk_usd = lot_size * stop_pips * pip_value_per_lot
    actual_risk_pct = actual_risk_usd / account_balance if account_balance > 0 else 0
    
    return {
        "lot_size": lot_size,
        "risk_usd": round(actual_risk_usd, 2),
        "stop_pips": round(stop_pips, 1),
        "actual_risk_pct": round(actual_risk_pct, 4),
    }
