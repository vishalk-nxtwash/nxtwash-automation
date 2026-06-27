import allure
import pytest

from tests.admin_portal.coupon_packages.conftest import COUPON_PACKAGE_NAME
from tests.admin_portal.coupon_packages.conftest import DISCOUNT_NAME
from tests.admin_portal.coupon_packages.conftest import GIVEAWAY_SERVICE
from tests.admin_portal.coupon_packages.conftest import create_coupon_package_if_missing
from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page
from tests.admin_portal.coupon_packages.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Coupon Packages"),
    allure.story("Negative"),
]


@allure.title("CP-NAM-003 Duplicate coupon package name is blocked on save")
@pytest.mark.regression
def test_coupon_package_duplicate_name_is_blocked(browser):

    page = create_coupon_package_if_missing(browser)
    page.open_create_coupon_package()
    page.enter_coupon_package_name(COUPON_PACKAGE_NAME)
    page.select_assign_discount(DISCOUNT_NAME)
    page.select_coupon_giveaway(GIVEAWAY_SERVICE)
    page.click_save_coupon_package()

    assert page.duplicate_name_error_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("CP-SEC-001 Special character search does not break the grid")
@pytest.mark.regression
def test_coupon_packages_special_character_search_stays_usable(browser):

    page = open_coupon_packages_page(browser)
    page.search_coupon_package("' OR 1=1 --")

    assert page_has_no_broken_state(page)
