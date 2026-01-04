#!/usr/bin/env python3
"""
Parameter Verification Script - STAP 4.

This script verifies that parameter saving and loading works correctly.
Run this after any changes to:
- params/defaults.py
- params/params_loader.py  
- strategy_core.py (StrategyParams)
- ftmo_challenge_analyzer.py (parameter saving)

Exit codes:
  0 - All checks passed
  1 - Some checks failed
"""

import json
import sys
import dataclasses
from pathlib import Path
from typing import Dict, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def verify_defaults_module():
    """Verify defaults module exists and is correct."""
    print("1️⃣ Checking params/defaults.py...")
    
    try:
        from params.defaults import PARAMETER_DEFAULTS, get_boolean_params, validate_params
        print(f"   ✅ Module imported successfully")
        print(f"   ✅ {len(PARAMETER_DEFAULTS)} parameters defined")
        
        bools = get_boolean_params()
        print(f"   ✅ {len(bools)} boolean parameters")
        
        return True, PARAMETER_DEFAULTS
        
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        return False, None


def verify_strategy_params_dataclass():
    """Verify StrategyParams dataclass has all required fields."""
    print("\n2️⃣ Checking strategy_core.py StrategyParams...")
    
    try:
        from strategy_core import StrategyParams
        from params.defaults import PARAMETER_DEFAULTS
        
        # Get all dataclass fields
        dc_fields = {f.name for f in dataclasses.fields(StrategyParams)}
        print(f"   ✅ StrategyParams has {len(dc_fields)} fields")
        
        # Check for critical fields
        critical_fields = [
            'tp1_r_multiple', 'tp2_r_multiple', 'tp3_r_multiple',
            'daily_loss_halt_pct', 'max_total_dd_warning', 'consecutive_loss_halt',
            'risk_per_trade_pct', 'min_confluence',
        ]
        
        missing_critical = [f for f in critical_fields if f not in dc_fields]
        if missing_critical:
            print(f"   ❌ Missing critical fields: {missing_critical}")
            return False
        
        print(f"   ✅ All critical fields present")
        
        # Test instantiation with defaults
        params = StrategyParams()
        print(f"   ✅ StrategyParams() instantiates correctly")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def verify_current_params_json():
    """Verify current_params.json is complete."""
    print("\n3️⃣ Checking params/current_params.json...")
    
    params_file = PROJECT_ROOT / 'params' / 'current_params.json'
    
    if not params_file.exists():
        print(f"   ❌ File not found!")
        return False, None
    
    try:
        with open(params_file) as f:
            data = json.load(f)
        
        # Handle nested 'parameters' key
        if 'parameters' in data:
            params = data['parameters']
        else:
            params = data
        
        print(f"   ✅ File loaded: {len(params)} parameters")
        
        return True, params
        
    except Exception as e:
        print(f"   ❌ Error loading file: {e}")
        return False, None


def verify_params_loader():
    """Verify params_loader.py works correctly."""
    print("\n4️⃣ Checking params/params_loader.py...")
    
    try:
        from params.params_loader import load_strategy_params, load_params_dict
        
        # Test loading raw dict
        params_dict = load_params_dict()
        print(f"   ✅ load_params_dict() works")
        
        # Test loading StrategyParams
        strategy_params = load_strategy_params()
        print(f"   ✅ load_strategy_params() works")
        
        # Verify critical values
        print(f"\n   Critical parameter values:")
        print(f"     risk_per_trade_pct: {strategy_params.risk_per_trade_pct}")
        print(f"     tp1_r_multiple: {strategy_params.tp1_r_multiple}")
        print(f"     tp2_r_multiple: {strategy_params.tp2_r_multiple}")
        print(f"     tp3_r_multiple: {strategy_params.tp3_r_multiple}")
        print(f"     min_confluence: {strategy_params.min_confluence}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_main_live_bot_loading():
    """Verify main_live_bot.py can load parameters correctly."""
    print("\n5️⃣ Checking main_live_bot.py parameter loading...")
    
    try:
        # Import the loading function
        sys.path.insert(0, str(PROJECT_ROOT))
        
        # Try to import the load function
        from main_live_bot import load_best_params_from_file
        
        params = load_best_params_from_file()
        print(f"   ✅ load_best_params_from_file() works")
        print(f"   ✅ Loaded {len(params)} parameters")
        
        # Check critical params
        if 'risk_per_trade_pct' in params:
            print(f"     risk_per_trade_pct: {params['risk_per_trade_pct']}")
        if 'tp1_r_multiple' in params:
            print(f"     tp1_r_multiple: {params['tp1_r_multiple']}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_boolean_values():
    """Specifically check boolean parameters are correctly saved/loaded."""
    print("\n6️⃣ Verifying boolean parameters...")
    
    try:
        from params.defaults import PARAMETER_DEFAULTS, get_boolean_params
        from params.params_loader import load_strategy_params
        
        bool_defaults = get_boolean_params()
        strategy_params = load_strategy_params()
        
        issues = []
        
        for param_name, default_value in bool_defaults.items():
            # Get value from loaded StrategyParams
            if hasattr(strategy_params, param_name):
                loaded_value = getattr(strategy_params, param_name)
                
                if not isinstance(loaded_value, bool):
                    issues.append(f"{param_name}: wrong type (got {type(loaded_value).__name__})")
                else:
                    status = "ON" if loaded_value else "OFF"
                    match = "✅" if loaded_value == default_value else "🔄"
                    print(f"   {match} {param_name}: {status}")
        
        if issues:
            print(f"\n   ⚠️ Issues found:")
            for issue in issues:
                print(f"      - {issue}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def compare_defaults_with_json():
    """Compare defaults.py with current_params.json."""
    print("\n7️⃣ Comparing defaults with JSON file...")
    
    try:
        from params.defaults import PARAMETER_DEFAULTS
        
        params_file = PROJECT_ROOT / 'params' / 'current_params.json'
        with open(params_file) as f:
            data = json.load(f)
        
        if 'parameters' in data:
            json_params = data['parameters']
        else:
            json_params = data
        
        default_keys = set(PARAMETER_DEFAULTS.keys())
        json_keys = set(json_params.keys())
        
        # Params in defaults but not in JSON (will use defaults)
        missing_from_json = default_keys - json_keys
        if missing_from_json:
            print(f"   ⚠️ {len(missing_from_json)} params missing from JSON (will use defaults)")
            # Only show first few
            for key in sorted(list(missing_from_json))[:5]:
                print(f"      - {key}: {PARAMETER_DEFAULTS[key]}")
            if len(missing_from_json) > 5:
                print(f"      ... and {len(missing_from_json) - 5} more")
        else:
            print(f"   ✅ All default params present in JSON")
        
        # Extra params in JSON (will be ignored or may cause issues)
        extra_in_json = json_keys - default_keys
        # Filter out metadata
        metadata = {'optimization_mode', 'timestamp', 'best_score', 'generated_at', 'generated_by', 'version'}
        extra_in_json = extra_in_json - metadata
        
        if extra_in_json:
            print(f"   ⚠️ {len(extra_in_json)} extra params in JSON (not in defaults)")
            for key in sorted(extra_in_json):
                print(f"      - {key}: {json_params[key]}")
        else:
            print(f"   ✅ No unexpected params in JSON")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    print("=" * 70)
    print("PARAMETER VERIFICATION - STAP 4")
    print("=" * 70)
    
    all_ok = True
    
    # Step 1: Check defaults module
    ok, defaults = verify_defaults_module()
    all_ok = all_ok and ok
    
    if not defaults:
        print("\n❌ Cannot continue without defaults module")
        sys.exit(1)
    
    # Step 2: Check StrategyParams dataclass
    ok = verify_strategy_params_dataclass()
    all_ok = all_ok and ok
    
    # Step 3: Check current params JSON
    ok, json_params = verify_current_params_json()
    all_ok = all_ok and ok
    
    # Step 4: Check params_loader
    ok = verify_params_loader()
    all_ok = all_ok and ok
    
    # Step 5: Check main_live_bot loading
    ok = verify_main_live_bot_loading()
    all_ok = all_ok and ok
    
    # Step 6: Check boolean values
    ok = verify_boolean_values()
    all_ok = all_ok and ok
    
    # Step 7: Compare defaults with JSON
    ok = compare_defaults_with_json()
    all_ok = all_ok and ok
    
    # Final verdict
    print("\n" + "=" * 70)
    if all_ok:
        print("✅ ALL CHECKS PASSED - Parameter system is correctly configured!")
    else:
        print("⚠️ SOME CHECKS FAILED - Review issues above")
    print("=" * 70)
    
    sys.exit(0 if all_ok else 1)


if __name__ == '__main__':
    main()
