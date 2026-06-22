import allure
import pytest

from tests.admin_portal.wash_extras.conftest import open_wash_extras_page
from tests.admin_portal.wash_extras.conftest import page_has_no_broken_state


_POS_SKIP = "Requires POS module integration to verify wash extra visibility. Deferred."
_DISCOUNTS_SKIP = (
    "Requires Discounts module integration to verify discount deactivation behaviour. "
    "Deferred."
)

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Extras"),
    allure.story("Dependency"),
]


@allure.title("WE-DEP-001 Active wash extra is visible at POS for assigned sites (deferred)")
@pytest.mark.regression
@pytest.mark.skip(reason=_POS_SKIP)
def test_active_wash_extra_visible_at_pos(browser):
    pass


@allure.title("WE-DEP-002 Deactivated wash extra no longer appears at POS (deferred)")
@pytest.mark.extended
@pytest.mark.skip(reason=_POS_SKIP)
def test_deactivated_wash_extra_removed_from_pos(browser):
    pass


@allure.title("WE-DEP-003 Deactivated discount no longer applied on wash extra (deferred)")
@pytest.mark.regression
@pytest.mark.skip(reason=_DISCOUNTS_SKIP)
def test_deactivated_discount_not_applied_on_wash_extra(browser):
    pass


@allure.title("WE-OPR-001 Open price toggle enabled saves correctly (deferred: POS verification)")
@pytest.mark.extended
@pytest.mark.skip(
    reason="WE-OPR-001: Verification that price is editable at POS during a sale requires "
    "POS integration. Deferred."
)
def test_open_price_toggle_enabled_saves(browser):
    pass


@allure.title("WE-DSC-001 Service description shows on ecommerce/customer-facing site (deferred)")
@pytest.mark.extended
@pytest.mark.skip(
    reason="WE-DSC-001: Requires Customer Portal integration to verify description display. "
    "Deferred."
)
def test_description_shows_on_ecommerce_site(browser):
    pass


@allure.title("WE-CTR-001 Controller code for a site saves correctly (deferred: POS verification)")
@pytest.mark.extended
@pytest.mark.skip(
    reason="WE-CTR-001: Requires POS integration to verify controller code behaviour. "
    "Deferred."
)
def test_controller_code_saves(browser):
    pass


@allure.title("WE-CTR-002 Duplicate controller code at same site is blocked (deferred)")
@pytest.mark.extended
@pytest.mark.skip(
    reason="WE-CTR-002: Requires POS integration to verify duplicate controller code "
    "rejection. Deferred."
)
def test_duplicate_controller_code_rejected(browser):
    pass
