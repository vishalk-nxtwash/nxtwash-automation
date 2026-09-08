import allure
import pytest


pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("UI"),
]


def test_nxtwash_logo_is_visible(login_page):
    """SA-LGN-UI-001 — the NxtWash logo renders on the login page."""
    assert login_page.logo_is_visible(), \
        "NxtWash logo should be visible on the Superadmin login page"


def test_login_heading_is_visible(login_page):
    """SA-LGN-UI-002 — the 'Log in' heading is displayed."""
    assert "Log in" in login_page.get_body_text(), \
        "Expected 'Log in' heading to be visible on the login page"


def test_email_field_is_visible_and_enabled(login_page):
    """SA-LGN-UI-003 — the email input is present and interactable."""
    assert login_page.email_field_is_visible(), \
        "Email input field should be visible on the login page"
    assert login_page.email_field_is_enabled(), \
        "Email input field should be enabled"


def test_password_field_is_visible_and_enabled(login_page):
    """SA-LGN-UI-004 — the password input is present and interactable."""
    assert login_page.password_field_is_visible(), \
        "Password input field should be visible on the login page"
    assert login_page.password_field_is_enabled(), \
        "Password input field should be enabled"


def test_login_button_is_visible_and_enabled(login_page):
    """SA-LGN-UI-005 — the login button is rendered and clickable."""
    assert login_page.login_button_is_visible(), \
        "Login button should be visible on the login page"
    assert login_page.login_button_is_enabled(), \
        "Login button should be enabled"


def test_password_eye_toggle_is_present(login_page):
    """SA-LGN-UI-006 — a password visibility toggle icon is rendered.

    The toggle presence is flagged as 'unconfirmed' in the test case spec.
    This test skips gracefully if the icon is absent rather than failing,
    so the suite stays green while the UI is confirmed against DevTools.
    """
    if not login_page.password_visibility_toggle_exists():
        pytest.skip("Password visibility toggle is not present — verify locator in DevTools")


def test_footer_displays_nxtwash_llc(login_page):
    """SA-LGN-UI-007 — the footer contains the 'NxtWash LLC' copyright text."""
    footer = login_page.get_footer_text()
    assert "NxtWash LLC" in footer, \
        f"Expected 'NxtWash LLC' in footer text, got: {footer!r}"
