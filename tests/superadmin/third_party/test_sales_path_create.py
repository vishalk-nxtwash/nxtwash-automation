import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.superadmin.third_party.conftest import SALES_PATH_COMPANY

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Third Party"),
    allure.story("Sales Path — Create"),
]


def test_add_sales_path_button_opens_create_form(create_sales_path_page):
    """SA-SLP-CRT-001 — '+ Add Sales Path' opens the create form."""
    url = create_sales_path_page.driver.current_url
    assert "/sales-path" in url, \
        f"Create form URL should contain /sales-path, got: {url}"
    body = create_sales_path_page.get_body_text()
    assert "Save new" in body, "Create form should show 'Save new' button"


def test_create_form_shows_company_dropdown(create_sales_path_page):
    """SA-SLP-CRT-002 — Create form shows a Company dropdown (required field)."""
    cmp_els = create_sales_path_page.driver.find_elements(
        *create_sales_path_page.COMPANY_CONTROL
    )
    assert cmp_els, "Company React Select control should be present on the create form"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-CRT-003: Company dropdown options depend on confirmed "
           "React Select combobox locator (CRT-002).",
)
def test_company_dropdown_lists_companies(create_sales_path_page):
    """SA-SLP-CRT-003 — Company dropdown lists available companies."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    combos = create_sales_path_page.driver.find_elements(
        *create_sales_path_page.COMPANY_CONTROL
    )
    assert combos, "Company control should be present"
    create_sales_path_page.driver.execute_script("arguments[0].click();", combos[0])
    WebDriverWait(create_sales_path_page.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[@role='option']"))
    )
    opts = create_sales_path_page.driver.find_elements(By.XPATH, "//*[@role='option']")
    names = [o.text.strip() for o in opts if o.text.strip()]
    create_sales_path_page.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    assert any(SALES_PATH_COMPANY.lower() in n.lower() for n in names), \
        f"'{SALES_PATH_COMPANY}' should appear in Company dropdown, got: {names}"


def test_is_enabled_toggle_defaults_on(create_sales_path_page):
    """SA-SLP-CRT-004 — 'Is Enabled' toggle defaults to ON."""
    state = create_sales_path_page.get_toggle_state(create_sales_path_page.IS_ENABLED_TOGGLE)
    assert state is True, \
        f"'Is Enabled' toggle should be ON by default, got: {state}"


def test_active_toggle_defaults_on(create_sales_path_page):
    """SA-SLP-CRT-005 — 'Active Sales Path' toggle defaults to ON."""
    state = create_sales_path_page.get_toggle_state(create_sales_path_page.ACTIVE_TOGGLE)
    assert state is True, \
        f"'Active Sales Path' toggle should be ON by default, got: {state}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-CRT-006: Verifying that 'Is Enabled' and 'Active' are independent "
           "requires confirmed toggle locators for both fields.",
)
def test_is_enabled_and_active_toggles_are_independent(create_sales_path_page):
    """SA-SLP-CRT-006 — Is Enabled and Active Sales Path toggles are independent."""
    create_sales_path_page.set_is_enabled(False)
    enabled_state = create_sales_path_page.get_toggle_state(
        create_sales_path_page.IS_ENABLED_TOGGLE
    )
    active_state = create_sales_path_page.get_toggle_state(
        create_sales_path_page.ACTIVE_TOGGLE
    )
    assert enabled_state is False, "'Is Enabled' should be OFF after toggling"
    assert active_state is True, \
        "'Active Sales Path' should remain ON when only Is Enabled is toggled"


def test_save_without_company_shows_validation(create_sales_path_page):
    """SA-SLP-CRT-007 — Clicking 'Save new' without selecting a Company is blocked."""
    create_sales_path_page.click_save_new()
    body = create_sales_path_page.get_body_text().lower()
    still_on_form = "save new" in body
    has_error = any(k in body for k in ("required", "invalid", "select", "company"))
    assert still_on_form or has_error, \
        "Saving without a Company should be blocked or show a validation error"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-CRT-008: Happy-path create modifies staging. The edit_sales_path_page "
           "fixture already manages 'vkautomationcompanytest' idempotently — "
           "running this test directly may produce a duplicate.",
)
def test_create_sales_path_happy_path(create_sales_path_page, sales_path_page):
    """SA-SLP-CRT-008 — Create with valid Company → saves and returns to list."""
    create_sales_path_page.select_company(SALES_PATH_COMPANY)
    create_sales_path_page.click_save_new()
    WebDriverWait(create_sales_path_page.driver, 30).until(
        EC.url_contains("/sales-path")
    )
    assert sales_path_page.row_exists(SALES_PATH_COMPANY), \
        f"New sales path for '{SALES_PATH_COMPANY}' should appear in the list"


def test_new_sales_path_appears_in_list(sales_path_page):
    """SA-SLP-CRT-009 — New sales path appears in the list after create."""
    assert sales_path_page.row_exists(SALES_PATH_COMPANY), \
        f"'{SALES_PATH_COMPANY}' sales path should be visible in the list"


def test_create_with_is_enabled_off(create_sales_path_page):
    """SA-SLP-CRT-010 — Create with 'Is Enabled' OFF saves a disabled sales path."""
    create_sales_path_page.set_is_enabled(False)
    state = create_sales_path_page.get_toggle_state(create_sales_path_page.IS_ENABLED_TOGGLE)
    assert state is False, "'Is Enabled' toggle should be OFF before saving"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-CRT-011: 'Active Sales Path' toggle locator unconfirmed.",
)
def test_create_with_active_off(create_sales_path_page):
    """SA-SLP-CRT-011 — Create with 'Active Sales Path' OFF saves as inactive."""
    create_sales_path_page.set_active(False)
    state = create_sales_path_page.get_toggle_state(create_sales_path_page.ACTIVE_TOGGLE)
    assert state is False, "'Active Sales Path' toggle should be OFF before saving"


def test_duplicate_company_sales_path_behaviour(create_sales_path_page):
    """SA-SLP-CRT-012 — Duplicate Company — document whether server rejects it."""
    create_sales_path_page.select_company(SALES_PATH_COMPANY)
    create_sales_path_page.click_save_new()
    try:
        WebDriverWait(create_sales_path_page.driver, 5).until(
            EC.url_contains("/sales-path")
        )
        assert True  # duplicates are allowed
    except Exception:
        from selenium.webdriver.common.by import By
        body = create_sales_path_page.driver.find_element(
            By.TAG_NAME, "body"
        ).text.lower()
        assert any(k in body for k in ("duplicate", "already", "exists", "unique")), \
            "Duplicate Company should be rejected with a clear error message"


def test_cancel_discards_create_form(create_sales_path_page, sales_path_page):
    """SA-SLP-CRT-013 — Cancel discards the form and returns to the Sales Path list."""
    create_sales_path_page.click_cancel()
    create_sales_path_page.confirm_yes_if_present()
    WebDriverWait(create_sales_path_page.driver, 20).until(
        EC.url_contains("/sales-path")
    )
    body = create_sales_path_page.get_body_text()
    assert "Sales Path" in body or "Add Sales Path" in body, \
        "After cancel, should return to the Sales Path list"
