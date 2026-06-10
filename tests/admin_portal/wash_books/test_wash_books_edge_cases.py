from tests.admin_portal.wash_books.conftest import WASH_BOOK_NAME
from tests.admin_portal.wash_books.conftest import create_wash_book_if_missing


def test_wash_book_create_is_idempotent(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.wait_for_list_loaded()
    wash_books_page.search_wash_book(WASH_BOOK_NAME)

    assert wash_books_page.wait_for_wash_book_row(WASH_BOOK_NAME).is_displayed()


def test_wash_book_redemption_settings_persist(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.open_edit_wash_book(WASH_BOOK_NAME)
    wash_books_page.open_redemption_settings()
    body_text = wash_books_page.get_body_text().lower()

    assert "vk detail wash" in body_text
    assert "detail cleaning" in body_text


def test_wash_book_long_description_does_not_break_form(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.open_edit_wash_book(WASH_BOOK_NAME)
    wash_books_page.set_wash_book_description("Long description " + ("A" * 256))

    assert wash_books_page.get_wash_book_description_value().startswith(
        "Long description "
    )
