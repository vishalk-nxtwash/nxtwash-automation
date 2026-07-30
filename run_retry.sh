#!/usr/bin/env bash
# run_retry.sh — Re-run only the shards that failed in the last full suite.
#
# Usage:
#   ./run_retry.sh              # headless (matches CI), all 7 shards
#   ./run_retry.sh --headed     # visible browser
#   ./run_retry.sh --dry-run    # print shard assignments, do not run
#
# Single shard (skip the others):
#   ./run_retry.sh --shard wash-packages
#   ./run_retry.sh --shard wash-catalog
#   ./run_retry.sh --shard services
#   ./run_retry.sh --shard settings-pos
#   ./run_retry.sh --shard settings-hw
#   ./run_retry.sh --shard promotions
#   ./run_retry.sh --shard people

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTEST="$SCRIPT_DIR/venv/bin/pytest"
PYTHON="$SCRIPT_DIR/venv/bin/python"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RUN_DIR="$SCRIPT_DIR/reports/runs/retry_$TIMESTAMP"

HEADLESS_FLAG="--headless"
DRY_RUN=0
ONLY_SHARD=""

PREV_ARG=""
for arg in "$@"; do
    case $arg in
        --dry-run) DRY_RUN=1 ;;
        --headed)  HEADLESS_FLAG="" ;;
        *)
            if [ "$PREV_ARG" = "--shard" ]; then
                ONLY_SHARD="$arg"
            fi
            ;;
    esac
    PREV_ARG="$arg"
done

# ── Shard definitions (failing shards only) ────────────────────────────────

SHARD_wash_packages="tests/admin_portal/wash_packages tests/admin_portal/wash_extras"
SHARD_wash_catalog="tests/admin_portal/wash_books tests/admin_portal/coupon_packages"
SHARD_services="tests/admin_portal/custom_services tests/admin_portal/gift_cards tests/admin_portal/bank_drop"
SHARD_settings_pos="tests/admin_portal/pos_settings tests/admin_portal/user_roles"
SHARD_settings_hw="tests/admin_portal/kiosk_settings tests/admin_portal/tunnel_settings"
SHARD_promotions="tests/admin_portal/discounts tests/admin_portal/memberships"
SHARD_people="tests/admin_portal/users tests/admin_portal/employees"

SHARD_NAMES="wash-packages wash-catalog services settings-pos settings-hw promotions people"

shard_paths() {
    local name="$1"
    local key
    key=$(echo "$name" | tr '-' '_')
    eval echo "\$SHARD_${key}"
}

# ── Dry-run output ─────────────────────────────────────────────────────────
if [ "$DRY_RUN" -eq 1 ]; then
    echo "DRY RUN — retry shard assignments:"
    echo ""
    for name in $SHARD_NAMES; do
        echo "  [$name]"
        for path in $(shard_paths "$name"); do echo "    $path"; done
        echo ""
    done
    exit 0
fi

mkdir -p "$RUN_DIR"

echo "════════════════════════════════════════════════════════════════════"
echo "  NxtWash Admin Portal — Retry Failed Shards"
echo "  Started : $(date '+%Y-%m-%d %H:%M:%S')"
echo "  Run dir : $RUN_DIR"
echo "  Mode    : $([ -n "$HEADLESS_FLAG" ] && echo headless || echo headed)"
[ -n "$ONLY_SHARD" ] && echo "  Shard   : $ONLY_SHARD only"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# ── Shard runner ───────────────────────────────────────────────────────────
run_shard() {
    local name="$1"
    shift
    local log="$RUN_DIR/${name}.log"
    local allure_dir="$RUN_DIR/${name}-allure"
    local junit="$RUN_DIR/${name}-junit.xml"

    mkdir -p "$allure_dir"

    {
        echo "════════════════════════════════════════════════════"
        echo "  Shard [$name] started at $(date '+%H:%M:%S')"
        echo "  Modules: $*"
        echo "════════════════════════════════════════════════════"
        echo ""
    } > "$log"

    # shellcheck disable=SC2086
    "$PYTEST" $@ \
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
        echo "  Shard [$name] finished at $(date '+%H:%M:%S') — exit code: $ec"
        echo "════════════════════════════════════════════════════"
    } >> "$log"
    exit $ec
}

# ── Single-shard mode ──────────────────────────────────────────────────────
if [ -n "$ONLY_SHARD" ]; then
    paths=$(shard_paths "$ONLY_SHARD")
    if [ -z "$paths" ]; then
        echo "Unknown shard '$ONLY_SHARD'. Valid names: $SHARD_NAMES"
        exit 1
    fi
    mkdir -p "$RUN_DIR"
    run_shard "$ONLY_SHARD" $paths
    exit $?
fi

# ── Launch all failing shards in parallel ──────────────────────────────────
PIDS=""
for name in $SHARD_NAMES; do
    paths=$(shard_paths "$name")
    run_shard "$name" $paths &
    pid=$!
    PIDS="$PIDS $name:$pid"
    echo "  Started [$name]  PID=$pid"
done
echo ""
echo "Monitor live progress:"
for name in $SHARD_NAMES; do
    echo "  tail -f $RUN_DIR/${name}.log"
done
echo ""

# ── Wait and collect results ───────────────────────────────────────────────
OVERALL=0
RESULTS=""
for entry in $PIDS; do
    name="${entry%%:*}"
    pid="${entry##*:}"
    wait "$pid"
    ec=$?
    RESULTS="$RESULTS $name:$ec"
    [ "$ec" -ne 0 ] && OVERALL=1
done

echo "Results:"
for entry in $RESULTS; do
    name="${entry%%:*}"
    ec="${entry##*:}"
    label=$([ "$ec" -eq 0 ] && echo "PASS" || echo "FAIL (exit $ec)")
    echo "  [$name] → $label"
done
echo ""

# ── Generate report ────────────────────────────────────────────────────────
EC_ARGS=""
for entry in $RESULTS; do
    EC_ARGS="$EC_ARGS ${entry##*:}"
done
"$PYTHON" "$SCRIPT_DIR/generate_report.py" "$RUN_DIR" $EC_ARGS 2>/dev/null || true

SUMMARY="$RUN_DIR/summary.txt"
if [ -f "$SUMMARY" ]; then
    cat "$SUMMARY"
    echo ""
    echo "Report saved: $SUMMARY"
fi

exit $OVERALL
