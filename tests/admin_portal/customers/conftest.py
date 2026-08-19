import pytest
from selenium.common.exceptions import TimeoutException
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

# Set to True after _restore_customer_state runs at least once this session,
# guaranteeing the phone number is written to the managed customer in the DB.
_phone_ensured_this_session = False


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
    Turns off the Active-accounts-only toggle so inactive customers are visible.
    Leaves the filter panel open so callers can inspect or act on the row.
    """
    page.open_filter_panel()
    page.ensure_active_filter_off()
    page.filter_by_email(CUSTOMER_EMAIL)
    page.apply_filters()
    return page.get_visible_row_count() > 0


def _restore_customer_state(browser):
    """
    Find the managed customer by email (active or inactive), open edit, restore
    the correct last name, ensure the Active switch is ON, then save.
    Returns True on success, False if the customer was not found.
    """
    page = open_customers_page(browser)
    if not _find_customer_row_by_email(page):
        return False

    row = page.wait.until(
        EC.visibility_of_element_located((By.XPATH, "//table//tr[td]"))
    )
    edit_btn = row.find_element(
        By.XPATH, ".//button[.//*[normalize-space()='Edit']]"
    )
    page.driver.execute_script("arguments[0].click();", edit_btn)
    page.wait_for_edit_loaded()

    if page.get_last_name_value() != CUSTOMER_LAST:
        page.enter_last_name(CUSTOMER_LAST)
    # Always re-set phone so the managed customer reliably has it,
    # even if it was created in a prior session without a phone number.
    page.enter_phone(CUSTOMER_PHONE)
    page.ensure_active_switch_on()
    page.click_save_customer()
    # Staging may not redirect to the list after save; let create_customer_if_missing
    # handle navigation via its own open_customers_page() call.
    try:
        page.wait_for_list_loaded()
    except TimeoutException:
        pass
    return True


def create_customer_if_missing(browser):
    """
    Ensure the managed customer exists, is active, and has the correct name.

    Algorithm:
    1. Filter by email with active-only ON (default — no toggle manipulation).
       Found + correct name → customer is healthy; return immediately (no edit/save).
       Found + wrong name  → restore (name fix needed).
    2. Not found with active-only ON → try with active-only OFF.
       Found  → customer is deactivated → restore (reactivate + fix name).
       Not found → customer doesn't exist → create.
    Always clears any active filter before returning so subsequent tests start clean.
    """
    page = open_customers_page(browser)

    # ── Phase 1: quick check — is customer active with the correct name? ──────
    page.open_filter_panel()
    page.filter_by_email(CUSTOMER_EMAIL)
    page.apply_filters()

    if page.get_visible_row_count() > 0:
        # Customer IS active (visible with default active-only ON).
        # Quick row scan — no waiting — to see if the name is already correct.
        rows_with_name = [
            el for el in page.driver.find_elements(
                By.XPATH,
                # Exact match on any cell so "auto customer1 edited" does NOT
                # satisfy a check for "auto customer1" — it falls through to restore.
                "//table//tr[td and .//*[normalize-space()='%s']]"
                % CUSTOMER_LAST,
            )
            if el.is_displayed()
        ]
        if rows_with_name:
            # Active and correct name.
            # On the first call this session, run restore once to guarantee the
            # phone number is written to the DB (it may have been missing if the
            # customer was created before the enter_phone fix was added).
            global _phone_ensured_this_session
            if not _phone_ensured_this_session:
                _phone_ensured_this_session = True
                _restore_customer_state(browser)
            page = open_customers_page(browser)
            page._reset_active_filter_if_present()
            return page
        # Active but name is wrong — fall through to _restore_customer_state.
        # ensure_active_switch_on() returns immediately for an already-active
        # customer (no API call, no phone-clearing side effect).

    else:
        # ── Phase 2: not found with active-only ON — try with active-only OFF ─
        # Navigate fresh so React state is clean before toggling the filter.
        # The filter panel closes after Phase 1's apply_filters(), leaving the
        # toggle in an uncertain state that JS clicks can't reliably update.
        page = open_customers_page(browser)
        if not _find_customer_row_by_email(page):
            # Customer truly doesn't exist — create it.
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
            except Exception as _exc:
                # A parallel worker may have created the customer a moment ago;
                # do one more search (with active-only OFF) before giving up.
                try:
                    _recovery = open_customers_page(browser)
                    if _find_customer_row_by_email(_recovery):
                        _recovery = open_customers_page(browser)
                        _recovery._reset_active_filter_if_present()
                        return _recovery
                except Exception:
                    pass
                next_slot = SLOT + 1
                print(
                    f"\n[test_data] Customer '{CUSTOMER_LAST}' / '{CUSTOMER_EMAIL}' "
                    f"could not be created.\n"
                    f"  → Open tests/admin_portal/customers/test_data.py and set "
                    f"SLOT = {next_slot}, then re-run."
                )
                raise _exc
            page = open_customers_page(browser)
            page._reset_active_filter_if_present()
            return page
        # Customer found with active-only OFF → it's deactivated → restore.

    # ── Restore: reactivate and/or correct the name ───────────────────────────
    _restore_customer_state(browser)
    page = open_customers_page(browser)
    page._reset_active_filter_if_present()
    return page


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def managed_customer(browser):
    """Ensure the managed customer exists before the test; restore after."""
    page = create_customer_if_missing(browser)
    yield page
    create_customer_if_missing(browser)
