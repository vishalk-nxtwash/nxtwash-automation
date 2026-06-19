import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    ASSIGNMENT_SITE,
    ASSIGNMENT_SITE_2,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    PACKAGE_NAME,
    SITE_OVERRIDE_COMMISSION,
    SITE_OVERRIDE_PRICE,
    SITE_OVERRIDE_PRICE_HIGH,
    open_wash_packages_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("Site Assignment"),
]


@allure.title("WP-SIT-002 Site assignment persists after re-save")
@pytest.mark.regression
def test_assign_multiple_sites_persists(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.assign_site_with_price_and_commission(
        ASSIGNMENT_SITE, GLOBAL_PRICE, GLOBAL_COMMISSION
    )
    page.click_save_package()
    page.wait_for_list_loaded()

    page.open_edit_package(PACKAGE_NAME)
    body = page.get_body_text()

    assert ASSIGNMENT_SITE in body
    assert page_has_no_broken_state(page)


@allure.title("WP-SIT-003 Select all sites via the header checkbox")
@pytest.mark.regression
def test_select_all_sites_via_header_checkbox(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.select_all_sites()
    body = page.get_body_text()

    assert ASSIGNMENT_SITE in body
    assert page_has_no_broken_state(page)


@allure.title("WP-SIT-005 Saving a wash package with zero sites selected does not crash")
@pytest.mark.regression
def test_save_wash_package_without_site_selection(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("VK zero-sites test")
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)
    page.click_save_package()

    assert page_has_no_broken_state(page)


@allure.title("WP-PRC-001 Global price is reflected at the site level by default")
@pytest.mark.regression
def test_global_price_reflected_at_site(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)

    assert page.get_site_price_value(ASSIGNMENT_SITE) == GLOBAL_PRICE
    assert page_has_no_broken_state(page)


@allure.title("WP-PRC-002 Location price override for a specific site persists after save")
@pytest.mark.regression
def test_location_price_override_persists(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.assign_site_with_price_and_commission(
        ASSIGNMENT_SITE, SITE_OVERRIDE_PRICE, GLOBAL_COMMISSION
    )
    page.click_save_package()
    page.wait_for_list_loaded()

    page.open_edit_package(PACKAGE_NAME)
    assert page.get_site_price_value(ASSIGNMENT_SITE) == SITE_OVERRIDE_PRICE
    assert page_has_no_broken_state(page)


@allure.title("WP-PRC-003 Location price override higher than global price persists")
@pytest.mark.regression
def test_location_price_override_higher_than_global_persists(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.assign_site_with_price_and_commission(
        ASSIGNMENT_SITE, SITE_OVERRIDE_PRICE_HIGH, GLOBAL_COMMISSION
    )
    page.click_save_package()
    page.wait_for_list_loaded()

    page.open_edit_package(PACKAGE_NAME)
    assert page.get_site_price_value(ASSIGNMENT_SITE) == SITE_OVERRIDE_PRICE_HIGH
    assert page_has_no_broken_state(page)


@allure.title("WP-PRC-004 Location price override lower than global price persists")
@pytest.mark.regression
def test_location_price_override_lower_than_global_persists(managed_package):
    lower_price = str(int(GLOBAL_PRICE) - 10)
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.assign_site_with_price_and_commission(
        ASSIGNMENT_SITE, lower_price, GLOBAL_COMMISSION
    )
    page.click_save_package()
    page.wait_for_list_loaded()

    page.open_edit_package(PACKAGE_NAME)
    assert page.get_site_price_value(ASSIGNMENT_SITE) == lower_price
    assert page_has_no_broken_state(page)


@allure.title("WP-PRC-005 Location commission override for a specific site persists after save")
@pytest.mark.regression
def test_location_commission_override_persists(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.assign_site_with_price_and_commission(
        ASSIGNMENT_SITE, GLOBAL_PRICE, SITE_OVERRIDE_COMMISSION
    )
    page.click_save_package()
    page.wait_for_list_loaded()

    page.open_edit_package(PACKAGE_NAME)
    assert page.get_site_commission_value(ASSIGNMENT_SITE) == SITE_OVERRIDE_COMMISSION
    assert page_has_no_broken_state(page)


@allure.title("WP-PRC-006 Location commission override higher than global commission persists")
@pytest.mark.regression
def test_location_commission_higher_than_global_persists(managed_package):
    higher_commission = str(int(GLOBAL_COMMISSION) + 10)
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.assign_site_with_price_and_commission(
        ASSIGNMENT_SITE, GLOBAL_PRICE, higher_commission
    )
    page.click_save_package()
    page.wait_for_list_loaded()

    page.open_edit_package(PACKAGE_NAME)
    assert page.get_site_commission_value(ASSIGNMENT_SITE) == higher_commission
    assert page_has_no_broken_state(page)
