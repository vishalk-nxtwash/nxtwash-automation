from selenium.common.exceptions import TimeoutException

from pages.admin_portal.wash_extras_page import WashExtrasPage
from tests.admin_portal.admin_session import open_admin_path


EXISTING_EXTRA = "Detailing"
MISSING_EXTRA = "wash-extra-does-not-exist-automation"
WASH_EXTRA_NAME = "VK EWA2"
UPDATED_WASH_EXTRA_NAME = "VK EWA2 updated"
GLOBAL_PRICE = "15"
GLOBAL_COMMISSION = "2"
DISCOUNT_NAME = "Plus discount"
UPDATED_DISCOUNT_NAME = "Basic discount"
VISIBLE_PRICE = "$15.00"
FIRST_LOCATION_PRICE = "10"
SECOND_LOCATION_PRICE = "20"
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def open_wash_extras_page(browser):

    open_admin_path(browser, "/services/washExtras")

    page = WashExtrasPage(browser)
    page.wait_for_list_loaded()

    return page


def create_wash_extra_if_missing(browser, extra_name=WASH_EXTRA_NAME):

    page = open_wash_extras_page(browser)

    if page.extra_exists(extra_name):
        page = open_wash_extras_page(browser)
        page.open_edit_extra(extra_name)
        page.fill_extra_form(extra_name, GLOBAL_PRICE, GLOBAL_COMMISSION)
        page.open_discount_settings()
        page.select_applicable_discount(DISCOUNT_NAME)
        page.click_save_extra()
        return open_wash_extras_page(browser)

    page.create_extra(
        extra_name,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        DISCOUNT_NAME
    )
    page.search_extra(extra_name)
    page.wait_for_extra_row(extra_name)

    return page


def ensure_edit_wash_extra_source(browser):

    page = open_wash_extras_page(browser)

    if page.extra_exists(UPDATED_WASH_EXTRA_NAME):
        return page, UPDATED_WASH_EXTRA_NAME

    try:
        if page.extra_exists(WASH_EXTRA_NAME):
            return page, WASH_EXTRA_NAME
    except TimeoutException:
        pass

    page = create_wash_extra_if_missing(browser)
    return page, WASH_EXTRA_NAME


def update_wash_extra_if_needed(browser):

    page, current_name = ensure_edit_wash_extra_source(browser)

    if current_name == UPDATED_WASH_EXTRA_NAME:
        page.open_edit_extra(UPDATED_WASH_EXTRA_NAME)
        page.set_location_price_by_index(0, FIRST_LOCATION_PRICE)
        page.set_location_price_by_index(1, SECOND_LOCATION_PRICE)
        page.open_discount_settings()
        page.replace_applicable_discount(DISCOUNT_NAME, UPDATED_DISCOUNT_NAME)
        page.click_save_extra()
        return open_wash_extras_page(browser)

    page.update_extra_name_location_prices_and_discount(
        WASH_EXTRA_NAME,
        UPDATED_WASH_EXTRA_NAME,
        FIRST_LOCATION_PRICE,
        SECOND_LOCATION_PRICE,
        DISCOUNT_NAME,
        UPDATED_DISCOUNT_NAME
    )
    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)
