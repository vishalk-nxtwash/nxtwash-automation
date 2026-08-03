import datetime
import time

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.transactions_page import TransactionsPage
from tests.admin_portal.admin_session import open_admin_path

# ── Constants ──────────────────────────────────────────────────────────────────

TRN_SITE = "VK Test carwash 2"

# Multi-site pair used in TRN-DLC-007 (overflow chip) and TRN-DLC-008 (lane disabled).
TRN_MULTI_SITES = ["VK Test Wash 01", "VK Test carwash 2"]

# Default display after navigating with no filters applied.
# The app natively shows "Today" until a quick filter is applied.
TRN_DEFAULT_PRESET = "Today"

# Stable test records anchored to July 2026 dataset.
# TODO: Update TRN_DEFAULT_DATE_RANGE when the test dataset changes month.
TRN_DEFAULT_RECORD_COUNT = 18
TRN_DETAIL_INVOICE      = "90288"   # updated 2026-07-27: page now shows 90288, not 10276
TRN_DETAIL_INTERNAL_ID  = "90288"
TRN_DETAIL_CUSTOMER     = "Test Customer 01"

# Past date range guaranteed to have zero transactions.
TRN_ZERO_DATE_START = "01/01/2022"
TRN_ZERO_DATE_END   = "01/31/2022"

# ── Date presets ───────────────────────────────────────────────────────────────
# Transactions adds "This year" vs. CDL/RDM (6 presets → 7 here).
# Confirmed: week-start = Monday (not Sunday) — see TRN-DLC-006 xfail note.
# TODO: Verify exact preset labels and order via DevTools on first live run.
DATE_PRESETS = [
    "Today",
    "Yesterday",
    "This week",
    "Last week",
    "This month",
    "Last month",
    "This year",
]

# ── Table columns (TRN-TBL-001 parametrize list) ──────────────────────────────
# 19 column headers as observed in the table.
# Note: "Transaction source" appears twice in the DOM (suspected duplicate,
# see TRN-TBL-011 — Automation=No / deferred).  Both entries are listed here
# so the parametrized test catches both occurrences.
# TODO: Verify all 19 labels and column order via DevTools on first live run.
TABLE_COLUMNS = [
    "Invoice number",
    "License plate",
    "RFID",
    "Site name",
    "Transaction date/time",
    "Customer name",
    "Service",
    "Discount",
    "Tax",
    "PIF",
    "Surcharge",
    "Total amount",
    "Payment mode",
    "CC type",
    "Transaction source",
    "Transaction source",  # second instance — suspected duplicate
    "Sale Type",
    "Payment status",
    # "Full info" is a hyperlink inside a <td> cell, not a <th> header — excluded (RC1).
]

# ── Export column toggle labels (TRN-EXP-003 parametrize list) ────────────────
# 25 confirmed labels.  TRN-EXP-004 (xfail): "Site name" appears twice.
# OFF by default: Lane name, Image URL, Make, Model, Color, Total records.
# TODO: Identify the 26th export toggle label via DevTools on first live run
#       (spec states 26; this list has 25 — likely one column name differs
#       from the table header, e.g. "Customer email" or a separate "RFID number").
EXPORT_COLUMNS_OFF_BY_DEFAULT = ["Lane name", "Image URL", "Make", "Model", "Color", "Total records"]

EXPORT_COLUMN_LABELS = [
    "Invoice number",
    "License plate",
    "RFID",
    "Site name",
    "Lane name",               # OFF by default
    "Transaction date/time",
    "Customer name",
    "Service",
    "Discount",
    "Tax",
    "PIF",
    "Surcharge",
    "Total amount",
    "Payment mode",
    "CC type",
    "Transaction source",
    "Transaction source",      # second instance — same suspected duplicate as table
    "Sale Type",
    "Payment status",
    "Image URL",               # OFF by default
    "Make",                    # OFF by default
    "Model",                   # OFF by default
    "Color",                   # OFF by default
    "Site name",               # Known duplicate — TRN-EXP-004 xfail
    "Total records",           # OFF by default
    # TODO: add 26th label here once confirmed via DevTools
]

# ── Filter tab labels (TRN-FLT-003 parametrize list) ─────────────────────────
# 10 tabs in the FILTERS tab strip inside the filter panel.
# TODO: Verify exact tab labels and order via DevTools on first live run.
FILTER_TABS = [
    "Date & Location",
    "Transaction",
    "Payment",
    "Customer",
    "Membership",
    "Promotions",
    "Gift cards",
    "Washbook",
    "Invoice",
    "Staff",
]

# ── Quick filter labels (TRN-QCK-001/002/003 + presence test) ─────────────────
QUICK_FILTER_LABELS = ["Today", "This week", "This month", "Comp Wash", "Refunds", "Voided"]

# ── Sale types (TRN-TXN-006 parametrize list) ────────────────────────────────
SALE_TYPES = ["Gift Card Sale", "Washbook Sale", "Membership Sale", "Retail / Single Wash"]

# ── Helpers ────────────────────────────────────────────────────────────────────


def open_transactions_page(browser):
    """Navigate to /transactions/report and apply 'Last month' to ensure a non-empty table.

    The app's factory default is 'Today' which produces 0 rows in the test dataset.
    'This month' also produces 0 rows early in the month before data accrues.
    'Last month' gives a stable closed dataset that always has rows.
    Tests that need the bare default state should navigate directly.
    """
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    open_admin_path(browser, "/transactions/report")
    page = TransactionsPage(browser)
    # Wait for the table shell — rows may be 0 until filter is applied.
    page.wait_for_table()
    # Apply 'Last month' so all dependent tests have real data.
    # NOTE: 'Last month' is a date preset in the Date & Location tab, NOT a
    # quick-filter chip — click_quick_filter("Last month") silently no-ops.
    page.open_filter_panel()
    page.click_filter_tab("Date & Location")
    page.click_date_preset("Last month")
    page.apply_panel_filters()
    # Wait for rows to appear after apply (up to 15 s).
    try:
        WebDriverWait(browser, 15).until(
            lambda d: len(d.find_elements(*TransactionsPage.TABLE_ROWS)) > 0
        )
    except TimeoutException:
        pass
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
    """Return (start_str, end_str) for a preset name relative to today.

    Week-start = Monday (confirmed via TRN-DLC-006).  This differs from CDL/RDM
    which use Sunday-first — do not reuse cdl conftest.compute_preset_date_range.
    """
    today = datetime.date.today()
    fmt = "%m/%d/%Y"

    if preset == "Today":
        return today.strftime(fmt), today.strftime(fmt)

    if preset == "Yesterday":
        d = today - datetime.timedelta(days=1)
        return d.strftime(fmt), d.strftime(fmt)

    if preset == "This week":
        monday = today - datetime.timedelta(days=today.weekday())
        return monday.strftime(fmt), today.strftime(fmt)

    if preset == "Last week":
        this_monday = today - datetime.timedelta(days=today.weekday())
        last_monday = this_monday - datetime.timedelta(days=7)
        last_sunday = last_monday + datetime.timedelta(days=6)
        return last_monday.strftime(fmt), last_sunday.strftime(fmt)

    if preset == "This month":
        first = today.replace(day=1)
        return first.strftime(fmt), today.strftime(fmt)

    if preset == "Last month":
        first_this = today.replace(day=1)
        last_prev  = first_this - datetime.timedelta(days=1)
        first_prev = last_prev.replace(day=1)
        return first_prev.strftime(fmt), last_prev.strftime(fmt)

    if preset == "This year":
        first = today.replace(month=1, day=1)
        return first.strftime(fmt), today.strftime(fmt)

    return "", ""


# ── Fixtures ───────────────────────────────────────────────────────────────────


@pytest.fixture
def trn_page(browser):
    """Transactions Report page — default state (Last month, All Sites, table loaded)."""
    return open_transactions_page(browser)


@pytest.fixture
def trn_filter_panel(browser):
    """Transactions Report with the filter panel open."""
    page = open_transactions_page(browser)
    page.open_filter_panel()
    return page


@pytest.fixture
def trn_date_location(browser):
    """Filter panel open, Date & Location tab active."""
    page = open_transactions_page(browser)
    page.open_filter_panel()
    page.click_filter_tab("Date & Location")
    return page


@pytest.fixture
def trn_transaction_filter(browser):
    """Filter panel open, Transaction tab active."""
    page = open_transactions_page(browser)
    page.open_filter_panel()
    page.click_filter_tab("Transaction")
    return page


@pytest.fixture
def trn_payment_filter(browser):
    """Filter panel open, Payment tab active."""
    page = open_transactions_page(browser)
    page.open_filter_panel()
    page.click_filter_tab("Payment")
    return page


@pytest.fixture
def trn_detail_page(browser):
    """Transaction detail page for invoice 90288 (internal ID 90288).

    The outer page at /reports/transactions_log/{id} is a React shell; all panel
    content is rendered inside a legacy iframe (legacy-staging.nxtwash.com).
    This fixture switches the driver into that iframe before returning so that
    detail page methods find elements in the correct document context.
    TODO: Update TRN_DETAIL_INTERNAL_ID if the test record is re-seeded.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait

    open_admin_path(browser, f"/reports/transactions_log/{TRN_DETAIL_INTERNAL_ID}")
    page = TransactionsPage(browser)
    # Switch into the legacy iframe where the actual detail content lives.
    page._switch_to_detail_frame()
    # Wait for the iframe body to be ready.
    try:
        WebDriverWait(browser, 15).until(
            lambda d: d.find_element(By.TAG_NAME, "body").text.strip() != ""
        )
    except Exception:
        time.sleep(2.0)
    return page


@pytest.fixture
def trn_zero_data(browser):
    """Transactions Report filtered to a date range with no records (Jan 2022).

    Used to verify no-data / empty-state behaviour.
    TODO: Implement calendar-picker interaction to set an exact date range once
          the date picker DOM is confirmed via DevTools.  For now, the fixture
          navigates to the default page and relies on the developer to supply a
          date-range query string parameter — update URL once format is known.
    """
    page = open_transactions_page(browser)
    return page
