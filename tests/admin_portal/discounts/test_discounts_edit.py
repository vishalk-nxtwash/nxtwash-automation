import allure
import pytest

from tests.admin_portal.discounts.conftest import DISCOUNT_AMOUNT
from tests.admin_portal.discounts.conftest import DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import END_DAY
from tests.admin_portal.discounts.conftest import END_TIME
from tests.admin_portal.discounts.conftest import MANAGED_DISCOUNT
from tests.admin_portal.discounts.conftest import REQUESTED_SERVICE_CATEGORY
from tests.admin_portal.discounts.conftest import SERVICE_CATEGORY
from tests.admin_portal.discounts.conftest import START_DAY
from tests.admin_portal.discounts.conftest import START_TIME
from tests.admin_portal.discounts.conftest import create_discount_if_missing


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Edit Flow"),
]


@allure.title("DS-HP-005 Edit discount value and reapply expected settings")
@pytest.mark.regression
def test_edit_discount_reapplies_expected_settings(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.update_discount(
        DISCOUNT_NAME,
        REQUESTED_SERVICE_CATEGORY,
        DISCOUNT_AMOUNT,
        START_DAY,
        START_TIME,
        SERVICE_CATEGORY
    )

    discounts_page.open_edit_discount(DISCOUNT_NAME)

    assert discounts_page.get_discount_name_value() == DISCOUNT_NAME
    assert discounts_page.amount_discount_type_is_selected()
    assert discounts_page.get_discount_amount_value() == DISCOUNT_AMOUNT
    assert discounts_page.active_switch_is_on()


@allure.title("DS-UPD-001 Change discount name persists")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Manual — headless: wait_for_list_loaded times out after the rename save "
        "when run in headless mode. Passes reliably in non-headless mode."
    )
)
def test_edit_discount_name_persists(managed_discount):

    page = managed_discount
    new_name = MANAGED_DISCOUNT + " RENAMED"

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.enter_discount_name(new_name)
    page.click_save_discount()
    page.wait_for_list_loaded()
    page.search_discount(new_name)

    assert page.wait_for_discount_row(new_name).is_displayed()


@allure.title("DS-UPD-002 Change start date persists")
@pytest.mark.regression
def test_edit_discount_start_date_persists(managed_discount):

    page = managed_discount
    new_day = "15"
    new_time = "12:00 PM"

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.set_discount_start(new_day, new_time)
    page.click_save_discount()
    page.wait_for_list_loaded()
    page.open_edit_discount(MANAGED_DISCOUNT)

    assert new_time in page.get_discount_start_value()


@allure.title("DS-UPD-003 Change end date persists")
@pytest.mark.regression
def test_edit_discount_end_date_persists(managed_discount):

    page = managed_discount

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.set_discount_end(END_DAY, END_TIME)
    page.click_save_discount()
    page.wait_for_list_loaded()
    page.open_edit_discount(MANAGED_DISCOUNT)

    assert END_TIME in page.get_discount_end_value()


@allure.title("DS-UPD-004 Change service category assignment persists")
@pytest.mark.regression
def test_edit_discount_category_assignment_persists(managed_discount):

    page = managed_discount

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.select_service_category(SERVICE_CATEGORY, REQUESTED_SERVICE_CATEGORY)
    page.click_save_discount()
    page.wait_for_list_loaded()
    page.open_edit_discount(MANAGED_DISCOUNT)

    assert page.get_selected_service_category() != ""


@allure.title("DS-UPD-005 Change selected locations to all locations persists")
@pytest.mark.regression
@pytest.mark.xfail(
    reason=(
        "BUG 4 (edit variant) — the all-locations switch toggles on and the form "
        "saves without error, but the backend does not persist the all-locations=true "
        "state. Switch is off when the form is reopened. Remove xfail once fixed."
    ),
    strict=False,
)
def test_edit_discount_selected_to_all_locations(managed_discount):

    page = managed_discount

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.ensure_all_locations_switch_on()
    page.click_save_discount()
    page.wait_for_list_loaded()
    page.open_edit_discount(MANAGED_DISCOUNT)

    assert page.all_locations_switch_is_on()


@allure.title("DS-UPD-006 Change all locations to selected locations persists")
@pytest.mark.regression
def test_edit_discount_all_to_selected_locations(managed_discount):

    page = managed_discount

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.ensure_all_locations_switch_on()
    page.click_save_discount()
    page.wait_for_list_loaded()

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.ensure_all_locations_switch_off()
    page.set_location_discount_value_by_index(0, DISCOUNT_AMOUNT)
    page.select_location_discount_type_by_index(0, "Amount")
    page.assign_location_by_index(0)
    page.click_save_discount()
    page.wait_for_list_loaded()
    page.open_edit_discount(MANAGED_DISCOUNT)

    assert not page.all_locations_switch_is_on()
    assert page.location_is_assigned_by_index(0)
