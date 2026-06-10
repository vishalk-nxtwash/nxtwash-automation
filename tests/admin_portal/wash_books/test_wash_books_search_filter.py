from tests.admin_portal.wash_books.conftest import EXISTING_WASH_BOOK
from tests.admin_portal.wash_books.conftest import MISSING_WASH_BOOK
from tests.admin_portal.wash_books.conftest import open_wash_books_page
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


def test_wash_books_existing_search(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book(EXISTING_WASH_BOOK)

    assert wash_books_page.wait_for_wash_book_row(EXISTING_WASH_BOOK).is_displayed()


def test_wash_books_missing_search(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book(MISSING_WASH_BOOK)

    assert MISSING_WASH_BOOK not in wash_books_page.get_body_text()
    assert page_has_no_broken_state(wash_books_page)


def test_wash_books_filter_panel_shows_controls(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.open_filter_panel()
    body_text = wash_books_page.get_body_text()

    assert "Select site" in body_text
    assert "Apply filters" in body_text
    assert "Reset all" in body_text


def test_wash_books_search_payloads_do_not_break_grid(browser):

    wash_books_page = open_wash_books_page(browser)

    for payload in ("' OR 1=1 --", "<script>alert(1)</script>"):
        wash_books_page.search_wash_book(payload)
        assert page_has_no_broken_state(wash_books_page)
