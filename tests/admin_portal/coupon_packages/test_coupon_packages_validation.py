import allure
import pytest

from tests.admin_portal.coupon_packages.conftest import DISCOUNT_NAME
from tests.admin_portal.coupon_packages.conftest import GIVEAWAY_SERVICE
from tests.admin_portal.coupon_packages.conftest import create_coupon_package_if_missing
from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page
from tests.admin_portal.coupon_packages.conftest import page_has_no_broken_state
from tests.admin_portal.discounts.conftest import create_discount_if_missing


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Coupon Packages"),
    allure.story("Validation"),
]


@allure.title("CP-NAM-002 Blank name is blocked on save and shows validation message")
@pytest.mark.smoke
def test_coupon_package_blank_name_is_blocked(browser):

    page = open_coupon_packages_page(browser)
    page.open_create_coupon_package()
    page.click_save_coupon_package()

    assert not page.coupon_package_name_input_is_valid()
    assert page.get_coupon_package_name_validation_message() != ""
    assert "Coupon package name" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("CP-NAM-005 Whitespace-only name is rejected on save")
@pytest.mark.extended
def test_coupon_package_whitespace_name_is_rejected(browser):

    page = open_coupon_packages_page(browser)
    page.open_create_coupon_package()
    page.enter_coupon_package_name("   ")
    page.click_save_coupon_package()

    assert "Coupon package name" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("CP-DIS-002 Blank discount selection is blocked on save")
@pytest.mark.smoke
def test_coupon_package_blank_discount_is_blocked(browser):

    page = open_coupon_packages_page(browser)
    page.open_create_coupon_package()
    page.enter_coupon_package_name("VK Discount Blank Test")
    page.click_save_coupon_package()

    body_text = page.get_body_text()
    assert "Assign discount" in body_text or "required" in body_text.lower()
    assert page_has_no_broken_state(page)
