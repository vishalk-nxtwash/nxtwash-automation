import allure
import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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


def test_unauthenticated_create_redirects_to_login(browser):
    """SA-CMP-ACC-002 — Unauthenticated access to /companies/create redirects to login."""
    browser.delete_all_cookies()
    browser.get(_CREATE_URL)

    try:
        WebDriverWait(browser, 10).until(lambda d: "login" in d.current_url.lower())
    except TimeoutException:
        pass  # asserted below with the landed URL
    assert "login" in browser.current_url.lower(), \
        f"Unauthenticated /companies/create should redirect to /login, " \
        f"got: {browser.current_url}"
