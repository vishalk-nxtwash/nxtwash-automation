import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.admin_portal.customers_page import CustomersPage
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal.customers.test_data import (
    BROKEN_STATE_TEXTS,
    CUSTOMER_ADDRESS,
    CUSTOMER_CAR_RFID,
    CUSTOMER_CITY,
    CUSTOMER_DOB,
    CUSTOMER_EMAIL,
    CUSTOMER_FIRST,
    CUSTOMER_LAST,
    CUSTOMER_LICENSE_PLATE,
    CUSTOMER_PHONE,
    CUSTOMER_SITE,
    CUSTOMER_STATE,
    CUSTOMER_ZIP,
    MISSING_PHONE,
    MISSING_PLATE,
    SLOT,
    UPDATED_LAST,
)

# Re-export so test files that already import from conftest continue to work.
__all__ = [
    "BROKEN_STATE_TEXTS",
    "CUSTOMER_ADDRESS",
    "CUSTOMER_CAR_RFID",
    "CUSTOMER_CITY",
    "CUSTOMER_DOB",
    "CUSTOMER_EMAIL",
    "CUSTOMER_FIRST",
    "CUSTOMER_LAST",
    "CUSTOMER_LICENSE_PLATE",
    "CUSTOMER_PHONE",
    "CUSTOMER_SITE",
    "CUSTOMER_STATE",
    "CUSTOMER_ZIP",
    "MISSING_PHONE",
    "MISSING_PLATE",
    "UPDATED_LAST",
]


# ─────────────────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────────────────

def open_customers_page(browser):
    open_admin_path(browser, "/customers")
    page = CustomersPage(browser)
    page.wait_for_list_loaded()
    return page


def page_has_no_broken_state(page):
    body = page.get_body_text()
    return not any(text in body for text in BROKEN_STATE_TEXTS)


# ─────────────────────────────────────────────────────────────────────────────
# Self-healing customer fixture helpers
# ─────────────────────────────────────────────────────────────────────────────

def _find_customer_row_by_email(page):
    """
    Filter the list by CUSTOMER_EMAIL and return True if any row appears.
    Leaves the filter panel open so callers can inspect or act on the row.
    """
    page.open_filter_panel()
    page.filter_by_email(CUSTOMER_EMAIL)
    page.apply_filters()
    return page.get_visible_row_count() > 0


def _restore_customer_name(browser):
    """
    Open the edit form for the managed customer (found by email) and reset
    the last name to CUSTOMER_LAST. Returns True on success, False if the
    customer was not found by email.
    """
    page = open_customers_page(browser)
    if not _find_customer_row_by_email(page):
        return False

    # Click Edit on the first matching row (filter is still active).
    row = page.wait.until(
        EC.visibility_of_element_located((By.XPATH, "//table//tr[td]"))
    )
    edit_btn = row.find_element(
        By.XPATH, ".//button[.//*[normalize-space()='Edit']]"
    )
    page.driver.execute_script("arguments[0].click();", edit_btn)
    page.wait_for_edit_loaded()

    page.enter_last_name(CUSTOMER_LAST)
    page.click_save_customer()
    page.wait_for_list_loaded()
    return True


def create_customer_if_missing(browser):
    """
    Ensure the managed customer exists with the correct name and email.

    Algorithm:
    1. Search the list by CUSTOMER_EMAIL.
       - Found with correct name  → nothing to do.
       - Found with wrong name    → open edit, restore CUSTOMER_LAST.
    2. Not found by email         → create fresh.
    3. Creation fails (name taken by different email) → print hint and re-raise.
    """
    page = open_customers_page(browser)

    if _find_customer_row_by_email(page):
        body = page.get_body_text()
        if CUSTOMER_LAST not in body:
            # Customer exists but was renamed — restore.
            _restore_customer_name(browser)
        return open_customers_page(browser)

    # Customer not found by email — create it.
    page = open_customers_page(browser)
    try:
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
    except Exception:
        next_slot = SLOT + 1
        print(
            f"\n[test_data] Customer '{CUSTOMER_LAST}' / '{CUSTOMER_EMAIL}' "
            f"could not be created.\n"
            f"  → Open tests/admin_portal/customers/test_data.py and set "
            f"SLOT = {next_slot}, then re-run."
        )
        raise

    return open_customers_page(browser)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def managed_customer(browser):
    """Ensure the managed customer exists before the test; restore after."""
    page = create_customer_if_missing(browser)
    yield page
    create_customer_if_missing(browser)
