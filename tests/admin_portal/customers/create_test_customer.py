"""
One-time setup script: creates the managed test customer in the admin portal.

Run once before executing the customer test suite:

    venv/bin/pytest tests/admin_portal/customers/create_test_customer.py -v -s

After this passes the customer exists in the system and managed_customer
fixture tests will find it via the email filter instead of trying to create it.
"""
import allure
import pytest

from tests.admin_portal.customers.conftest import (
    CUSTOMER_ADDRESS,
    CUSTOMER_CITY,
    CUSTOMER_DOB,
    CUSTOMER_EMAIL,
    CUSTOMER_FIRST,
    CUSTOMER_LAST,
    CUSTOMER_PHONE,
    CUSTOMER_SITE,
    CUSTOMER_STATE,
    CUSTOMER_ZIP,
    open_customers_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Customers"),
    allure.story("Setup"),
]


@allure.title("SETUP Create managed test customer in the admin portal")
def test_create_managed_test_customer(browser):
    """
    Creates the standard test customer used by the customer test suite.
    Safe to re-run — if the customer already exists the test still passes.
    """
    page = open_customers_page(browser)

    # Check if customer already exists by email filter.
    page.open_filter_panel()
    page.filter_by_email(CUSTOMER_EMAIL)
    page.apply_filters()

    if CUSTOMER_LAST in page.get_body_text():
        pytest.skip("Customer '%s %s' already exists — nothing to do." % (
            CUSTOMER_FIRST, CUSTOMER_LAST
        ))

    # Customer does not exist — create it with all fields.
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

    # Verify the customer now appears in the list.
    page = open_customers_page(browser)
    page.open_filter_panel()
    page.filter_by_email(CUSTOMER_EMAIL)
    page.apply_filters()

    assert CUSTOMER_LAST in page.get_body_text(), (
        "Customer '%s %s' was not found after creation. "
        "Check the form field locators in customers_page.py against the live DOM." % (
            CUSTOMER_FIRST, CUSTOMER_LAST
        )
    )
    assert page_has_no_broken_state(page)
