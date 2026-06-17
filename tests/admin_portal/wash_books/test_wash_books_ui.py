from tests.admin_portal.wash_books.conftest import open_wash_books_page
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


def test_wash_books_page_loads_with_primary_controls(browser):

    wash_books_page = open_wash_books_page(browser)
    body_text = wash_books_page.get_body_text()

    assert "Wash books" in body_text
    assert wash_books_page.driver.find_element(
        *wash_books_page.SEARCH_INPUT
    ).is_displayed()
    assert wash_books_page.driver.find_element(
        *wash_books_page.FILTER_BUTTON
    ).is_displayed()
    assert wash_books_page.download_button_is_clickable()
    assert wash_books_page.driver.find_element(
        *wash_books_page.ADD_WASH_BOOK_BUTTON
    ).is_displayed()
    assert page_has_no_broken_state(wash_books_page)


def test_wash_books_grid_columns_are_visible(browser):

    wash_books_page = open_wash_books_page(browser)
    body_text = wash_books_page.get_body_text()

    assert "ID" in body_text
    assert "Wash book name" in body_text
    assert "Washes number" in body_text
    assert "Price" in body_text
    assert "Status" in body_text


def test_add_wash_book_form_loads(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.open_create_wash_book()
    body_text = wash_books_page.get_body_text()

    assert "Add new wash book" in body_text
    assert "Wash book name" in body_text
    assert "Number of washes" in body_text
    assert "Global price" in body_text
