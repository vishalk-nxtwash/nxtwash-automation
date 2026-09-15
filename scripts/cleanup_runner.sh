#!/usr/bin/env bash
# Emergency cleanup for self-hosted EC2 runners.
# Run this via SSH when the runner disk is too full to start GitHub Actions jobs:
#
#   ssh ec2-user@<IP> 'bash -s' < scripts/cleanup_runner.sh
#
# Or copy it to the instance and run:
#   ssh ec2-user@<IP>
#   bash ~/cleanup_runner.sh

set -euo pipefail

echo "=== Disk before cleanup ==="
df -h /

echo ""
echo "--- Killing stale Chrome / chromedriver processes ---"
pkill -f "chrome" || true
pkill -f "chromedriver" || true

echo ""
echo "--- Removing Chrome temp profiles from /tmp ---"
rm -rf /tmp/.com.google.Chrome* /tmp/chrome_* /tmp/.org.chromium.* \
       /tmp/scoped_dir* /tmp/.chromium* \
       2>/dev/null || true

echo ""
echo "--- Removing test artifacts from runner workspaces ---"
RUNNER_HOME="${RUNNER_HOME:-/home/ec2-user/runners}"
for slot_dir in "$RUNNER_HOME"/*/; do
    work_root="${slot_dir}_work/nxtwash-automation/nxtwash-automation"
    if [ -d "$work_root" ]; then
        echo "  Cleaning: $work_root"
        rm -rf \
            "$work_root/reports" \
            "$work_root/allure-results" \
            "$work_root/allure-report" \
            "$work_root/screenshots" \
            "$work_root/logs" \
            "$work_root/report.html" \
            "$work_root/results.xml" \
            2>/dev/null || true
        find "$work_root" -maxdepth 5 -name "__pycache__" -type d \
            -exec rm -rf {} + 2>/dev/null || true
    fi
done

echo ""
echo "--- Purging pip cache ---"
python3.11 -m pip cache purge 2>/dev/null || true

echo ""
echo "--- Purging npm cache ---"
npm cache clean --force 2>/dev/null || true

echo ""
echo "=== Disk after cleanup ==="
df -h /
