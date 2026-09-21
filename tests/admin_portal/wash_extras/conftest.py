from selenium.common.exceptions import TimeoutException

from pages.admin_portal.wash_extras_page import WashExtrasPage
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._managed import managed_name, managed_resource
from tests.admin_portal._data import load as _load

_D = _load("wash_extras")

EXISTING_EXTRA          = _D["reference"]["existing_extra"]
MISSING_EXTRA           = _D["search"]["nonexistent"]
WASH_EXTRA_NAME         = _D["template"]["extra_name"]
UPDATED_WASH_EXTRA_NAME = _D["updated"]["extra_name"]
GLOBAL_PRICE            = _D["template"]["global_price"]
GLOBAL_COMMISSION       = _D["template"]["global_commission"]
DISCOUNT_NAME           = _D["reference"]["discount_name"]
UPDATED_DISCOUNT_NAME   = _D["reference"]["updated_discount"]
VISIBLE_PRICE           = _D["template"]["visible_price"]
FIRST_LOCATION_PRICE    = _D["template"]["first_location_price"]
SECOND_LOCATION_PRICE   = _D["template"]["second_location_price"]
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
        try:
            rows = page.get_location_rows()
            for i in range(len(rows)):
                page.set_location_price_by_index(i, GLOBAL_PRICE)
        except Exception:
            pass
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


MANAGED_WASH_EXTRA = managed_name("Wash Extra")


def _reset_managed_wash_extra(browser):
    page = open_wash_extras_page(browser)
    if page.extra_exists(MANAGED_WASH_EXTRA):
        page = open_wash_extras_page(browser)
        page.open_edit_extra(MANAGED_WASH_EXTRA)
        page.fill_extra_form(MANAGED_WASH_EXTRA, GLOBAL_PRICE, GLOBAL_COMMISSION)
        page.open_discount_settings()
        page.select_applicable_discount(DISCOUNT_NAME)
        page.click_save_extra()
        return open_wash_extras_page(browser)
    page.create_extra(
        MANAGED_WASH_EXTRA,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        DISCOUNT_NAME,
    )
    return open_wash_extras_page(browser)


managed_wash_extra = managed_resource(_reset_managed_wash_extra)
