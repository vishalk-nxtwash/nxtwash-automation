import allure
import pytest

from tests.admin_portal.wash_books.conftest import WASH_BOOK_NAME
from tests.admin_portal.wash_books.conftest import create_wash_book_if_missing
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


_CUSTOMERS_SKIP = (
    "WB-DEP: Requires Customers module integration to verify wash book appears "
    "in the Select wash book dropdown during customer wash book creation. Deferred."
)

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Dependency"),
]


@allure.title("WB-DEP-001 Active wash book appears in Select wash book dropdown for CWB creation")
@pytest.mark.regression
@pytest.mark.skip(reason=_CUSTOMERS_SKIP)
def test_active_wash_book_available_for_cwb_creation(browser):
    pass


@allure.title("WB-DEP-002 Deactivated wash book no longer appears in Select wash book dropdown")
@pytest.mark.regression
@pytest.mark.skip(reason=_CUSTOMERS_SKIP)
def test_deactivated_wash_book_not_available_for_cwb_creation(browser):
    pass


@allure.title("WB-LTY-001 Valid points awarded saves and points are actually awarded (deferred)")
@pytest.mark.extended
@pytest.mark.skip(
    reason="WB-LTY-001: Verification that points are awarded requires Loyalty module "
    "integration. Deferred."
)
def test_valid_points_awarded_saves(browser):
    pass


@allure.title("WB-BAR-003 Duplicate barcode is rejected on save (deferred fixtures)")
@pytest.mark.regression
@pytest.mark.skip(
    reason="WB-BAR-003: Requires a known barcode already assigned to another wash book. "
    "Deferred until barcode fixtures are established."
)
def test_duplicate_barcode_rejected(browser):
    pass


@allure.title("WB-DSC-001 Wash book description shows on ecommerce/customer portal (deferred)")
@pytest.mark.extended
@pytest.mark.skip(
    reason="WB-DSC-001: Requires Customer Portal integration to verify description display. "
    "Deferred."
)
def test_description_shows_on_customer_portal(browser):
    pass


@allure.title("WB-CPT-001 Show on customer portal enabled — wash book visible to customers (deferred)")
@pytest.mark.extended
@pytest.mark.skip(
    reason="WB-CPT-001: Requires Customer Portal integration to verify portal visibility. "
    "Deferred."
)
def test_customer_portal_enabled_wash_book_visible(browser):
    pass
