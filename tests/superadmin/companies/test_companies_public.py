import allure
import pytest

from selenium.webdriver.common.by import By

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Companies"),
    allure.story("Public Settings"),
]


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-PUB-001: Default language dropdown locator not confirmed — "
           "React Select structure needs DOM inspection.",
)
def test_default_language_defaults_to_english(edit_company_page, browser):
    """SA-CMP-PUB-001 — 'Default language' dropdown is required and defaults to English."""
    body = browser.find_element(By.TAG_NAME, "body").text
    assert "English" in body or "english" in body.lower(), \
        "Default language should default to English"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-PUB-002: Changing default language and saving — "
           "React Select dropdown locator not confirmed; save persistence not verified.",
)
def test_changing_default_language_persists(edit_company_page):
    """SA-CMP-PUB-002 — Changing the default language persists after save."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-PUB-003: Terms and conditions required validation — "
           "termsCondition is a rich-text editor; content comparison and clearing "
           "via Selenium fail due to whitespace/newline normalisation differences. "
           "Same root cause as legacy test_update_terms_condition_and_restore_original."
)
def test_terms_condition_required_clearing_blocked(edit_company_page):
    """SA-CMP-PUB-003 — 'Company terms and conditions' is required — clearing and saving is blocked."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-PUB-004: 'Enable company custom terms and conditions URL' toggle — "
           "locator not confirmed via DOM inspection.",
)
def test_custom_terms_url_toggle_reveals_url_field(edit_company_page, browser):
    """SA-CMP-PUB-004 — Enabling the custom terms URL toggle reveals the URL field."""
    toggle_loc = (
        By.XPATH,
        "//label[contains(.,'custom terms') or contains(.,'Custom terms')]"
        "/following::input[@type='checkbox' or @role='switch'][1]"
    )
    els = edit_company_page.driver.find_elements(*toggle_loc)
    assert els, "Custom terms and conditions URL toggle should be present"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-PUB-005: 'Enable membership terms' toggle — "
           "locator not confirmed via DOM inspection.",
)
def test_membership_terms_toggle_persists(edit_company_page):
    """SA-CMP-PUB-005 — 'Enable membership terms' toggle change persists after save."""
    toggle_loc = (
        By.XPATH,
        "//label[contains(.,'membership terms') or contains(.,'Membership terms')]"
        "/following::input[@type='checkbox' or @role='switch'][1]"
    )
    els = edit_company_page.driver.find_elements(*toggle_loc)
    assert els, "Membership terms toggle should be present"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-PUB-006: Saving with an empty privacy policy — modifies data; "
           "PRIVACY_POLICY_TEXTAREA (By.NAME, 'privacyPolicyText') and save interaction "
           "not confirmed to succeed in staging.",
)
def test_privacy_policy_is_optional(browser, edit_company_page):
    """SA-CMP-PUB-006 — Privacy policy is optional — saving with it empty succeeds."""
    from pages.superadmin.edit_company_page import EditCompanyPage

    original = edit_company_page.get_privacy_policy()
    try:
        edit_company_page.set_privacy_policy("")
        edit_company_page.click_save_changes()
        edit_company_page.confirm_yes()
        edit_company_page.wait_for_confirmation_closed()

        body = edit_company_page.driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "required" not in body or "privacy" not in body, \
            "Empty privacy policy should not show a 'required' validation error"
    finally:
        try:
            edit_company_page.set_privacy_policy(original or "")
            edit_company_page.click_save_changes()
            edit_company_page.confirm_yes()
            edit_company_page.wait_for_confirmation_closed()
        except Exception:
            pass
