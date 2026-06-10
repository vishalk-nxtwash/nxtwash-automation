from tests.admin_portal.wash_books.conftest import WASH_BOOK_DESCRIPTION
from tests.admin_portal.wash_books.conftest import WASH_BOOK_NAME
from tests.admin_portal.wash_books.conftest import create_wash_book_if_missing


def test_edit_wash_book_description(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.update_wash_book_description(
        WASH_BOOK_NAME,
        WASH_BOOK_DESCRIPTION
    )
    wash_books_page.open_edit_wash_book(WASH_BOOK_NAME)

    assert wash_books_page.get_wash_book_description_value() == WASH_BOOK_DESCRIPTION
