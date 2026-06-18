#!/usr/bin/env bash
# Run only the 6 SC inactive-category tests that were previously broken.
# Usage: bash scripts/run_sc_inactive_tests.sh
# Optional: bash scripts/run_sc_inactive_tests.sh --headed  (skip headless for debugging)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
RESULTS_DIR="reports/allure-results-sc-inactive"
REPORT_DIR="reports/allure-report-sc-inactive"
PYTEST="$PROJECT_DIR/venv/bin/pytest"

HEADLESS="--headless"
if [[ "$1" == "--headed" ]]; then
  HEADLESS=""
  echo "Running in headed mode (browser visible)"
fi

TESTS=(
  "tests/admin_portal/service_categories/test_service_categories_positive.py::test_activate_service_category"
  "tests/admin_portal/service_categories/test_service_categories_positive.py::test_deactivate_service_category"
  "tests/admin_portal/service_categories/test_service_categories_edge_cases.py::test_activate_deactivate_activate_cycle"
  "tests/admin_portal/service_categories/test_service_categories_edge_cases.py::test_edit_inactive_category_saves_changes"
  "tests/admin_portal/service_categories/test_service_categories_edge_cases.py::test_deactivated_category_findable_via_filter"
  "tests/admin_portal/service_categories/test_service_categories_managed.py::test_managed_category_rename_is_reset_on_teardown"
)

echo "========================================"
echo " SC Inactive Category Tests"
echo " TCs: SC-HP-004, SC-HP-005, SC-EC-003,"
echo "      SC-EC-005, SC-EC-006, SC-MANAGED-002"
echo "========================================"
echo ""

cd "$PROJECT_DIR"

"$PYTEST" \
  "${TESTS[@]}" \
  $HEADLESS \
  --alluredir="$RESULTS_DIR" \
  --clean-alluredir \
  -v

echo ""
echo "Generating Allure report..."
allure generate "$RESULTS_DIR" --output "$REPORT_DIR" --clean

echo ""
echo "Opening report..."
allure open "$REPORT_DIR"
