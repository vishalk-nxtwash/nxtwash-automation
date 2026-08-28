import allure
import pytest

from tests.admin_portal.coupon_packages.conftest import COUPON_PACKAGE_NAME
from tests.admin_portal.coupon_packages.conftest import DISCOUNT_NAME
from tests.admin_portal.coupon_packages.conftest import EXPIRATION_DAYS
from tests.admin_portal.coupon_packages.conftest import GIVEAWAY_SERVICE
from tests.admin_portal.coupon_packages.conftest import create_coupon_package_if_missing
from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page
from tests.admin_portal.coupon_packages.conftest import page_has_no_broken_state
from tests.admin_portal.discounts.conftest import create_discount_if_missing


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Coupon Packages"),
    allure.story("Edge Cases"),
]


@allure.title("CP-NAM-004 Maximum length name does not break the form")
@pytest.mark.extended
def test_coupon_package_long_name_does_not_break_form(browser):

    page = create_coupon_package_if_missing(browser)
    page.open_create_coupon_package()
    page.enter_coupon_package_name("VK " + ("C" * 128))

    assert page.get_coupon_package_name_value().startswith("VK ")
    assert "Coupon package name" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("CP-EXD-001 Valid positive expiration days saves and persists")
@pytest.mark.regression
def test_coupon_package_valid_expiration_days(browser):

    page = create_coupon_package_if_missing(browser)
    page.update_expiration_days(COUPON_PACKAGE_NAME, EXPIRATION_DAYS)
    page.open_edit_coupon_package(COUPON_PACKAGE_NAME)

    assert page.get_expiration_days_value() == EXPIRATION_DAYS


@allure.title("CP-EXD-002 Zero expiration days creates package with no expiry")
@pytest.mark.extended
def test_coupon_package_zero_expiration_days(browser):

    page = create_coupon_package_if_missing(browser)
    page.update_expiration_days(COUPON_PACKAGE_NAME, "0")
    page.open_edit_coupon_package(COUPON_PACKAGE_NAME)

    assert page.get_expiration_days_value() == "0"
    assert page_has_no_broken_state(page)


@allure.title("CP-EXD-003 Negative expiration days are rejected or corrected")
@pytest.mark.extended
@pytest.mark.skip(reason="App bug: negative expiration days accepted without error — pending fix")
def test_coupon_package_negative_expiration_days_rejected(browser):

    page = create_coupon_package_if_missing(browser)
    page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
    page.enter_expiration_days("-1")
    page.click_save_coupon_package()

    body_text = page.get_body_text().lower()
    value = page.get_expiration_days_value() if "coupon package name" in page.get_body_text() else "-1"
    assert value != "-1" or "invalid" in body_text or "error" in body_text or not page.coupon_package_name_input_is_valid()
    assert page_has_no_broken_state(page)


NO_GIVEAWAY_NAME = "VK No Giveaway Test"


@allure.title("CP-CGR-004 Save without coupon giveaway succeeds (optional field)")
@pytest.mark.extended
def test_coupon_package_save_without_giveaway(browser):

    create_discount_if_missing(browser, DISCOUNT_NAME)
    page = open_coupon_packages_page(browser)

    if not page.coupon_package_exists(NO_GIVEAWAY_NAME):
        page = open_coupon_packages_page(browser)
        page.open_create_coupon_package()
        page.enter_coupon_package_name(NO_GIVEAWAY_NAME)
        page.select_assign_discount(DISCOUNT_NAME)
        page.click_save_coupon_package()
        page.wait_for_list_loaded()

    assert page_has_no_broken_state(page)


@allure.title("CP-CGR-003 Remove a giveaway wash package persists after save")
@pytest.mark.extended
@pytest.mark.skip(reason="staging data / intermittent — deferred")
def test_coupon_package_remove_giveaway_service(browser):

    from tests.admin_portal.coupon_packages.conftest import GIVEAWAY_SERVICES

    page = create_coupon_package_if_missing(browser)
    page.update_coupon_giveaway_services(COUPON_PACKAGE_NAME, GIVEAWAY_SERVICES)
    page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
    page.remove_giveaway_service("Detail cleaning")
    page.click_save_coupon_package()
    page.wait_for_list_loaded()
    page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
    remaining = page.checked_giveaway_values()

    assert "detail cleaning" not in remaining
    assert page_has_no_broken_state(page)
