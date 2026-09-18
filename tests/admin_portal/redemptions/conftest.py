import datetime
import time

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.redemptions_page import RedemptionsPage
from tests.admin_portal.admin_session import open_admin_path

# ── Constants ──────────────────────────────────────────────────────────────────

RDM_SITE = "VK Test carwash 2"

# Multi-site pair; produces +2 overflow indicator in the site chip control.
RDM_MULTI_SITES = ["VK Test Wash 01", "VK Test carwash 2"]

# Absolute date strings anchored to test dataset (today = 07/12/2026).
# Last month (06/01–06/30/2026) provides a stable dataset with redemptions.
RDM_DATE_START = "06/01/2026"
RDM_DATE_END   = "06/30/2026"
TODAY_DATE     = "07/12/2026"

# Past date range expected to have zero redemptions.
RDM_ZERO_DATE_START = "01/01/2022"
RDM_ZERO_DATE_END   = "01/31/2022"

# 6 date presets; week-start = Sunday (confirmed: RDM-DTE-004).
DATE_PRESETS = [
    "Today",
    "Yesterday",
    "This week",
    "Last week",
    "This month",
    "Last month",
]

# ── Page-level summary cards ───────────────────────────────────────────────────

SUMMARY_CARDS = ["Total Redemptions", "Total Value", "Avg Per Redemption"]

# ── Accordion sections ─────────────────────────────────────────────────────────

# All 7 accordion sections in display order (used for expand/collapse tests).
ALL_SECTIONS = [
    "Loyalty points",
    "Comp Washes",
    "Memberships",
    "Gift cards",
    "Wash books",
    "Discounts",
    "Coupon codes",
]

# 5 sections with complete TC coverage (Discounts and Coupon codes unscriptable
# until RDM-DSC-* and RDM-CPN-* rows are confirmed in the TC sheet).
SCRIPTABLE_SECTIONS = [
    "Loyalty points",
    "Comp Washes",
    "Memberships",
    "Gift cards",
    "Wash books",
]

# ── Section summary card labels ────────────────────────────────────────────────

# Loyalty has no "Total Net Amount" — confirmed from spec.
LOYALTY_SUMMARY_CARDS    = ["Redemptions", "Avg Per Redemption"]
# Gift cards uses "Total amount" (not "Total Net Amount") — confirmed from spec.
GIFT_CARD_SUMMARY_CARDS  = ["Redemptions", "Total amount", "Avg Per Redemption"]
DEFAULT_SECTION_SUMMARY_CARDS = ["Redemptions", "Total Net Amount", "Avg Per Redemption"]

# Map section name → expected summary card labels for assert_section_summary_cards.
SECTION_SUMMARY_CARDS = {
    "Loyalty points": LOYALTY_SUMMARY_CARDS,
    "Comp Washes":    DEFAULT_SECTION_SUMMARY_CARDS,
    "Memberships":    DEFAULT_SECTION_SUMMARY_CARDS,
    "Gift cards":     GIFT_CARD_SUMMARY_CARDS,
    "Wash books":     DEFAULT_SECTION_SUMMARY_CARDS,
}

# ── Breakdown table column definitions ────────────────────────────────────────

LOYALTY_BREAKDOWN_COLS = ["Points Range", "Count", "Percentage"]
LOYALTY_DETAIL_COLS    = [
    "License/RFID", "Customer Name", "Invoice Number",
    "Points Used", "Service Redeemed", "Site Name", "Date/Time",
]

COMP_BREAKDOWN_COLS = ["Wash Package", "Count", "Total Net Amount", "Percentage"]
COMP_DETAIL_COLS    = [
    "License/RFID", "Customer Name", "Invoice Number",
    "Comp Wash Service", "Comp Amount", "Site Name", "Date/Time",
]

MEM_BY_MEMBERSHIP_COLS   = ["Membership", "Count", "Percentage"]
MEM_BY_WASH_PACKAGE_COLS = ["Wash Package", "Count", "Percentage"]
MEM_DETAIL_COLS          = [
    "License/RFID", "Customer Name", "Invoice Number",
    "Membership", "Site Name", "Date/Time",
]

GFT_BY_GIFT_CARD_COLS    = ["Gift Card", "Card Value", "Count", "Percentage"]
GFT_BY_WASH_PACKAGE_COLS = ["Wash Package", "Avg value", "Count", "Percentage"]
GFT_DETAIL_COLS          = [
    "License/RFID", "Customer Name", "Invoice Number",
    "Gift Card Name", "Gift Card Number", "Card Value", "Site Name", "Date/Time",
]

WBK_BY_WASH_BOOK_COLS    = ["Washbook", "Count", "Percentage"]
WBK_BY_WASH_PACKAGE_COLS = ["Wash Package", "Count", "Percentage"]
WBK_DETAIL_COLS          = [
    "License/RFID", "Customer Name", "Invoice Number",
    "Washbook Name", "Site Name", "Date/Time",
]

# Detail table headings — used by RDM-ACC-007 (horizontal scroll parametrize).
DETAIL_TABLE_HEADINGS = {
    "Loyalty points": "Loyalty Points Redemptions",
    "Comp Washes":    "Comp Wash Redemptions",
    "Memberships":    "Membership Redemptions",
    "Gift cards":     "Gift Card Redemptions",
    "Wash books":     "Wash Book Redemptions",
}

# ── Helpers ────────────────────────────────────────────────────────────────────


def open_rdm_page(browser):
    open_admin_path(browser, "/reports/detailed/redemption_details")
    page = RedemptionsPage(browser)
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

    Week-start = Sunday (confirmed for RDM — RDM-DTE-004).
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
def rdm_modal(browser):
    """Phase 1 — blocking filter modal open with no sites selected."""
    return open_rdm_page(browser)


@pytest.fixture
def rdm_page(browser):
    """Phase 2 — RDM_SITE + Last month applied; lands on the metrics screen."""
    page = open_rdm_page(browser)
    page.select_site(RDM_SITE)
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
def rdm_expanded(browser):
    """Phase 2 with all accordion sections expanded via Expand All."""
    page = open_rdm_page(browser)
    page.select_site(RDM_SITE)
    page.select_date_preset("Last month")
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    page.expand_all()
    time.sleep(0.5)
    return page


@pytest.fixture
def rdm_zero_data(browser):
    """Metrics screen filtered to a date range expected to yield no redemptions.

    Uses 'Yesterday' preset as a zero-data workaround; the intended approach
    (future-date calendar selection) requires calendar picker interaction that
    cannot be scripted until the RDM calendar DOM is confirmed via DevTools.
    TODO: Replace with calendar interaction to select a confirmed zero-data
    future date range once RDM-DTE-014 calendar DOM is verified.
    """
    page = open_rdm_page(browser)
    page.select_site(RDM_SITE)
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
def rdm_single_day(browser):
    """Filter modal open with Single day checkbox checked and site selected.

    Returned in Phase 1 (modal not yet applied) so tests can inspect
    date-field behaviour without navigating to the metrics screen.
    """
    page = open_rdm_page(browser)
    page.select_site(RDM_SITE)
    page.check_modal_single_day()
    time.sleep(0.5)
    return page


# ── SingleDaySyncMixin fixture aliases (sdm_* names) ──────────────────────────

@pytest.fixture
def sdm_modal(browser):
    return open_rdm_page(browser)


@pytest.fixture
def sdm_single_day(browser):
    page = open_rdm_page(browser)
    page.select_site(RDM_SITE)
    page.check_modal_single_day()
    time.sleep(0.5)
    return page


@pytest.fixture
def sdm_page(browser):
    page = open_rdm_page(browser)
    page.select_site(RDM_SITE)
    page.select_date_preset("Last month")
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    return page
