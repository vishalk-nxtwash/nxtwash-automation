import allure
import pytest

from tests.admin_portal.wash_packages.conftest import open_wash_packages_page


_MEMBERSHIPS_SKIP = "Requires Memberships module fixtures and cross-module setup. Deferred."
_DISCOUNTS_SKIP = "Requires active Discount mapped to this package. Deferred."

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("Dependency"),
]


@allure.title("WP-DEP-001 Wash package is selectable during membership redemption mapping")
@pytest.mark.regression
@pytest.mark.skip(reason=_MEMBERSHIPS_SKIP)
def test_wash_package_available_for_membership_redemption(browser):
    pass


@allure.title("WP-DEP-002 Deactivate a wash package mapped to an active membership redemption")
@pytest.mark.regression
@pytest.mark.skip(reason=_MEMBERSHIPS_SKIP)
def test_deactivate_wash_package_mapped_to_membership(browser):
    pass


@allure.title("WP-DEP-003 Rename a wash package mapped to a membership reflects correctly")
@pytest.mark.regression
@pytest.mark.skip(reason=_MEMBERSHIPS_SKIP)
def test_rename_wash_package_mapped_to_membership(browser):
    pass


@allure.title("WP-DEP-004 Deactivated discount no longer applied on the wash package")
@pytest.mark.regression
@pytest.mark.skip(reason=_DISCOUNTS_SKIP)
def test_deactivated_discount_removed_from_wash_package(browser):
    pass


@allure.title("WP-DEP-005 Unassigning a site does not affect membership redemption at other sites")
@pytest.mark.regression
@pytest.mark.skip(reason=_MEMBERSHIPS_SKIP)
def test_site_unassignment_does_not_affect_other_redemption_sites(browser):
    pass
