#!/usr/bin/env bash
# run_retry.sh — Re-run only the shards that failed in the last full suite.
#
# Mirrors the GitHub Actions retry workflow (suite-admin-retry.yml) locally.
# Runs 7 parallel shards; skips the 6 already-green ones.
#
# Usage:
#   ./run_retry.sh              # headless (matches CI)
#   ./run_retry.sh --headed     # visible browser
#   ./run_retry.sh --dry-run    # print shard assignments, do not run
#
# Individual shard (skip the others):
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

for arg in "$@"; do
    case $arg in
        --dry-run)  DRY_RUN=1 ;;
        --headed)   HEADLESS_FLAG="" ;;
        --shard)    ;;   # consumed by next iteration
        *)
            if [[ "${PREV_ARG:-}" == "--shard" ]]; then
                ONLY_SHARD="$arg"
            fi
            ;;
    esac
    PREV_ARG="$arg"
done

# ── Shard definitions (failing shards only) ────────────────────────────────
declare -A SHARD_PATHS
declare -A SHARD_COMMENTS

SHARD_PATHS["wash-packages"]="tests/admin_portal/wash_packages tests/admin_portal/wash_extras"
SHARD_COMMENTS["wash-packages"]="stale element on edit / checkbox closure"

SHARD_PATHS["wash-catalog"]="tests/admin_portal/wash_books tests/admin_portal/coupon_packages"
SHARD_COMMENTS["wash-catalog"]="stale element on open_edit_wash_book"

SHARD_PATHS["services"]="tests/admin_portal/custom_services tests/admin_portal/gift_cards tests/admin_portal/bank_drop"
SHARD_COMMENTS["services"]="iframe 8s timeout + gift card field doubling"

SHARD_PATHS["settings-pos"]="tests/admin_portal/pos_settings tests/admin_portal/user_roles"
SHARD_COMMENTS["settings-pos"]="user_roles toggle stale closure"

SHARD_PATHS["settings-hw"]="tests/admin_portal/kiosk_settings tests/admin_portal/tunnel_settings"
SHARD_COMMENTS["settings-hw"]="kiosk pagination timeout"

SHARD_PATHS["promotions"]="tests/admin_portal/discounts tests/admin_portal/memberships"
SHARD_COMMENTS["promotions"]="memberships filter contamination (was CANCELLED)"

SHARD_PATHS["people"]="tests/admin_portal/users tests/admin_portal/employees"
SHARD_COMMENTS["people"]="fixture cascade timeout (was CANCELLED)"

SHARD_ORDER=(wash-packages wash-catalog services settings-pos settings-hw promotions people)

# ── Dry-run output ─────────────────────────────────────────────────────────
if [ "$DRY_RUN" -eq 1 ]; then
    echo "DRY RUN — retry shard assignments:"
    echo ""
    for name in "${SHARD_ORDER[@]}"; do
        echo "  [$name]  ${SHARD_COMMENTS[$name]}"
        for path in ${SHARD_PATHS[$name]}; do echo "    $path"; done
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
if [ -n "$ONLY_SHARD" ]; then
    echo "  Shard   : $ONLY_SHARD only"
fi
echo "════════════════════════════════════════════════════════════════════"
echo ""

# ── Shard runner ───────────────────────────────────────────────────────────
run_shard() {
    local name=$1
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

# ── Launch shards ─────────────────────────────────────────────────────────
declare -A PIDS
declare -A ECS

if [ -n "$ONLY_SHARD" ]; then
    if [ -z "${SHARD_PATHS[$ONLY_SHARD]+_}" ]; then
        echo "Unknown shard '$ONLY_SHARD'. Valid names: ${SHARD_ORDER[*]}"
        exit 1
    fi
    run_shard "$ONLY_SHARD" ${SHARD_PATHS[$ONLY_SHARD]}
    exit $?
fi

for name in "${SHARD_ORDER[@]}"; do
    run_shard "$name" ${SHARD_PATHS[$name]} &
    PIDS[$name]=$!
    echo "  Started [$name]  PID=${PIDS[$name]}"
done
echo ""
echo "Monitor live progress:"
for name in "${SHARD_ORDER[@]}"; do
    echo "  tail -f $RUN_DIR/${name}.log"
done
echo ""

# ── Wait and collect exit codes ────────────────────────────────────────────
for name in "${SHARD_ORDER[@]}"; do
    wait "${PIDS[$name]}"
    ECS[$name]=$?
done

echo ""
echo "Results:"
OVERALL=0
for name in "${SHARD_ORDER[@]}"; do
    ec="${ECS[$name]}"
    label=$([ "$ec" -eq 0 ] && echo "PASS" || echo "FAIL (exit $ec)")
    echo "  [$name] → $label"
    [ "$ec" -ne 0 ] && OVERALL=1
done
echo ""

# ── Generate report ────────────────────────────────────────────────────────
EC_ARGS=()
for name in "${SHARD_ORDER[@]}"; do
    EC_ARGS+=("${ECS[$name]}")
done
"$PYTHON" "$SCRIPT_DIR/generate_report.py" "$RUN_DIR" "${EC_ARGS[@]}" 2>/dev/null || true

SUMMARY="$RUN_DIR/summary.txt"
if [ -f "$SUMMARY" ]; then
    echo ""
    cat "$SUMMARY"
    echo ""
    echo "Report saved: $SUMMARY"
fi

exit $OVERALL
