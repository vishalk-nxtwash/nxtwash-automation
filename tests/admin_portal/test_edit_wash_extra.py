from selenium.common.exceptions import TimeoutException

from tests.admin_portal.test_create_wash_extra import DISCOUNT_NAME
from tests.admin_portal.test_create_wash_extra import GLOBAL_COMMISSION
from tests.admin_portal.test_create_wash_extra import GLOBAL_PRICE
from tests.admin_portal.test_create_wash_extra import VISIBLE_PRICE
from tests.admin_portal.test_create_wash_extra import WASH_EXTRA_NAME
from tests.admin_portal.test_create_wash_extra import create_wash_extra_if_missing
from tests.admin_portal.test_wash_extras import open_wash_extras_page


UPDATED_WASH_EXTRA_NAME = "VK EWA2 updated"
FIRST_LOCATION_PRICE = "10"
SECOND_LOCATION_PRICE = "20"
UPDATED_DISCOUNT_NAME = "Basic discount"


def ensure_edit_wash_extra_source(browser):

    wash_extras_page = open_wash_extras_page(browser)

    if wash_extras_page.extra_exists(UPDATED_WASH_EXTRA_NAME):
        return wash_extras_page, UPDATED_WASH_EXTRA_NAME

    try:
        if wash_extras_page.extra_exists(WASH_EXTRA_NAME):
            return wash_extras_page, WASH_EXTRA_NAME
    except TimeoutException:
        pass

    wash_extras_page = create_wash_extra_if_missing(browser)
    return wash_extras_page, WASH_EXTRA_NAME


def update_wash_extra_if_needed(browser):

    wash_extras_page, current_name = ensure_edit_wash_extra_source(browser)

    if current_name == UPDATED_WASH_EXTRA_NAME:
        wash_extras_page.open_edit_extra(UPDATED_WASH_EXTRA_NAME)
        wash_extras_page.set_location_price_by_index(0, FIRST_LOCATION_PRICE)
        wash_extras_page.set_location_price_by_index(1, SECOND_LOCATION_PRICE)
        wash_extras_page.open_discount_settings()
        wash_extras_page.replace_applicable_discount(
            DISCOUNT_NAME,
            UPDATED_DISCOUNT_NAME
        )
        wash_extras_page.click_save_extra()
        wash_extras_page.wait_for_list_loaded()
        return wash_extras_page

    wash_extras_page.update_extra_name_location_prices_and_discount(
        WASH_EXTRA_NAME,
        UPDATED_WASH_EXTRA_NAME,
        FIRST_LOCATION_PRICE,
        SECOND_LOCATION_PRICE,
        DISCOUNT_NAME,
        UPDATED_DISCOUNT_NAME
    )
    return wash_extras_page


def test_edit_vk_ewa2_wash_extra_updates_name_price_and_discount(browser):

    wash_extras_page = update_wash_extra_if_needed(browser)
    wash_extras_page.search_extra(UPDATED_WASH_EXTRA_NAME)

    assert wash_extras_page.wait_for_extra_row(
        UPDATED_WASH_EXTRA_NAME
    ).is_displayed()
    assert wash_extras_page.get_extra_price(UPDATED_WASH_EXTRA_NAME) == VISIBLE_PRICE
    assert wash_extras_page.get_extra_status(UPDATED_WASH_EXTRA_NAME) == "Active"


def test_edit_vk_ewa2_updated_record_is_searchable_after_old_name_search(browser):

    wash_extras_page = update_wash_extra_if_needed(browser)
    wash_extras_page.search_extra(WASH_EXTRA_NAME)

    assert wash_extras_page.wait_for_extra_row(
        UPDATED_WASH_EXTRA_NAME
    ).is_displayed()


def test_edit_vk_ewa2_updated_values_persist(browser):

    wash_extras_page = update_wash_extra_if_needed(browser)
    wash_extras_page.open_edit_extra(UPDATED_WASH_EXTRA_NAME)

    assert wash_extras_page.get_service_name_value() == UPDATED_WASH_EXTRA_NAME
    assert wash_extras_page.get_location_price_by_index(0) == FIRST_LOCATION_PRICE
    assert wash_extras_page.get_location_price_by_index(1) == SECOND_LOCATION_PRICE

    wash_extras_page.open_discount_settings()

    assert wash_extras_page.discount_is_selected(UPDATED_DISCOUNT_NAME)
    assert not wash_extras_page.discount_is_selected(DISCOUNT_NAME)


def test_edit_vk_ewa2_keeps_global_price_and_commission(browser):

    wash_extras_page = update_wash_extra_if_needed(browser)
    wash_extras_page.open_edit_extra(UPDATED_WASH_EXTRA_NAME)

    assert wash_extras_page.get_service_name_value() == UPDATED_WASH_EXTRA_NAME
    assert wash_extras_page.get_global_price_value() == GLOBAL_PRICE
    assert wash_extras_page.get_global_commission_value() == GLOBAL_COMMISSION
    assert wash_extras_page.get_location_price_by_index(0) == FIRST_LOCATION_PRICE
    assert wash_extras_page.get_location_price_by_index(1) == SECOND_LOCATION_PRICE
