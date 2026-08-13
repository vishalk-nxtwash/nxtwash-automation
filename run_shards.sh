#!/usr/bin/env bash
# run_shards.sh — Parallel sharded test runner for NxtWash Admin Portal
#
# Splits 29 modules across 4 balanced shards and runs them in parallel.
# Each shard gets its own log, JUnit XML, and Allure results directory.
# A consolidated summary report is generated after all shards finish.
#
# Usage:
#   ./run_shards.sh                  # run all 4 shards
#   ./run_shards.sh --dry-run        # print shard assignments, do not run
#   ./run_shards.sh --headed         # run with visible browser windows

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTEST="$SCRIPT_DIR/venv/bin/pytest"
PYTHON="$SCRIPT_DIR/venv/bin/python"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RUN_DIR="$SCRIPT_DIR/reports/runs/$TIMESTAMP"

HEADLESS_FLAG="--headless"
DRY_RUN=0

for arg in "$@"; do
    case $arg in
        --dry-run)  DRY_RUN=1 ;;
        --headed)   HEADLESS_FLAG="" ;;
    esac
done

# ── Shard definitions (balanced ~520 tests each) ───────────────────────────
# Round-robin assigned by descending test count so shards finish at similar times.

SHARD_1_MODULES=(
    tests/admin_portal/transactions        # 121
    tests/admin_portal/customers           #  93
    tests/admin_portal/wash_activity       #  83
    tests/admin_portal/wash_extras         #  79
    tests/admin_portal/user_roles          #  70
    tests/admin_portal/sites               #  66
    tests/admin_portal/login               #  44
    tests/admin_portal/bank_drop           #  27
)   # total ≈ 583

SHARD_2_MODULES=(
    tests/admin_portal/redemptions         # 101
    tests/admin_portal/kiosk_settings      #  91
    tests/admin_portal/general_sales_report  #  83
    tests/admin_portal/wash_packages       #  78
    tests/admin_portal/pos_settings        #  68
    tests/admin_portal/custom_services  #  58
    tests/admin_portal/tunnel_settings  #  44
)   # total ≈ 523

SHARD_3_MODULES=(
    tests/admin_portal/revenue_overview    # 100
    tests/admin_portal/labor_shifts        #  86
    tests/admin_portal/card_declines       #  84
    tests/admin_portal/overview            #  76
    tests/admin_portal/memberships         #  66
    tests/admin_portal/cash_report         #  56
    tests/admin_portal/service_categories  #  36
)   # total ≈ 504

SHARD_4_MODULES=(
    tests/admin_portal/employees           #  98
    tests/admin_portal/performance_metrics #  86
    tests/admin_portal/wash_books          #  82
    tests/admin_portal/discounts           #  73
    tests/admin_portal/users               #  66
    tests/admin_portal/coupon_packages     #  45
    tests/admin_portal/gift_cards          #  37
)   # total ≈ 487

# ── Dry-run output ─────────────────────────────────────────────────────────
if [ "$DRY_RUN" -eq 1 ]; then
    echo "DRY RUN — shard assignments:"
    echo ""
    for s in 1 2 3 4; do
        eval "modules=(\"\${SHARD_${s}_MODULES[@]}\")"
        echo "Shard $s:"
        for m in "${modules[@]}"; do echo "  $m"; done
        echo ""
    done
    exit 0
fi

# ── Setup ──────────────────────────────────────────────────────────────────
mkdir -p "$RUN_DIR"

echo "════════════════════════════════════════════════════════════════════"
echo "  NxtWash Admin Portal — Parallel Sharded Run"
echo "  Started : $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Run dir : $RUN_DIR"
echo "  Mode    : $([ -n "$HEADLESS_FLAG" ] && echo headless || echo headed)"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# ── Shard runner (called in subshell via &) ────────────────────────────────
run_shard() {
    local num=$1
    shift
    local log="$RUN_DIR/shard-${num}.log"
    local allure_dir="$RUN_DIR/shard-${num}-allure"
    local junit="$RUN_DIR/shard-${num}-junit.xml"

    mkdir -p "$allure_dir"

    {
        echo "════════════════════════════════════════════════════"
        echo "  Shard $num started at $(date '+%H:%M:%S')"
        echo "  Modules:"
        for m in "$@"; do echo "    $m"; done
        echo "════════════════════════════════════════════════════"
        echo ""
    } > "$log"

    # shellcheck disable=SC2086
    "$PYTEST" "$@" \
        $HEADLESS_FLAG \
        -n 2 \
        --override-ini="addopts=-v --strict-markers --timeout=420 --timeout-method=signal" \
        --alluredir="$allure_dir" \
        --junit-xml="$junit" \
        --tb=short \
        >> "$log" 2>&1

    local ec=$?
    {
        echo ""
        echo "════════════════════════════════════════════════════"
        echo "  Shard $num finished at $(date '+%H:%M:%S') — exit code: $ec"
        echo "════════════════════════════════════════════════════"
    } >> "$log"
    exit $ec
}

# ── Launch all shards ──────────────────────────────────────────────────────
cd "$SCRIPT_DIR"

run_shard 1 "${SHARD_1_MODULES[@]}" &
PID_1=$!

run_shard 2 "${SHARD_2_MODULES[@]}" &
PID_2=$!

run_shard 3 "${SHARD_3_MODULES[@]}" &
PID_3=$!

run_shard 4 "${SHARD_4_MODULES[@]}" &
PID_4=$!

echo "All 4 shards running. PIDs: $PID_1  $PID_2  $PID_3  $PID_4"
echo ""
echo "Monitor live progress (open 4 terminals):"
echo "  tail -f $RUN_DIR/shard-1.log"
echo "  tail -f $RUN_DIR/shard-2.log"
echo "  tail -f $RUN_DIR/shard-3.log"
echo "  tail -f $RUN_DIR/shard-4.log"
echo ""

# ── Wait for all shards ────────────────────────────────────────────────────
wait $PID_1; EC1=$?
wait $PID_2; EC2=$?
wait $PID_3; EC3=$?
wait $PID_4; EC4=$?

echo ""
echo "All shards finished:"
for s in 1 2 3 4; do
    eval "ec=\$EC${s}"
    label=$([ "$ec" -eq 0 ] && echo "PASS" || echo "FAIL (exit $ec)")
    echo "  Shard $s → $label"
done
echo ""

# ── Generate consolidated report ───────────────────────────────────────────
echo "Generating report..."
"$PYTHON" "$SCRIPT_DIR/generate_report.py" "$RUN_DIR" "$EC1" "$EC2" "$EC3" "$EC4"

SUMMARY="$RUN_DIR/summary.txt"
if [ -f "$SUMMARY" ]; then
    echo ""
    cat "$SUMMARY"
    echo ""
    echo "Report saved: $SUMMARY"
fi

# ── Merge Allure results (optional, requires allure CLI) ───────────────────
if command -v allure &>/dev/null; then
    MERGED="$RUN_DIR/allure-merged"
    mkdir -p "$MERGED"
    cp "$RUN_DIR"/shard-*-allure/* "$MERGED/" 2>/dev/null || true
    echo "Allure results merged → $MERGED"
    echo "Run:  allure serve $MERGED"
fi

# ── Exit with failure if any shard failed ─────────────────────────────────
[ "$EC1" -eq 0 ] && [ "$EC2" -eq 0 ] && [ "$EC3" -eq 0 ] && [ "$EC4" -eq 0 ]
