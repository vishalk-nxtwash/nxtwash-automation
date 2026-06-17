import allure
import pytest

from tests.admin_portal.discounts.conftest import MISSING_DISCOUNT
from tests.admin_portal.discounts.conftest import REQUESTED_SERVICE_CATEGORY
from tests.admin_portal.discounts.conftest import SERVICE_CATEGORY
from tests.admin_portal.discounts.conftest import START_DAY
from tests.admin_portal.discounts.conftest import START_TIME
from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Negative"),
]


@allure.title("DS-SRH-NEG-001 Missing discount is not returned")
@pytest.mark.regression
def test_missing_discount_is_not_returned(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.search_discount(MISSING_DISCOUNT)

    assert MISSING_DISCOUNT not in discounts_page.get_body_text()
    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-NG-006 Special-character discount search remains stable")
@pytest.mark.regression
def test_discounts_special_character_search_stays_usable(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.search_discount("%%%___###")

    assert page_has_no_broken_state(discounts_page)
    assert discounts_page.driver.find_element(*discounts_page.SEARCH_INPUT).is_displayed()


@allure.title("DS-NG-001 Create discount without service category is blocked")
@pytest.mark.validation
def test_create_discount_without_category_blocked(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("no-category-discount")
    discounts_page.set_discount_amount("5")
    discounts_page.click_save_discount()

    assert "Add new discount" in discounts_page.get_body_text()
    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-NG-002 Create discount without value is blocked")
@pytest.mark.validation
def test_create_discount_without_value_blocked(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("no-value-discount")
    discounts_page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    discounts_page.click_save_discount()

    assert "Add new discount" in discounts_page.get_body_text()
    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-NG-003 Start date after end date is blocked")
@pytest.mark.validation
def test_create_discount_start_after_end_blocked(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("date-order-test-discount")
    discounts_page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    discounts_page.select_amount_discount_type()
    discounts_page.set_discount_amount("5")
    # Set end date (day 10) before start date (day 20)
    discounts_page.set_discount_end("10", "10:00 AM")
    discounts_page.set_discount_start("20", "11:00 AM")
    discounts_page.click_save_discount()

    assert "Add new discount" in discounts_page.get_body_text()
    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-NG-004 Percentage above 100 is blocked")
@pytest.mark.validation
def test_create_discount_percentage_above_limit_blocked(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("pct-above-limit-discount")
    discounts_page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    discounts_page.select_percentage_discount_type()
    discounts_page.set_discount_amount("150")
    discounts_page.set_discount_start(START_DAY, START_TIME)
    discounts_page.click_save_discount()

    assert "Add new discount" in discounts_page.get_body_text()
    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-NG-005 No location selected when required is blocked")
@pytest.mark.validation
def test_create_discount_no_location_blocked(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("no-location-discount")
    discounts_page.select_service_category(REQUESTED_SERVICE_CATEGORY, SERVICE_CATEGORY)
    discounts_page.select_amount_discount_type()
    discounts_page.set_discount_amount("5")
    discounts_page.set_discount_start(START_DAY, START_TIME)
    discounts_page.ensure_all_locations_switch_off()
    discounts_page.click_save_discount()

    assert "Add new discount" in discounts_page.get_body_text()
    assert page_has_no_broken_state(discounts_page)
