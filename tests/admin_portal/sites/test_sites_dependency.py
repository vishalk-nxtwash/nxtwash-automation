import allure
import pytest

from tests.admin_portal.sites.conftest import create_site_if_missing


_CROSS_MODULE_SKIP = (
    "Requires cross-module navigation fixtures (Services / Customers). "
    "Deferred until module-level fixtures are available."
)
_DEACTIVATE_SKIP = (
    "Requires deactivating the test site and verifying dropdown removal across "
    "multiple modules. Deferred to avoid leaving the shared fixture site inactive."
)

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Sites / Locations"),
    allure.story("Dependency"),
]


@allure.title("SL-DEP-001 Active site appears in Services module site dropdowns")
@pytest.mark.smoke
@pytest.mark.skip(reason=_CROSS_MODULE_SKIP)
def test_active_site_in_services_dropdowns(logged_in_admin_browser):
    pass


@allure.title("SL-DEP-002 Active site appears in Customers assign-to site dropdown")
@pytest.mark.smoke
@pytest.mark.skip(reason=_CROSS_MODULE_SKIP)
def test_active_site_in_customers_assign_dropdown(logged_in_admin_browser):
    pass


@allure.title("SL-DEP-003 Tax rates set on a site appear read-only in service assignment grids")
@pytest.mark.regression
@pytest.mark.skip(reason=_CROSS_MODULE_SKIP)
def test_site_tax_rates_visible_in_service_assignment(logged_in_admin_browser):
    pass


@allure.title("SL-DEP-004 Deactivating a site removes it from active-site dropdowns")
@pytest.mark.regression
@pytest.mark.skip(reason=_DEACTIVATE_SKIP)
def test_deactivated_site_removed_from_dropdowns(logged_in_admin_browser):
    pass


@allure.title("SL-DEP-005 Pay API token gates credit-card saving in Customers module")
@pytest.mark.regression
@pytest.mark.skip(reason=_CROSS_MODULE_SKIP)
def test_pay_api_token_gates_card_saving(logged_in_admin_browser):
    pass


@allure.title("SL-DEP-006 Lane count in Sites list matches lanes added via Lanes settings")
@pytest.mark.regression
@pytest.mark.skip(reason="Requires lane creation via EditSitePage Lanes tab. Deferred.")
def test_lane_count_in_list_matches_saved_lanes(logged_in_admin_browser):
    pass


@allure.title("SL-DEP-007 Customer Portal visibility toggle controls ecommerce site listing")
@pytest.mark.regression
@pytest.mark.skip(reason=_CROSS_MODULE_SKIP)
def test_customer_portal_toggle_controls_ecommerce_listing(logged_in_admin_browser):
    pass
