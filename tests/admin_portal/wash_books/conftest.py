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
    wash_books_page.clear_all_filters()

    return wash_books_page


def create_wash_book_if_missing(browser, wash_book_name=WASH_BOOK_NAME):
    from selenium.common.exceptions import TimeoutException

    wash_books_page = open_wash_books_page(browser)

    if wash_books_page.wash_book_exists(wash_book_name):
        wash_books_page = open_wash_books_page(browser)
        wash_books_page.open_edit_wash_book(wash_book_name)
        wash_books_page.ensure_active_switch_on()
        wash_books_page.ensure_customer_portal_switch_on()
        wash_books_page.click_save_wash_book()
        wash_books_page.wait_for_list_loaded()
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
        pass

    # Return a fresh page so the caller always starts with an empty search
    # field — avoids the JS-select/Backspace deselect race on a pre-filled input.
    return open_wash_books_page(browser)


def open_customer_wash_books_page(browser):

    open_admin_path(browser, "/services/customerWashBooks")

    page = WashBooksPage(browser)
    page.wait_for_cwb_list_loaded()

    return page


def create_customer_wash_book_if_missing(
    browser,
    wash_book_number=CWB_WASH_BOOK_NUMBER
):
    # Ensure the wash book template exists with its canonical name before
    # trying to select it in the CWB create form.
    create_wash_book_if_missing(browser)

    page = open_customer_wash_books_page(browser)

    if page.cwb_exists(wash_book_number):
        # Verify wash count matches the constant — prior CI runs may have created
        # the record with a different value, causing assertion failures downstream.
        actual = page.get_cwb_number_of_washes_from_row(wash_book_number)
        if actual == str(CWB_NUMBER_OF_WASHES):
            return page
        # Wrong count — update the record so tests see the expected value.
        page.open_edit_cwb(wash_book_number)
        page.set_cwb_number_of_washes(CWB_NUMBER_OF_WASHES)
        page.click_save_cwb()
        page.wait_for_cwb_list_loaded()
        page.search_cwb(wash_book_number)
        return page

    page.create_customer_wash_book(
        WASH_BOOK_NAME,
        wash_book_number,
        CWB_NUMBER_OF_WASHES
    )
    page.search_cwb(wash_book_number)
    page.wait_for_cwb_row(wash_book_number)

    return page


MANAGED_WASH_BOOK = managed_name("Wash Book")


def _reset_managed_wash_book(browser):
    page = open_wash_books_page(browser)
    if page.wash_book_exists(MANAGED_WASH_BOOK):
        page = open_wash_books_page(browser)
        page.open_edit_wash_book(MANAGED_WASH_BOOK)
        page.fill_wash_book_form(
            MANAGED_WASH_BOOK,
            NUMBER_OF_WASHES,
            POINTS_AWARDED,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION,
        )
        page.click_save_wash_book()
        return open_wash_books_page(browser)
    page.create_wash_book(
        MANAGED_WASH_BOOK,
        NUMBER_OF_WASHES,
        POINTS_AWARDED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
    )
    return open_wash_books_page(browser)


managed_wash_book = managed_resource(_reset_managed_wash_book)
