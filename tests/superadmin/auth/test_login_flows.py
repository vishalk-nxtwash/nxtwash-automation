"""Superadmin login / session flows.

Smoke tests here are marked explicitly with @pytest.mark.smoke.

Not covered on purpose: a wrong password for the real superadmin account. Every
suite shares that one account, and repeated failed attempts could trigger a
lockout that takes down all CI runs. Credential rejection is exercised with an
email that does not exist instead.
"""
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.superadmin.login_page import LoginPage

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Authentication"),
]

_UNKNOWN_EMAIL = "no-such-user-autotest@yopmail.com"


@pytest.fixture
def login_page(browser):
    page = LoginPage(browser)
    page.open()
    page.wait_for_any_visible(page.EMAIL_INPUT)
    return page


@pytest.fixture
def logged_in(login_page):
    login_page.login()
    login_page.wait_for_overview()
    return login_page


# ── Smoke ─────────────────────────────────────────────────────────────────────

@pytest.mark.smoke
def test_unknown_email_is_rejected(login_page):
    """Invalid credentials do not authenticate and show the backend error."""
    login_page.login_with(_UNKNOWN_EMAIL, "Wrong@12345")
    assert login_page.wait_for_page_text(login_page.INVALID_CREDENTIALS_TEXT), \
        f"Expected '{login_page.INVALID_CREDENTIALS_TEXT}' after invalid credentials"
    assert login_page.is_on_login_page() and not login_page.has_session_token(), \
        f"Invalid credentials must not log in, landed on {login_page.driver.current_url}"


@pytest.mark.smoke
def test_empty_submit_shows_email_validation(login_page):
    """Submitting the empty form is blocked with a field validation message."""
    login_page.click_login()
    assert login_page.wait_for_page_text("Invalid email address"), \
        "Empty submit should show 'Invalid email address'"
    assert login_page.stays_on_login(3), "Empty submit must not leave /login"


@pytest.mark.smoke
def test_unauthenticated_root_redirects_to_login(browser):
    """A browser without a session is sent to /login from a protected page."""
    page = LoginPage(browser)
    browser.get(page.base_url() + "/companies")
    page.wait.until(lambda d: "/login" in d.current_url)
    assert not page.has_session_token()


@pytest.mark.smoke
def test_session_persists_after_refresh(logged_in):
    """A logged-in session survives a full page reload."""
    logged_in.driver.refresh()
    logged_in.wait_for_overview()
    assert not logged_in.is_on_login_page(), "Refresh should keep the user logged in"


@pytest.mark.smoke
def test_logged_in_user_visiting_login_is_redirected_home(logged_in):
    """An authenticated user opening /login is sent back to the app."""
    logged_in.open()
    logged_in.wait.until(lambda d: "/login" not in d.current_url)
    logged_in.wait_for_overview()


@pytest.mark.smoke
def test_logout_ends_session_and_protects_pages(logged_in):
    """Log out clears the session, and protected pages then redirect to /login.

    Logout is client-side only (no API call), so it does not affect other
    sessions of the shared account — safe to run in parallel.
    """
    logged_in.logout()
    assert not logged_in.has_session_token(), "Logout should clear the session token"
    logged_in.driver.get(logged_in.base_url() + "/users")
    logged_in.wait.until(lambda d: "/login" in d.current_url)


# ── Full suite ────────────────────────────────────────────────────────────────

def test_login_page_shows_fields_and_button(login_page):
    driver = login_page.driver
    assert driver.title == "SuperAdmin NxtWash", f"Unexpected title: {driver.title!r}"
    assert driver.find_element(*login_page.EMAIL_INPUT).get_attribute("type") == "email"
    assert driver.find_element(*login_page.PASSWORD_INPUT).is_displayed()
    assert driver.find_element(*login_page.LOGIN_BUTTON).text.strip() == "Log in"


def test_password_is_masked(login_page):
    field = login_page.driver.find_element(*login_page.PASSWORD_INPUT)
    assert field.get_attribute("type") == "password", "Password input must be masked"


def test_malformed_email_is_blocked_by_field_validation(login_page):
    """type=email blocks a malformed address before any request is sent."""
    login_page.login_with("not-an-email", "Whatever@123")
    assert not login_page.email_field_is_valid(), "'not-an-email' should fail email validity"
    assert login_page.stays_on_login(3)


def test_valid_email_with_empty_password_does_not_authenticate(login_page):
    login_page.login_with(login_page.config.get_username("superadmin"), "")
    assert login_page.stays_on_login(5), "Empty password must not log in"
    assert not login_page.has_session_token()


def test_enter_key_submits_login(login_page):
    login_page.enter_email(login_page.config.get_username("superadmin"))
    login_page.enter_password(login_page.config.get_password("superadmin"))
    login_page.driver.find_element(*login_page.PASSWORD_INPUT).send_keys(Keys.ENTER)
    login_page.wait_for_overview()


def test_session_is_shared_across_tabs(logged_in):
    driver = logged_in.driver
    driver.switch_to.new_window("tab")
    driver.get(logged_in.base_url() + "/users")
    logged_in.wait.until(lambda d: d.current_url.rstrip("/").endswith("/users"))
    assert not logged_in.is_on_login_page(), "A new tab should reuse the session"
