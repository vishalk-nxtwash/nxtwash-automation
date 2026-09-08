import allure
import pytest


pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("Positive"),
]


def test_valid_credentials_redirect_to_overview(login_page):
    """SA-LGN-HP-001 — valid credentials land on the overview page."""
    login_page.login()
    login_page.wait_for_overview()

    assert not login_page.is_login_page(), \
        "Should have navigated away from login after successful authentication"
    assert login_page.get_overview_text() == "Overview", \
        f"Expected 'Overview' page title, got: {login_page.get_overview_text()!r}"


def test_login_via_enter_key(login_page, login_credentials):
    """SA-LGN-HP-002 — submitting the form with Enter authenticates the user."""
    email, password = login_credentials

    login_page.submit_with_enter(email, password)
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview", \
        f"Expected 'Overview' after Enter-key submission, got: {login_page.get_overview_text()!r}"


def test_session_persists_after_page_reload(browser, login_page):
    """SA-LGN-HP-003 — reloading the page keeps the user authenticated."""
    login_page.login()
    login_page.wait_for_overview()

    browser.refresh()
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview", \
        "Session was lost after page reload — user should remain authenticated"
