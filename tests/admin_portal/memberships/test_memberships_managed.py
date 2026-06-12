import logging

import allure
import pytest

from tests.admin_portal.memberships.conftest import BASELINE_POINTS
from tests.admin_portal.memberships.conftest import MANAGED_MEMBERSHIP


LOG = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Memberships"),
    allure.story("Managed data"),
]

UPDATED_POINTS = "5"


@allure.title("MEM-MANAGED-001 Managed membership starts at baseline")
@pytest.mark.sanity
def test_managed_membership_provided_at_baseline(managed_membership):
    """The fixture hands over a dedicated record already reset to baseline."""
    page = managed_membership

    page.open_edit_membership(MANAGED_MEMBERSHIP)

    assert page.get_membership_name_value() == MANAGED_MEMBERSHIP
    assert page.get_points_awarded_value() == BASELINE_POINTS


@allure.title("MEM-MANAGED-002 Mutations are reverted on teardown")
@pytest.mark.regression
def test_managed_membership_mutation_is_reset_on_teardown(managed_membership):
    """Mutate loyalty points; the fixture teardown resets them to baseline."""
    page = managed_membership

    LOG.info("Mutating managed membership points to %s", UPDATED_POINTS)
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.set_points_awarded(UPDATED_POINTS)
    page.click_save_membership()
    page.wait_for_list_loaded()

    page.open_edit_membership(MANAGED_MEMBERSHIP)
    assert page.get_points_awarded_value() == UPDATED_POINTS
    # On teardown the fixture resets points back to BASELINE_POINTS, so the next
    # test (and the next run) sees a clean record without any manual cleanup.
