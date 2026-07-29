#!/usr/bin/env python3
"""
generate_report.py — Consolidate sharded pytest run results into a summary.

Usage:
    python generate_report.py <run_dir> <ec1> <ec2> <ec3> <ec4>

Parses the 4 shard log files in <run_dir>, extracts per-module pass/fail/skip/
xfail counts and failed test names, then prints and saves a formatted report.
"""

import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict, OrderedDict
from datetime import datetime
from pathlib import Path

# ── Shard → module mapping (mirrors run_shards.sh) ────────────────────────
SHARD_MODULES = {
    1: [
        "transactions", "customers", "wash_activity", "wash_extras",
        "user_roles", "sites", "login", "bank_drop",
    ],
    2: [
        "redemptions", "kiosk_settings", "general_sales_report", "wash_packages",
        "pos_settings", "custom_services", "tunnel_settings",
    ],
    3: [
        "revenue_overview", "labor_shifts", "card_declines", "overview",
        "memberships", "cash_report", "service_categories",
    ],
    4: [
        "employees", "performance_metrics", "wash_books", "discounts",
        "users", "coupon_packages", "gift_cards",
    ],
}

# Matches a verbose test result line:
# tests/admin_portal/<module>/test_foo.py::Class::test PASSED   [100%]
_TEST_LINE = re.compile(
    r"tests/admin_portal/([^/]+)/[^\s]+::[^\s]+\s+"
    r"(PASSED|FAILED|ERROR|SKIPPED|xfailed|xpassed|XFAILED|XPASSED)"
)

# Matches the final summary line from pytest:
# 142 passed, 3 failed, 5 skipped, 2 xfailed in 1823.45s (0:30:23)
_SUMMARY_LINE = re.compile(
    r"(?:(\d+) passed)?[, ]*"
    r"(?:(\d+) failed)?[, ]*"
    r"(?:(\d+) error)?[, ]*"
    r"(?:(\d+) skipped)?[, ]*"
    r"(?:(\d+) xfailed)?[, ]*"
    r"(?:(\d+) xpassed)?[, ]*"
    r"in ([\d.]+)s"
)

# Failed test in short summary section:
# FAILED tests/admin_portal/bank_drop/test_bank_drop_edit.py::Class::test - msg
_FAILED_ITEM = re.compile(r"^FAILED (tests/admin_portal/[^\s]+)")
_ERROR_ITEM  = re.compile(r"^ERROR (tests/admin_portal/[^\s]+)")


def parse_log(log_path: str):
    """Return (module_stats, failed_tests, shard_summary, duration_s)."""
    module_stats = defaultdict(lambda: {
        "passed": 0, "failed": 0, "skipped": 0,
        "xfailed": 0, "xpassed": 0, "error": 0,
    })
    failed_tests: list[str] = []
    shard_totals = {"passed": 0, "failed": 0, "error": 0,
                    "skipped": 0, "xfailed": 0, "xpassed": 0}
    duration_s = 0.0
    in_summary_section = False

    if not os.path.exists(log_path):
        return module_stats, failed_tests, shard_totals, duration_s

    with open(log_path, encoding="utf-8", errors="replace") as fh:
        for raw_line in fh:
            line = raw_line.rstrip()

            # ── Detect short test summary section ─────────────────────────
            if "short test summary info" in line:
                in_summary_section = True
                continue

            if in_summary_section:
                m = _FAILED_ITEM.match(line)
                if m:
                    failed_tests.append(m.group(1))
                    continue
                m = _ERROR_ITEM.match(line)
                if m:
                    failed_tests.append(m.group(1) + "  [ERROR]")
                    continue
                # End of summary section when we hit the === line
                if line.startswith("="):
                    in_summary_section = False

            # ── Per-test verbose line ──────────────────────────────────────
            m = _TEST_LINE.search(line)
            if m:
                mod, status = m.group(1), m.group(2).lower()
                if status == "passed":
                    module_stats[mod]["passed"] += 1
                elif status == "failed":
                    module_stats[mod]["failed"] += 1
                elif status in ("skipped",):
                    module_stats[mod]["skipped"] += 1
                elif status in ("xfailed",):
                    module_stats[mod]["xfailed"] += 1
                elif status in ("xpassed",):
                    module_stats[mod]["xpassed"] += 1
                elif status == "error":
                    module_stats[mod]["error"] += 1
                continue

            # ── Final summary line ─────────────────────────────────────────
            m = _SUMMARY_LINE.search(line)
            if m and ("passed" in line or "failed" in line or "error" in line):
                g = m.groups()
                if any(g):
                    shard_totals["passed"]  = int(g[0] or 0)
                    shard_totals["failed"]  = int(g[1] or 0)
                    shard_totals["error"]   = int(g[2] or 0)
                    shard_totals["skipped"] = int(g[3] or 0)
                    shard_totals["xfailed"] = int(g[4] or 0)
                    shard_totals["xpassed"] = int(g[5] or 0)
                    duration_s = float(g[6] or 0)

    return module_stats, failed_tests, shard_totals, duration_s


def fmt_duration(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    if h:
        return f"{h}h {m:02d}m {sec:02d}s"
    if m:
        return f"{m}m {sec:02d}s"
    return f"{sec}s"


def status_bar(passed, failed, error, skipped, xfailed, total) -> str:
    """One-line compact counts."""
    parts = []
    if passed:  parts.append(f"{passed:>4} passed")
    if failed:  parts.append(f"{failed:>4} FAILED")
    if error:   parts.append(f"{error:>4} ERROR ")
    if skipped: parts.append(f"{skipped:>4} skipped")
    if xfailed: parts.append(f"{xfailed:>4} xfailed")
    return "  ".join(parts) if parts else "  (no results)"


def build_report(run_dir: str, exit_codes: list[int]) -> str:
    lines: list[str] = []
    sep = "═" * 72

    # Header
    lines += [
        sep,
        "  NxtWash Admin Portal — Sharded Test Run Report",
        f"  Run dir : {run_dir}",
        f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        sep,
        "",
    ]

    grand = {"passed": 0, "failed": 0, "error": 0,
             "skipped": 0, "xfailed": 0, "xpassed": 0}
    all_failed_tests: list[tuple[int, str]] = []
    total_duration = 0.0

    for shard_num in [1, 2, 3, 4]:
        log_path = os.path.join(run_dir, f"shard-{shard_num}.log")
        ec = exit_codes[shard_num - 1]
        mod_stats, failed_tests, totals, duration = parse_log(log_path)

        total_duration = max(total_duration, duration)  # shards run in parallel

        shard_pass = "PASS" if ec == 0 else f"FAIL (exit {ec})"
        lines += [
            f"  SHARD {shard_num}  [{shard_pass}]  {fmt_duration(duration)}",
            "  " + "─" * 68,
        ]

        # Per-module rows
        col_w = 28
        for mod in SHARD_MODULES[shard_num]:
            s = mod_stats.get(mod, {})
            p  = s.get("passed",  0)
            f  = s.get("failed",  0)
            e  = s.get("error",   0)
            sk = s.get("skipped", 0)
            xf = s.get("xfailed", 0)
            tot = p + f + e + sk + xf
            bar = status_bar(p, f, e, sk, xf, tot)
            collected = f"({tot} collected)" if tot else "(no data)"
            lines.append(f"  {mod:<{col_w}}  {bar}  {collected}")

        # Shard totals row
        tp = totals["passed"]
        tf = totals["failed"] + totals["error"]
        ts = totals["skipped"]
        tx = totals["xfailed"]
        t_total = tp + tf + ts + tx
        lines += [
            "  " + "─" * 68,
            f"  {'SHARD TOTAL':<{col_w}}  {status_bar(tp, tf, 0, ts, tx, t_total)}",
            "",
        ]

        # Accumulate grand totals
        for k in grand:
            grand[k] += totals.get(k, 0)

        # Collect failed test names
        for ft in failed_tests:
            all_failed_tests.append((shard_num, ft))

    # Grand total
    gt = grand["passed"]
    gf = grand["failed"] + grand["error"]
    gs = grand["skipped"]
    gx = grand["xfailed"]
    g_total = gt + gf + gs + gx
    pct_pass = (gt / g_total * 100) if g_total else 0

    lines += [
        sep,
        "  OVERALL TOTALS",
        "  " + "─" * 68,
        f"  Total tests : {g_total}",
        f"  Passed      : {gt}  ({pct_pass:.1f}%)",
        f"  Failed      : {gf}",
        f"  Skipped     : {gs}",
        f"  XFailed     : {gx}",
        f"  Wall time   : ~{fmt_duration(total_duration)}  (parallel, longest shard)",
        sep,
        "",
    ]

    # Failed tests list
    if all_failed_tests:
        lines += [f"  FAILED TESTS  ({len(all_failed_tests)} total)", "  " + "─" * 68]
        current_shard = None
        for shard_num, ft in sorted(all_failed_tests, key=lambda x: (x[0], x[1])):
            if shard_num != current_shard:
                lines.append(f"  [Shard {shard_num}]")
                current_shard = shard_num
            lines.append(f"    {ft}")
        lines += ["", sep]
    else:
        lines += ["  ALL TESTS PASSED — no failures recorded.", sep]

    lines += [
        "",
        "  Logs    : tail -f {run_dir}/shard-N.log".replace("{run_dir}", run_dir),
        "  Allure  : allure serve {run_dir}/shard-N-allure".replace("{run_dir}", run_dir),
        sep,
    ]

    return "\n".join(lines)


def main():
    if len(sys.argv) < 6:
        print("Usage: generate_report.py <run_dir> <ec1> <ec2> <ec3> <ec4>")
        sys.exit(1)

    run_dir = sys.argv[1]
    exit_codes = [int(x) for x in sys.argv[2:6]]

    report = build_report(run_dir, exit_codes)

    summary_path = os.path.join(run_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as fh:
        fh.write(report)


if __name__ == "__main__":
    main()
