import allure
import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Users"),
    allure.story("Access Control"),
]

_LOGIN_URL = "https://superadmin.nxtwash.com/login"
_USERS_URL = "https://superadmin.nxtwash.com/users"
_CREATE_URL = "https://superadmin.nxtwash.com/users/create"


def test_unauthenticated_users_list_redirects_to_login(browser):
    """SA-USR-ACC-001 — Unauthenticated access to /users redirects to the login page."""
    # Ensure no active session (fresh browser fixture has no cookies)
    browser.delete_all_cookies()
    browser.get(_USERS_URL)

    try:
        WebDriverWait(browser, 10).until(lambda d: "login" in d.current_url.lower())
    except TimeoutException:
        pass  # asserted below with the landed URL
    # The app should redirect to login — if it stays on /users then it failed to protect
    assert "login" in browser.current_url.lower(), \
        f"Unauthenticated access to /users should redirect to /login, " \
        f"got: {browser.current_url}"


def test_unauthenticated_create_user_redirects_to_login(browser):
    """SA-USR-ACC-002 — Unauthenticated access to /users/create redirects to the login page."""
    browser.delete_all_cookies()
    browser.get(_CREATE_URL)

    try:
        WebDriverWait(browser, 10).until(lambda d: "login" in d.current_url.lower())
    except TimeoutException:
        pass  # asserted below with the landed URL
    assert "login" in browser.current_url.lower(), \
        f"Unauthenticated access to /users/create should redirect to /login, " \
        f"got: {browser.current_url}"
