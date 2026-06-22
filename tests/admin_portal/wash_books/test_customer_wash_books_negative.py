import allure
import pytest

from tests.admin_portal.wash_books.conftest import (
    CWB_WASH_BOOK_NUMBER,
    create_customer_wash_book_if_missing,
    open_customer_wash_books_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Customer Wash Books — Validation"),
]


@allure.title("CWB-VAL-001 Saving without selecting a wash book template is blocked")
@pytest.mark.smoke
def test_create_cwb_blank_wash_book_selection_blocked(browser):

    page = open_customer_wash_books_page(browser)
    page.open_create_cwb()
    page.enter_cwb_wash_book_number("CWB-VAL-001-test")
    page.set_cwb_number_of_washes("5")
    page.click_save_cwb()

    body_text = page.get_body_text()
    assert (
        not page.cwb_wash_book_number_input_is_valid()
        or "Add customer wash book" in body_text
        or "required" in body_text.lower()
        or "Select wash book" in body_text
    )
    assert page_has_no_broken_state(page)


@allure.title("CWB-VAL-002 Saving with a blank wash book number is blocked")
@pytest.mark.smoke
def test_create_cwb_blank_wash_book_number_blocked(browser):

    page = open_customer_wash_books_page(browser)
    page.open_create_cwb()
    page.set_cwb_number_of_washes("5")
    page.click_save_cwb()

    assert not page.cwb_wash_book_number_input_is_valid()
    assert page.get_cwb_wash_book_number_validation_message() != ""


@allure.title("CWB-VAL-003 Saving with a blank number of washes is blocked")
@pytest.mark.smoke
def test_create_cwb_blank_number_of_washes_blocked(browser):

    page = open_customer_wash_books_page(browser)
    page.open_create_cwb()
    page.enter_cwb_wash_book_number("CWB-VAL-003-test")
    page.click_save_cwb()

    assert not page.cwb_number_of_washes_input_is_valid()
    assert page.get_cwb_number_of_washes_validation_message() != ""


@allure.title("CWB-VAL-004 Duplicate wash book number is rejected on save")
@pytest.mark.regression
def test_create_cwb_duplicate_number_rejected(browser):

    create_customer_wash_book_if_missing(browser)

    page = open_customer_wash_books_page(browser)
    page.open_create_cwb()
    page.enter_cwb_wash_book_number(CWB_WASH_BOOK_NUMBER)
    page.set_cwb_number_of_washes("5")
    page.click_save_cwb()

    body_text = page.get_body_text()
    error_shown = any(
        phrase in body_text.lower()
        for phrase in ("already exists", "duplicate", "exist", "taken")
    )
    still_on_form = "Add customer wash book" in body_text or "Save customer wash book" in body_text
    assert error_shown or still_on_form
    assert page_has_no_broken_state(page)
