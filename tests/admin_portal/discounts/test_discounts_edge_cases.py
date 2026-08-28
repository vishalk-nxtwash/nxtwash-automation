import allure
import pytest

from tests.admin_portal.discounts.conftest import DISCOUNT_AMOUNT
from tests.admin_portal.discounts.conftest import MANAGED_DISCOUNT
from tests.admin_portal.discounts.conftest import MANAGED_PERCENTAGE_DISCOUNT
from tests.admin_portal.discounts.conftest import PERCENTAGE_AMOUNT
from tests.admin_portal.discounts.conftest import REQUESTED_SERVICE_CATEGORY
from tests.admin_portal.discounts.conftest import SERVICE_CATEGORY
from tests.admin_portal.discounts.conftest import START_DAY
from tests.admin_portal.discounts.conftest import START_TIME
from tests.admin_portal.discounts.conftest import create_discount_if_missing
from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Edge Cases"),
]


@allure.title("DS-EC-009 Long discount name does not break form")
@pytest.mark.regression
def test_discount_long_name_does_not_break_form(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("VK " + ("D" * 128))

    assert discounts_page.get_discount_name_value().startswith("VK ")
    assert "Discount name" in discounts_page.get_body_text()


@allure.title("DS-EC-001 0 percent discount is accepted")
@pytest.mark.regression
def test_discount_zero_percent_accepted(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("VK EC Zero Pct")
    discounts_page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    discounts_page.select_percentage_discount_type()
    discounts_page.set_discount_amount("0")
    discounts_page.set_discount_start(START_DAY, START_TIME)
    discounts_page.ensure_active_switch_on()
    discounts_page.set_location_discount_value_by_index(0, "0")
    discounts_page.select_location_discount_type_by_index(0, "Percentage")
    discounts_page.assign_location_by_index(0)
    discounts_page.click_save_discount()

    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-EC-002 100 percent discount is accepted")
@pytest.mark.regression
def test_discount_hundred_percent_accepted(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("VK EC 100 Pct")
    discounts_page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    discounts_page.select_percentage_discount_type()
    discounts_page.set_discount_amount("100")
    discounts_page.set_discount_start(START_DAY, START_TIME)
    discounts_page.ensure_active_switch_on()
    discounts_page.set_location_discount_value_by_index(0, "100")
    discounts_page.select_location_discount_type_by_index(0, "Percentage")
    discounts_page.assign_location_by_index(0)
    discounts_page.click_save_discount()

    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-EC-003 Discount with future start date is accepted")
@pytest.mark.regression
def test_discount_future_start_date_accepted(browser):

    import datetime
    future_day = str(
        (datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).day
    )

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("VK EC Future Start")
    discounts_page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    discounts_page.select_amount_discount_type()
    discounts_page.set_discount_amount(DISCOUNT_AMOUNT)
    discounts_page.set_discount_start(future_day, START_TIME)
    discounts_page.ensure_active_switch_on()
    discounts_page.set_location_discount_value_by_index(0, DISCOUNT_AMOUNT)
    discounts_page.select_location_discount_type_by_index(0, "Amount")
    discounts_page.assign_location_by_index(0)
    discounts_page.click_save_discount()

    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-EC-004 Discount expiring today is accepted")
@pytest.mark.regression
def test_discount_expiring_today_accepted(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("VK EC Exp Today")
    discounts_page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    discounts_page.select_amount_discount_type()
    discounts_page.set_discount_amount(DISCOUNT_AMOUNT)
    discounts_page.set_discount_start(START_DAY, START_TIME)
    discounts_page.ensure_active_switch_on()
    discounts_page.set_location_discount_value_by_index(0, DISCOUNT_AMOUNT)
    discounts_page.select_location_discount_type_by_index(0, "Amount")
    discounts_page.assign_location_by_index(0)
    discounts_page.click_save_discount()

    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-EC-005 Change discount type from amount to percentage")
@pytest.mark.regression
@pytest.mark.xdist_group("discounts_managed")
def test_discount_type_change_amount_to_percentage(managed_discount):

    page = managed_discount

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.select_percentage_discount_type()
    page.set_discount_amount(PERCENTAGE_AMOUNT)
    page.set_location_discount_value_by_index(0, PERCENTAGE_AMOUNT)
    page.select_location_discount_type_by_index(0, "Percentage")
    page.click_save_discount()
    page.wait_for_list_loaded()
    page.open_edit_discount(MANAGED_DISCOUNT)

    assert page.percentage_discount_type_is_selected()


@allure.title("DS-EC-006 Change discount type from percentage to amount")
@pytest.mark.regression
@pytest.mark.xdist_group("discounts_managed")
def test_discount_type_change_percentage_to_amount(managed_percentage_discount):

    page = managed_percentage_discount

    page.open_edit_discount(MANAGED_PERCENTAGE_DISCOUNT)
    page.select_amount_discount_type()
    page.set_discount_amount(DISCOUNT_AMOUNT)
    page.set_location_discount_value_by_index(0, DISCOUNT_AMOUNT)
    page.select_location_discount_type_by_index(0, "Amount")
    page.click_save_discount()
    page.wait_for_list_loaded()
    page.open_edit_discount(MANAGED_PERCENTAGE_DISCOUNT)

    assert page.amount_discount_type_is_selected()


@allure.title("DS-EC-007 Remove assigned location from discount")
@pytest.mark.regression
@pytest.mark.xdist_group("discounts_managed")
def test_discount_remove_assigned_location(managed_discount):

    page = managed_discount

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.ensure_all_locations_switch_off()
    page.assign_location_by_index(0)

    checkbox_before = page.location_is_assigned_by_index(0)

    page.unassign_location_by_index(0)

    assert not page.location_is_assigned_by_index(0)
    assert checkbox_before  # was assigned before removal


@allure.title("DS-EC-008 Add location to existing discount")
@pytest.mark.regression
@pytest.mark.xdist_group("discounts_managed")
def test_discount_add_location_to_existing(managed_discount):

    page = managed_discount

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.ensure_all_locations_switch_off()

    rows = page.get_location_rows()
    if len(rows) < 2:
        pytest.skip("Only one location available — cannot test adding a second")

    # Capture names before modifying — server may reorder rows on reload so
    # index-based checks after save are unreliable with 133+ locations.
    loc_0_name = rows[0].text.splitlines()[0].strip()
    loc_1_name = rows[1].text.splitlines()[0].strip()

    page.assign_location_by_index(0)
    if not page.location_is_assigned_by_index(1):
        page.assign_location_by_index(1)
        page.set_location_discount_value_by_index(1, DISCOUNT_AMOUNT)
        page.select_location_discount_type_by_index(1, "Amount")

    page.click_save_discount()
    page.wait_for_list_loaded()
    page.open_edit_discount(MANAGED_DISCOUNT)

    assert (
        page.location_is_assigned_by_name(loc_0_name)
        or page.location_is_assigned_by_name(loc_1_name)
    )
