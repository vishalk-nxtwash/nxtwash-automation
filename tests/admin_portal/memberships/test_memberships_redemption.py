import logging

import allure
import pytest

from tests.admin_portal.memberships.conftest import MANAGED_MEMBERSHIP
from tests.admin_portal.memberships.conftest import REDEEM_AS_SERVICE
from tests.admin_portal.memberships.conftest import managed_membership  # noqa: F401


LOG = logging.getLogger(__name__)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Redemption Settings")
@allure.title("MB-RDM-001 Redemption single location assignment persists")
@pytest.mark.regression
def test_redemption_single_location_persists(managed_membership):

    page = managed_membership
    LOG.info(
        "Configuring single redemption location for %s with service %s",
        MANAGED_MEMBERSHIP,
        REDEEM_AS_SERVICE,
    )
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.configure_redemption_settings(0, REDEEM_AS_SERVICE)
    page.click_save_membership()
    page.wait_for_list_loaded()

    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.open_redemption_settings()

    assert page.redemption_location_is_assigned_by_index(0)
    assert REDEEM_AS_SERVICE.lower() in page.get_body_text().lower()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Redemption Settings")
@allure.title("MB-RDM-002 Redemption multiple locations persist")
@pytest.mark.regression
def test_redeem_at_multiple_locations_persists(managed_membership):

    page = managed_membership
    LOG.info(
        "Configuring two redemption locations for %s", MANAGED_MEMBERSHIP
    )
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.open_redemption_settings()
    page.assign_redemption_location_by_index(0)
    page.select_redeem_as_option(REDEEM_AS_SERVICE, 0)
    page.assign_redemption_location_by_index(1)
    page.select_redeem_as_option(REDEEM_AS_SERVICE, 1)
    page.click_save_membership()
    page.wait_for_list_loaded()

    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.open_redemption_settings()

    assert page.redemption_location_is_assigned_by_index(0)
    assert page.redemption_location_is_assigned_by_index(1)
