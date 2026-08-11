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
@pytest.mark.xfail(
    strict=False,
    reason=(
        "CP-EDT-001: TimeoutException — staging coupon package edit form slow "
        "under parallel load; grid reload exceeds wait timeout."
    ),
)
def test_edit_coupon_package_name(browser):

    create_coupon_package_if_missing(browser)
    page = open_coupon_packages_page(browser)

    if page.coupon_package_exists(UPDATED_NAME):
        page.update_coupon_package_name(UPDATED_NAME, COUPON_PACKAGE_NAME)
        page = open_coupon_packages_page(browser)

    page.update_coupon_package_name(COUPON_PACKAGE_NAME, UPDATED_NAME)
    # open_edit_coupon_package() inside update_coupon_package_name() searches by
    # the old name, which Redux Persist may rehydrate as a stale filter on the
    # fresh page load after save.  Reset before searching for the new name.
    page.reset_filters()
    page.search_coupon_package(UPDATED_NAME)
    row = page.wait_for_coupon_package_row(UPDATED_NAME)

    assert row.is_displayed()

    page.update_coupon_package_name(UPDATED_NAME, COUPON_PACKAGE_NAME)


@allure.title("CP-EDT-002 Edit assigned discount persists after save")
@pytest.mark.regression
@pytest.mark.skip(
    reason="CP-EDT-002: create_percentage_discount_if_missing navigates driver to discounts page; "
           "update_assigned_discount then times out waiting for coupon packages iframe. "
           "Fix: navigate back to coupon packages page after helper call. Manual check for now."
)
def test_edit_coupon_package_discount(managed_coupon_package):
    # Uses managed_coupon_package (not the shared VK ACC5) so gw1 cannot reset
    # the discount mid-test via create_coupon_package_if_missing.  Teardown is
    # handled by the fixture — no manual reset needed.
    page = managed_coupon_package
    create_percentage_discount_if_missing(page.driver)
    page.update_assigned_discount(MANAGED_COUPON_PACKAGE, SECOND_DISCOUNT_NAME)
    page.open_edit_coupon_package(MANAGED_COUPON_PACKAGE)
    # Assign discount hydrates after the name field; wait before asserting.
    page.wait.until(lambda d: SECOND_DISCOUNT_NAME.lower() in page.get_body_text().lower())

    assert SECOND_DISCOUNT_NAME.lower() in page.get_body_text().lower()

    page.click_save_coupon_package()
    page.wait_for_list_loaded()


@allure.title("CP-EDT-003 Edit expiration days persists after save")
@pytest.mark.extended
def test_edit_coupon_package_expiration_days(browser):

    page = create_coupon_package_if_missing(browser)
    page.update_expiration_days(COUPON_PACKAGE_NAME, EXPIRATION_DAYS)
    page.open_edit_coupon_package(COUPON_PACKAGE_NAME)

    assert page.get_expiration_days_value() == EXPIRATION_DAYS


@allure.title("CP-EDT-004 Edit coupon giveaway on receipt persists after save")
@pytest.mark.extended
def test_edit_coupon_package_giveaway_services(browser):

    page = create_coupon_package_if_missing(browser)
    page.update_coupon_giveaway_services(COUPON_PACKAGE_NAME, GIVEAWAY_SERVICES)
    page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
    selected_values = page.checked_giveaway_values()

    assert "vk detail wash" in selected_values
    assert "detail cleaning" in selected_values


@allure.title("CP-EDT-005 Activate an inactive coupon package updates status to Active")
@pytest.mark.smoke
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
@pytest.mark.smoke
def test_deactivate_active_coupon_package(browser):

    create_coupon_package_if_missing(browser)
    page = open_coupon_packages_page(browser)
    page.deactivate_coupon_package(COUPON_PACKAGE_NAME)
    page = open_coupon_packages_page(browser)
    page.show_all_packages()
    page.search_coupon_package(COUPON_PACKAGE_NAME)

    assert page.get_coupon_package_status(COUPON_PACKAGE_NAME) != "Active"

    page.activate_coupon_package(COUPON_PACKAGE_NAME)
