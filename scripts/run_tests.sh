#!/usr/bin/env bash
# run_tests.sh — run pytest and open the Allure HTML report.
#
# Usage:
#   bash scripts/run_tests.sh                          # all tests
#   bash scripts/run_tests.sh tests/admin_portal/overview
#   bash scripts/run_tests.sh tests/admin_portal/pos_settings -m smoke
#   bash scripts/run_tests.sh --headed                 # skip headless
#
# All output is written under reports/:
#   reports/allure-results/   raw JSON for Allure
#   reports/allure-report/    browsable HTML report
#   reports/screenshots/      failure screenshots
#   reports/logs/             test-run log

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PYTEST=("$PROJECT_DIR/venv/bin/python" -m pytest)

RESULTS_DIR="$PROJECT_DIR/reports/allure-results"
REPORT_DIR="$PROJECT_DIR/reports/allure-report"

# ── Argument parsing ──────────────────────────────────────────────────────────
HEADLESS="--headless"
EXTRA_ARGS=()

for arg in "$@"; do
  case "$arg" in
    --headed) HEADLESS="" ;;
    *)        EXTRA_ARGS+=("$arg") ;;
  esac
done

# ── Prepare output directories ────────────────────────────────────────────────
mkdir -p "$RESULTS_DIR" "$REPORT_DIR" \
         "$PROJECT_DIR/reports/screenshots" \
         "$PROJECT_DIR/reports/logs"

# ── Run tests ─────────────────────────────────────────────────────────────────
cd "$PROJECT_DIR"

echo "========================================"
echo " NxtWash Automation Test Run"
echo " Results : reports/allure-results/"
echo " Report  : reports/allure-report/"
echo "========================================"
echo ""

"${PYTEST[@]}" \
  $HEADLESS \
  --clean-alluredir \
  --alluredir="$RESULTS_DIR" \
  "${EXTRA_ARGS[@]:-tests}"

# ── Generate Allure HTML report ───────────────────────────────────────────────
echo ""
echo "Generating Allure report..."

if command -v allure &>/dev/null; then
  allure generate "$RESULTS_DIR" --clean --output "$REPORT_DIR"
  echo ""
  echo "Report ready. Opening..."
  allure open "$REPORT_DIR"
else
  echo "⚠  'allure' command not found — install it to view the HTML report."
  echo "   brew install allure   (macOS)"
  echo "   Raw JSON results are in: $RESULTS_DIR"
fi
