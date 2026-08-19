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
    echo "DRY RUN — shard assignments (sequential, one at a time):"
    echo ""
    for s in 1 2 3 4; do
        eval "modules=(\"\${SHARD_${s}_MODULES[@]}\")"
        workers=$([ "$s" -eq 2 ] || [ "$s" -eq 4 ] && echo 2 || echo 3)
        echo "Shard $s  (-n $workers --dist loadscope):"
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

# ── Shard runner ───────────────────────────────────────────────────────────
# $1 = shard number, $2 = xdist worker count, $3..N = module paths
# Runs in the foreground (no &). Shards are sequential so only one shard's
# Chrome instances are alive at a time — safe on 8 GB RAM.
# --dist loadscope keeps all tests from the same Python module on the same
# worker, preventing managed-fixture write contention between workers.
run_shard() {
    local num=$1
    local workers=$2
    shift 2
    local log="$RUN_DIR/shard-${num}.log"
    local allure_dir="$RUN_DIR/shard-${num}-allure"
    local junit="$RUN_DIR/shard-${num}-junit.xml"

    mkdir -p "$allure_dir"

    {
        echo "════════════════════════════════════════════════════"
        echo "  Shard $num started at $(date '+%H:%M:%S') (workers: $workers)"
        echo "  Modules:"
        for m in "$@"; do echo "    $m"; done
        echo "════════════════════════════════════════════════════"
        echo ""
    } > "$log"

    # shellcheck disable=SC2086
    "$PYTEST" "$@" \
        $HEADLESS_FLAG \
        -n "$workers" \
        --dist loadscope \
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
    return $ec
}

# ── Launch shards sequentially ─────────────────────────────────────────────
# One shard at a time → max 3 Chrome instances on 8 GB RAM, no swapping.
# Each shard completes in ~1–1.5 h so the staging auth token never expires.
# Shards 2 & 4 use -n 2 (matching CI parallel:2) because they contain
# write-heavy modules: wash_packages, wash_books, coupon_packages, employees.
cd "$SCRIPT_DIR"

echo "Shard 1 / 4 starting...  tail -f $RUN_DIR/shard-1.log"
run_shard 1 3 "${SHARD_1_MODULES[@]}"; EC1=$?
echo "Shard 1 → $([ "$EC1" -eq 0 ] && echo PASS || echo "FAIL (exit $EC1)")"
echo ""

echo "Shard 2 / 4 starting...  tail -f $RUN_DIR/shard-2.log"
run_shard 2 2 "${SHARD_2_MODULES[@]}"; EC2=$?
echo "Shard 2 → $([ "$EC2" -eq 0 ] && echo PASS || echo "FAIL (exit $EC2)")"
echo ""

echo "Shard 3 / 4 starting...  tail -f $RUN_DIR/shard-3.log"
run_shard 3 3 "${SHARD_3_MODULES[@]}"; EC3=$?
echo "Shard 3 → $([ "$EC3" -eq 0 ] && echo PASS || echo "FAIL (exit $EC3)")"
echo ""

echo "Shard 4 / 4 starting...  tail -f $RUN_DIR/shard-4.log"
run_shard 4 2 "${SHARD_4_MODULES[@]}"; EC4=$?
echo "Shard 4 → $([ "$EC4" -eq 0 ] && echo PASS || echo "FAIL (exit $EC4)")"
echo ""

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
