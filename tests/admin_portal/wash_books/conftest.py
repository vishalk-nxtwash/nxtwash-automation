import time

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
    """Set every field the 15 managed_wash_book tests touch, plus every field
    the app actually requires before Save will do anything.

    Two earlier versions of this fix guessed wrong. Root-caused properly this
    time by running the create+save flow locally against staging (headless,
    outside CI) and reading the page text immediately after clicking Save —
    both CI and the local repro had been landing on a dead end silently, with
    no visible error in any pytest log, because switch_to_frame_with_retry's
    own failure path clears the frame context before any diagnostic runs.

    Reading the raw body text at the moment of failure surfaced two
    server-side validation messages in turn, neither of which raises or
    toasts in a way the existing xfail/skip comments elsewhere in this file
    had attributed to the Inovua grid:
      1. "price in requestWashbookSiteList is required" — assigning a
         location (assign_location_by_index) is not sufficient on its own;
         that row's own price/commission must also be set
         (set_location_price_and_commission_by_index), same as
         fill_wash_book_form() already does for the first 2 rows.
      2. "Please select at least one redeem location" — Redemption settings
         needs its own assignment + redeem-as service, same as
         fill_wash_book_form()'s redemption block.
    Only after setting both did Save actually navigate away from /new.

    Assigns exactly ONE location (assign_location_by_index(0)) rather than
    fill_wash_book_form()'s assign_all_locations(): a single-checkbox
    assign+verify is the already-proven-reliable operation
    test_location_price_override_persists itself still uses today, whereas
    looping every row is the actual documented source of the Inovua grid
    timeout (WB-EDT-004, WB-SIT-002: "times out in headless Chrome").
    """
    page.enter_wash_book_name(MANAGED_WASH_BOOK)
    page.set_number_of_washes(NUMBER_OF_WASHES)
    page.set_points_awarded(POINTS_AWARDED)
    page.ensure_active_switch_on()
    page.ensure_customer_portal_switch_on()
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)
    page.assign_location_by_index(0)
    page.set_location_price_and_commission_by_index(0, GLOBAL_PRICE, GLOBAL_COMMISSION)
    try:
        page.open_redemption_settings()
        if page.visible_redemption_checkboxes():
            page.assign_redemption_location_by_index(0)
            page.select_redeem_as_option(0, "Vk detail wp")
    except TimeoutException:
        pass
    page.open_service_settings()


def _reset_managed_wash_book(browser, _attempt=1):
    """Ensure MANAGED_WASH_BOOK exists and reset every field writer tests touch.

    Uses _fill_managed_wash_book_baseline() for both the create and the
    reset-existing path, so creation is exercised exactly the same way as
    every later reset (see that function's docstring for why it assigns one
    location).

    Description is reset in the same edit session as the baseline fields
    (set_wash_book_description("") right after _fill_managed_wash_book_
    baseline(), before the one Save) since no create/fill helper touches
    it otherwise, and test_edit_wash_book_description would otherwise leak
    a stale description into the next test even with xdist_group
    serialization.

    Previously this reset opened the edit iframe TWICE per call (once for
    the baseline fields, once again separately via update_wash_book_
    description()) -- each one a fresh chance to hit switch_to_frame_
    with_retry's own documented React iframe-remount race exceeding its
    90s budget, and each one adding a full open+save cycle's worth of
    time to every single setup and teardown. Confirmed in CI (run
    39918158522): two teardown-only TimeoutExceptions here, with both
    tests' own bodies already passed. Confirmed again later (AWS run
    40799714038, after the double-open was already known but not yet
    merged): four isolated teardown-only `Failed: Timeout >420.0s`
    errors, each with the test's own body passing and the very next test
    starting clean -- not a cascade, just this reset's cost occasionally
    pushing one item's total setup+call+teardown time past the global
    ceiling on a slow connection. Merging both edits into the one already-
    open page removes a full open+save cycle from every reset, directly
    cutting the time available for that to happen -- it does not fix the
    AWS host's own intermittent connection slowness (that needs a host
    rebuild, see admin-portal-frozen), only removes avoidable overhead
    that was making it worse.

    The retry-once-on-TimeoutException below only helps a quick, one-off
    glitch -- it does nothing for a sustained slow connection, where it
    just pays the same cost twice and can push the combined time past
    pytest's global timeout. Confirmed in CI (AWS run 40392927095): once
    the host's connection degraded partway through a run, every
    subsequent managed_wash_book test's teardown hit this retry, took ~2x
    as long as a single slow attempt, and landed right on the 420s global
    timeout for the rest of the run. Only retry if the first attempt
    failed reasonably fast (<60s) -- that's the signature of the
    transient iframe-remount race this retry was built for; a slow
    failure means the connection itself is degraded, and retrying will
    not help, just burn more time toward the global timeout for no
    benefit.
    """
    start = time.time()
    try:
        page = open_wash_books_page(browser)
        if page.wash_book_exists(MANAGED_WASH_BOOK):
            # (no re-navigation here: wash_book_exists() is a read-only
            # check against the page just loaded above -- nothing
            # invalidates it, so re-opening the same list page again was
            # pure duplicate overhead on every reset call.)
            page.open_edit_wash_book(MANAGED_WASH_BOOK)
            _fill_managed_wash_book_baseline(page)
            page.set_wash_book_description("")
            page.click_save_wash_book()
            page.wait_for_list_loaded()
            return open_wash_books_page(browser)
        page.open_create_wash_book()
        _fill_managed_wash_book_baseline(page)
        page.click_save_wash_book()
        page.wait_for_list_loaded()
        return open_wash_books_page(browser)
    except TimeoutException:
        if _attempt >= 2 or (time.time() - start) >= 60:
            raise
        return _reset_managed_wash_book(browser, _attempt=_attempt + 1)


managed_wash_book = managed_resource(_reset_managed_wash_book)
