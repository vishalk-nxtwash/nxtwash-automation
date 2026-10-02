import allure
import pytest

from tests.admin_portal.memberships.conftest import MEMBERSHIP_NAME
from tests.admin_portal.memberships.conftest import create_membership_if_missing


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Memberships"),
    allure.story("Edge Cases"),
]


@allure.title("MB-EC-001 Membership create workflow is idempotent")
@pytest.mark.regression
def test_membership_create_is_idempotent(browser):

    memberships_page = create_membership_if_missing(browser)
    memberships_page.wait_for_list_loaded()
    memberships_page.search_membership(MEMBERSHIP_NAME)

    assert memberships_page.wait_for_membership_row(MEMBERSHIP_NAME).is_displayed()


@allure.title("MB-SIT-001 Membership only first location is assigned at baseline")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "BUG 8 (docs/bug_reports.md): location-assignment checkbox changes "
        "are not reliably saved (both assign and unassign) — leftover "
        "locations from earlier runs' MEMBERSHIP_NAME record can't be "
        "cleaned up via the UI, so more than one location may show assigned "
        "at baseline. Reports XPASS once fixed."
    ),
)
def test_membership_only_first_location_is_assigned(browser):

    memberships_page = create_membership_if_missing(browser)
    memberships_page.open_edit_membership(MEMBERSHIP_NAME)

    first_name = memberships_page.get_location_name_by_index(0)
    assert memberships_page.assigned_location_names() == [first_name]


@allure.title("MB-NAM-004 Maximum length membership name does not break form")
@pytest.mark.regression
def test_membership_long_name_does_not_break_form(browser):

    memberships_page = create_membership_if_missing(browser)
    memberships_page.open_create_membership()
    memberships_page.enter_membership_name("VK " + ("M" * 128))

    assert memberships_page.get_membership_name_value().startswith("VK ")
    assert "Membership name" in memberships_page.get_body_text()
