from tests.admin_portal.wash_books.conftest import open_wash_books_page


def test_wash_book_required_name_validation(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.open_create_wash_book()
    wash_books_page.click_save_wash_book()

    assert not wash_books_page.wash_book_name_input_is_valid()
    assert wash_books_page.get_wash_book_name_validation_message() != ""


def test_wash_book_blank_required_form_stays_on_form(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.open_create_wash_book()
    wash_books_page.click_save_wash_book()

    assert "Add new wash book" in wash_books_page.get_body_text()
    assert "Wash book name" in wash_books_page.get_body_text()


def test_wash_book_invalid_numeric_values_do_not_break_form(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.open_create_wash_book()
    wash_books_page.enter_wash_book_name("invalid-wash-book-numeric")
    wash_books_page.set_number_of_washes("-1")
    wash_books_page.set_global_price("-5")

    assert wash_books_page.get_wash_book_name_value() == "invalid-wash-book-numeric"
    assert "Number of washes" in wash_books_page.get_body_text()
