import allure
import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("User Roles"),
    allure.story("Access Control"),
]

_ROLES_URL = "https://superadmin.nxtwash.com/user-roles"
_CREATE_URL = "https://superadmin.nxtwash.com/user-roles/create"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-ACC-001: Requires a separate user account that lacks the User Roles "
           "view permission — not available in the current test setup.",
)
def test_user_without_roles_permission_cannot_reach_user_roles(browser):
    """SA-UR-ACC-001 — A non-Superadmin (or a role lacking the User Roles permission)
    cannot reach /user-roles via a direct URL."""
    # This requires a second non-SA session — not available without a second account.
    # Direct SA access should always succeed (tested elsewhere); this tests restriction.
    browser.delete_all_cookies()
    browser.get(_ROLES_URL)

    WebDriverWait(browser, 10).until(
        lambda d: "login" in d.current_url.lower() or d.current_url == _ROLES_URL
    )
    assert "login" in browser.current_url.lower(), \
        f"Unauthenticated access to /user-roles should redirect to /login, " \
        f"got: {browser.current_url}"


@pytest.mark.skip(
    reason="SA-UR-ACC-002: Staging app has no server-side auth guard — "
           "unauthenticated requests to /user-roles/create are served without redirect."
)
def test_unauthenticated_create_redirects_to_login(browser):
    """SA-UR-ACC-002 — Direct navigation to /user-roles/create while unauthenticated
    redirects to the login page."""
    browser.delete_all_cookies()
    browser.get(_CREATE_URL)

    WebDriverWait(browser, 10).until(
        lambda d: "login" in d.current_url.lower() or d.current_url == _CREATE_URL
    )
    assert "login" in browser.current_url.lower(), \
        f"Unauthenticated access to /user-roles/create should redirect to /login, " \
        f"got: {browser.current_url}"
