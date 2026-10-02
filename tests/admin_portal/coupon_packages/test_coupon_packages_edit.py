import allure
import pytest

from tests.admin_portal.coupon_packages.conftest import COUPON_PACKAGE_INACTIVE_NAME
from tests.admin_portal.coupon_packages.conftest import COUPON_PACKAGE_NAME
from tests.admin_portal.coupon_packages.conftest import DISCOUNT_NAME
from tests.admin_portal.coupon_packages.conftest import EXPIRATION_DAYS
from tests.admin_portal.coupon_packages.conftest import GIVEAWAY_SERVICES
from tests.admin_portal.coupon_packages.conftest import MANAGED_COUPON_PACKAGE
from tests.admin_portal.coupon_packages.conftest import SECOND_DISCOUNT_NAME
from tests.admin_portal.coupon_packages.conftest import create_coupon_package_if_missing
from tests.admin_portal.coupon_packages.conftest import create_inactive_coupon_package_if_missing
from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page
from tests.admin_portal.discounts.conftest import create_percentage_discount_if_missing


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Coupon Packages"),
    allure.story("Edit"),
]

UPDATED_NAME = "VK ACC2 Renamed"


@allure.title("CP-EDT-001 Edit coupon package name persists after save")
@pytest.mark.regression
def test_edit_coupon_package_name(browser, managed_coupon_package):

    page = managed_coupon_package

    if page.coupon_package_exists(UPDATED_NAME):
        page.update_coupon_package_name(UPDATED_NAME, MANAGED_COUPON_PACKAGE)
        page = open_coupon_packages_page(browser)

    page.update_coupon_package_name(MANAGED_COUPON_PACKAGE, UPDATED_NAME)
    page.search_coupon_package(UPDATED_NAME)
    row = page.wait_for_coupon_package_row(UPDATED_NAME)

    assert row.is_displayed()

    page.update_coupon_package_name(UPDATED_NAME, MANAGED_COUPON_PACKAGE)


@allure.title("CP-EDT-002 Edit assigned discount persists after save")
@pytest.mark.regression
def test_edit_coupon_package_discount(browser, managed_coupon_package):

    create_percentage_discount_if_missing(browser)
    # create_percentage_discount_if_missing navigates to /services/discounts to
    # check/create the discount, leaving the browser off the coupon packages
    # page the managed_coupon_package fixture set up before this test body ran.
    # Re-navigate back before touching the coupon package.
    page = open_coupon_packages_page(browser)
    page.update_assigned_discount(MANAGED_COUPON_PACKAGE, SECOND_DISCOUNT_NAME)
    page.open_edit_coupon_package(MANAGED_COUPON_PACKAGE)
    # Assign discount hydrates after the name field; wait before asserting.
    page.wait.until(lambda d: SECOND_DISCOUNT_NAME.lower() in page.get_body_text().lower())

    assert SECOND_DISCOUNT_NAME.lower() in page.get_body_text().lower()

    page.click_save_coupon_package()
    page.wait_for_list_loaded()
    page.update_assigned_discount(MANAGED_COUPON_PACKAGE, DISCOUNT_NAME)


@allure.title("CP-EDT-003 Edit expiration days persists after save")
@pytest.mark.extended
def test_edit_coupon_package_expiration_days(managed_coupon_package):

    page = managed_coupon_package
    page.update_expiration_days(MANAGED_COUPON_PACKAGE, EXPIRATION_DAYS)
    page.open_edit_coupon_package(MANAGED_COUPON_PACKAGE)

    assert page.get_expiration_days_value() == EXPIRATION_DAYS


@allure.title("CP-EDT-004 Edit coupon giveaway on receipt persists after save")
@pytest.mark.extended
@pytest.mark.skip(reason="manual check: React controlled input send_keys fix applied, pending clean CI verification")
def test_edit_coupon_package_giveaway_services(browser):

    page = create_coupon_package_if_missing(browser)
    page.update_coupon_giveaway_services(COUPON_PACKAGE_NAME, GIVEAWAY_SERVICES)
    page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
    selected_values = page.checked_giveaway_values()

    assert "vk detail wash" in selected_values
    assert "detail cleaning" in selected_values


@allure.title("CP-EDT-005 Activate an inactive coupon package updates status to Active")
@pytest.mark.skip(reason="Manual: activation of an inactive package does not persist via automation - needs investigation of legacy iframe form submit behaviour")
def test_activate_inactive_coupon_package(browser):

    create_inactive_coupon_package_if_missing(browser)
    page = open_coupon_packages_page(browser)
    page.show_all_packages()
    page.activate_coupon_package(COUPON_PACKAGE_INACTIVE_NAME)
    page = open_coupon_packages_page(browser)
    page.search_coupon_package(COUPON_PACKAGE_INACTIVE_NAME)

    assert page.get_coupon_package_status(COUPON_PACKAGE_INACTIVE_NAME) == "Active"

    page.deactivate_coupon_package(COUPON_PACKAGE_INACTIVE_NAME)


@allure.title("CP-EDT-006 Deactivate an active coupon package updates status")
@pytest.mark.skip(reason="manual check: FILTER_BUTTON locator exact text match fails when active filter shows 'Filter by (1)' — fix contains() across all page objects")
def test_deactivate_active_coupon_package(browser):

    create_coupon_package_if_missing(browser)
    page = open_coupon_packages_page(browser)
    page.deactivate_coupon_package(COUPON_PACKAGE_NAME)
    page = open_coupon_packages_page(browser)
    page.show_all_packages()
    page.search_coupon_package(COUPON_PACKAGE_NAME)

    assert page.get_coupon_package_status(COUPON_PACKAGE_NAME) != "Active"

    page.activate_coupon_package(COUPON_PACKAGE_NAME)
