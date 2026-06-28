import allure
import pytest

from tests.admin_portal.bank_drop.conftest import (
    open_bank_drop_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Bank Drop"),
    allure.story("Validation"),
]


@allure.title("BD-VAL-001 Blank bank drop name is blocked on save")
@pytest.mark.smoke
@pytest.mark.validation
def test_blank_name_is_blocked(browser):

    page = open_bank_drop_page(browser)
    page.open_create()
    page.enter_order("10")
    page.click_save()

    assert not page.bank_drop_name_input_is_valid()
    assert page.get_bank_drop_name_validation_message() != ""
    assert page_has_no_broken_state(page)


@allure.title("BD-VAL-002 Blank order is blocked on save")
@pytest.mark.smoke
@pytest.mark.validation
def test_blank_order_is_blocked(browser):

    page = open_bank_drop_page(browser)
    page.open_create()
    page.enter_name("VK val-no-order")
    page.click_save()

    assert not page.bank_drop_order_input_is_valid()
    assert page.get_bank_drop_order_validation_message() != ""
    assert page_has_no_broken_state(page)


@allure.title("BD-VAL-003 Non-numeric value in order field is rejected")
@pytest.mark.regression
@pytest.mark.validation
def test_non_numeric_order_rejected(browser):

    page = open_bank_drop_page(browser)
    page.open_create()
    page.enter_name("VK ABD INVALID ORDER")
    page.enter_order("abc")
    page.click_save()

    assert not page.bank_drop_order_input_is_valid()
    assert page_has_no_broken_state(page)
