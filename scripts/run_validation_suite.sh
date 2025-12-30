#!/bin/bash
# Run complete validation suite with proper cleanup between runs

set -e  # Exit on error

BASE_DIR="/workspaces/BestOutcomeQuant"
PARAMS_FILE="$BASE_DIR/ftmo_analysis_output/TPE/history/run_006/best_params.json"
VALIDATE_DIR="$BASE_DIR/ftmo_analysis_output/VALIDATE"

# Validation periods
declare -a PERIODS=(
    "2014-01-01 2016-12-31"
    "2017-01-01 2019-12-31"
    "2020-01-01 2022-12-31"
)

echo "========================================="
echo "VALIDATION SUITE RUNNER"
echo "========================================="
echo "Params: $PARAMS_FILE"
echo "Periods: ${#PERIODS[@]}"
echo ""

for period in "${PERIODS[@]}"; do
    read -r start end <<< "$period"
    echo "========================================="
    echo "Running validation: $start to $end"
    echo "========================================="
    
    # Clean root VALIDATE directory before each run
    echo "🧹 Cleaning root VALIDATE directory..."
    rm -f "$VALIDATE_DIR"/*.txt "$VALIDATE_DIR"/*.csv "$VALIDATE_DIR"/*.json
    
    # Run validation
    cd "$BASE_DIR"
    python ftmo_challenge_analyzer.py \
        --validate \
        --start "$start" \
        --end "$end" \
        --params-file "$PARAMS_FILE"
    
    echo "✅ Completed: $start to $end"
    echo ""
done

echo "========================================="
echo "✅ ALL VALIDATIONS COMPLETE"
echo "========================================="
echo "Results in: $VALIDATE_DIR/history/"
ls -lh "$VALIDATE_DIR/history/"
