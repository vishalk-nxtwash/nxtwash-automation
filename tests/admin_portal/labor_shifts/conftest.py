import datetime
import time

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.labor_shifts_page import LaborShiftsPage
from tests.admin_portal.admin_session import open_admin_path

# ── Constants ──────────────────────────────────────────────────────────────────

# Dependency: Sites & Locations module — LAB-FMD-001, LAB-SIT-001, LAB-SIT-003,
# LAB-SIT-013.
LAB_SITE = "VK Test carwash 2"

# 5 sites used in LAB-SIT-004 and LAB-SIT-005 (2 chips + "+3" overflow).
# TODO: confirm exact names for all 5 sites via DevTools on first run.
LAB_MULTI_SITES_5 = [
    "VK Test carwash 2",
    "VK Test Wash 01",
    "VK AL11",
    "VK Test Wash 03",   # TODO: confirm site name
    "VK Test Wash 04",   # TODO: confirm site name
]
LAB_MULTI_CHIP_COUNT    = 2
LAB_MULTI_OVERFLOW_TEXT = "+3"

# Primary dataset: This month (07/01/2026 – current date).
LAB_DATE_PRESET        = "This month"
LAB_THIS_MONTH_START   = "07/01/2026"
LAB_THIS_MONTH_END     = "07/13/2026"   # at time of test data collection

# Zero-state dataset: Today has no activity in the test environment.
LAB_ZERO_PRESET = "Today"
LAB_ZERO_DATE   = datetime.date.today().strftime("%m/%d/%Y")

# Known test data values (VK Test carwash 2, This month).
LAB_COST_PER_CAR        = "$27.27"
LAB_COMMISSION_TOTAL    = "$24.00"
LAB_COMMISSION_RETAIL   = "$24.00"
LAB_COMMISSION_MEMBERSHIP = "$0.00"
LAB_COMMISSION_WASHBOOK = "$0.00"
LAB_CTX_ROW_COUNT       = 7

# No-match search term for both employee table and CTX table.
LAB_SEARCH_NO_MATCH = "test"

# ── Date presets ───────────────────────────────────────────────────────────────
# LAB exposes 7 presets (same as Wash Activity — includes Custom).
# TODO: confirm week-start convention (Sun vs Mon) — not confirmed for Labor & Shifts.
# Wash Activity also unconfirmed. Transactions = Monday, Revenue Overview/Redemptions = Sunday.
DATE_PRESETS = [
    "Today",
    "Yesterday",
    "This week",
    "Last week",
    "This month",
    "Last month",
    "Custom",
]

DATE_PRESETS_PARAMETRIZED = [
    "Today",
    "Yesterday",
    "This week",
    "Last week",
    "This month",
    "Last month",
]

# ── Widget labels ──────────────────────────────────────────────────────────────

# 4 KPI/metric widgets (LAB-KPI-001).
KPI_CARD_LABELS = [
    "Labor",
    "Cost Per Car",
    "Productivity",
    "Employee",     # Employees summary card — contains "Employee" in heading
]

# 4 commission card labels (LAB-CSM-001).
COMMISSION_CARDS = [
    "Membership Sales",
    "Retail Sales",
    "Washbook Sales",
    "Total Commission",
]

# ── Table column definitions ───────────────────────────────────────────────────

# Employee table columns (LAB-EMP-001).
EMP_COLUMNS = [
    "Employee",
    "Membership sales",
    "Resignups",
    "Commission",
    "Total shifts",
    "Hours Worked",
    "Overtime",
    "Status",
]

# Commission Transactions table columns (LAB-CTX-001).
CTX_COLUMNS = [
    "Date",
    "Employee",
    "Customer",
    "Type",
    "Service",
    "License plate",
    "Service Price",
    "Commission Amount",
]

# ── Helpers ────────────────────────────────────────────────────────────────────


def open_lab_page(browser):
    """Navigate to /reports/detailed/employee_labor and wait for the filter modal."""
    open_admin_path(browser, "/reports/detailed/employee_labor")
    page = LaborShiftsPage(browser)
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
    """Return (start_str, end_str) for a named preset relative to today.

    TODO: confirm week-start convention (Sun vs Mon) — not confirmed for Labor & Shifts.
    Using Sunday-start tentatively to match CDL / Card Declines until confirmed.
    """
    today = datetime.date.today()
    fmt = "%m/%d/%Y"

    if preset == "Today":
        return today.strftime(fmt), today.strftime(fmt)

    if preset == "Yesterday":
        d = today - datetime.timedelta(days=1)
        return d.strftime(fmt), d.strftime(fmt)

    if preset == "This week":
        days_since_sunday = (today.weekday() + 1) % 7
        sunday = today - datetime.timedelta(days=days_since_sunday)
        return sunday.strftime(fmt), today.strftime(fmt)

    if preset == "Last week":
        days_since_sunday = (today.weekday() + 1) % 7
        this_sunday = today - datetime.timedelta(days=days_since_sunday)
        last_sunday = this_sunday - datetime.timedelta(days=7)
        last_saturday = last_sunday + datetime.timedelta(days=6)
        return last_sunday.strftime(fmt), last_saturday.strftime(fmt)

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
def lab_modal(browser):
    """Phase 1 — blocking filter modal open; no site or date selected."""
    return open_lab_page(browser)


@pytest.fixture
def lab_page(browser):
    """Phase 2 — LAB_SITE + This month applied; metrics screen visible.

    Primary dataset (07/01/2026 – current date):
    Cost Per Car = $27.27, Commission Total = $24.00 (all Retail),
    7 Commission Transactions rows.
    """
    page = open_lab_page(browser)
    page.select_site(LAB_SITE)
    page.select_date_preset(LAB_DATE_PRESET)
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    return page


@pytest.fixture
def lab_zero_data(browser):
    """Phase 2 — LAB_SITE + Today; all KPIs = 0 / $0.00, both tables = 0 records.

    Shared by LAB-KPI-003 (all metrics zero), LAB-EMP-002 (employee table empty),
    and LAB-CSM-002 (commission cards $0.00).
    """
    page = open_lab_page(browser)
    page.select_site(LAB_SITE)
    page.select_date_preset(LAB_ZERO_PRESET)
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(1.0)
    page.apply_modal_filters()
    return page


@pytest.fixture
def lab_single_day(browser):
    """Phase 1 — filter modal open with Single day checkbox checked and LAB_SITE set."""
    page = open_lab_page(browser)
    page.select_site(LAB_SITE)
    page.check_modal_single_day()
    time.sleep(0.5)
    return page


# ── SingleDaySyncMixin fixture aliases (sdm_* names) ─────────────────────────
# These satisfy the fixture names expected by SingleDaySyncMixin in mixins.py.


@pytest.fixture
def sdm_modal(browser):
    return open_lab_page(browser)


@pytest.fixture
def sdm_single_day(browser):
    page = open_lab_page(browser)
    page.select_site(LAB_SITE)
    page.check_modal_single_day()
    time.sleep(0.5)
    return page


@pytest.fixture
def sdm_page(browser):
    page = open_lab_page(browser)
    page.select_site(LAB_SITE)
    page.select_date_preset(LAB_DATE_PRESET)
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    return page
