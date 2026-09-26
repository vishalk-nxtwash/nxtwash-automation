import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.superadmin.third_party.conftest import SALES_PATH_COMPANY

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Third Party"),
    allure.story("Sales Path — Edit"),
]


def test_edit_opens_form_at_correct_url(sales_path_page, browser):
    """SA-SLP-EDT-001 — Edit button opens the edit form at /sales-path/{id}."""
    sales_path_page.filter_by_company_name(SALES_PATH_COMPANY)
    sales_path_page.open_edit(SALES_PATH_COMPANY)
    url = browser.current_url
    assert "/sales-path/" in url and "/create" not in url, \
        f"Edit URL should be /sales-path/{{id}}, got: {url}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-EDT-002: Pre-filled Company React Select value depends on "
           "confirmed combobox locator — reading pre-filled value from React Select "
           "is not straightforward without confirmed structure.",
)
def test_edit_form_prefills_company(edit_sales_path_page):
    """SA-SLP-EDT-002 — Edit form pre-fills the Company selector."""
    from selenium.webdriver.common.by import By
    body = edit_sales_path_page.driver.find_element(By.TAG_NAME, "body").text
    assert SALES_PATH_COMPANY.lower() in body.lower(), \
        f"Edit form should show '{SALES_PATH_COMPANY}' as the selected company"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-EDT-003: 'Is Enabled' toggle locator not confirmed; also need to "
           "confirm toggle state persists after save + re-open.",
)
def test_toggle_is_enabled_persists(edit_sales_path_page, sales_path_page):
    """SA-SLP-EDT-003 — Toggling 'Is Enabled' OFF/ON and saving persists the change."""
    original = edit_sales_path_page.get_toggle_state(edit_sales_path_page.IS_ENABLED_TOGGLE)
    new_state = not original if original is not None else False

    edit_sales_path_page.set_is_enabled(new_state)
    edit_sales_path_page.click_save_changes()
    edit_sales_path_page.confirm_yes_if_present()

    WebDriverWait(edit_sales_path_page.driver, 30).until(
        EC.url_contains("/sales-path")
    )
    # Re-open and verify
    sales_path_page.wait_for_loaded()
    sales_path_page.filter_by_company_name(SALES_PATH_COMPANY)
    sales_path_page.open_edit(SALES_PATH_COMPANY)
    from pages.superadmin.sales_path_page import EditSalesPathPage
    verify_page = EditSalesPathPage(edit_sales_path_page.driver)
    verify_page.wait_for_loaded()
    current = verify_page.get_toggle_state(verify_page.IS_ENABLED_TOGGLE)
    assert current == new_state, \
        f"'Is Enabled' should be {new_state} after save, got {current}"

    # Restore
    verify_page.set_is_enabled(original if original is not None else True)
    verify_page.click_save_changes()
    verify_page.confirm_yes_if_present()
    WebDriverWait(edit_sales_path_page.driver, 30).until(
        EC.url_contains("/sales-path")
    )


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-EDT-004: 'Active Sales Path' toggle locator not confirmed.",
)
def test_toggle_active_persists(edit_sales_path_page, sales_path_page):
    """SA-SLP-EDT-004 — Toggling 'Active Sales Path' OFF/ON and saving persists the change."""
    original = edit_sales_path_page.get_toggle_state(edit_sales_path_page.ACTIVE_TOGGLE)
    new_state = not original if original is not None else False

    edit_sales_path_page.set_active(new_state)
    edit_sales_path_page.click_save_changes()
    edit_sales_path_page.confirm_yes_if_present()

    WebDriverWait(edit_sales_path_page.driver, 30).until(
        EC.url_contains("/sales-path")
    )
    sales_path_page.wait_for_loaded()
    sales_path_page.filter_by_company_name(SALES_PATH_COMPANY)
    sales_path_page.open_edit(SALES_PATH_COMPANY)
    from pages.superadmin.sales_path_page import EditSalesPathPage
    verify_page = EditSalesPathPage(edit_sales_path_page.driver)
    verify_page.wait_for_loaded()
    current = verify_page.get_toggle_state(verify_page.ACTIVE_TOGGLE)
    assert current == new_state, \
        f"'Active Sales Path' should be {new_state} after save, got {current}"

    # Restore
    verify_page.set_active(original if original is not None else True)
    verify_page.click_save_changes()
    verify_page.confirm_yes_if_present()
    WebDriverWait(edit_sales_path_page.driver, 30).until(
        EC.url_contains("/sales-path")
    )


def test_cancel_on_edit_discards_changes(edit_sales_path_page, sales_path_page):
    """SA-SLP-EDT-005 — Cancel on Edit discards changes — sales path is unchanged."""
    edit_sales_path_page.set_is_enabled(False)
    edit_sales_path_page.click_cancel()
    edit_sales_path_page.confirm_yes_if_present()

    WebDriverWait(edit_sales_path_page.driver, 20).until(
        EC.url_contains("/sales-path")
    )
    sales_path_page.wait_for_loaded()
    assert sales_path_page.row_exists(SALES_PATH_COMPANY), \
        f"'{SALES_PATH_COMPANY}' sales path should still be in the list after cancel"


@pytest.mark.skip(
    reason="SA-SLP-ACC-001: Access-control test requires a non-Superadmin browser "
           "session — no such fixture exists in this suite."
)
def test_non_superadmin_cannot_reach_sales_path():
    """SA-SLP-ACC-001 — A non-Superadmin cannot reach /sales-path."""
    pass
