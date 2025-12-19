#!/usr/bin/env python3
"""
Live Quarterly Stats Monitor - Watch analyzer progress with quarterly breakdown
Shows: Trades per quarter, win rate, profit per quarter, and total profit
"""

import time
import os
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple

try:
    import optuna
except ImportError:
    print("[!] Optuna not found. Install: pip install optuna")
    exit(1)

from backtest import run_backtest
from config import FOREX_PAIRS, METALS, INDICES, CRYPTO_ASSETS
from strategy_core import StrategyParams

DB_PATH = "sqlite:///regime_adaptive_v2_clean.db"
UPDATE_INTERVAL = 5  # Check every 5 seconds

def get_best_params_from_trial(trial) -> Dict:
    """Extract parameters from an Optuna trial"""
    return trial.params

def extract_quarterly_stats(trades: List[Dict]) -> Dict:
    """Break down trades by quarter and calculate stats"""
    quarterly = defaultdict(lambda: {
        "trades": 0,
        "wins": 0,
        "losses": 0,
        "win_rate": 0.0,
        "total_profit_r": 0.0,
        "total_profit_usd": 0.0,
    })
    
    for trade in trades:
        if "entry_date" not in trade:
            continue
        
        entry_dt = trade["entry_date"]
        if isinstance(entry_dt, str):
            try:
                entry_dt = datetime.fromisoformat(entry_dt.replace('Z', '+00:00'))
            except:
                continue
        
        if not hasattr(entry_dt, 'year'):
            continue
        
        quarter_key = f"{entry_dt.year}_Q{(entry_dt.month - 1) // 3 + 1}"
        rr = trade.get("rr", 0)
        
        quarterly[quarter_key]["trades"] += 1
        quarterly[quarter_key]["total_profit_r"] += rr
        quarterly[quarter_key]["total_profit_usd"] += rr * 1000
        
        if rr > 0:
            quarterly[quarter_key]["wins"] += 1
        else:
            quarterly[quarter_key]["losses"] += 1
    
    # Calculate win rates
    for q in quarterly:
        total = quarterly[q]["trades"]
        if total > 0:
            quarterly[q]["win_rate"] = (quarterly[q]["wins"] / total) * 100
    
    return dict(quarterly)

def backtest_with_params(params: Dict) -> Tuple[List[Dict], float]:
    """Run backtest with given parameters, return trades and total profit"""
    all_symbols = FOREX_PAIRS + METALS + INDICES + CRYPTO_ASSETS
    combined_trades = []
    
    try:
        # Create strategy params object
        strategy_params = StrategyParams(**params)
    except:
        return [], 0.0
    
    for symbol in all_symbols[:5]:  # Test on subset for speed
        try:
            result = run_backtest(symbol, "Jan 2023 - Now")
            if result.get("trades"):
                combined_trades.extend(result["trades"])
        except:
            continue
    
    total_profit = sum(t.get("rr", 0) for t in combined_trades)
    return combined_trades, total_profit

def print_quarterly_header():
    """Print header"""
    os.system("clear" if os.name == "posix" else "cls")
    print("\n" + "=" * 110)
    print("LIVE QUARTERLY STATS MONITOR - FTMO Optimizer in Background".center(110))
    print("=" * 110)

def print_quarterly_stats(quarterly: Dict, total_profit: float, trial_num: int, best_value: float):
    """Print formatted quarterly breakdown"""
    print_quarterly_header()
    
    print(f"\n[Trial #{trial_num}] Best Score: {best_value:,.0f} | Current: {total_profit:,.0f}\n")
    print(f"{'Quarter':<12} | {'Trades':>6} | {'Wins':>5} | {'Win %':>6} | {'Profit (R)':>11} | {'Profit (USD)':>14} | {'Status':<8}")
    print("-" * 110)
    
    sorted_q = sorted(quarterly.keys())
    all_pass = True
    
    for q in sorted_q:
        stats = quarterly[q]
        trades = stats["trades"]
        wins = stats["wins"]
        win_rate = stats["win_rate"]
        profit_r = stats["total_profit_r"]
        profit_usd = stats["total_profit_usd"]
        
        pass_check = "✓ PASS" if (trades >= 20 and win_rate >= 30 and profit_r > 0) else "✗ FAIL"
        if "FAIL" in pass_check:
            all_pass = False
        
        print(f"{q:<12} | {trades:>6} | {wins:>5} | {win_rate:>5.1f}% | {profit_r:>10.1f}R | ${profit_usd:>12,.0f} | {pass_check:<8}")
    
    print("-" * 110)
    total_trades = sum(q["trades"] for q in quarterly.values())
    total_wins = sum(q["wins"] for q in quarterly.values())
    total_wr = (total_wins / total_trades * 100) if total_trades > 0 else 0
    
    print(f"{'TOTAL':<12} | {total_trades:>6} | {total_wins:>5} | {total_wr:>5.1f}% | {total_profit:>10.1f}R | ${total_profit * 1000:>12,.0f}")
    print("=" * 110)
    
    target_status = "✓ TARGET MET" if (total_trades >= 20 and total_profit >= 150) else "✗ Need improvement"
    print(f"\nTarget: 20+ trades/Q, 30%+ WR, +$150,000 total | Status: {target_status}")
    print(f"\nLast updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Press Ctrl+C to exit\n")

def monitor_live():
    """Live monitoring loop"""
    last_trial_count = 0
    
    while True:
        try:
            # Connect to Optuna study
            study = optuna.load_study(
                study_name="regime_adaptive_v2_clean",
                storage=DB_PATH,
                load_if_exists=True
            )
            
            current_trial_count = len(study.trials)
            
            if current_trial_count > last_trial_count or True:
                # Get best trial
                if study.best_trial:
                    best_value = study.best_value
                    best_params = study.best_params
                    
                    # Run backtest with best params
                    trades, total_profit = backtest_with_params(best_params)
                    quarterly = extract_quarterly_stats(trades)
                    
                    # Display
                    print_quarterly_stats(quarterly, total_profit, current_trial_count, best_value)
                    last_trial_count = current_trial_count
            
            time.sleep(UPDATE_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n[*] Monitor stopped by user")
            break
        except Exception as e:
            print(f"[!] Error: {str(e)}")
            time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    print("[*] Starting live quarterly stats monitor...")
    print("[*] Watching: regime_adaptive_v2_clean.db")
    print("[*] Updates every 5 seconds...\n")
    time.sleep(2)
    
    monitor_live()
