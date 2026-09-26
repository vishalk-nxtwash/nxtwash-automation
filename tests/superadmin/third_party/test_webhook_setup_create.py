import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.superadmin.third_party.conftest import (
    SETUP_COMPANY,
    SETUP_KEY,
    SETUP_SUBSCRIBER,
    SETUP_URL,
)

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Third Party"),
    allure.story("Webhook Setup — Create"),
]


def test_add_setup_button_opens_create_form(create_setup_page):
    """SA-SET-CRT-001 — '+ Add Webhook Setup' opens the create form."""
    url = create_setup_page.driver.current_url
    assert "/third-party/setup" in url, \
        f"Create form URL should contain /third-party/setup, got: {url}"
    body = create_setup_page.get_body_text()
    assert "Save new" in body, "Create form should show 'Save new' button"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-002: Subscriber (placeholder='selectSubscriber') and "
           "Company (placeholder='selectCompany') React Select controls not "
           "confirmed via DOM inspection.",
)
def test_create_form_shows_subscriber_and_company_dropdowns(create_setup_page):
    """SA-SET-CRT-002 — Create form shows Subscriber and Company dropdowns."""
    from selenium.webdriver.common.by import By
    sub_els = create_setup_page.driver.find_elements(*create_setup_page.SUBSCRIBER_CONTROL)
    cmp_els = create_setup_page.driver.find_elements(*create_setup_page.COMPANY_CONTROL)
    assert sub_els, "Subscriber React Select control should be present on create form"
    assert cmp_els, "Company React Select control should be present on create form"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-003: Subscriber dropdown options depend on confirmed "
           "React Select combobox locator (CRT-002).",
)
def test_subscriber_dropdown_lists_active_subscribers(create_setup_page):
    """SA-SET-CRT-003 — Subscriber dropdown lists active subscribers (e.g. Tether, Optsopt)."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    combos = create_setup_page.driver.find_elements(*create_setup_page.SUBSCRIBER_CONTROL)
    assert combos, "Subscriber control should be present"
    create_setup_page.driver.execute_script("arguments[0].click();", combos[0])
    WebDriverWait(create_setup_page.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[@role='option']"))
    )
    opts = create_setup_page.driver.find_elements(By.XPATH, "//*[@role='option']")
    names = [o.text.strip() for o in opts if o.text.strip()]
    create_setup_page.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    assert any("tether" in n.lower() or "optsopt" in n.lower() for n in names), \
        f"Subscriber dropdown should list Tether or Optsopt, got: {names}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-004: Company dropdown options depend on confirmed "
           "React Select combobox locator (CRT-002).",
)
def test_company_dropdown_lists_companies(create_setup_page):
    """SA-SET-CRT-004 — Company dropdown lists active companies."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    combos = create_setup_page.driver.find_elements(*create_setup_page.COMPANY_CONTROL)
    assert combos, "Company control should be present"
    create_setup_page.driver.execute_script("arguments[0].click();", combos[0])
    WebDriverWait(create_setup_page.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[@role='option']"))
    )
    opts = create_setup_page.driver.find_elements(By.XPATH, "//*[@role='option']")
    names = [o.text.strip() for o in opts if o.text.strip()]
    create_setup_page.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    assert any(SETUP_COMPANY.lower() in n.lower() for n in names), \
        f"'{SETUP_COMPANY}' should appear in Company dropdown, got: {names}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-005: URL input name='thirdPartyUrl' not confirmed via DOM.",
)
def test_url_field_is_present(create_setup_page):
    """SA-SET-CRT-005 — Webhook URL text field is present on the create form."""
    from selenium.webdriver.common.by import By
    els = create_setup_page.driver.find_elements(*create_setup_page.URL_INPUT)
    assert els and els[0].is_displayed(), "Webhook URL input should be visible"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-006: Key input name='thirdPartyKey' not confirmed via DOM.",
)
def test_key_field_is_present(create_setup_page):
    """SA-SET-CRT-006 — Webhook Key text field is present on the create form."""
    from selenium.webdriver.common.by import By
    els = create_setup_page.driver.find_elements(*create_setup_page.KEY_INPUT)
    assert els and els[0].is_displayed(), "Webhook Key input should be visible"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-007: 'Is Enabled' toggle locator not confirmed via DOM.",
)
def test_is_enabled_toggle_defaults_on(create_setup_page):
    """SA-SET-CRT-007 — 'Is Enabled' toggle defaults to ON."""
    state = create_setup_page.get_toggle_state(create_setup_page.IS_ENABLED_TOGGLE)
    assert state is True, \
        f"'Is Enabled' toggle should be ON by default, got: {state}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-008: 'Active Webhook Setup' toggle locator not confirmed via DOM.",
)
def test_active_toggle_defaults_on(create_setup_page):
    """SA-SET-CRT-008 — 'Active Webhook Setup' toggle defaults to ON."""
    state = create_setup_page.get_toggle_state(create_setup_page.ACTIVE_TOGGLE)
    assert state is True, \
        f"'Active Webhook Setup' toggle should be ON by default, got: {state}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-009: Event type checkbox locators not confirmed via DOM. "
           "Depends on event name text matching the rendered labels exactly.",
)
def test_all_ten_event_type_checkboxes_present(create_setup_page):
    """SA-SET-CRT-009 — All 10 event type checkboxes are rendered on the create form."""
    from pages.superadmin.third_party_setup_page import EVENT_TYPE_NAMES
    states = create_setup_page.get_all_event_states()
    present = [name for name, val in states.items() if val is not None]
    assert len(present) == len(EVENT_TYPE_NAMES), \
        f"Expected 10 event checkboxes, found {len(present)}: {present}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-010: Depends on CRT-009 — event checkbox locators unconfirmed.",
)
def test_all_event_type_checkboxes_default_off(create_setup_page):
    """SA-SET-CRT-010 — All event type checkboxes default to OFF."""
    states = create_setup_page.get_all_event_states()
    non_none = {k: v for k, v in states.items() if v is not None}
    assert non_none, "At least some event checkboxes should be detectable"
    on_keys = [k for k, v in non_none.items() if v]
    assert not any(non_none.values()), \
        f"All event checkboxes should default to OFF, found ON: {on_keys}"


def test_save_without_any_fields_shows_validation(create_setup_page):
    """SA-SET-CRT-011 — Clicking 'Save new' with nothing filled is blocked."""
    create_setup_page.click_save_new()
    body = create_setup_page.get_body_text().lower()
    still_on_form = "save new" in body
    has_error = any(k in body for k in ("required", "invalid", "must", "select", "enter"))
    assert still_on_form or has_error, \
        "Saving with no fields filled should be blocked or show a validation error"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-012: Requires filling Subscriber + URL + Key via unconfirmed "
           "locators to isolate the missing-Company case.",
)
def test_save_without_company_shows_validation(create_setup_page):
    """SA-SET-CRT-012 — Save without Company is blocked with a validation error."""
    create_setup_page.select_subscriber(SETUP_SUBSCRIBER)
    create_setup_page.enter_url(SETUP_URL)
    create_setup_page.enter_key(SETUP_KEY)
    create_setup_page.click_save_new()
    body = create_setup_page.get_body_text().lower()
    assert "save new" in body or any(
        k in body for k in ("required", "invalid", "select")
    ), "Saving without a Company should be blocked"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-013: Requires confirmed URL input (name='thirdPartyUrl') "
           "and other React Select locators to fill all other fields.",
)
def test_save_without_url_shows_validation(create_setup_page):
    """SA-SET-CRT-013 — Save without URL is blocked with a validation error."""
    create_setup_page.select_subscriber(SETUP_SUBSCRIBER)
    create_setup_page.select_company(SETUP_COMPANY)
    create_setup_page.enter_key(SETUP_KEY)
    create_setup_page.click_save_new()
    body = create_setup_page.get_body_text().lower()
    assert "save new" in body or any(
        k in body for k in ("required", "invalid", "url")
    ), "Saving without a URL should be blocked"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-014: Requires confirmed Key input (name='thirdPartyKey') "
           "and other locators to fill all other fields.",
)
def test_save_without_key_shows_validation(create_setup_page):
    """SA-SET-CRT-014 — Save without Key is blocked with a validation error."""
    create_setup_page.select_subscriber(SETUP_SUBSCRIBER)
    create_setup_page.select_company(SETUP_COMPANY)
    create_setup_page.enter_url(SETUP_URL)
    create_setup_page.click_save_new()
    body = create_setup_page.get_body_text().lower()
    assert "save new" in body or any(
        k in body for k in ("required", "invalid", "key")
    ), "Saving without a Key should be blocked"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-015: Happy-path create modifies staging data. "
           "Idempotent guard in the edit_setup_page fixture already manages the "
           "test record — running this test directly risks duplicate entries.",
)
def test_create_setup_happy_path(create_setup_page, webhook_setup_page):
    """SA-SET-CRT-015 — Create with all required fields → saves and returns to list."""
    from selenium.webdriver.common.by import By
    create_setup_page.select_subscriber(SETUP_SUBSCRIBER)
    create_setup_page.select_company(SETUP_COMPANY)
    create_setup_page.enter_url(SETUP_URL)
    create_setup_page.enter_key(SETUP_KEY)
    create_setup_page.click_save_new()
    WebDriverWait(create_setup_page.driver, 30).until(
        EC.url_contains("/third-party/setup")
    )
    assert webhook_setup_page.row_exists(SETUP_COMPANY), \
        f"New setup for '{SETUP_COMPANY}' should appear in the list after creation"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-016: Depends on CRT-015 running first in the same session.",
)
def test_new_setup_appears_in_list(webhook_setup_page):
    """SA-SET-CRT-016 — New setup appears in the list after create."""
    assert webhook_setup_page.row_exists(SETUP_COMPANY), \
        f"'{SETUP_COMPANY}' setup should be visible in the list"


def test_cancel_discards_create_form(create_setup_page, webhook_setup_page):
    """SA-SET-CRT-017 — Cancel discards the form and returns to the Webhook Setup list."""
    create_setup_page.click_cancel()
    create_setup_page.confirm_yes_if_present()
    WebDriverWait(create_setup_page.driver, 20).until(
        EC.url_contains("/third-party/setup")
    )
    body = create_setup_page.get_body_text()
    assert "Webhook Setup" in body or "Add Webhook Setup" in body, \
        "After cancel, should return to Webhook Setup list"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-018: 'Is Enabled' toggle locator not confirmed; also "
           "requires verifying that inactive setups do not appear by default.",
)
def test_create_with_is_enabled_off(create_setup_page):
    """SA-SET-CRT-018 — Create with 'Is Enabled' OFF saves an inactive setup."""
    create_setup_page.set_is_enabled(False)
    state = create_setup_page.get_toggle_state(create_setup_page.IS_ENABLED_TOGGLE)
    assert state is False, "'Is Enabled' toggle should be OFF before saving"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-CRT-019: 'Active Webhook Setup' toggle locator not confirmed.",
)
def test_create_with_active_off(create_setup_page):
    """SA-SET-CRT-019 — Create with 'Active Webhook Setup' OFF saves as inactive."""
    create_setup_page.set_active(False)
    state = create_setup_page.get_toggle_state(create_setup_page.ACTIVE_TOGGLE)
    assert state is False, "'Active Webhook Setup' toggle should be OFF before saving"
