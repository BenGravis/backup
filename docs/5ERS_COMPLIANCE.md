# 5ers Compliance Guide (Production)

**Last Updated**: January 5, 2026
**Account**: 5ers 60K High Stakes Challenge
**Strategy Risk**: 0.6% per trade = $360/R

---

## 5ers Challenge Rules

### Total Drawdown (TDD) - STATIC
- **Stop-out level**: 10% below STARTING balance ($54,000 for 60K account)
- **NOT trailing**: If you grow to $80K and drop to $55K, you're still SAFE (above $54K)
- Maximum loss = $6,000 from starting balance

> ⚠️ **Key Difference from FTMO**: 5ers TDD is STATIC, not trailing!

### Daily Drawdown (DDD)
**5ers DOES track daily drawdown!** (Contrary to earlier documentation)
- **Limit**: 5% from day start balance ($3,000 max daily loss)
- **Reset**: Daily at 00:00 broker time

### Profit Targets
| Step | Target | Amount |
|------|--------|--------|
| Step 1 | 8% | $4,800 |
| Step 2 | 5% | $3,000 |

### Other Rules
- Min profitable days: **3**
- No weekend holding restrictions (unlike FTMO)

---

## Bot Compliance Implementation

### DDD Safety System (3-Tier)
The live bot implements graduated daily drawdown protection:

| Tier | Daily DD | Action | Configuration |
|------|----------|--------|---------------|
| Warning | ≥2.0% | Log warning | `daily_loss_warning_pct = 0.020` |
| Reduce | ≥3.0% | Reduce risk 0.6%→0.4% | `daily_loss_reduce_pct = 0.030` |
| Halt | ≥3.5% | Stop new trades | `daily_loss_halt_pct = 0.035` |

**Margin to 5ers limit**: 5.0% - 3.5% = **1.5% safety buffer**

### TDD Implementation
```python
# Stop-out level = starting_balance * 0.90 (STATIC)
stop_out_level = 60000 * 0.90  # = $54,000

# Trade is stopped if:
is_stopped_out = current_balance < stop_out_level
```

### FIVEERS_CONFIG (ftmo_config.py)
```python
class FIVEERS_CONFIG:
    starting_balance = 60000
    profit_target_step1_pct = 0.08    # 8% = $4,800
    profit_target_step2_pct = 0.05    # 5% = $3,000
    max_total_dd_pct = 0.10           # 10% = $6,000
    max_daily_dd_pct = 0.05           # 5% = $3,000
    daily_loss_warning_pct = 0.020    # 2.0%
    daily_loss_reduce_pct = 0.030     # 3.0%
    daily_loss_halt_pct = 0.035       # 3.5%
    min_profitable_days = 3
```

---

## Validated Compliance (January 5, 2026)

### Simulation Results (2023-2025)
```
Starting Balance:     $60,000
Final Balance:        $3,203,619 (+5,239%)
Max Total DD:         7.75% (limit 10%) ✅
Max Daily DD:         3.80% (limit 5%) ✅
DDD Margin:           1.20% with 3.5% halt
Trades Blocked by DD: 21
Total Trades:         1,777
Win Rate:             72.3%
```

### Equivalence Test
```
TPE Validate Trades: 1,779
Live Bot Matched:    1,737 (97.6%)
Status: Systems are EQUIVALENT ✅
```

---

## Challenge Pass Strategy

### Step 1 (8% = $4,800)
- Target: ~$4,800 profit
- At 0.6% risk ($360/trade) × 72.3% WR
- Expected duration: 1-2 weeks

### Step 2 (5% = $3,000)
- Target: ~$3,000 profit
- Same parameters as Step 1
- Expected duration: 1 week

### Risk Settings
- Max position risk: 0.6% = $360 per trade
- 5-TP partial exit system
- Trailing stop after TP1
- DDD safety system active

---

## AccountSnapshot Fields

The `ChallengeRiskManager` provides real-time risk monitoring:

```python
@dataclass
class AccountSnapshot:
    balance: float
    equity: float
    floating_pnl: float
    margin_used: float
    free_margin: float
    total_dd_pct: float       # Current TDD percentage
    daily_dd_pct: float       # Current DDD percentage
    is_stopped_out: bool      # True if balance < $54K
    timestamp: datetime
    total_risk_usd: float     # Total open position risk in USD
    total_risk_pct: float     # Total open position risk as %
    open_positions: int       # Number of open positions
```

---

## Operational Checklist

- [x] TDD set to static $54,000 stop-out
- [x] DDD safety system enabled (3.5%/3.0%/2.0%)
- [x] AccountSnapshot includes risk tracking
- [x] Dynamic lot sizing based on current balance
- [x] Equivalence test passed (97.6%)
- [x] 5ers compliance simulation passed
- [ ] Load params via `params_loader.py` (no hardcoding)
- [ ] Verify `.env` for MT5 credentials
- [ ] Run `main_live_bot.py` on Windows VM with MT5

---

## Important Notes

### DDD Correction
Earlier documentation incorrectly stated "5ers has NO daily drawdown limit". This is **FALSE**.

**5ers DOES track daily drawdown with a 5% limit.**

The bot now implements a 3-tier DDD safety system with a halt at 3.5% to provide a 1.5% safety buffer.

### TDD vs FTMO
| | FTMO | 5ers |
|--|------|------|
| TDD Type | Trailing from peak | Static from start |
| TDD Limit | 10% | 10% |
| DDD Limit | 5% | 5% |

---

## References

- Session Archive: `analysis/SESSION_JAN05_2026_RESULTS.md`
- Config File: `ftmo_config.py`
- Risk Manager: `challenge_risk_manager.py`
- Live Bot: `main_live_bot.py`
- Equivalence Test: `scripts/test_equivalence_v2.py`

---

**Last Validated**: January 5, 2026
**Validated By**: Equivalence Test (97.6%), 5ers Compliance Simulation
