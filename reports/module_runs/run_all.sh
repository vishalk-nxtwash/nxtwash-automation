#!/usr/bin/env bash
# Run all admin portal modules sequentially, one per log file.
# Usage: bash run_all.sh  (from nxtwash-automation/)

set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
LOGDIR="$REPO/reports/module_runs"
PYTHON="$REPO/venv/bin/python"
SUMMARY="$LOGDIR/SUMMARY.txt"

MODULES=(
  login
  overview
  sites
  bank_drop
  card_declines
  cash_report
  coupon_packages
  custom_services
  customers
  discounts
  employees
  general_sales_report
  gift_cards
  kiosk_settings
  labor_shifts
  memberships
  performance_metrics
  pos_settings
  redemptions
  revenue_overview
  service_categories
  transactions
  tunnel_settings
  user_roles
  users
  wash_activity
  wash_books
  wash_extras
  wash_packages
)

mkdir -p "$LOGDIR"
echo "Module Regression Run — $(date)" > "$SUMMARY"
echo "============================================================" >> "$SUMMARY"
printf "%-25s %6s %6s %6s %6s %6s  %s\n" \
  "MODULE" "PASS" "FAIL" "SKIP" "XFAIL" "XPASS" "TIME" >> "$SUMMARY"
echo "------------------------------------------------------------" >> "$SUMMARY"

for MODULE in "${MODULES[@]}"; do
  LOGFILE="$LOGDIR/${MODULE}.log"
  # Skip if already completed (allows restart)
  if [ -f "$LOGFILE" ] && grep -q "passed\|failed\|error" "$LOGFILE" 2>/dev/null; then
    echo "[SKIP-CACHED] $MODULE (log exists)"
  else
    echo "[START] $MODULE — $(date +%H:%M:%S)"
    "$PYTHON" -m pytest "tests/admin_portal/${MODULE}/" \
      --headless -q --tb=line \
      --timeout=120 \
      --no-header \
      -p no:alluredir \
      2>&1 | tee "$LOGFILE" || true
    echo "[DONE]  $MODULE — $(date +%H:%M:%S)"
  fi

  # Parse last summary line
  LAST=$(grep -E "^=+.*(passed|failed|error).*=+$" "$LOGFILE" 2>/dev/null | tail -1 || echo "")
  PASS=$(echo "$LAST" | grep -oE "[0-9]+ passed"  | grep -oE "[0-9]+" || echo "0")
  FAIL=$(echo "$LAST" | grep -oE "[0-9]+ failed"  | grep -oE "[0-9]+" || echo "0")
  SKIP=$(echo "$LAST" | grep -oE "[0-9]+ skipped" | grep -oE "[0-9]+" || echo "0")
  XFAIL=$(echo "$LAST" | grep -oE "[0-9]+ xfailed" | grep -oE "[0-9]+" || echo "0")
  XPASS=$(echo "$LAST" | grep -oE "[0-9]+ xpassed" | grep -oE "[0-9]+" || echo "0")
  TIME=$(echo "$LAST" | grep -oE "[0-9]+\.[0-9]+s" | tail -1 || echo "?")
  STATUS="OK"
  [ "$FAIL" -gt 0 ] 2>/dev/null && STATUS="FAIL"
  printf "%-25s %6s %6s %6s %6s %6s  %s  [%s]\n" \
    "$MODULE" "$PASS" "$FAIL" "$SKIP" "$XFAIL" "$XPASS" "$TIME" "$STATUS" >> "$SUMMARY"
  echo "  → $LAST"
done

echo "------------------------------------------------------------" >> "$SUMMARY"
echo "Completed: $(date)" >> "$SUMMARY"
echo ""
echo "===== REGRESSION COMPLETE ====="
cat "$SUMMARY"
