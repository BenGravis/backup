# 5ers Compliance Guide (Production)

**Date**: 2025-01-02  
**Account**: 5ers 60K High Stakes Challenge  
**Strategy Risk**: 0.6% per trade = $360/R

## 5ers Challenge Rules (CRITICAL DIFFERENCES FROM FTMO)

### Daily Drawdown
**5ers has NO daily drawdown limit!** Unlike FTMO's 5% daily max, 5ers only tracks total drawdown.

### Total Drawdown (Stop-Out)
- **Stop-out level**: 10% below STARTING balance (constant $54,000 for 60K account)
- **NOT trailing**: If you grow to $80K and drop to $55K, you're still safe (above $54K)
- Maximum loss = $6,000 from starting balance

### Profit Targets
- Step 1 target: **+8%** ($4,800)
- Step 2 target: **+5%** ($3,000)

### Other Rules
- Min profitable days: **3**
- No weekend holding restrictions (unlike FTMO)

## Bot Compliance Implementation

### FTMOComplianceTracker (now 5ers-compatible)
```python
# Stop-out level = starting_balance * 0.90
stop_out_level = 60000 * 0.90  # = $54,000

# Trade is stopped if:
is_stopped_out = current_balance < stop_out_level
```

### Key Parameters
- `max_total_dd_warning`: 8.0% (informational warning, not a hard stop)
- `consecutive_loss_halt`: 999 (disabled - no streak-based halt)
- `use_graduated_risk`: False (disabled - 5ers has no daily DD to tier against)

### Removed Parameters
- `daily_loss_halt_pct`: REMOVED - 5ers doesn't have daily DD limit
- Daily DD tracking: REMOVED from compliance reports

## Challenge Pass Strategy
- Use finalized params (`best_params.json` / `params/current_params.json`)
- Step 1 (8%): Target ~22R at 0.6% risk = ~$4,800
- Step 2 (5%): Target ~14R at 0.6% risk = ~$3,000
- Focus on total equity curve, not daily performance

## Risk Management
- Max position risk: 0.6% = $360 per trade
- Partial exit at 1R to lock in 50% profit
- TP structure: 0.8R / 1.5R / 3.0R (current optimized values)

## Operational Checklist
- [x] Daily DD tracking removed from optimizer
- [x] stop_out_level set to constant $54,000
- [x] All backtest calls updated to remove daily_loss_halt_pct
- [x] Graduated risk disabled (use_graduated_risk=False)
- [ ] Load params via `params_loader.py` (no hardcoding)
- [ ] Verify `.env` for MT5 credentials
- [ ] Run `main_live_bot.py` on Windows VM with MT5

## References
- Optimization database: `regime_adaptive_v2_clean_warm.db`
- Training period: 2023-01-01 to 2024-09-30 (21 months)
- Validation period: 2024-10-01 to 2025-12-26 (15 months)
- Best params: `ftmo_analysis_output/TPE/best_params.json`
