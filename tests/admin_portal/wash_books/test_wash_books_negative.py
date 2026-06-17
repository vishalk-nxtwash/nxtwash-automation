from tests.admin_portal.wash_books.conftest import MISSING_WASH_BOOK
from tests.admin_portal.wash_books.conftest import open_wash_books_page
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


def test_missing_wash_book_is_not_returned(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book(MISSING_WASH_BOOK)

    assert MISSING_WASH_BOOK not in wash_books_page.get_body_text()
    assert page_has_no_broken_state(wash_books_page)


def test_wash_books_special_character_search_stays_usable(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book("%%%___###")

    assert page_has_no_broken_state(wash_books_page)
    assert wash_books_page.driver.find_element(
        *wash_books_page.SEARCH_INPUT
    ).is_displayed()
