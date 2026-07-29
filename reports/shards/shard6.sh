#!/usr/bin/env bash
# Shard 6: performance_metrics, kiosk_settings, pos_settings, card_declines, user_roles
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
SHARDDIR="$REPO/reports/shards"
PYTHON="$REPO/venv/bin/python"
SHARD="shard6"
LOG="$SHARDDIR/${SHARD}.log"

MODULES=(performance_metrics kiosk_settings pos_settings card_declines user_roles)

mkdir -p "$SHARDDIR"
echo "[$SHARD] Started: $(date)" | tee "$LOG"

for MODULE in "${MODULES[@]}"; do
  MODLOG="$SHARDDIR/${SHARD}_${MODULE}.log"
  echo "[$SHARD] START $MODULE — $(date +%H:%M:%S)" | tee -a "$LOG"
  "$PYTHON" -m pytest "tests/admin_portal/${MODULE}/" \
    --headless -q --tb=line \
    --no-header \
    -p no:alluredir \
    2>&1 | tee "$MODLOG" || true
  LAST=$(grep -E "^=+.*(passed|failed|error).*=+$" "$MODLOG" 2>/dev/null | tail -1 || echo "no summary")
  echo "[$SHARD] DONE  $MODULE — $LAST" | tee -a "$LOG"
done

echo "[$SHARD] Finished: $(date)" | tee -a "$LOG"
