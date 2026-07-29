import allure
import pytest

from tests.admin_portal.coupon_packages.conftest import COUPON_PACKAGE_INACTIVE_NAME
from tests.admin_portal.coupon_packages.conftest import COUPON_PACKAGE_NAME
from tests.admin_portal.coupon_packages.conftest import DISCOUNT_NAME
from tests.admin_portal.coupon_packages.conftest import GIVEAWAY_SERVICE
from tests.admin_portal.coupon_packages.conftest import create_coupon_package_if_missing
from tests.admin_portal.coupon_packages.conftest import create_inactive_coupon_package_if_missing
from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Coupon Packages"),
    allure.story("CRUD"),
]


@allure.title("CP-TGL-001 / CP-NAM-001 Create active coupon package appears in list")
@pytest.mark.smoke
def test_create_coupon_package(browser):

    page = create_coupon_package_if_missing(browser)
    page.search_coupon_package(COUPON_PACKAGE_NAME)

    assert page.wait_for_coupon_package_row(COUPON_PACKAGE_NAME).is_displayed()


@allure.title("CP-DIS-001 / CP-CGR-001 Coupon package settings persist after save")
@pytest.mark.regression
def test_coupon_package_settings_persist(browser):

    page = create_coupon_package_if_missing(browser)
    page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
    body_text = page.get_body_text().lower()

    assert page.get_coupon_package_name_value() == COUPON_PACKAGE_NAME
    assert DISCOUNT_NAME.lower() in body_text
    assert GIVEAWAY_SERVICE.lower() in page.checked_giveaway_values()
    assert page.active_switch_is_on()


@allure.title("CP-TGL-002 Create inactive coupon package")
@pytest.mark.regression
@pytest.mark.skip(reason="staging data / intermittent — deferred")
def test_create_inactive_coupon_package(browser):

    page = create_inactive_coupon_package_if_missing(browser)
    page.search_coupon_package(COUPON_PACKAGE_INACTIVE_NAME)
    row = page.wait_for_coupon_package_row(COUPON_PACKAGE_INACTIVE_NAME)

    assert row.is_displayed()
    assert page.get_coupon_package_status(COUPON_PACKAGE_INACTIVE_NAME) != "Active"
