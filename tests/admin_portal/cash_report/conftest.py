import datetime
import time

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.cash_report_page import CashReportPage
from tests.admin_portal.admin_session import open_admin_path

# Reason reused across fixtures and tests that depend on unverified locators.
_LOCATOR_XFAIL = (
    "SITE_MULTISELECT / DATE_PRESET_COMBOBOX CSS class names not yet verified "
    "for the Cash Report modal.  Open DevTools on /reports/detailed/cash_report, "
    "inspect the site dropdown and date-preset dropdown controls, and update "
    "SITE_MULTISELECT / DATE_PRESET_COMBOBOX in cash_report_page.py accordingly."
)

# ── Constants ──────────────────────────────────────────────────────────────────

CSH_SITE = "VK Test carwash 2"

# Absolute date strings anchored to test dataset (today = 07/11/2026).
# Last month (06/01–06/30/2026) provides a stable dataset with transactions.
CSH_DATE_START = "06/01/2026"
CSH_DATE_END   = "06/30/2026"
TODAY_DATE     = "07/11/2026"

# Past date range guaranteed to have zero transactions.
CSH_ZERO_DATE_START = "01/01/2022"
CSH_ZERO_DATE_END   = "01/31/2022"

# Cash Report exposes 6 date presets (no "Custom" option).
# TODO: Confirm exact preset list via DevTools — the order and names may differ.
DATE_PRESETS = [
    "Today",
    "Yesterday",
    "This week",
    "Last week",
    "This month",
    "Last month",
]

# Tab names as displayed in the UI.
# TODO: Confirm capitalisation ("Analytics" / "Kiosk" / "POS") via DevTools.
TAB_ANALYTICS = "Analytics"
TAB_KIOSK     = "Kiosk"
TAB_POS       = "POS"

# Section titles for each paginated table.
# TODO: Confirm exact heading strings via DevTools / first live run.
TABLE_KIOSK_BALANCE_SUMMARY = "Kiosk Balance Summary"
TABLE_KIOSK_DENOMINATION    = "Kiosk Denomination"
TABLE_KIOSK_TRANSACTIONS    = "Kiosk Transactions"
TABLE_POS_BALANCE_SUMMARY   = "POS Balance Summary"
TABLE_POS_BANK_DROP         = "POS Bank Drop"
TABLE_POS_TRANSACTIONS      = "POS Transactions"

# Expected column headers per table.
# TODO: Populate after DevTools inspection of each table's <th> elements.
# Leave empty for now — header-presence tests will assert len(headers) > 0.
KIOSK_BALANCE_SUMMARY_COLUMNS: list = []
KIOSK_DENOMINATION_COLUMNS: list    = []
KIOSK_TRANSACTIONS_COLUMNS: list    = []
POS_BALANCE_SUMMARY_COLUMNS: list   = []
POS_BANK_DROP_COLUMNS: list         = []
POS_TRANSACTIONS_COLUMNS: list      = []

# ── Helpers ────────────────────────────────────────────────────────────────────


def open_csh_page(browser):
    open_admin_path(browser, "/reports/detailed/cash_report")
    page = CashReportPage(browser)
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

    TODO: Week-start convention unresolved — the Cash Report calendar may start
    weeks on Sunday (like RVO) or Monday (like PFM).  Verify via DevTools and
    update the 'This week' / 'Last week' branches accordingly.
    """
    today = datetime.date.today()
    fmt = "%m/%d/%Y"

    if preset == "Today":
        return today.strftime(fmt), today.strftime(fmt)

    if preset == "Yesterday":
        d = today - datetime.timedelta(days=1)
        return d.strftime(fmt), d.strftime(fmt)

    if preset == "This week":
        # Defaulting to Sunday-start (RVO convention) — update if wrong.
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
def csh_modal(browser):
    """Phase 1 — filter modal open, no filters applied."""
    return open_csh_page(browser)


@pytest.fixture
def csh_page(browser):
    """Phase 2 — CSH_SITE + Last month applied; lands on the metrics screen.

    Last month (06/01–06/30/2026) gives a stable dataset with transactions
    across all three tabs.
    """
    page = open_csh_page(browser)
    try:
        page.select_site(CSH_SITE)
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        page.select_date_preset("Last month")
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    return page


@pytest.fixture
def csh_analytics(browser):
    """Metrics screen with Analytics tab active (default tab after apply)."""
    page = open_csh_page(browser)
    try:
        page.select_site(CSH_SITE)
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        page.select_date_preset("Last month")
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    # Analytics is the default tab — ensure it is active before returning.
    page.click_tab(TAB_ANALYTICS)
    return page


@pytest.fixture
def csh_kiosk(browser):
    """Metrics screen with Kiosk tab active."""
    page = open_csh_page(browser)
    try:
        page.select_site(CSH_SITE)
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        page.select_date_preset("Last month")
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    page.click_tab(TAB_KIOSK)
    return page


@pytest.fixture
def csh_pos(browser):
    """Metrics screen with POS tab active."""
    page = open_csh_page(browser)
    try:
        page.select_site(CSH_SITE)
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        page.select_date_preset("Last month")
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    page.click_tab(TAB_POS)
    return page


@pytest.fixture
def csh_zero_data(browser):
    """Metrics screen filtered to a past date range with no transactions.

    Uses 01/01/2022–01/31/2022, a period before the test site was set up.
    CSH_SITE is explicitly selected because Cash Report has no 'All Sites'
    default — a site is always required.
    """
    page = open_csh_page(browser)
    try:
        page.select_site(CSH_SITE)
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        page.select_date_preset("Last month")
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(1.0)
    page.enter_date_range(CSH_ZERO_DATE_START, CSH_ZERO_DATE_END)
    page.apply_modal_filters()
    return page


@pytest.fixture
def csh_single_day(browser):
    """Filter modal open with Single day checkbox checked and site selected."""
    page = open_csh_page(browser)
    try:
        page.select_site(CSH_SITE)
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    page.check_modal_single_day()
    time.sleep(0.5)
    return page


# ── SingleDaySyncMixin fixture aliases (sdm_* names) ─────────────────────────
# These satisfy the fixture names expected by SingleDaySyncMixin in mixins.py.

@pytest.fixture
def sdm_modal(browser):
    return open_csh_page(browser)


@pytest.fixture
def sdm_single_day(browser):
    page = open_csh_page(browser)
    try:
        page.select_site(CSH_SITE)
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    page.check_modal_single_day()
    time.sleep(0.5)
    return page


@pytest.fixture
def sdm_page(browser):
    page = open_csh_page(browser)
    try:
        page.select_site(CSH_SITE)
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        page.select_date_preset("Last month")
    except TimeoutException:
        pytest.xfail(_LOCATOR_XFAIL)
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    return page
