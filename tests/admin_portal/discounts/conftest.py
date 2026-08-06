from datetime import date as _date

from pages.admin_portal.discounts_page import DiscountsPage
from tests.admin_portal._managed import managed_name
from tests.admin_portal._managed import managed_resource
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._data import load as _load

_D = _load("discounts")

EXISTING_DISCOUNT          = _D["reference"]["existing_discount"]
MISSING_DISCOUNT           = _D["search"]["nonexistent"]
DISCOUNT_NAME              = _D["template"]["discount_name"]
REQUESTED_SERVICE_CATEGORY = _D["reference"]["service_category"]
SERVICE_CATEGORY           = _D["reference"]["service_category"]
DISCOUNT_AMOUNT            = _D["template"]["amount"]
START_DAY                  = _D["template"]["start_day"]
START_TIME                 = _D["template"]["start_time"]

_today = _date.today()
START_VALUE = (
    _date(_today.year, _today.month, int(START_DAY)).strftime("%B")
    + f" {int(START_DAY)}, {_today.year} "
    + START_TIME
)
PERCENTAGE_DISCOUNT_NAME   = _D["percentage"]["discount_name"]
PERCENTAGE_AMOUNT          = _D["percentage"]["amount"]
ALL_LOC_DISCOUNT_NAME      = _D["reference"]["all_locations_discount"]
END_DAY                    = _D["template"]["end_day"]
END_TIME                   = _D["template"]["end_time"]
MANAGED_PERCENTAGE_DISCOUNT = managed_name("Pct Discount")


BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


def open_discounts_page(browser):

    open_admin_path(browser, "/services/discounts")

    discounts_page = DiscountsPage(browser)
    discounts_page.wait_for_list_loaded()
    discounts_page.reset_filters_if_active()

    return discounts_page


def create_discount_if_missing(browser, discount_name=DISCOUNT_NAME):

    discounts_page = open_discounts_page(browser)

    if discounts_page.discount_exists(discount_name):
        discounts_page.open_edit_discount(discount_name)
        discounts_page.ensure_active_switch_on()
        discounts_page.click_save_discount()
        discounts_page.wait_for_list_loaded()
        return discounts_page

    # reset_filters_if_active() only clears the active-status filter.  A
    # deactivate test may have left the discount inactive so discount_exists()
    # (active-only view) returns False.  Reset all filters and re-check before
    # falling through to create — creating a duplicate name fails silently.
    from selenium.common.exceptions import TimeoutException as _TE
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    discounts_page.reset_filters()
    discounts_page.search_discount(discount_name)
    locator = discounts_page.get_discount_row_locator(discount_name)
    try:
        WebDriverWait(discounts_page.driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        inactive_found = True
    except _TE:
        inactive_found = False

    if inactive_found:
        discounts_page.open_edit_discount(discount_name)
        discounts_page.ensure_active_switch_on()
        discounts_page.click_save_discount()
        discounts_page.wait_for_list_loaded()
        return discounts_page

    discounts_page.create_discount(
        discount_name,
        REQUESTED_SERVICE_CATEGORY,
        DISCOUNT_AMOUNT,
        START_DAY,
        START_TIME,
        SERVICE_CATEGORY
    )
    discounts_page.search_discount(discount_name)
    discounts_page.wait_for_discount_row(discount_name)

    return discounts_page


def create_percentage_discount_if_missing(browser, discount_name=PERCENTAGE_DISCOUNT_NAME):

    discounts_page = open_discounts_page(browser)

    if discounts_page.discount_exists(discount_name):
        return discounts_page

    discounts_page.create_percentage_discount(
        discount_name,
        REQUESTED_SERVICE_CATEGORY,
        PERCENTAGE_AMOUNT,
        START_DAY,
        START_TIME,
        SERVICE_CATEGORY
    )
    discounts_page.search_discount(discount_name)
    discounts_page.wait_for_discount_row(discount_name)

    return discounts_page


def create_all_locations_discount_if_missing(browser, discount_name=ALL_LOC_DISCOUNT_NAME):

    discounts_page = open_discounts_page(browser)

    if discounts_page.discount_exists(discount_name):
        return discounts_page

    discounts_page.create_discount_all_locations(
        discount_name,
        REQUESTED_SERVICE_CATEGORY,
        DISCOUNT_AMOUNT,
        START_DAY,
        START_TIME,
        SERVICE_CATEGORY
    )
    discounts_page.search_discount(discount_name)
    discounts_page.wait_for_discount_row(discount_name)

    return discounts_page


# --- Managed (self-cleaning) discount --------------------------------------
# A dedicated record reset to baseline before and after each test that mutates
# it. Discounts cannot be deleted in the product, so teardown resets mutable
# fields instead of deleting. See tests/admin_portal/_managed.py.

MANAGED_DISCOUNT = managed_name("Discount")


def reset_managed_discount(browser):
    """Ensure the managed discount exists and reset its mutable fields."""
    discounts_page = open_discounts_page(browser)

    if not discounts_page.discount_exists(MANAGED_DISCOUNT):
        discounts_page.create_discount(
            MANAGED_DISCOUNT,
            REQUESTED_SERVICE_CATEGORY,
            DISCOUNT_AMOUNT,
            START_DAY,
            START_TIME,
            SERVICE_CATEGORY
        )

    # Reset mutable fields touched by tests back to a known baseline.
    # ensure_all_locations_switch_off() must run before save: if a previous
    # run left all-locations=on, saving with it on triggers BUG 4 and times out.
    discounts_page.open_edit_discount(MANAGED_DISCOUNT)
    discounts_page.set_discount_amount(DISCOUNT_AMOUNT)
    discounts_page.select_amount_discount_type()
    discounts_page.ensure_active_switch_on()
    discounts_page.ensure_all_locations_switch_off()
    discounts_page.click_save_discount()
    discounts_page.wait_for_list_loaded()

    return discounts_page


managed_discount = managed_resource(reset_managed_discount)


def reset_managed_percentage_discount(browser):
    """Ensure the managed percentage discount exists and reset its mutable fields."""
    discounts_page = open_discounts_page(browser)

    if not discounts_page.discount_exists(MANAGED_PERCENTAGE_DISCOUNT):
        discounts_page.create_percentage_discount(
            MANAGED_PERCENTAGE_DISCOUNT,
            REQUESTED_SERVICE_CATEGORY,
            PERCENTAGE_AMOUNT,
            START_DAY,
            START_TIME,
            SERVICE_CATEGORY
        )

    discounts_page.open_edit_discount(MANAGED_PERCENTAGE_DISCOUNT)
    discounts_page.select_percentage_discount_type()
    discounts_page.set_discount_amount(PERCENTAGE_AMOUNT)
    discounts_page.ensure_active_switch_on()
    discounts_page.click_save_discount()
    discounts_page.wait_for_list_loaded()

    return discounts_page


managed_percentage_discount = managed_resource(reset_managed_percentage_discount)
