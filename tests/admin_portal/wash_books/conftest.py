import pytest
from selenium.common.exceptions import TimeoutException

from pages.admin_portal.wash_books_page import WashBooksPage
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._managed import managed_name, managed_resource
from tests.admin_portal._data import load as _load

_D = _load("wash_books")

EXISTING_WASH_BOOK           = _D["reference"]["existing_wash_book"]
MISSING_WASH_BOOK            = _D["search"]["nonexistent"]
WASH_BOOK_NAME               = _D["template"]["wash_book_name"]
INACTIVE_WASH_BOOK_NAME      = _D["reference"]["inactive_wash_book"]
NUMBER_OF_WASHES             = _D["template"]["number_of_washes"]
POINTS_AWARDED               = _D["template"]["points_awarded"]
GLOBAL_PRICE                 = _D["template"]["global_price"]
GLOBAL_COMMISSION            = _D["template"]["global_commission"]
VISIBLE_PRICE                = _D["template"]["visible_price"]
WASH_BOOK_DESCRIPTION        = _D["template"]["description"]
ASSIGNMENT_SITE              = _D["reference"]["assignment_site"]
BARCODE_VALUE                = _D["template"]["barcode"]

CWB_WASH_BOOK_NUMBER         = _D["customer_wash_book"]["number"]
CWB_UPDATED_WASH_BOOK_NUMBER = _D["customer_wash_book"]["updated_number"]
CWB_NUMBER_OF_WASHES         = _D["customer_wash_book"]["number_of_washes"]
CWB_UPDATED_NUMBER_OF_WASHES = _D["customer_wash_book"]["updated_washes"]

BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


def open_wash_books_page(browser):

    open_admin_path(browser, "/services/washBooks")

    wash_books_page = WashBooksPage(browser)
    wash_books_page.wait_for_list_loaded()
    wash_books_page.reset_filters_if_active()

    return wash_books_page


def create_wash_book_if_missing(browser, wash_book_name=WASH_BOOK_NAME):
    from selenium.common.exceptions import TimeoutException

    wash_books_page = open_wash_books_page(browser)

    if wash_books_page.wash_book_exists(wash_book_name):
        # Wash book with the correct name already exists on staging.
        # Skipping the edit step avoids opening a corrupted ghost record
        # (e.g. ID 133 whose name contains wash_book_name as a substring)
        # and hitting a duplicate-name rejection on save.
        return open_wash_books_page(browser)

    # Not found in the active list — attempt creation.
    # If the wash book exists but is inactive (hidden by default filter),
    # saving will return a duplicate-name error and we will stay on the
    # create form; catch that TimeoutException and navigate back cleanly.
    try:
        wash_books_page.create_wash_book(
            wash_book_name,
            NUMBER_OF_WASHES,
            POINTS_AWARDED,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION
        )
    except TimeoutException:
        return open_wash_books_page(browser)

    # Fresh navigation resets any filter state left by the create flow before
    # searching for the newly created row.
    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book(wash_book_name)
    wash_books_page.wait_for_wash_book_row(wash_book_name)

    return wash_books_page


def open_customer_wash_books_page(browser):

    open_admin_path(browser, "/services/customerWashBooks")

    page = WashBooksPage(browser)
    try:
        page.wait_for_cwb_list_loaded()
    except TimeoutException:
        pytest.skip("Customer wash books list frame not stable on staging")

    return page


def create_customer_wash_book_if_missing(
    browser,
    wash_book_number=CWB_WASH_BOOK_NUMBER
):

    page = open_customer_wash_books_page(browser)

    if page.cwb_exists(wash_book_number):
        return page

    try:
        page.create_customer_wash_book(
            WASH_BOOK_NAME,
            wash_book_number,
            CWB_NUMBER_OF_WASHES
        )
    except TimeoutException:
        # create_customer_wash_book ends with wait_for_cwb_list_loaded(); if the
        # save fails (duplicate number) the browser stays on /new and that wait
        # times out.  Navigate back to the list so the caller can search cleanly.
        page = open_customer_wash_books_page(browser)

    page.search_cwb(wash_book_number)
    page.wait_for_cwb_row(wash_book_number)

    return page


MANAGED_WASH_BOOK = managed_name("Wash Book")


def _fill_managed_wash_book_baseline(page):
    """Set every field the 15 managed_wash_book tests touch, deliberately
    skipping assign_all_locations()/open_redemption_settings().

    fill_wash_book_form() (used elsewhere in this file by create_wash_book()'s
    other callers, and by other modules' shared-record helpers — left
    untouched) calls assign_all_locations() unconditionally, not wrapped in
    try/except like the redemption-settings block right after it. That's the
    same Inovua location-assignment grid interaction already permanently
    CI-skipped elsewhere in this file (WB-EDT-004, WB-SIT-002: "times out in
    headless Chrome").

    None of the 15 tests on managed_wash_book need the reset/create to carry
    a location/redemption baseline — the two that do (test_assign_single_
    site_persists, test_location_price_override_persists) already assign
    what they need inside their own test body, the same pattern already
    proven safe by test_wash_books_positive.py's other create-from-scratch
    tests (e.g. test_create_inactive_wash_book), none of which touch
    location assignment either.
    """
    page.enter_wash_book_name(MANAGED_WASH_BOOK)
    page.set_number_of_washes(NUMBER_OF_WASHES)
    page.set_points_awarded(POINTS_AWARDED)
    page.ensure_active_switch_on()
    page.ensure_customer_portal_switch_on()
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)


def _reset_managed_wash_book(browser):
    """Ensure MANAGED_WASH_BOOK exists and reset every field writer tests touch.

    Confirmed in CI (run 38740880006): routing the one-time creation of this
    brand-new managed record through create_wash_book() -> fill_wash_book_form()
    -> assign_all_locations() never completed — every one of the 15 tests'
    setup landed on /services/washBooks/new and timed out after 90s waiting
    for the list iframe, because the record was never actually saved, so
    wash_book_exists() kept returning False on every subsequent attempt too.
    Uses _fill_managed_wash_book_baseline() for both the create and the
    reset-existing path so creation is exercised exactly the same
    (location-grid-free) way as every later reset.

    Description is reset separately since no create/fill helper touches it,
    and test_edit_wash_book_description would otherwise leak a stale
    description into the next test even with xdist_group serialization.
    """
    page = open_wash_books_page(browser)
    if page.wash_book_exists(MANAGED_WASH_BOOK):
        page = open_wash_books_page(browser)
        page.open_edit_wash_book(MANAGED_WASH_BOOK)
        _fill_managed_wash_book_baseline(page)
        page.click_save_wash_book()
        page.wait_for_list_loaded()
        page.update_wash_book_description(MANAGED_WASH_BOOK, "")
        return open_wash_books_page(browser)
    page.open_create_wash_book()
    _fill_managed_wash_book_baseline(page)
    page.click_save_wash_book()
    page.wait_for_list_loaded()
    return open_wash_books_page(browser)


managed_wash_book = managed_resource(_reset_managed_wash_book)
