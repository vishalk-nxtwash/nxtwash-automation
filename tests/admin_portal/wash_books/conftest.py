from pages.admin_portal.wash_books_page import WashBooksPage
from tests.admin_portal.admin_session import open_admin_path


EXISTING_WASH_BOOK = "Basic washbook"
MISSING_WASH_BOOK = "wash-book-does-not-exist-automation"
WASH_BOOK_NAME = "VK AWB2"
INACTIVE_WASH_BOOK_NAME = "VK AWB2-I"
NUMBER_OF_WASHES = "15"
POINTS_AWARDED = "5"
GLOBAL_PRICE = "55"
GLOBAL_COMMISSION = "5"
VISIBLE_PRICE = "$55.00"
WASH_BOOK_DESCRIPTION = "Test washbook created using automation"
ASSIGNMENT_SITE = "VK AL11"
BARCODE_VALUE = "VK-WB-BAR-001"

CWB_WASH_BOOK_NUMBER = "AWB-AUTO-001"
CWB_UPDATED_WASH_BOOK_NUMBER = "AWB-AUTO-001-U"
CWB_NUMBER_OF_WASHES = "15"
CWB_UPDATED_NUMBER_OF_WASHES = "8"

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

    return wash_books_page


def create_wash_book_if_missing(browser, wash_book_name=WASH_BOOK_NAME):
    from selenium.common.exceptions import TimeoutException

    wash_books_page = open_wash_books_page(browser)

    if wash_books_page.wash_book_exists(wash_book_name):
        # wash_book_exists() leaves the browser in a filtered-list state with
        # the search field already populated.  open_edit_wash_book() calls
        # wait_for_list_loaded() (frame switch) then search_wash_book() again;
        # clearing a React-controlled input that already has content via
        # send_keys is unreliable in headless Chrome.  A fresh navigation
        # guarantees an empty search field for the second search.
        wash_books_page = open_wash_books_page(browser)
        wash_books_page.open_edit_wash_book(wash_book_name)
        wash_books_page.fill_wash_book_form(
            wash_book_name,
            NUMBER_OF_WASHES,
            POINTS_AWARDED,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION
        )
        wash_books_page.click_save_wash_book()
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

    wash_books_page.search_wash_book(wash_book_name)
    wash_books_page.wait_for_wash_book_row(wash_book_name)

    return wash_books_page


def open_customer_wash_books_page(browser):

    open_admin_path(browser, "/services/customerWashBooks")

    page = WashBooksPage(browser)
    page.wait_for_cwb_list_loaded()

    return page


def create_customer_wash_book_if_missing(
    browser,
    wash_book_number=CWB_WASH_BOOK_NUMBER
):

    page = open_customer_wash_books_page(browser)

    if page.cwb_exists(wash_book_number):
        return page

    page.create_customer_wash_book(
        WASH_BOOK_NAME,
        wash_book_number,
        CWB_NUMBER_OF_WASHES
    )
    page.search_cwb(wash_book_number)
    page.wait_for_cwb_row(wash_book_number)

    return page
