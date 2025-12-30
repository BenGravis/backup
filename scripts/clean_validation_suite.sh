#!/bin/bash
# Clean validation runner voor 3 periodes

set -e  # Exit on error

BASE_DIR="/workspaces/BestOutcomeQuant"
PARAMS_FILE="$BASE_DIR/ftmo_analysis_output/TPE/history/run_006/best_params.json"
VALIDATE_DIR="$BASE_DIR/ftmo_analysis_output/VALIDATE"

echo "========================================="
echo "STARTING CLEAN VALIDATION SUITE"
echo "========================================="
echo ""

# Run 2014-2016
echo "📅 [1/3] VALIDATION 2014-2016"
echo "Cleaning root VALIDATE..."
rm -f "$VALIDATE_DIR"/*.txt "$VALIDATE_DIR"/*.csv "$VALIDATE_DIR"/*.json
cd "$BASE_DIR"
python ftmo_challenge_analyzer.py --validate --start 2014-01-01 --end 2016-12-31 --params-file "$PARAMS_FILE" > /tmp/val_2014.log 2>&1
echo "✓ Completed 2014-2016"
sleep 2

# Run 2017-2019
echo "📅 [2/3] VALIDATION 2017-2019"
echo "Cleaning root VALIDATE..."
rm -f "$VALIDATE_DIR"/*.txt "$VALIDATE_DIR"/*.csv "$VALIDATE_DIR"/*.json
cd "$BASE_DIR"
python ftmo_challenge_analyzer.py --validate --start 2017-01-01 --end 2019-12-31 --params-file "$PARAMS_FILE" > /tmp/val_2017.log 2>&1
echo "✓ Completed 2017-2019"
sleep 2

# Run 2020-2022
echo "📅 [3/3] VALIDATION 2020-2022"
echo "Cleaning root VALIDATE..."
rm -f "$VALIDATE_DIR"/*.txt "$VALIDATE_DIR"/*.csv "$VALIDATE_DIR"/*.json
cd "$BASE_DIR"
python ftmo_challenge_analyzer.py --validate --start 2020-01-01 --end 2022-12-31 --params-file "$PARAMS_FILE" > /tmp/val_2020.log 2>&1
echo "✓ Completed 2020-2022"

echo ""
echo "========================================="
echo "✅ ALL VALIDATIONS COMPLETE"
echo "========================================="
echo "Results in: $VALIDATE_DIR/history/"
echo ""
echo "Directory structure:"
ls -lh "$VALIDATE_DIR/history/" | grep val_
echo ""
echo "Analysis summary files per period:"
for dir in $(ls -d "$VALIDATE_DIR/history/val_"* 2>/dev/null | sort); do
  count=$(ls "$dir"/analysis_summary_*.txt 2>/dev/null | wc -l)
  echo "  $(basename $dir): $count file(s)"
done
