import allure
import pytest

from tests.admin_portal.wash_books.conftest import EXISTING_WASH_BOOK
from tests.admin_portal.wash_books.conftest import open_wash_books_page
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Negative"),
]


@allure.title("Special-character search does not crash the grid")
@pytest.mark.extended
def test_wash_books_special_character_search_stays_usable(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book("%%%___###")

    assert page_has_no_broken_state(wash_books_page)
    assert wash_books_page.driver.find_element(
        *wash_books_page.SEARCH_INPUT
    ).is_displayed()


@allure.title("WB-NAM-003 Duplicate wash book name is blocked on save")
@pytest.mark.regression
def test_duplicate_wash_book_name_is_blocked(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name(EXISTING_WASH_BOOK)
    page.set_number_of_washes("5")
    page.set_global_price("10")
    page.click_save_wash_book()

    body_text = page.get_body_text()
    saved = "Add new wash book" not in body_text and EXISTING_WASH_BOOK in page.get_body_text()
    error_shown = any(
        phrase in body_text
        for phrase in ("already exists", "duplicate", "exist")
    )
    assert error_shown or not saved


@allure.title("WB-NAM-005 A whitespace-only wash book name is rejected on save")
@pytest.mark.extended
def test_whitespace_only_wash_book_name_is_rejected(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("   ")
    page.set_number_of_washes("5")
    page.set_global_price("10")
    page.click_save_wash_book()

    body_text = page.get_body_text()
    assert (
        not page.wash_book_name_input_is_valid()
        or "Add new wash book" in body_text
    ), "Expected whitespace-only name to be rejected — form should remain open"
    assert page_has_no_broken_state(page)


@allure.title("WB-WNO-003 Negative number of washes is rejected on save")
@pytest.mark.extended
def test_negative_number_of_washes_is_rejected(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-neg-washes-test")
    page.set_number_of_washes("-1")
    page.set_global_price("10")
    page.click_save_wash_book()

    body_text = page.get_body_text()
    assert "Add new wash book" in body_text, (
        "Expected form to stay open after negative washes — app may have accepted the value"
    )
    assert page_has_no_broken_state(page)


@allure.title("WB-PRI-005 Negative global price is rejected on save")
@pytest.mark.regression
def test_negative_global_price_is_rejected(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-neg-price-test")
    page.set_number_of_washes("5")
    page.set_global_price("-10")
    page.click_save_wash_book()

    body_text = page.get_body_text()
    assert "Add new wash book" in body_text, (
        "Expected form to stay open after negative price — app may have accepted the value"
    )
    assert page_has_no_broken_state(page)


@allure.title("WB-COM-002 Negative global commission is rejected on save")
@pytest.mark.extended
def test_negative_global_commission_is_rejected(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-neg-commission-test")
    page.set_number_of_washes("5")
    page.set_global_price("10")
    page.set_global_commission("-2")
    page.click_save_wash_book()

    body_text = page.get_body_text()
    assert "Add new wash book" in body_text, (
        "Expected form to stay open after negative commission — app may have accepted the value"
    )
    assert page_has_no_broken_state(page)



