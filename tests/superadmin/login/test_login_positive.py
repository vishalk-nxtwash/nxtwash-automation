import allure
import pytest

from pages.superadmin.login_page import LoginPage

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("Positive"),
]


def test_enter_key_submits_login_form(login_page):
    """SA-LGN-HP-002 — Pressing Enter on the password field submits the login form."""
    login_page.login_with_enter_key()
    login_page.wait_for_overview()
    text = login_page.get_overview_text()
    assert text == "Overview", \
        f"Expected Overview page after Enter-key login, got: {text!r}"


def test_session_persists_after_reload(logged_in_browser):
    """SA-LGN-HP-003 — Login session survives a full page reload."""
    logged_in_browser.refresh()
    page = LoginPage(logged_in_browser)
    page.wait_for_overview(timeout=20)
    text = page.get_overview_text()
    assert text == "Overview", \
        f"Expected session to persist after reload, but got: {text!r}"
