from pages.admin_portal.discounts_page import DiscountsPage
from tests.admin_portal._managed import managed_name
from tests.admin_portal._managed import managed_resource
from tests.admin_portal.admin_session import open_admin_path


EXISTING_DISCOUNT = "Basic Discount"
MISSING_DISCOUNT = "discount-does-not-exist-automation"
DISCOUNT_NAME = "VK AD02"
REQUESTED_SERVICE_CATEGORY = "VK ASC1"
SERVICE_CATEGORY = "VK ASC1"
DISCOUNT_AMOUNT = "5"
START_DAY = "9"
START_TIME = "10:00 AM"
START_VALUE = "June 9, 2026 10:00 AM"
PERCENTAGE_DISCOUNT_NAME = "VK PD02"
PERCENTAGE_AMOUNT = "10"
ALL_LOC_DISCOUNT_NAME = "VK AL01"
END_DAY = "28"
END_TIME = "11:00 PM"
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

    return discounts_page


def create_discount_if_missing(browser, discount_name=DISCOUNT_NAME):

    discounts_page = open_discounts_page(browser)

    if discounts_page.discount_exists(discount_name):
        discounts_page.open_edit_discount(discount_name)
        discounts_page.fill_discount_form(
            discount_name,
            REQUESTED_SERVICE_CATEGORY,
            DISCOUNT_AMOUNT,
            START_DAY,
            START_TIME,
            SERVICE_CATEGORY
        )
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
    discounts_page.open_edit_discount(MANAGED_DISCOUNT)
    discounts_page.set_discount_amount(DISCOUNT_AMOUNT)
    discounts_page.select_amount_discount_type()
    discounts_page.ensure_active_switch_on()
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
