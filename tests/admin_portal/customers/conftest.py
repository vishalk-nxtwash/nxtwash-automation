import pytest

from pages.admin_portal.customers_page import CustomersPage
from tests.admin_portal.admin_session import open_admin_path


# ── Test data constants ────────────────────────────────────────────────────────
CUSTOMER_FIRST = "vk test"
CUSTOMER_LAST = "auto customer1"
CUSTOMER_EMAIL = "vktestcust1@yopmail.com"
CUSTOMER_PHONE = "1001001"
CUSTOMER_SITE = "Vk AL01"
CUSTOMER_DOB = "2026-07-01"          # July 1 2026 in HTML date format
CUSTOMER_ADDRESS = "Vk test cust 1 test address"
CUSTOMER_ZIP = "10001"
CUSTOMER_STATE = "Arizona"
CUSTOMER_CITY = "Amado"
CUSTOMER_LICENSE_PLATE = "07"
CUSTOMER_CAR_RFID = "VK-CAR7"
UPDATED_LAST = "auto customer1 edited"
MISSING_PLATE = "NOMATCH-99999"
MISSING_PHONE = "0000000000"
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def open_customers_page(browser):
    open_admin_path(browser, "/customers")
    page = CustomersPage(browser)
    page.wait_for_list_loaded()
    return page


def page_has_no_broken_state(page):
    body = page.get_body_text()
    return not any(text in body for text in BROKEN_STATE_TEXTS)


def _customer_exists_in_list(page):
    """Check whether the managed customer exists — search by unique email."""
    page.open_filter_panel()
    page.filter_by_email(CUSTOMER_EMAIL)
    page.apply_filters()
    return CUSTOMER_LAST in page.get_body_text()


def create_customer_if_missing(browser):
    page = open_customers_page(browser)

    if _customer_exists_in_list(page):
        return open_customers_page(browser)

    page = open_customers_page(browser)
    page.create_full_customer(
        first_name=CUSTOMER_FIRST,
        last_name=CUSTOMER_LAST,
        site=CUSTOMER_SITE,
        email=CUSTOMER_EMAIL,
        phone=CUSTOMER_PHONE,
        dob=CUSTOMER_DOB,
        address=CUSTOMER_ADDRESS,
        zip_code=CUSTOMER_ZIP,
        state=CUSTOMER_STATE,
        city=CUSTOMER_CITY,
    )
    return open_customers_page(browser)


@pytest.fixture
def managed_customer(browser):
    """Ensure the managed customer exists before the test. Restore after."""
    page = create_customer_if_missing(browser)
    yield page
    create_customer_if_missing(browser)
