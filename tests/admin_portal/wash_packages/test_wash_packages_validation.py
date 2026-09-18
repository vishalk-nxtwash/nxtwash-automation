import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    GLOBAL_PRICE,
    open_wash_packages_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("Validation"),
]


@allure.title("WP-VAL Blank required form stays on the create page")
@pytest.mark.smoke
def test_wash_package_blank_required_form_stays_on_form(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.click_save_package()

    assert "Service name" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("WP-PRI-004 Decimal global price is accepted and the form remains usable")
@pytest.mark.edge
def test_wash_package_decimal_price_is_accepted(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("VK decimal-price-test")
    page.set_global_price("12.50")

    assert page.global_price_input_is_valid()
    assert page_has_no_broken_state(page)


@allure.title("WP-COM-002 Decimal global commission is accepted by the form")
@pytest.mark.edge
def test_wash_package_decimal_commission_is_accepted(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("VK decimal-commission-test")
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission("2.50")

    assert page.global_commission_input_is_valid()
    assert page_has_no_broken_state(page)


@allure.title("WP-VAL Invalid numeric inputs do not break the create form")
@pytest.mark.edge
def test_wash_package_invalid_numeric_values_do_not_break_form(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("VK invalid-numeric-test")
    page.set_loyalty_points("-1", "abc")
    page.set_global_price("-10")
    page.set_global_commission("abc")

    assert page_has_no_broken_state(page)
