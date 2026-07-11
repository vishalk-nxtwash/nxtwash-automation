import datetime
import time

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.card_declines_page import CardDeclinesPage
from tests.admin_portal.admin_session import open_admin_path

# ── Constants ──────────────────────────────────────────────────────────────────

CDL_SITE = "VK Test carwash 2"

# Multi-site pair used in CDL-SIT-004.
CDL_MULTI_SITES = ["VK Test Wash 01", "VK Test carwash 2"]

# Known defect site — appears in Best & Worst Sites outside any active site
# filter (see CDL-BWS-004 xfail).
CDL_DEFECT_SITE = "Test Location 1"

# Absolute date strings anchored to test dataset (today = 07/12/2026).
# Last month (06/01–06/30/2026) provides a stable dataset with CC declines.
CDL_DATE_START = "06/01/2026"
CDL_DATE_END   = "06/30/2026"
TODAY_DATE     = datetime.date.today().strftime("%m/%d/%Y")

# Past date range guaranteed to have zero CC decline records.
CDL_ZERO_DATE_START = "01/01/2022"
CDL_ZERO_DATE_END   = "01/31/2022"

# Card Declines exposes 6 date presets (same as other detailed reports).
# TODO: Confirm exact preset labels and order via DevTools on first live run.
DATE_PRESETS = [
    "Today",
    "Yesterday",
    "This week",
    "Last week",
    "This month",
    "Last month",
]

# ── Glossary terms (CDL-GLS-002 parametrize list) ─────────────────────────────
# 9 terms as specified in the test sheet.
GLOSSARY_TERMS = [
    "Initial Recharge",
    "Successful Initial Recharges",
    "Initial Decline",
    "Recovery Attempt",
    "Successfully Recovered",
    "Recover Day 1",
    "Recover Day 2+",
    "Unrecovered",
    "Important",
]

# ── KPI card labels (CDL-KPI-001 parametrize list) ────────────────────────────
# 8 cards as specified in the test sheet.
KPI_CARDS = [
    "Initial Recharge Attempts",
    "Successful Initial Recharges",
    "Initial Declines",
    "Total Recovery Attempts",
    "Successfully Recovered",
    "Recover Day 1",
    "Recover Day 2+",
    "Unrecovered",
]

# ── Matrix column headers (CDL-MTX-002 parametrize list) ──────────────────────
# 13 columns as specified in the test sheet.
MATRIX_COLUMNS = [
    "Plan Name",
    "Initial Recharge Attempts",
    "Initial Successful Recharges",
    "Initial Declines",
    "Attempt 1",
    "Attempt 2",
    "Attempt 3+",
    "Total Attempts",
    "Day 1",
    "Day 2",
    "Day 3+",
    "Total Recovered",
    "Unrecovered",
]

# ── Helpers ────────────────────────────────────────────────────────────────────


def open_cdl_page(browser):
    open_admin_path(browser, "/reports/detailed/cc_declines")
    page = CardDeclinesPage(browser)
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

    TODO: Week-start convention unresolved — verify Sunday vs Monday via
    DevTools and update the 'This week' / 'Last week' branches accordingly.
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
def cdl_modal(browser):
    """Phase 1 — filter modal open with All Sites default; no filters applied."""
    return open_cdl_page(browser)


@pytest.fixture
def cdl_page(browser):
    """Phase 2 — CDL_SITE + Last month applied; lands on the metrics screen."""
    page = open_cdl_page(browser)
    page.select_site(CDL_SITE)
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
def cdl_zero_data(browser):
    """Metrics screen filtered to a date range expected to have minimal/zero records.

    The CDL date range input is readonly — direct keyboard entry is not
    supported (enter_date_range raises NotImplementedError).  As a workaround
    we use 'Yesterday' preset: on a test environment with no recent activity
    this reliably returns an empty dataset.
    TODO: Implement calendar-picker interaction to set an exact zero-data range
    (01/01/2022–01/31/2022) once DevTools inspection confirms the calendar DOM.
    """
    page = open_cdl_page(browser)
    page.select_site(CDL_SITE)
    page.select_date_preset("Yesterday")
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(1.0)
    page.apply_modal_filters()
    return page


@pytest.fixture
def cdl_single_day(browser):
    """Filter modal open with Single day checkbox checked and site selected.

    Returned in Phase 1 (modal not yet applied) so tests can inspect date-field
    behaviour without navigating to the metrics screen.
    """
    page = open_cdl_page(browser)
    page.select_site(CDL_SITE)
    page.check_modal_single_day()
    time.sleep(0.5)
    return page


# ── SingleDaySyncMixin fixture aliases (sdm_* names) ─────────────────────────
# These satisfy the fixture names expected by SingleDaySyncMixin in mixins.py.

@pytest.fixture
def sdm_modal(browser):
    return open_cdl_page(browser)


@pytest.fixture
def sdm_single_day(browser):
    page = open_cdl_page(browser)
    page.select_site(CDL_SITE)
    page.check_modal_single_day()
    time.sleep(0.5)
    return page


@pytest.fixture
def sdm_page(browser):
    page = open_cdl_page(browser)
    page.select_site(CDL_SITE)
    page.select_date_preset("Last month")
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    return page
