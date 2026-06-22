import allure
import pytest

from tests.admin_portal.wash_books.conftest import BARCODE_VALUE
from tests.admin_portal.wash_books.conftest import GLOBAL_PRICE
from tests.admin_portal.wash_books.conftest import open_wash_books_page
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Validation"),
]


@allure.title("WB-NAM-002 Blank wash book name is blocked on save — validation message shown")
@pytest.mark.smoke
def test_wash_book_required_name_validation(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.open_create_wash_book()
    wash_books_page.click_save_wash_book()

    assert not wash_books_page.wash_book_name_input_is_valid()
    assert wash_books_page.get_wash_book_name_validation_message() != ""


@allure.title("WB-NAM-002 Submitting a blank form keeps the user on the Add form")
@pytest.mark.smoke
def test_wash_book_blank_required_form_stays_on_form(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.open_create_wash_book()
    wash_books_page.click_save_wash_book()

    assert "Add new wash book" in wash_books_page.get_body_text()
    assert "Wash book name" in wash_books_page.get_body_text()


@allure.title("WB-PRI-002 Blank global price is blocked on save — validation message shown")
@pytest.mark.smoke
def test_wash_book_blank_global_price_is_blocked(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-no-price-test")
    page.set_number_of_washes("5")
    page.click_save_wash_book()

    assert "Add new wash book" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("WB-WNO-001 Valid number of washes saves correctly")
@pytest.mark.regression
def test_wash_book_valid_number_of_washes_saves(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-valid-washes-test")
    page.set_number_of_washes("10")
    page.set_global_price(GLOBAL_PRICE)

    assert page.get_number_of_washes_value() == "10"
    assert page_has_no_broken_state(page)


@allure.title("WB-WNO-002 Zero washes — boundary behaviour documented")
@pytest.mark.extended
def test_wash_book_zero_washes_boundary_behaviour(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-zero-washes-test")
    page.set_number_of_washes("0")
    page.set_global_price(GLOBAL_PRICE)
    page.click_save_wash_book()

    assert page_has_no_broken_state(page)


@allure.title("WB-PRI-003 Zero global price — boundary behaviour documented")
@pytest.mark.extended
def test_wash_book_zero_price_boundary_behaviour(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-zero-price-test")
    page.set_number_of_washes("5")
    page.set_global_price("0")
    page.click_save_wash_book()

    assert page_has_no_broken_state(page)


@allure.title("WB-COM-001 Valid global commission saves correctly")
@pytest.mark.extended
def test_wash_book_valid_commission_saves(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-commission-test")
    page.set_number_of_washes("5")
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission("3")

    assert page.get_global_commission_value() == "3"
    assert page_has_no_broken_state(page)


@allure.title("WB-COM-003 Saving without global commission succeeds — field is optional")
@pytest.mark.extended
def test_wash_book_save_without_commission_succeeds(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-no-commission-test")
    page.set_number_of_washes("5")
    page.set_global_price(GLOBAL_PRICE)

    assert page_has_no_broken_state(page)


@allure.title("WB-NAM-004 Maximum-length wash book name is handled without breaking the form")
@pytest.mark.extended
def test_wash_book_max_length_name_handled(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK " + ("A" * 128))

    assert page.get_wash_book_name_value().startswith("VK ")
    assert page_has_no_broken_state(page)


@allure.title("WB-BAR-001 Wash book with a barcode saves correctly")
@pytest.mark.extended
def test_wash_book_invalid_numeric_values_do_not_break_form(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.open_create_wash_book()
    wash_books_page.enter_wash_book_name("invalid-wash-book-numeric")
    wash_books_page.set_number_of_washes("-1")
    wash_books_page.set_global_price("-5")

    assert wash_books_page.get_wash_book_name_value() == "invalid-wash-book-numeric"
    assert "Number of washes" in wash_books_page.get_body_text()
