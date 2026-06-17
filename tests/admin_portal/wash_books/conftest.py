from pages.admin_portal.wash_books_page import WashBooksPage
from tests.admin_portal.admin_session import open_admin_path


EXISTING_WASH_BOOK = "Basic washbook"
MISSING_WASH_BOOK = "wash-book-does-not-exist-automation"
WASH_BOOK_NAME = "VK AWB2"
NUMBER_OF_WASHES = "15"
POINTS_AWARDED = "5"
GLOBAL_PRICE = "55"
GLOBAL_COMMISSION = "5"
VISIBLE_PRICE = "$55.00"
WASH_BOOK_DESCRIPTION = "Test washbook created using automation"


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

    wash_books_page = open_wash_books_page(browser)

    if wash_books_page.wash_book_exists(wash_book_name):
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

    wash_books_page.create_wash_book(
        wash_book_name,
        NUMBER_OF_WASHES,
        POINTS_AWARDED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION
    )
    wash_books_page.search_wash_book(wash_book_name)
    wash_books_page.wait_for_wash_book_row(wash_book_name)

    return wash_books_page
