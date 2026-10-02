import logging

import allure
import pytest

from tests.admin_portal.memberships.conftest import MANAGED_MEMBERSHIP
from tests.admin_portal.memberships.conftest import REDEEM_AS_SERVICE
from tests.admin_portal.memberships.conftest import managed_membership  # noqa: F401


LOG = logging.getLogger(__name__)
pytestmark = pytest.mark.timeout(900)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Redemption Settings")
@allure.title("MB-RED-001 Redemption single location assignment persists")
@pytest.mark.regression
def test_redemption_single_location_persists(managed_membership):

    page = managed_membership
    LOG.info(
        "Configuring single redemption location for %s with service %s",
        MANAGED_MEMBERSHIP,
        REDEEM_AS_SERVICE,
    )
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    site_name = page.configure_redemption_settings(REDEEM_AS_SERVICE)
    page.save_and_return_to_list()

    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.open_redemption_settings()

    assert page.redemption_location_is_assigned(site_name)
    assert REDEEM_AS_SERVICE.lower() in page.get_body_text().lower()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Redemption Settings")
@allure.title("MB-RED-002 Redemption multiple locations persist")
@pytest.mark.regression
def test_redeem_at_multiple_locations_persists(managed_membership):

    page = managed_membership
    LOG.info(
        "Configuring two redemption locations for %s", MANAGED_MEMBERSHIP
    )
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.open_redemption_settings()
    # Capture concrete site names once — index isn't a stable identity across
    # the reload below (grid virtualizes; see get_redemption_location_name_by_index).
    first_name = page.get_redemption_location_name_by_index(0)
    page.assign_redemption_location(first_name)
    page.select_redeem_as_option(first_name, REDEEM_AS_SERVICE)
    second_name = page.get_redemption_location_name_by_index(1)
    page.assign_redemption_location(second_name)
    page.select_redeem_as_option(second_name, REDEEM_AS_SERVICE)
    page.save_and_return_to_list()

    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.open_redemption_settings()

    assert page.redemption_location_is_assigned(first_name)
    assert page.redemption_location_is_assigned(second_name)
