import datetime
import time

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.performance_metrics_page import PerformanceMetricsPage
from tests.admin_portal.admin_session import open_admin_path

# ── Constants ──────────────────────────────────────────────────────────────────

PFM_SITE  = "VK Test carwash 2"
PFM_SITE_2 = "VK AL02"

# Absolute date strings anchored to test dataset (today = 07/10/2026).
LAST_MONTH_START = "06/01/2026"
LAST_MONTH_END   = "06/30/2026"
THIS_MONTH_START = "07/01/2026"
THIS_MONTH_END   = "07/10/2026"
TODAY_DATE       = "07/10/2026"
YESTERDAY_DATE   = "07/09/2026"

# 6 date presets (no Custom — PFM differs from Revenue Overview)
DATE_PRESETS = ["Today", "Yesterday", "This week", "Last week", "This month", "Last month"]

CVR_CONSTRAINT_TEXT = "At least week range for this widget is required"

# Exact 18-column list for PFM-MHT-002.
MHT_COLUMNS = [
    "Date",
    "Site Name",
    "Total",
    "Recurring",
    "Prepaid",
    "New",
    "New Recurring",
    "New Prepaid",
    "Resignup",
    "Recharges",
    "Current day recharges",
    "Prev. day recharge",
    "Cancelled",
    "Declined",
    "Declined & Canceled",
    "Current day declines count",
    "Previous day declines count",
    "Net movement",
]

CST_TOGGLE_COUNT = 17   # toggles in Column Settings modal (Date is pinned, not in list)

# ── Helpers ────────────────────────────────────────────────────────────────────


def open_pfm_page(browser):
    open_admin_path(browser, "/performance-metrics")
    page = PerformanceMetricsPage(browser)
    page.wait_for_modal()
    return page


def page_has_no_broken_state(page):
    try:
        body = page.get_body_text().lower()
    except Exception:
        return True
    broken_signals = [
        "something went wrong", "internal server error",
        "application error", "cannot read", "typeerror", "uncaught error",
    ]
    return not any(s in body for s in broken_signals)


def compute_preset_date_range(preset):
    """Return (start_str, end_str) for a preset computed against today.

    Week start = Monday (PFM convention; differs from Revenue Overview).
    """
    today = datetime.date.today()
    fmt = "%m/%d/%Y"

    if preset == "Today":
        return today.strftime(fmt), today.strftime(fmt)

    if preset == "Yesterday":
        y = today - datetime.timedelta(days=1)
        return y.strftime(fmt), y.strftime(fmt)

    if preset == "This week":
        # Monday of the current week
        mon = today - datetime.timedelta(days=today.weekday())
        sun = mon + datetime.timedelta(days=6)
        return mon.strftime(fmt), min(today, sun).strftime(fmt)

    if preset == "Last week":
        mon = today - datetime.timedelta(days=today.weekday() + 7)
        sun = mon + datetime.timedelta(days=6)
        return mon.strftime(fmt), sun.strftime(fmt)

    if preset == "This month":
        first = today.replace(day=1)
        return first.strftime(fmt), today.strftime(fmt)

    if preset == "Last month":
        first_this = today.replace(day=1)
        last_prev  = first_this - datetime.timedelta(days=1)
        first_prev = last_prev.replace(day=1)
        return first_prev.strftime(fmt), last_prev.strftime(fmt)

    return "", ""


# ── Fixtures ───────────────────────────────────────────────────────────────────


@pytest.fixture
def pfm_modal(browser):
    """Phase 1 — filter modal open, no filters applied."""
    return open_pfm_page(browser)


@pytest.fixture
def pfm_page(browser):
    """Phase 2 — VK Test carwash 2 + Last month applied.

    Last month (06/01–06/30/2026, 30 days) gives a stable dataset:
    CVR renders the chart (≥ 7 days) and MHT has Jun 30→Jun 1 rows.
    """
    page = open_pfm_page(browser)
    page.select_site(PFM_SITE)
    page.select_date_preset("Last month")
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    return page


@pytest.fixture
def zero_data_filter(browser):
    """Phase 2 — All Sites + Today.

    Today (single day) produces:
      CVR → constraint message (< 7 days)
      MHT → "No data for this site/period"
    """
    page = open_pfm_page(browser)
    # Leave site at default (All Sites — no selection needed)
    page.select_date_preset("Today")
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(1.5)
    page.apply_modal_filters()
    return page
