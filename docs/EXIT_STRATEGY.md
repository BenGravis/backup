# Exit Strategy - Complete Technical Documentation

> **Doel**: Dit document beschrijft EXACT hoe de exit strategy werkt in de huidige backtest code (`strategy_core.py`), zodat een toekomstige H1-based backtester exact dezelfde logica kan implementeren.

## 1. Overzicht

De exit strategy gebruikt een **gefaseerde take-profit structuur** met 5 TP niveaus en een dynamische trailing stop. De positie wordt in delen gesloten naarmate TP niveaus worden bereikt.

### Key Functies
| Functie | Bestand | Regel | Doel |
|---------|---------|-------|------|
| `simulate_trades()` | strategy_core.py | 2562 | Hoofdfunctie voor trade simulatie en exits |
| `calculate_risk_reward()` | strategy_core.py | 2232 | Berekent TP niveaus bij signal generatie |
| `generate_signals()` | strategy_core.py | 2384 | Genereert signals met TP niveaus |

---

## 2. Take Profit Niveaus

### 2.1 TP Berekening in Signal Generatie

De TP niveaus worden berekend in `calculate_risk_reward()` (stratgy_core.py:2232-2380) met **ATR-based multipliers**:

```python
# strategy_core.py line 2322-2327 (bullish)
risk = entry - sl
tp1 = entry + risk * params.atr_tp1_multiplier  # Default: 0.6
tp2 = entry + risk * params.atr_tp2_multiplier  # Default: 1.2
tp3 = entry + risk * params.atr_tp3_multiplier  # Default: 2.0
tp4 = entry + risk * 2.5                        # Hardcoded
tp5 = entry + risk * 3.5                        # Hardcoded
```

**⚠️ BELANGRIJK**: De parameters `tp1_r_multiple`, `tp2_r_multiple`, `tp3_r_multiple` zijn gedefinieerd in `StrategyParams` maar worden **NIET gebruikt** voor prijsberekening in de backtest. Ze zijn legacy/metadata. De daadwerkelijke prijzen komen uit `atr_tp_multiplier` parameters.

### 2.2 Huidige Parameter Waarden (val_2023_2025_003)

```json
{
  "tp1_r_multiple": 1.7,       // Niet gebruikt in backtest prijsberekening
  "tp2_r_multiple": 2.7,       // Niet gebruikt in backtest prijsberekening
  "tp3_r_multiple": 6.0,       // Niet gebruikt in backtest prijsberekening
  "tp1_close_pct": 0.34,       // 34% van positie sluit bij TP1
  "tp2_close_pct": 0.16,       // 16% van positie sluit bij TP2
  "tp3_close_pct": 0.35,       // 35% van positie sluit bij TP3
  "tp4_close_pct": 0.20,       // 20% sluit bij TP4 (legacy)
  "tp5_close_pct": 0.45,       // 45% sluit bij TP5 (final)
  "trail_activation_r": 0.65,  // Trailing activeerd na 0.65R winst
  "atr_trail_multiplier": 1.6  // Trailing afstand = 1.6 * ATR
}
```

### 2.3 Close Percentages (gewogen)

De `tp_close_pct` parameters bepalen welk percentage van de positie sluit bij elk TP niveau. De totale R/R wordt berekend als een **gewogen som**:

```python
# strategy_core.py line 2604-2609
TP1_CLOSE_PCT = params.tp1_close_pct  # 0.34
TP2_CLOSE_PCT = params.tp2_close_pct  # 0.16
TP3_CLOSE_PCT = params.tp3_close_pct  # 0.35
TP4_CLOSE_PCT = params.tp4_close_pct  # 0.20
TP5_CLOSE_PCT = params.tp5_close_pct  # 0.45
```

**⚠️ Let op**: De som van close_pct hoeft niet exact 1.0 te zijn. De percentages worden direct gebruikt als weights voor R/R berekening.

---

## 3. Exit Check Volgorde

De exit checks in `simulate_trades()` volgen een **strikte volgorde** per candle:

### 3.1 LONG Trades (direction == "bullish")

```
Per candle:
1. [EERST] SL/Trailing Check: Is LOW ≤ trailing_sl?
   → JA: Trade sluit, bereken RR op basis van welke TPs geraakt
   → NEE: Ga naar stap 2

2. TP1 Check: Is HIGH ≥ tp1 EN tp1 nog niet hit?
   → JA: Mark tp1_hit = True
   → Activeer trailing als tp1_rr ≥ trail_activation_r
   
3. TP2 Check: Is tp1_hit EN HIGH ≥ tp2 EN tp2 nog niet hit?
   → JA: Mark tp2_hit = True
   → Update trailing_sl naar tp1 + 0.5*risk
   
4. TP3 Check: Is tp2_hit EN HIGH ≥ tp3 EN tp3 nog niet hit?
   → JA: Mark tp3_hit = True
   → Update trailing_sl naar tp2 + 0.5*risk
   
5. TP4 Check: Is tp3_hit EN HIGH ≥ tp4 EN tp4 nog niet hit?
   → JA: Mark tp4_hit = True
   → Update trailing_sl naar tp3 + 0.5*risk

6. TP5 Check: Is tp4_hit EN HIGH ≥ tp5 EN tp5 nog niet hit?
   → JA: Trade VOLLEDIG GESLOTEN bij TP5
   → RR = gewogen som van alle TP levels
```

### 3.2 SHORT Trades (direction == "bearish")

Gespiegelde logica:
- SL check: `HIGH ≥ trailing_sl`
- TP checks: `LOW ≤ tpX`
- Trailing updates: `trailing_sl = tpX + 0.5*risk` (boven entry)

---

## 4. Trailing Stop Mechanisme

### 4.1 Activatie Voorwaarde

```python
# strategy_core.py line 2718-2722 (bullish)
if tp1_rr >= params.trail_activation_r:  # 0.65R
    ot["trailing_sl"] = entry_price       # Move to breakeven
    ot["trailing_activated"] = True
```

De trailing stop wordt **pas geactiveerd** als het eerste TP niveau een R-multiple heeft van minimaal `trail_activation_r` (default: 0.65).

### 4.2 Trailing SL Updates per TP Level

| Event | Bullish Trailing SL | Bearish Trailing SL |
|-------|---------------------|---------------------|
| TP1 hit (als `tp1_rr ≥ 0.65R`) | `entry_price` (breakeven) | `entry_price` (breakeven) |
| TP2 hit | `tp1 + 0.5*risk` | `tp1 - 0.5*risk` |
| TP3 hit | `tp2 + 0.5*risk` | `tp2 - 0.5*risk` |
| TP4 hit | `tp3 + 0.5*risk` | `tp3 - 0.5*risk` |

### 4.3 Code Referentie

```python
# strategy_core.py lines 2723-2742 (bullish example)
if not trade_closed and tp1_hit and tp2 is not None and high >= tp2 and not tp2_hit:
    ot["tp2_hit"] = True
    tp2_hit = True
    if tp2_rr >= params.trail_activation_r and tp1 is not None:
        ot["trailing_sl"] = tp1 + 0.5 * risk
        ot["trailing_activated"] = True
```

---

## 5. R/R Berekening

### 5.1 Trailing Stop Hit (na 1+ TP geraakt)

Wanneer de trailing stop wordt geraakt nadat minstens één TP niveau is geraakt, wordt de RR als volgt berekend:

```python
# strategy_core.py lines 2683-2710 (bullish)
trail_rr = (trailing_sl - entry_price) / risk

if tp4_hit:
    remaining_pct = TP5_CLOSE_PCT
    rr = TP1_CLOSE_PCT * tp1_rr + TP2_CLOSE_PCT * tp2_rr + 
         TP3_CLOSE_PCT * tp3_rr + TP4_CLOSE_PCT * tp4_rr + 
         remaining_pct * trail_rr
    exit_reason = "TP4+Trail"
    is_winner = True

elif tp3_hit:
    remaining_pct = TP4_CLOSE_PCT + TP5_CLOSE_PCT
    rr = TP1_CLOSE_PCT * tp1_rr + TP2_CLOSE_PCT * tp2_rr + 
         TP3_CLOSE_PCT * tp3_rr + remaining_pct * trail_rr
    exit_reason = "TP3+Trail"
    is_winner = True

elif tp2_hit:
    remaining_pct = TP3_CLOSE_PCT + TP4_CLOSE_PCT + TP5_CLOSE_PCT
    rr = TP1_CLOSE_PCT * tp1_rr + TP2_CLOSE_PCT * tp2_rr + 
         remaining_pct * trail_rr
    exit_reason = "TP2+Trail"
    is_winner = rr >= 0  # Kan negatief zijn als trail ver onder entry

elif tp1_hit:
    remaining_pct = TP2_CLOSE_PCT + TP3_CLOSE_PCT + TP4_CLOSE_PCT + TP5_CLOSE_PCT
    rr = TP1_CLOSE_PCT * tp1_rr + remaining_pct * trail_rr
    exit_reason = "TP1+Trail"
    is_winner = rr >= 0
```

### 5.2 Pure Stop Loss (geen TP geraakt)

```python
else:
    rr = -1.0
    exit_reason = "SL"
    is_winner = False
```

### 5.3 TP5 Volledig Geraakt

```python
# strategy_core.py line 2745
if not trade_closed and tp4_hit and tp5 is not None and high >= tp5:
    ot["tp5_hit"] = True
    rr = TP1_CLOSE_PCT * tp1_rr + TP2_CLOSE_PCT * tp2_rr + 
         TP3_CLOSE_PCT * tp3_rr + TP4_CLOSE_PCT * tp4_rr + 
         TP5_CLOSE_PCT * tp5_rr
    exit_reason = "TP5"
    is_winner = True
```

---

## 6. Win/Loss Bepaling

### 6.1 Altijd WIN
- `exit_reason = "TP5"` (alle TP niveaus geraakt)
- `exit_reason = "TP4+Trail"` (4 TPs geraakt, trailing hit)
- `exit_reason = "TP3+Trail"` (3 TPs geraakt, trailing hit)

### 6.2 WIN als RR ≥ 0
- `exit_reason = "TP2+Trail"`
- `exit_reason = "TP1+Trail"`

### 6.3 Altijd LOSS
- `exit_reason = "SL"` (geen TP geraakt, originele SL hit) → `rr = -1.0`

### 6.4 Transaction Cost Adjustment

```python
# strategy_core.py lines 2821-2825
cost_r = ot.get("transaction_cost_r", 0.0)
adjusted_rr = rr - cost_r
adjusted_reward = adjusted_rr * risk
adjusted_is_winner = is_winner and adjusted_rr >= 0
```

De final win/loss check gebruikt de **adjusted RR** na aftrek van transaction costs.

---

## 7. Voorbeeld Scenario's

### Scenario A: Full TP5 Exit (Best Case)
```
Entry: 1.1000
SL: 1.0950 (risk = 0.0050)
TP1: 1.1030 (0.6R), TP2: 1.1060 (1.2R), TP3: 1.1100 (2.0R)
TP4: 1.1125 (2.5R), TP5: 1.1175 (3.5R)

Price hits: TP1 → TP2 → TP3 → TP4 → TP5
Final RR = 0.34*0.6 + 0.16*1.2 + 0.35*2.0 + 0.20*2.5 + 0.45*3.5
         = 0.204 + 0.192 + 0.70 + 0.50 + 1.575
         = 3.171R
```

### Scenario B: TP2 + Trailing Hit
```
Entry: 1.1000
SL: 1.0950, TP1: 1.1030, TP2: 1.1060
Trail activates at TP1, moves to 1.1000 (breakeven)
After TP2, trail moves to: tp1 + 0.5*risk = 1.1030 + 0.0025 = 1.1055

Price hits TP1, TP2, then reverses and hits trailing at 1.1055
trail_rr = (1.1055 - 1.1000) / 0.0050 = 1.1R
remaining_pct = 0.35 + 0.20 + 0.45 = 1.0

RR = 0.34*0.6 + 0.16*1.2 + 1.0*1.1 = 0.204 + 0.192 + 1.1 = 1.496R
```

### Scenario C: Pure SL Hit
```
Entry: 1.1000
SL: 1.0950
Price drops directly to 1.0950 without hitting any TP

RR = -1.0R
exit_reason = "SL"
is_winner = False
```

---

## 8. Edge Cases

### 8.1 Same-Candle SL+TP
De code checkt **SL eerst**, dan TP niveaus. Als binnen dezelfde candle zowel SL als TP geraakt kunnen worden, wordt aangenomen dat SL eerst geraakt werd.

### 8.2 Gap Door TP Niveaus
Als een candle meerdere TP niveaus in één keer passeert (gap), worden alle geraakte TPs gemarkeerd als hit in dezelfde bar.

### 8.3 Trailing Nooit Geactiveerd
Als `tp1_rr < trail_activation_r`, blijft de trailing SL op de originele SL staan totdat een hoger TP niveau wel de drempel haalt.

---

## 9. Parameters Samenvatting voor H1 Backtester

```python
# Vereiste parameters voor H1 backtester implementatie
REQUIRED_EXIT_PARAMS = {
    # TP Niveaus (berekend bij entry)
    'atr_tp1_multiplier': 0.6,    # TP1 = entry ± risk * multiplier
    'atr_tp2_multiplier': 1.2,
    'atr_tp3_multiplier': 2.0,
    # TP4/TP5 zijn hardcoded: 2.5R en 3.5R
    
    # Close Percentages (weights voor RR)
    'tp1_close_pct': 0.34,
    'tp2_close_pct': 0.16,
    'tp3_close_pct': 0.35,
    'tp4_close_pct': 0.20,
    'tp5_close_pct': 0.45,
    
    # Trailing Stop
    'trail_activation_r': 0.65,   # Min R voor trailing activatie
    'atr_trail_multiplier': 1.6,  # Trail afstand (niet gebruikt in huidige code!)
}
```

---

## 10. Bekende Inconsistenties

### 10.1 `tp_r_multiple` vs `atr_tp_multiplier`
De StrategyParams bevat twee sets TP parameters:
- `tp1_r_multiple` (1.7, 2.7, 6.0) - **Niet gebruikt** in backtest
- `atr_tp1_multiplier` (0.6, 1.2, 2.0) - **Wel gebruikt** in backtest

De `tp_r_multiple` parameters worden alleen opgeslagen voor referentie/logging.

### 10.2 `atr_trail_multiplier` Niet Actief
De parameter `atr_trail_multiplier` (1.6) wordt **niet gebruikt** in de huidige trailing logica. De trailing SL wordt berekend als:
- Breakeven bij TP1: `trailing_sl = entry_price`
- Na TP2+: `trailing_sl = previous_tp + 0.5*risk`

### 10.3 Partial Exit Parameters Ongebruikt
`partial_exit_at_1r` en `partial_exit_pct` zijn gedefinieerd maar worden niet geïmplementeerd in de backtest - de TP close percentages bepalen de partial exits.

---

## 11. Code Locaties Quick Reference

| Concept | File | Lines | Function |
|---------|------|-------|----------|
| TP Prijs Berekening | strategy_core.py | 2322-2377 | `calculate_risk_reward()` |
| Close % Laden | strategy_core.py | 2604-2609 | `simulate_trades()` |
| SL Check (Long) | strategy_core.py | 2683-2714 | `simulate_trades()` |
| SL Check (Short) | strategy_core.py | 2750-2780 | `simulate_trades()` |
| TP1 Check (Long) | strategy_core.py | 2716-2722 | `simulate_trades()` |
| TP2-5 Checks | strategy_core.py | 2724-2746 | `simulate_trades()` |
| RR Berekening | strategy_core.py | 2683-2746 | `simulate_trades()` |
| Trade Object Maken | strategy_core.py | 2823-2847 | `simulate_trades()` |

---

*Document gegenereerd: 2026-01-04*
*Broncode versie: Post-validation run val_2023_2025_003*
