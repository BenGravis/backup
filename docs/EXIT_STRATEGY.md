# Exit Strategy - 5-TP System

## Overview

The trading strategy uses a **5 Take Profit Level** exit system with partial position closing and dynamic trailing stops.

> ⚠️ **CRITICAL**: This 5-TP system is essential for correct R calculations. Attempts to simplify to 3 TPs have been proven to break the exit logic.

---

## Take Profit Levels

| Level | R-Multiple | Close % | Cumulative Closed |
|-------|------------|---------|-------------------|
| TP1 | 0.6R | 10% | 10% |
| TP2 | 1.2R | 10% | 20% |
| TP3 | 2.0R | 15% | 35% |
| TP4 | 2.5R | 20% | 55% |
| TP5 | 3.5R | 45% | 100% |

### Parameters
```python
# R-Multiples (in strategy_core.py StrategyParams)
atr_tp1_multiplier: float = 0.6
atr_tp2_multiplier: float = 1.2
atr_tp3_multiplier: float = 2.0
atr_tp4_multiplier: float = 2.5
atr_tp5_multiplier: float = 3.5

# Close Percentages
tp1_close_pct: float = 0.10  # 10%
tp2_close_pct: float = 0.10  # 10%
tp3_close_pct: float = 0.15  # 15%
tp4_close_pct: float = 0.20  # 20%
tp5_close_pct: float = 0.45  # 45%
```

---

## Trailing Stop Logic

### Activation
Trailing stop activates after **TP1 is hit**, controlled by `trail_activation_r` parameter (default 0.65).

### Movement Rules

| Event | Trailing SL Position |
|-------|---------------------|
| TP1 Hit | Move to entry (breakeven) |
| TP2 Hit | Move to TP1 + 0.5R |
| TP3 Hit | Move to TP2 + 0.5R |
| TP4 Hit | Move to TP3 + 0.5R |
| TP5 Hit | Close all remaining |

### Code Implementation
```python
# After TP1 hit (bullish example)
if tp1_rr >= params.trail_activation_r:
    trailing_sl = entry_price  # Breakeven

# After TP2 hit
if tp2_rr >= params.trail_activation_r and tp1 is not None:
    trailing_sl = tp1 + 0.5 * risk

# After TP3 hit
if tp3_rr >= params.trail_activation_r and tp2 is not None:
    trailing_sl = tp2 + 0.5 * risk
```

---

## Exit Scenarios

### Scenario A: Full TP5 Exit
All TPs hit in sequence:
```
Entry: 100.00, SL: 99.00 (risk = 1.00)
TP1: 100.60 → Close 10% at 0.6R
TP2: 101.20 → Close 10% at 1.2R  
TP3: 102.00 → Close 15% at 2.0R
TP4: 102.50 → Close 20% at 2.5R
TP5: 103.50 → Close 45% at 3.5R

Total R = 0.10*0.6 + 0.10*1.2 + 0.15*2.0 + 0.20*2.5 + 0.45*3.5
       = 0.06 + 0.12 + 0.30 + 0.50 + 1.575
       = 2.555R
```

### Scenario B: TP2 + Trailing Exit
Price reverses after TP2:
```
Entry: 100.00, SL: 99.00, TP1: 100.60, TP2: 101.20
TP1 hit → Trailing SL moves to 100.00
TP2 hit → Trailing SL moves to 100.60 + 0.50 = 101.10
Price reverses, hits trailing at 101.10

Trail R = (101.10 - 100.00) / 1.00 = 1.1R
Remaining after TP1+TP2 = 80%

Total R = 0.10*0.6 + 0.10*1.2 + 0.80*1.1 = 0.06 + 0.12 + 0.88 = 1.06R
```

### Scenario C: Pure Stop Loss
No TPs hit, SL triggered:
```
Entry: 100.00, SL: 99.00
Price drops to 99.00 immediately

Total R = -1.0R
```

---

## R Calculation Formula

### When Trade Closes
```python
# If TP5 hit (all TPs reached)
rr = (TP1_CLOSE_PCT * tp1_rr + 
      TP2_CLOSE_PCT * tp2_rr + 
      TP3_CLOSE_PCT * tp3_rr + 
      TP4_CLOSE_PCT * tp4_rr + 
      TP5_CLOSE_PCT * tp5_rr)

# If trailing stop hit after TP3
remaining_pct = TP4_CLOSE_PCT + TP5_CLOSE_PCT  # 0.65
rr = (TP1_CLOSE_PCT * tp1_rr + 
      TP2_CLOSE_PCT * tp2_rr + 
      TP3_CLOSE_PCT * tp3_rr + 
      remaining_pct * trail_rr)
```

---

## Implementation Location

### strategy_core.py
- `simulate_trades()` function (line ~2580)
- Contains complete exit logic for both bullish and bearish trades
- Handles all 5 TP levels and trailing stop

### tradr/backtest/h1_trade_simulator.py
- `H1TradeSimulator.simulate_trade()` method
- Hour-by-hour simulation matching strategy_core.py exactly

---

## Key Constants (params/defaults.py)

```python
PARAMETER_DEFAULTS = {
    # TP R-Multiples
    'atr_tp1_multiplier': 0.6,
    'atr_tp2_multiplier': 1.2,
    'atr_tp3_multiplier': 2.0,
    'atr_tp4_multiplier': 2.5,
    'atr_tp5_multiplier': 3.5,
    
    # Close Percentages
    'tp1_close_pct': 0.10,
    'tp2_close_pct': 0.10,
    'tp3_close_pct': 0.15,
    'tp4_close_pct': 0.20,
    'tp5_close_pct': 0.45,
    
    # Trailing
    'trail_activation_r': 0.65,
}
```

---

## Validation Results

With this 5-TP system (2023-2025):
- **Win Rate**: 71.8%
- **Average Winner**: ~1.5R
- **Total R**: +274.71R
- **Final Balance**: $1,160,462 (from $60,000)

---

**Last Updated**: January 4, 2026
