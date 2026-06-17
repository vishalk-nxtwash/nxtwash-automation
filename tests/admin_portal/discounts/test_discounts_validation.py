import allure
import pytest

from tests.admin_portal.discounts.conftest import open_discounts_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Validation"),
]


@allure.title("DIS-VAL-001 Discount name is mandatory")
@pytest.mark.validation
def test_discount_required_name_validation(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.click_save_discount()

    assert not discounts_page.discount_name_input_is_valid()
    assert discounts_page.get_discount_name_validation_message() != ""


@allure.title("DIS-VAL-002 Blank required discount form stays on form")
@pytest.mark.validation
def test_discount_blank_required_form_stays_on_form(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.click_save_discount()

    assert "Add new discount" in discounts_page.get_body_text()
    assert "Discount name" in discounts_page.get_body_text()


@allure.title("DIS-VAL-003 Invalid negative discount amount does not break form")
@pytest.mark.validation
def test_discount_invalid_amount_does_not_break_form(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("invalid-discount-amount")
    discounts_page.set_discount_amount("-5")

    assert discounts_page.get_discount_name_value() == "invalid-discount-amount"
    assert "Discount amount" in discounts_page.get_body_text()
