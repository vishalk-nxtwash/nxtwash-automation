import allure
import pytest

from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page
from tests.admin_portal.coupon_packages.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Coupon Packages"),
    allure.story("UI"),
]


@allure.title("CP-LST-001 Coupon packages page loads with primary controls")
@pytest.mark.smoke
def test_coupon_packages_page_loads_with_primary_controls(browser):

    page = open_coupon_packages_page(browser)
    body_text = page.get_body_text()

    assert "Coupon package name" in body_text
    assert "Discount assigned" in body_text
    assert "Services assigned" in body_text
    assert "Status" in body_text
    assert "Add new coupon package" in body_text
    assert page_has_no_broken_state(page)


@allure.title("CP-LST-002 Coupon packages grid columns are visible")
@pytest.mark.regression
def test_coupon_packages_grid_columns_are_visible(browser):

    page = open_coupon_packages_page(browser)
    body_text = page.get_body_text()

    assert "Coupon package name" in body_text
    assert "Discount assigned" in body_text
    assert "Services assigned" in body_text
    assert "Status" in body_text
    assert page_has_no_broken_state(page)


@allure.title("CP-LST-003 Customer coupon packages tab is accessible")
@pytest.mark.smoke
def test_customer_coupon_packages_tab_is_accessible(browser):

    page = open_coupon_packages_page(browser)
    page.click_customer_coupon_packages_tab()

    assert page_has_no_broken_state(page)


@allure.title("CP-LST-004 Add new coupon package form loads correctly")
@pytest.mark.regression
def test_add_coupon_package_form_loads(browser):

    page = open_coupon_packages_page(browser)
    page.open_create_coupon_package()

    assert "Coupon package name" in page.get_body_text()
    assert "Assign discount" in page.get_body_text()
    assert page.active_switch_is_on()
