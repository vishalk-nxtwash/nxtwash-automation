#!/usr/bin/env bash
# Aggregate results from all 6 shards into a single SUMMARY.txt
set -euo pipefail
SHARDDIR="$(cd "$(dirname "$0")" && pwd)"
SUMMARY="$SHARDDIR/SUMMARY.txt"

ALL_MODULES=(
  bank_drop login service_categories gift_cards wash_extras wash_activity coupon_packages
  transactions tunnel_settings sites custom_services cash_report
  overview discounts redemptions revenue_overview
  customers memberships general_sales_report wash_books wash_packages
  employees labor_shifts users
  performance_metrics kiosk_settings pos_settings card_declines user_roles
)

echo "Module Regression Run (Sharded) — $(date)" > "$SUMMARY"
echo "============================================================" >> "$SUMMARY"
printf "%-25s %6s %6s %6s %6s %6s  %s\n" \
  "MODULE" "PASS" "FAIL" "SKIP" "XFAIL" "XPASS" "TIME" >> "$SUMMARY"
echo "------------------------------------------------------------" >> "$SUMMARY"

for MODULE in "${ALL_MODULES[@]}"; do
  # Find module log in any shard
  MODLOG=$(ls "$SHARDDIR"/shard*_${MODULE}.log 2>/dev/null | head -1 || echo "")
  if [ -z "$MODLOG" ] || [ ! -f "$MODLOG" ]; then
    printf "%-25s  %5s  %5s  %5s  %5s  %5s  %s  [%s]\n" \
      "$MODULE" "-" "-" "-" "-" "-" "?" "NOT RUN" >> "$SUMMARY"
    continue
  fi
  LAST=$(grep -E "^=+.*(passed|failed|error).*=+$" "$MODLOG" 2>/dev/null | tail -1 || echo "")
  PASS=$(echo "$LAST"  | grep -oE "[0-9]+ passed"   | grep -oE "[0-9]+" || echo "0")
  FAIL=$(echo "$LAST"  | grep -oE "[0-9]+ failed"   | grep -oE "[0-9]+" || echo "0")
  SKIP=$(echo "$LAST"  | grep -oE "[0-9]+ skipped"  | grep -oE "[0-9]+" || echo "0")
  XFAIL=$(echo "$LAST" | grep -oE "[0-9]+ xfailed"  | grep -oE "[0-9]+" || echo "0")
  XPASS=$(echo "$LAST" | grep -oE "[0-9]+ xpassed"  | grep -oE "[0-9]+" || echo "0")
  TIME=$(echo "$LAST"  | grep -oE "[0-9]+\.[0-9]+s" | tail -1 || echo "?")
  STATUS="OK"
  [ "${FAIL:-0}" -gt 0 ] 2>/dev/null && STATUS="FAIL"
  [ -z "$LAST" ] && STATUS="NO LOG"
  printf "%-25s %6s %6s %6s %6s %6s  %s  [%s]\n" \
    "$MODULE" "$PASS" "$FAIL" "$SKIP" "$XFAIL" "$XPASS" "$TIME" "$STATUS" >> "$SUMMARY"
done

echo "------------------------------------------------------------" >> "$SUMMARY"
echo "Summarized: $(date)" >> "$SUMMARY"
cat "$SUMMARY"
