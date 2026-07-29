import allure
import pytest

from tests.admin_portal.discounts.conftest import ALL_LOC_DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import DISCOUNT_AMOUNT
from tests.admin_portal.discounts.conftest import DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import MANAGED_DISCOUNT
from tests.admin_portal.discounts.conftest import PERCENTAGE_AMOUNT
from tests.admin_portal.discounts.conftest import PERCENTAGE_DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import START_VALUE
from tests.admin_portal.discounts.conftest import create_all_locations_discount_if_missing
from tests.admin_portal.discounts.conftest import create_discount_if_missing
from tests.admin_portal.discounts.conftest import create_percentage_discount_if_missing


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Happy Path"),
]


@allure.title("DS-HP-001 Create amount discount")
@pytest.mark.sanity
def test_create_amount_discount(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.wait_for_list_loaded()
    discounts_page.search_discount(DISCOUNT_NAME)

    assert discounts_page.wait_for_discount_row(DISCOUNT_NAME).is_displayed()
    assert discounts_page.get_discount_status(DISCOUNT_NAME) == "Active"


@allure.title("DS-PER-001 Discount settings persist after creation")
@pytest.mark.regression
@pytest.mark.skip(reason="staging data / intermittent — deferred")
def test_discount_settings_persist(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.open_edit_discount(DISCOUNT_NAME)

    assert discounts_page.get_discount_name_value() == DISCOUNT_NAME
    assert discounts_page.amount_discount_type_is_selected()
    assert discounts_page.get_discount_amount_value() == DISCOUNT_AMOUNT
    assert discounts_page.get_discount_start_value() == START_VALUE
    assert discounts_page.active_switch_is_on()


@allure.title("DS-HP-008 Create discount flow is idempotent")
@pytest.mark.regression
def test_discount_create_is_idempotent(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.wait_for_list_loaded()
    discounts_page.search_discount(DISCOUNT_NAME)

    assert discounts_page.wait_for_discount_row(DISCOUNT_NAME).is_displayed()


@allure.title("DS-HP-004 Specific location settings persist")
@pytest.mark.regression
def test_discount_first_location_settings_persist(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.open_edit_discount(DISCOUNT_NAME)

    assert discounts_page.location_is_assigned_by_index(0)
    assert discounts_page.get_location_discount_value_by_index(0) == DISCOUNT_AMOUNT


@allure.title("DS-HP-002 Create percentage discount")
@pytest.mark.sanity
def test_create_percentage_discount(browser):

    discounts_page = create_percentage_discount_if_missing(browser)
    discounts_page.wait_for_list_loaded()
    discounts_page.search_discount(PERCENTAGE_DISCOUNT_NAME)

    assert discounts_page.wait_for_discount_row(PERCENTAGE_DISCOUNT_NAME).is_displayed()
    assert discounts_page.get_discount_status(PERCENTAGE_DISCOUNT_NAME) == "Active"


@allure.title("DS-HP-003 Assign all locations to a discount")
@pytest.mark.sanity
@pytest.mark.xfail(
    reason=(
        "BUG 4 — create form does not submit when 'Allow discount at all locations' "
        "toggle is on. Remove xfail once the product defect is resolved."
    ),
    strict=False,
)
def test_create_discount_assign_all_locations(browser):

    discounts_page = create_all_locations_discount_if_missing(browser)
    discounts_page.open_edit_discount(ALL_LOC_DISCOUNT_NAME)

    assert discounts_page.all_locations_switch_is_on()


@allure.title("DS-HP-006 Activate discount")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Manual — headless: after two consecutive edit-save cycles the grid search "
        "does not resolve within the 10s wait. Passes reliably in non-headless mode."
    )
)
def test_activate_discount(managed_discount):

    page = managed_discount
    page.open_edit_discount(MANAGED_DISCOUNT)
    page.ensure_active_switch_off()
    page.click_save_discount()
    page.wait_for_list_loaded()

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.ensure_active_switch_on()
    page.click_save_discount()
    page.wait_for_list_loaded()

    page.search_discount(MANAGED_DISCOUNT)
    assert page.get_discount_status(MANAGED_DISCOUNT) == "Active"


@allure.title("DS-HP-007 Deactivate discount")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Manual — headless: after two consecutive edit-save cycles the grid search "
        "does not resolve within the 10s wait. Passes reliably in non-headless mode."
    )
)
def test_deactivate_discount(managed_discount):

    page = managed_discount
    page.open_edit_discount(MANAGED_DISCOUNT)
    page.ensure_active_switch_off()
    page.click_save_discount()
    page.wait_for_list_loaded()

    page.search_discount(MANAGED_DISCOUNT)
    assert page.get_discount_status(MANAGED_DISCOUNT) == "Inactive"
