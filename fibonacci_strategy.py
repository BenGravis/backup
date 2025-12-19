"""
Fibonacci Trading Strategy Module

Implements Fibonacci retracement analysis with:
- Body-to-wick anchoring (not wick-to-wick)
- Golden zone: 0.618-0.796 (entry at 0.66)
- Target levels: -0.25, -0.65, -1, -1.5 extensions
- Pattern chain: Inverse H&S → N → 5-wave structure
"""

from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class FibonacciLevels:
    """Stores Fibonacci retracement levels"""
    level_0: float  # Start (0%)
    level_236: float  # 0.236
    level_382: float  # 0.382
    level_500: float  # 0.5
    level_618: float  # 0.618
    level_786: float  # 0.786
    level_1: float  # 1 (full move)
    # Extension levels
    ext_neg_25: float  # -0.25
    ext_neg_65: float  # -0.65
    ext_1: float  # 1.0
    ext_15: float  # 1.5
    
    golden_zone_low: float  # 0.618
    golden_zone_high: float  # 0.796
    golden_pocket: float  # 0.66


def calculate_fib_levels(low: float, high: float, is_bullish: bool = True) -> FibonacciLevels:
    """
    Calculate Fibonacci retracement levels.
    
    Blueprint rule: Body-to-wick anchoring (not wick-to-wick)
    - Bullish: From red close (low) to green open (high)
    - Bearish: From green close (high) to red open (low)
    
    Args:
        low: Starting point (body of red candle for bullish)
        high: Ending point (wick of green candle for bullish)
        is_bullish: True for bullish setup, False for bearish
    
    Returns:
        FibonacciLevels object with all retracement and extension levels
    """
    move = high - low
    
    if is_bullish:
        # Bullish: Price retraces from high down to low
        level_236 = high - move * 0.236
        level_382 = high - move * 0.382
        level_500 = high - move * 0.5
        level_618 = high - move * 0.618
        level_786 = high - move * 0.786
        
        # Extensions (going below the low)
        ext_neg_25 = low - move * 0.25
        ext_neg_65 = low - move * 0.65
        ext_1 = low - move * 1.0
        ext_15 = low - move * 1.5
        
        golden_zone_low = high - move * 0.796  # Lower boundary of golden zone
        golden_zone_high = high - move * 0.618  # Upper boundary of golden zone
        golden_pocket = high - move * 0.66  # Entry point
    else:
        # Bearish: Price retraces from low up to high
        level_236 = low + move * 0.236
        level_382 = low + move * 0.382
        level_500 = low + move * 0.5
        level_618 = low + move * 0.618
        level_786 = low + move * 0.786
        
        # Extensions (going above the high)
        ext_neg_25 = high + move * 0.25
        ext_neg_65 = high + move * 0.65
        ext_1 = high + move * 1.0
        ext_15 = high + move * 1.5
        
        golden_zone_low = low + move * 0.618
        golden_zone_high = low + move * 0.796
        golden_pocket = low + move * 0.66
    
    return FibonacciLevels(
        level_0=low if is_bullish else high,
        level_236=level_236,
        level_382=level_382,
        level_500=level_500,
        level_618=level_618,
        level_786=level_786,
        level_1=high if is_bullish else low,
        ext_neg_25=ext_neg_25,
        ext_neg_65=ext_neg_65,
        ext_1=ext_1,
        ext_15=ext_15,
        golden_zone_low=min(golden_zone_low, golden_zone_high),
        golden_zone_high=max(golden_zone_low, golden_zone_high),
        golden_pocket=golden_pocket,
    )


def find_swing_high_low(candles: List[Dict], lookback: int = 20) -> Tuple[Optional[float], Optional[float], int, int]:
    """
    Find recent swing high and low for Fibonacci anchoring.
    
    Returns:
        Tuple of (swing_high, swing_low, high_bar_index, low_bar_index)
    """
    if len(candles) < lookback:
        lookback = len(candles)
    
    recent = candles[-lookback:]
    highs = [(i, c.get("high", 0)) for i, c in enumerate(recent)]
    lows = [(i, c.get("low", float("inf"))) for i, c in enumerate(recent)]
    
    if not highs or not lows:
        return None, None, -1, -1
    
    swing_high_idx, swing_high = max(highs, key=lambda x: x[1])
    swing_low_idx, swing_low = min(lows, key=lambda x: x[1])
    
    return swing_high, swing_low, swing_high_idx, swing_low_idx


def is_price_in_golden_zone(price: float, fib_levels: FibonacciLevels) -> bool:
    """Check if price is in the golden zone (0.618-0.796)"""
    return fib_levels.golden_zone_low <= price <= fib_levels.golden_zone_high


def detect_inverse_head_shoulders(candles: List[Dict], lookback: int = 30) -> Tuple[bool, str, Dict]:
    """
    Detect Inverse Head & Shoulders pattern (bullish reversal).
    
    Pattern: Left Shoulder (low) → Head (lower low) → Right Shoulder (low) → Breakout
    
    Returns:
        Tuple of (pattern_found, description, pattern_details)
    """
    if len(candles) < lookback:
        return False, "", {}
    
    recent = candles[-lookback:]
    lows = [c.get("low", float("inf")) for c in recent]
    highs = [c.get("high", 0) for c in recent]
    closes = [c.get("close", 0) for c in recent]
    
    # Find potential shoulders and head
    # This is a simplified detection - a proper implementation would use more sophisticated pivot detection
    if len(lows) < 5:
        return False, "", {}
    
    # Look for: low → lower low → low pattern
    for i in range(1, len(lows) - 2):
        left_shoulder = lows[i - 1]
        head = lows[i]
        right_shoulder = lows[i + 1]
        neckline = max(closes[i - 1], closes[i], closes[i + 1])
        
        # Inverse H&S: head is lower than shoulders
        if head < left_shoulder and head < right_shoulder:
            # Check for neckline breakout (BOS up)
            if i + 2 < len(closes) and closes[i + 2] > neckline:
                return True, "Inverse H&S: Bullish reversal pattern detected", {
                    "left_shoulder": left_shoulder,
                    "head": head,
                    "right_shoulder": right_shoulder,
                    "neckline": neckline,
                    "pattern_strength": abs(left_shoulder - head) / head if head > 0 else 0,
                }
    
    return False, "", {}


def detect_n_pattern(candles: List[Dict], lookback: int = 20) -> Tuple[bool, str]:
    """
    Detect N-pattern (bullish impulse after correction).
    
    Pattern: Down move → Correction up → Continuation of uptrend
    
    Returns:
        Tuple of (pattern_found, description)
    """
    if len(candles) < lookback:
        return False, ""
    
    recent = candles[-lookback:]
    closes = [c.get("close", 0) for c in recent]
    lows = [c.get("low", float("inf")) for c in recent]
    highs = [c.get("high", 0) for c in recent]
    
    if len(closes) < 5:
        return False, ""
    
    # Look for: down move, then up move (correction), then another up move (continuation)
    # Simplified check: look for a higher low after a swing low
    recent_lows = min(lows[-10:]), min(lows[-5:])
    recent_highs = max(highs[-10:]), max(highs[-5:])
    
    if recent_lows[1] > recent_lows[0] and recent_highs[1] > recent_highs[0]:
        return True, "N-Pattern: Bullish momentum continuation detected"
    
    return False, ""


def detect_5_wave_structure(candles: List[Dict], lookback: int = 30) -> Tuple[bool, str]:
    """
    Detect 5-wave Elliott Wave structure (strong bullish move).
    
    Returns:
        Tuple of (pattern_found, description)
    """
    if len(candles) < lookback:
        return False, ""
    
    recent = candles[-lookback:]
    highs = [c.get("high", 0) for c in recent]
    lows = [c.get("low", float("inf")) for c in recent]
    
    # Simplified 5-wave detection: look for 5 distinct higher highs and higher lows
    # This is very simplified - real Elliott Wave is more complex
    if len(highs) < 5:
        return False, ""
    
    high_trend = all(highs[i] < highs[i + 1] for i in range(len(highs) - 5, len(highs) - 1))
    low_trend = all(lows[i] < lows[i + 1] for i in range(len(lows) - 5, len(lows) - 1))
    
    if high_trend and low_trend:
        return True, "5-Wave: Strong Elliott Wave structure detected"
    
    return False, ""


def analyze_fib_setup(candles: List[Dict], direction: str, price: float) -> Dict[str, Any]:
    """
    Complete Fibonacci setup analysis.
    
    Args:
        candles: List of OHLCV candles
        direction: "bullish" or "bearish"
        price: Current price
    
    Returns:
        Dict with analysis results including entry, stops, and targets
    """
    is_bullish = direction == "bullish"
    
    # Find swing points for Fibonacci anchoring
    swing_high, swing_low, _, _ = find_swing_high_low(candles, lookback=20)
    
    if swing_high is None or swing_low is None:
        return {"valid": False, "reason": "Could not find swing points"}
    
    # Calculate Fibonacci levels
    fib_levels = calculate_fib_levels(swing_low, swing_high, is_bullish)
    
    # Check if price is in golden zone
    in_golden_zone = is_price_in_golden_zone(price, fib_levels)
    
    # Detect patterns
    inv_hs, inv_hs_desc, inv_hs_data = detect_inverse_head_shoulders(candles)
    n_pattern, n_pattern_desc = detect_n_pattern(candles)
    wave_5, wave_5_desc = detect_5_wave_structure(candles)
    
    # Determine entry and targets
    if is_bullish:
        entry = fib_levels.golden_pocket if in_golden_zone else price
        stop_loss = swing_low - (swing_high - swing_low) * 0.1  # 10% below swing low
        tp1 = fib_levels.ext_neg_25  # -0.25 extension
        tp2 = fib_levels.ext_neg_65  # -0.65 extension
        tp3 = fib_levels.ext_1       # -1.0 extension
        tp4 = fib_levels.ext_15      # -1.5 extension
    else:
        entry = fib_levels.golden_pocket if in_golden_zone else price
        stop_loss = swing_high + (swing_high - swing_low) * 0.1
        tp1 = fib_levels.ext_neg_25
        tp2 = fib_levels.ext_neg_65
        tp3 = fib_levels.ext_1
        tp4 = fib_levels.ext_15
    
    pattern_score = (int(inv_hs) + int(n_pattern) + int(wave_5)) * 2  # Each pattern worth 2 confluence points
    
    return {
        "valid": True,
        "in_golden_zone": in_golden_zone,
        "entry": entry,
        "stop_loss": stop_loss,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "tp4": tp4,
        "fib_levels": fib_levels,
        "pattern_score": pattern_score,
        "patterns": {
            "inverse_head_shoulders": inv_hs,
            "n_pattern": n_pattern,
            "five_wave": wave_5,
        },
        "pattern_notes": f"IHS:{inv_hs}, N:{n_pattern}, 5W:{wave_5}",
        "swing_high": swing_high,
        "swing_low": swing_low,
    }
