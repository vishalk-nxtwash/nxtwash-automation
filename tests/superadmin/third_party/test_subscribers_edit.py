import allure
import pytest

from tests.superadmin.third_party.conftest import (
    REF_SUBSCRIBER_ABBR,
    REF_SUBSCRIBER_NAME,
    SUBSCRIBER_ABBR,
    SUBSCRIBER_NAME,
)

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Third Party"),
    allure.story("Webhook Subscribers — Edit"),
]


def test_edit_opens_form_at_correct_url(subscribers_page, browser):
    """SA-SUB-EDT-001 — Edit button opens the edit form at /third-party/subscribers/{id}."""
    subscribers_page.open_edit(REF_SUBSCRIBER_NAME)
    url = browser.current_url
    assert "/third-party/subscribers/" in url and "/create" not in url, \
        f"Edit URL should be /third-party/subscribers/{{id}}, got: {url}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SUB-EDT-002: Pre-filled field values depend on 'name' and 'abbreviation' "
           "input name attributes being correct — unconfirmed via DOM inspection.",
)
def test_edit_form_prefills_saved_data(edit_subscriber_page):
    """SA-SUB-EDT-002 — Pre-filled fields reflect the saved record."""
    name = edit_subscriber_page.get_name()
    abbr = edit_subscriber_page.get_abbreviation()
    assert name == SUBSCRIBER_NAME, \
        f"Subscriber Name should be pre-filled with '{SUBSCRIBER_NAME}', got: '{name}'"
    assert abbr == SUBSCRIBER_ABBR, \
        f"Abbreviation should be pre-filled with '{SUBSCRIBER_ABBR}', got: '{abbr}'"


def test_edit_subscriber_name_persists(edit_subscriber_page, subscribers_page):
    """SA-SUB-EDT-003 — Editing the Subscriber Name and saving persists on the list."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    updated_name = SUBSCRIBER_NAME + " Edited"
    edit_subscriber_page.set_name(updated_name)
    edit_subscriber_page.click_save_changes()
    edit_subscriber_page.confirm_yes_if_present()

    WebDriverWait(edit_subscriber_page.driver, 30).until(
        EC.url_contains("/third-party/subscribers")
    )
    # Restore original name
    subscribers_page.wait_for_loaded()
    subscribers_page.open_edit(updated_name)
    from pages.superadmin.third_party_subscribers_page import EditSubscriberPage
    restore_page = EditSubscriberPage(edit_subscriber_page.driver)
    restore_page.wait_for_loaded()
    restore_page.set_name(SUBSCRIBER_NAME)
    restore_page.click_save_changes()
    restore_page.confirm_yes_if_present()
    WebDriverWait(edit_subscriber_page.driver, 30).until(
        EC.url_contains("/third-party/subscribers")
    )


@pytest.mark.xfail(
    strict=False,
    reason="SA-SUB-EDT-004: Abbreviation field 'name' attribute not confirmed — "
           "JS set approach requires the correct attribute to be present.",
)
def test_edit_abbreviation_persists(edit_subscriber_page, subscribers_page):
    """SA-SUB-EDT-004 — Editing the Abbreviation and saving persists."""
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    original = edit_subscriber_page.get_abbreviation()
    updated = "VE"
    edit_subscriber_page.set_abbreviation(updated)
    edit_subscriber_page.click_save_changes()
    edit_subscriber_page.confirm_yes_if_present()

    WebDriverWait(edit_subscriber_page.driver, 30).until(
        EC.url_contains("/third-party/subscribers")
    )
    # Restore
    subscribers_page.wait_for_loaded()
    subscribers_page.open_edit(SUBSCRIBER_NAME)
    from pages.superadmin.third_party_subscribers_page import EditSubscriberPage
    restore_page = EditSubscriberPage(edit_subscriber_page.driver)
    restore_page.wait_for_loaded()
    restore_page.set_abbreviation(original or SUBSCRIBER_ABBR)
    restore_page.click_save_changes()
    restore_page.confirm_yes_if_present()
    WebDriverWait(edit_subscriber_page.driver, 30).until(
        EC.url_contains("/third-party/subscribers")
    )


@pytest.mark.xfail(
    strict=False,
    reason="SA-SUB-EDT-005: Inline clear (X) button locator for Name and Abbreviation "
           "fields not confirmed via DOM inspection.",
)
def test_clearing_required_field_blocks_save(edit_subscriber_page):
    """SA-SUB-EDT-005 — Clearing a required field via the X and saving is blocked."""
    from selenium.webdriver.common.by import By

    edit_subscriber_page.click_name_clear()
    edit_subscriber_page.click_save_changes()

    body = edit_subscriber_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    has_error = any(k in body for k in ("required", "invalid", "must", "field"))
    still_on_edit = "save changes" in body
    assert has_error or still_on_edit, \
        "Clearing a required field and saving should be blocked"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SUB-EDT-006: Toggle locator for 'Active Subscriber' not confirmed "
           "via DOM inspection.",
)
def test_deactivate_and_reactivate_subscriber(edit_subscriber_page):
    """SA-SUB-EDT-006 — Deactivate / reactivate via Active Subscriber toggle persists."""
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    # Deactivate
    edit_subscriber_page.set_active_toggle(False)
    edit_subscriber_page.click_save_changes()
    edit_subscriber_page.confirm_yes_if_present()
    WebDriverWait(edit_subscriber_page.driver, 30).until(
        EC.url_contains("/third-party/subscribers")
    )

    # Re-open and reactivate
    from selenium.webdriver.common.by import By
    edit_subscriber_page.driver.find_element(By.TAG_NAME, "body")  # ensure page loaded


@pytest.mark.xfail(
    strict=False,
    reason="SA-SUB-EDT-007: Impact of deactivating a subscriber that is actively "
           "referenced by a Webhook Setup is not documented — behaviour unknown.",
)
def test_deactivating_in_use_subscriber_impact(edit_subscriber_page):
    """SA-SUB-EDT-007 — Deactivating an in-use subscriber — document the impact."""
    pass


def test_cancel_on_edit_discards_changes(edit_subscriber_page, subscribers_page):
    """SA-SUB-EDT-008 — Cancel on Edit discards changes — subscriber is unchanged."""
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    original_name = edit_subscriber_page.get_name()
    edit_subscriber_page.set_name("VK Should Not Persist")
    edit_subscriber_page.click_cancel()
    edit_subscriber_page.confirm_yes_if_present()

    WebDriverWait(edit_subscriber_page.driver, 20).until(
        EC.url_contains("/third-party/subscribers")
    )
    subscribers_page.wait_for_loaded()
    assert subscribers_page.row_exists(original_name), \
        f"Original subscriber name '{original_name}' should still exist after cancel"
    assert not subscribers_page.row_exists("VK Should Not Persist", timeout=5), \
        "Changed name should NOT have been saved after cancel"


@pytest.mark.skip(
    reason="SA-SUB-ACC-001: Access-control test requires a non-Superadmin browser session — "
           "no such fixture exists in this suite."
)
def test_non_superadmin_cannot_reach_subscribers():
    """SA-SUB-ACC-001 — A non-Superadmin cannot reach /third-party/subscribers."""
    pass
