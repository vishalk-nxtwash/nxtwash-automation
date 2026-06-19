import allure
import pytest

from tests.admin_portal.discounts.conftest import DISCOUNT_AMOUNT
from tests.admin_portal.discounts.conftest import END_DAY
from tests.admin_portal.discounts.conftest import END_TIME
from tests.admin_portal.discounts.conftest import PERCENTAGE_AMOUNT
from tests.admin_portal.discounts.conftest import REQUESTED_SERVICE_CATEGORY
from tests.admin_portal.discounts.conftest import SERVICE_CATEGORY
from tests.admin_portal.discounts.conftest import START_DAY
from tests.admin_portal.discounts.conftest import START_TIME
from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Combination"),
]


def _fill_and_save_amount_all_locations(page, name):
    if page.discount_exists(name):
        return
    page.open_create_discount()
    page.enter_discount_name(name)
    page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    page.select_amount_discount_type()
    page.set_discount_amount(DISCOUNT_AMOUNT)
    page.set_discount_start(START_DAY, START_TIME)
    page.ensure_active_switch_on()
    page.ensure_all_locations_switch_on()
    page.click_save_discount()
    page.wait_for_list_loaded()


def _fill_and_save_amount_selected_location(page, name):
    if page.discount_exists(name):
        return
    page.open_create_discount()
    page.enter_discount_name(name)
    page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    page.select_amount_discount_type()
    page.set_discount_amount(DISCOUNT_AMOUNT)
    page.set_discount_start(START_DAY, START_TIME)
    page.ensure_active_switch_on()
    page.set_location_discount_value_by_index(0, DISCOUNT_AMOUNT)
    page.select_location_discount_type_by_index(0, "Amount")
    page.fill_required_unassigned_location_values()
    page.assign_location_by_index(0)
    page.click_save_discount()
    page.wait_for_list_loaded()


def _fill_and_save_percentage_all_locations(page, name):
    if page.discount_exists(name):
        return
    page.open_create_discount()
    page.enter_discount_name(name)
    page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    page.select_percentage_discount_type()
    page.set_discount_amount(PERCENTAGE_AMOUNT)
    page.set_discount_start(START_DAY, START_TIME)
    page.ensure_active_switch_on()
    page.ensure_all_locations_switch_on()
    page.click_save_discount()
    page.wait_for_list_loaded()


def _fill_and_save_percentage_selected_location(page, name):
    if page.discount_exists(name):
        return
    page.open_create_discount()
    page.enter_discount_name(name)
    page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    page.select_percentage_discount_type()
    page.set_discount_amount(PERCENTAGE_AMOUNT)
    page.set_discount_start(START_DAY, START_TIME)
    page.ensure_active_switch_on()
    page.set_location_discount_value_by_index(0, PERCENTAGE_AMOUNT)
    page.select_location_discount_type_by_index(0, "Percentage")
    page.fill_required_unassigned_location_values()
    page.assign_location_by_index(0)
    page.click_save_discount()
    page.wait_for_list_loaded()


@allure.title("DS-CMB-001 Amount + all locations + active discount is created")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="BUG 4 — create form does not submit when all-locations toggle is on.",
    strict=False,
)
def test_cmb_amount_all_locations_active(browser):

    page = open_discounts_page(browser)
    _fill_and_save_amount_all_locations(page, "VK CMB001")

    page.search_discount("VK CMB001")
    assert page.wait_for_discount_row("VK CMB001").is_displayed()
    assert page.get_discount_status("VK CMB001") == "Active"
    assert page_has_no_broken_state(page)


@allure.title("DS-CMB-002 Amount + selected locations + active discount is created")
@pytest.mark.regression
def test_cmb_amount_selected_locations_active(browser):

    page = open_discounts_page(browser)
    _fill_and_save_amount_selected_location(page, "VK CMB002")

    page.search_discount("VK CMB002")
    assert page.wait_for_discount_row("VK CMB002").is_displayed()
    assert page.get_discount_status("VK CMB002") == "Active"
    assert page_has_no_broken_state(page)


@allure.title("DS-CMB-003 Percentage + all locations + active discount is created")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="BUG 4 — create form does not submit when all-locations toggle is on.",
    strict=False,
)
def test_cmb_percentage_all_locations_active(browser):

    page = open_discounts_page(browser)
    _fill_and_save_percentage_all_locations(page, "VK CMB003")

    page.search_discount("VK CMB003")
    assert page.wait_for_discount_row("VK CMB003").is_displayed()
    assert page.get_discount_status("VK CMB003") == "Active"
    assert page_has_no_broken_state(page)


@allure.title("DS-CMB-004 Percentage + selected locations + active discount is created")
@pytest.mark.regression
def test_cmb_percentage_selected_locations_active(browser):

    page = open_discounts_page(browser)
    _fill_and_save_percentage_selected_location(page, "VK CMB004")

    page.search_discount("VK CMB004")
    assert page.wait_for_discount_row("VK CMB004").is_displayed()
    assert page.get_discount_status("VK CMB004") == "Active"
    assert page_has_no_broken_state(page)


@allure.title("DS-CMB-005 Percentage discount with future start date is created")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="BUG 4 — create form does not submit when all-locations toggle is on.",
    strict=False,
)
def test_cmb_percentage_future_start_date(browser):

    import datetime
    future_day = str(
        (datetime.date.today().replace(day=1) + datetime.timedelta(days=32)).day
    )

    page = open_discounts_page(browser)
    if not page.discount_exists("VK CMB005"):
        page.open_create_discount()
        page.enter_discount_name("VK CMB005")
        page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
        page.select_percentage_discount_type()
        page.set_discount_amount(PERCENTAGE_AMOUNT)
        page.set_discount_start(future_day, START_TIME)
        page.ensure_active_switch_on()
        page.ensure_all_locations_switch_on()
        page.click_save_discount()
        page.wait_for_list_loaded()

    page.search_discount("VK CMB005")
    assert page.wait_for_discount_row("VK CMB005").is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("DS-CMB-006 Amount discount with end date is created")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="BUG 4 — create form does not submit when all-locations toggle is on.",
    strict=False,
)
def test_cmb_amount_with_end_date(browser):

    page = open_discounts_page(browser)
    if not page.discount_exists("VK CMB006"):
        page.open_create_discount()
        page.enter_discount_name("VK CMB006")
        page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
        page.select_amount_discount_type()
        page.set_discount_amount(DISCOUNT_AMOUNT)
        page.set_discount_start(START_DAY, START_TIME)
        page.set_discount_end(END_DAY, END_TIME)
        page.ensure_active_switch_on()
        page.ensure_all_locations_switch_on()
        page.click_save_discount()
        page.wait_for_list_loaded()

    page.search_discount("VK CMB006")
    assert page.wait_for_discount_row("VK CMB006").is_displayed()
    assert page_has_no_broken_state(page)
