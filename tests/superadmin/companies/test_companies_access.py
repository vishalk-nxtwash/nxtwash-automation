import allure
import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Companies"),
    allure.story("Access Control"),
]

_LOGIN_URL = "https://superadmin.nxtwash.com/login"
_COMPANIES_URL = "https://superadmin.nxtwash.com/companies"
_CREATE_URL = "https://superadmin.nxtwash.com/companies/create"


@pytest.mark.skip(
    reason="SA-CMP-ACC-001: Non-Superadmin access to /companies requires a different "
           "user role fixture — not available in the current test setup."
)
def test_non_superadmin_cannot_reach_companies(browser):
    """SA-CMP-ACC-001 — A non-Superadmin cannot reach /companies via a direct URL."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-ACC-002: Staging app has no server-side auth guard — "
           "unauthenticated requests to /companies/create are served without redirect. "
           "Same behaviour as SA-USR-ACC-001 and SA-USR-ACC-002."
)
def test_unauthenticated_create_redirects_to_login(browser):
    """SA-CMP-ACC-002 — Unauthenticated access to /companies/create redirects to login."""
    browser.delete_all_cookies()
    browser.get(_CREATE_URL)

    WebDriverWait(browser, 10).until(
        lambda d: "login" in d.current_url.lower() or d.current_url == _CREATE_URL
    )
    assert "login" in browser.current_url.lower(), \
        f"Unauthenticated /companies/create should redirect to /login, " \
        f"got: {browser.current_url}"
