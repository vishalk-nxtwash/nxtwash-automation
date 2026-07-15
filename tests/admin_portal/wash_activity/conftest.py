import datetime
import time

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.wash_activity_page import WashActivityPage
from tests.admin_portal.admin_session import open_admin_path

# ── Constants ──────────────────────────────────────────────────────────────────

# Dependency: Sites & Locations module — WAC-FMD-001, WAC-SIT-001, WAC-SIT-003,
# WAC-SIT-004, WAC-SIT-013
WAC_SITE = "VK Test carwash 2"

# 7 sites visible in the dropdown (2 chips + "+5" overflow).
# Dependency: Sites & Locations module — WAC-SIT-004 (multi-site test).
WAC_MULTI_SITES = ["VK Test Wash 01", "VK Test carwash 2"]
WAC_ALL_SITE_COUNT = 7

# Test dataset anchored to Last month (06/01/2026 – 06/30/2026).
WAC_DATE_START = "06/01/2026"
WAC_DATE_END   = "06/30/2026"
TODAY_DATE     = datetime.date.today().strftime("%m/%d/%Y")

# Expected values for the Last-month dataset (WAC-KPI-002, WAC-DTE-017).
WAC_TOTAL_CARS    = 9
WAC_TOTAL_PAID_KPI = 9    # KPI card value — differs from tab count (defect WAC-KPI-011)
WAC_PAID_TAB_COUNT = 11   # Paid Washes tab count — differs from KPI (defect WAC-PWS-006)

# Zero-data state: Today returns all-zero KPIs and "No information for this period" chart.
WAC_ZERO_PRESET = "Today"
WAC_ZERO_DATE   = "07/13/2026"   # today's date at time of test dataset creation

# Dependency: Wash Packages / Custom Services module — WAC-PWS-001, WAC-CMP-001.
PAID_WASHES_BREAKDOWN = [
    ("vk wash 2 package", 5, "45.5%"),
    ("Detail cleaning",   3, "27.3%"),
    ("Vk detail wash",    3, "27.3%"),
]

# ── Date presets ───────────────────────────────────────────────────────────────
# WAC exposes 7 presets (CDL/RDM have 6 — WAC adds "Custom").
# TODO: confirm week-start convention (Sun vs Mon) — not confirmed in screenshots
# for this module. Revenue Overview/Redemptions = Sunday; Performance
# Metrics/Transactions = Monday.
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

# ── KPI card labels (WAC-KPI-001 parametrize list) ────────────────────────────
# Dependency: none — these are aggregate counts.
KPI_CARDS = [
    "Total Cars",
    "Daily Average",
    "Hourly Average",
    "Total Redemptions",
    "Total Paid",
    "Total Comp Washes",
]

# ── KPI sub-labels (WAC-KPI-008/009/010 parametrize list) ────────────────────
# Each tuple: (card_label, expected_sublabel).
# Dependency: Membership module (Total Redemptions sub-label).
KPI_SUBLABELS = [
    ("Total Paid",         "Single Washes"),
    ("Total Redemptions",  "Membership"),
    ("Total Comp Washes",  "Comp Washes"),
]

# ── Usage Breakdown tabs ───────────────────────────────────────────────────────
USAGE_TABS = ["Memberships", "Paid Washes", "Comp Washes"]

# Tabs that are empty in the Today (zero-data) state.
EMPTY_TABS_ZERO_DATA = ["Memberships", "Comp Washes"]

# ── Helpers ────────────────────────────────────────────────────────────────────


def open_wac_page(browser):
    """Navigate to /reports/detailed/cars_washed and wait for the filter modal."""
    open_admin_path(browser, "/reports/detailed/cars_washed")
    page = WashActivityPage(browser)
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

    TODO: confirm week-start convention (Sun vs Mon) — not yet verified for WAC.
    Using Sunday-start to match Revenue Overview / Redemptions until confirmed.
    """
    today = datetime.date.today()
    fmt = "%m/%d/%Y"

    if preset == "Today":
        return today.strftime(fmt), today.strftime(fmt)

    if preset == "Yesterday":
        d = today - datetime.timedelta(days=1)
        return d.strftime(fmt), d.strftime(fmt)

    if preset == "This week":
        # TODO: confirm week-start convention (Sun vs Mon) for WAC.
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
def wac_modal(browser):
    """Phase 1 — blocking filter modal open; no site or date selected."""
    return open_wac_page(browser)


@pytest.fixture
def wac_page(browser):
    """Phase 2 — WAC_SITE + Last month applied; metrics screen visible."""
    page = open_wac_page(browser)
    page.select_site(WAC_SITE)
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
def wac_zero_data(browser):
    """Phase 2 — WAC_SITE + Today; all KPIs expected to be 0, chart shows no-data."""
    page = open_wac_page(browser)
    page.select_site(WAC_SITE)
    page.select_date_preset(WAC_ZERO_PRESET)
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(1.0)
    page.apply_modal_filters()
    return page


@pytest.fixture
def wac_single_day(browser):
    """Phase 1 — filter modal open with Single day checkbox checked and site set."""
    page = open_wac_page(browser)
    page.select_site(WAC_SITE)
    page.check_modal_single_day()
    time.sleep(0.5)
    return page


# ── SingleDaySyncMixin fixture aliases (sdm_* names) ─────────────────────────
# These satisfy the fixture names expected by SingleDaySyncMixin.

@pytest.fixture
def sdm_modal(browser):
    return open_wac_page(browser)


@pytest.fixture
def sdm_single_day(browser):
    page = open_wac_page(browser)
    page.select_site(WAC_SITE)
    page.check_modal_single_day()
    time.sleep(0.5)
    return page


@pytest.fixture
def sdm_page(browser):
    page = open_wac_page(browser)
    page.select_site(WAC_SITE)
    page.select_date_preset("Last month")
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    return page
