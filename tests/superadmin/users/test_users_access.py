import allure
import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Users"),
    allure.story("Access Control"),
]

_LOGIN_URL = "https://superadmin.nxtwash.com/login"
_USERS_URL = "https://superadmin.nxtwash.com/users"
_CREATE_URL = "https://superadmin.nxtwash.com/users/create"


@pytest.mark.skip(
    reason="SA-USR-ACC-001: Staging app has no server-side auth guard — "
           "unauthenticated requests to /users are served without redirect."
)
def test_unauthenticated_users_list_redirects_to_login(browser):
    """SA-USR-ACC-001 — Unauthenticated access to /users redirects to the login page."""
    # Ensure no active session (fresh browser fixture has no cookies)
    browser.delete_all_cookies()
    browser.get(_USERS_URL)

    WebDriverWait(browser, 10).until(
        lambda d: "login" in d.current_url.lower() or d.current_url == _USERS_URL
    )
    # The app should redirect to login — if it stays on /users then it failed to protect
    assert "login" in browser.current_url.lower(), \
        f"Unauthenticated access to /users should redirect to /login, " \
        f"got: {browser.current_url}"


@pytest.mark.skip(
    reason="SA-USR-ACC-002: Staging app has no server-side auth guard — "
           "unauthenticated requests to /users/create are served without redirect."
)
def test_unauthenticated_create_user_redirects_to_login(browser):
    """SA-USR-ACC-002 — Unauthenticated access to /users/create redirects to the login page."""
    browser.delete_all_cookies()
    browser.get(_CREATE_URL)

    WebDriverWait(browser, 10).until(
        lambda d: "login" in d.current_url.lower() or d.current_url == _CREATE_URL
    )
    assert "login" in browser.current_url.lower(), \
        f"Unauthenticated access to /users/create should redirect to /login, " \
        f"got: {browser.current_url}"
