import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.superadmin.third_party.conftest import SETUP_COMPANY, SETUP_KEY, SETUP_URL

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Third Party"),
    allure.story("Webhook Setup — Edit"),
]


def test_edit_opens_form_at_correct_url(edit_setup_page):
    """SA-SET-EDT-001 — Edit button opens the edit form at /third-party/setup/{id}."""
    url = edit_setup_page.driver.current_url
    assert "/third-party/setup/" in url and "/create" not in url, \
        f"Edit URL should be /third-party/setup/{{id}}, got: {url}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-EDT-002: Pre-filled Subscriber and Company React Select values "
           "depend on confirmed combobox locators — pre-fill reading pattern unconfirmed.",
)
def test_edit_form_prefills_subscriber_and_company(edit_setup_page):
    """SA-SET-EDT-002 — Edit form pre-fills the Subscriber and Company selectors."""
    from selenium.webdriver.common.by import By
    body = edit_setup_page.get_body_text()
    assert SETUP_COMPANY.lower() in body.lower(), \
        f"Edit form should show '{SETUP_COMPANY}' as the selected company"
    assert "Tether" in body or "tether" in body.lower(), \
        "Edit form should show the selected subscriber name"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-EDT-003: URL field name='thirdPartyUrl' not confirmed — "
           "get_attribute('value') may return empty if the name is wrong.",
)
def test_edit_form_prefills_url(edit_setup_page):
    """SA-SET-EDT-003 — Edit form pre-fills the Webhook URL field."""
    url_val = edit_setup_page.get_url_value()
    assert url_val, "Webhook URL field should be pre-filled on the edit form"
    assert "nxtwash" in url_val.lower() or "webhook" in url_val.lower(), \
        f"Pre-filled URL should contain 'nxtwash' or 'webhook', got: '{url_val}'"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-EDT-004: Key field name='thirdPartyKey' not confirmed — "
           "get_attribute('value') may return empty if the name is wrong.",
)
def test_edit_form_prefills_key(edit_setup_page):
    """SA-SET-EDT-004 — Edit form pre-fills the Webhook Key field."""
    key_val = edit_setup_page.get_key_value()
    assert key_val, "Webhook Key field should be pre-filled on the edit form"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-EDT-005: Requires confirmed URL input name + Save changes button "
           "to reliably edit and verify persistence.",
)
def test_editing_url_persists(edit_setup_page, webhook_setup_page):
    """SA-SET-EDT-005 — Editing the Webhook URL and saving persists the change."""
    updated_url = SETUP_URL + "/updated"
    edit_setup_page.set_url(updated_url)
    edit_setup_page.click_save_changes()
    edit_setup_page.confirm_yes_if_present()

    WebDriverWait(edit_setup_page.driver, 30).until(
        EC.url_contains("/third-party/setup")
    )
    # Reopen and verify, then restore
    webhook_setup_page.wait_for_loaded()
    webhook_setup_page.filter_by_company_name(SETUP_COMPANY)
    webhook_setup_page.open_edit(SETUP_COMPANY)
    from pages.superadmin.third_party_setup_page import EditSetupPage
    restore_page = EditSetupPage(edit_setup_page.driver)
    restore_page.wait_for_loaded()
    val = restore_page.get_url_value()
    assert updated_url in val, \
        f"Updated URL should persist, expected '{updated_url}', got '{val}'"
    restore_page.set_url(SETUP_URL)
    restore_page.click_save_changes()
    restore_page.confirm_yes_if_present()
    WebDriverWait(edit_setup_page.driver, 30).until(
        EC.url_contains("/third-party/setup")
    )


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-EDT-006: Requires confirmed Key input name + save interaction.",
)
def test_editing_key_persists(edit_setup_page, webhook_setup_page):
    """SA-SET-EDT-006 — Editing the Webhook Key and saving persists the change."""
    updated_key = SETUP_KEY + "_upd"
    edit_setup_page.set_key(updated_key)
    edit_setup_page.click_save_changes()
    edit_setup_page.confirm_yes_if_present()

    WebDriverWait(edit_setup_page.driver, 30).until(
        EC.url_contains("/third-party/setup")
    )
    webhook_setup_page.wait_for_loaded()
    webhook_setup_page.filter_by_company_name(SETUP_COMPANY)
    webhook_setup_page.open_edit(SETUP_COMPANY)
    from pages.superadmin.third_party_setup_page import EditSetupPage
    restore_page = EditSetupPage(edit_setup_page.driver)
    restore_page.wait_for_loaded()
    val = restore_page.get_key_value()
    assert updated_key in val, \
        f"Updated key should persist, expected '{updated_key}', got '{val}'"
    restore_page.set_key(SETUP_KEY)
    restore_page.click_save_changes()
    restore_page.confirm_yes_if_present()
    WebDriverWait(edit_setup_page.driver, 30).until(
        EC.url_contains("/third-party/setup")
    )


@pytest.mark.xfail(
    strict=False,
    reason="SA-SET-EDT-007: Editing event type selections depends on confirmed "
           "event checkbox locators (SA-SET-EVT-003).",
)
def test_editing_event_types_persists(edit_setup_page):
    """SA-SET-EDT-007 — Editing event type selections and saving persists the change."""
    from pages.superadmin.third_party_setup_page import EVENT_TYPE_NAMES
    event = EVENT_TYPE_NAMES[2]
    current = edit_setup_page.get_all_event_states().get(event)
    edit_setup_page.set_event(event, not current)
    edit_setup_page.click_save_changes()
    edit_setup_page.confirm_yes_if_present()
    WebDriverWait(edit_setup_page.driver, 30).until(
        EC.url_contains("/third-party/setup")
    )


@pytest.mark.skip(
    reason="SA-SET-EDT-008: 'Auto=No' / Auto progression OFF cannot be engineered "
           "on staging without additional setup — skip for manual verification."
)
def test_edit_setup_with_auto_no():
    """SA-SET-EDT-008 — Edit a setup with Auto=No — document behaviour."""
    pass


def test_cancel_on_edit_discards_changes(edit_setup_page, webhook_setup_page):
    """SA-SET-EDT-009 — Cancel on Edit discards changes — setup is unchanged."""
    original_url = edit_setup_page.get_url_value()
    edit_setup_page.set_url("https://should-not-persist.example.com/")
    edit_setup_page.click_cancel()
    edit_setup_page.confirm_yes_if_present()

    WebDriverWait(edit_setup_page.driver, 20).until(
        EC.url_contains("/third-party/setup")
    )
    webhook_setup_page.wait_for_loaded()
    webhook_setup_page.filter_by_company_name(SETUP_COMPANY)
    webhook_setup_page.open_edit(SETUP_COMPANY)
    from pages.superadmin.third_party_setup_page import EditSetupPage
    verify_page = EditSetupPage(edit_setup_page.driver)
    verify_page.wait_for_loaded()
    current_url = verify_page.get_url_value()
    assert "should-not-persist" not in current_url, \
        "Cancelled URL change should NOT have been saved"


@pytest.mark.skip(
    reason="SA-SET-ACC-001: Access-control test requires a non-Superadmin browser "
           "session — no such fixture exists in this suite."
)
def test_non_superadmin_cannot_reach_setup():
    """SA-SET-ACC-001 — A non-Superadmin cannot reach /third-party/setup."""
    pass
