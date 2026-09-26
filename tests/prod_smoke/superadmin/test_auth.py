import allure
import pytest

from pages.superadmin.login_page import LoginPage
from tests.prod_smoke.conftest import page_is_up


pytestmark = [
    allure.epic("Production Smoke"),
    allure.feature("Superadmin Authentication"),
    pytest.mark.prod_smoke,
]


@pytest.fixture
def unauthenticated_browser(browser):
    """Return a browser with no active session — needed for login-flow tests."""
    browser.delete_all_cookies()
    browser.execute_script("localStorage.clear(); sessionStorage.clear();")
    return browser


@allure.title("SA-PSMO-AUTH-001 Login page loads with email, password and login button")
@pytest.mark.prod_smoke
def test_login_page_loads(unauthenticated_browser):
    page = LoginPage(unauthenticated_browser)
    page.open()

    assert unauthenticated_browser.find_elements(*page.EMAIL_INPUT), \
        "Email field not visible"
    assert unauthenticated_browser.find_elements(*page.PASSWORD_INPUT), \
        "Password field not visible"
    assert unauthenticated_browser.find_elements(*page.LOGIN_BUTTON), \
        "Login button not visible"


@allure.title("SA-PSMO-AUTH-002 Valid superadmin credentials authenticate and reach Overview")
@pytest.mark.prod_smoke
def test_login_with_valid_credentials(unauthenticated_browser):
    page = LoginPage(unauthenticated_browser)
    page.open()
    page.login()
    page.wait_for_overview()

    assert page.get_overview_text() == "Overview"
    assert page_is_up(unauthenticated_browser)


@allure.title("SA-PSMO-AUTH-003 Session persists across sidebar navigation")
@pytest.mark.prod_smoke
def test_session_persists_across_navigation(superadmin_session, sidebar):
    sidebar.open_users()
    assert page_is_up(superadmin_session)

    sidebar.open_companies()
    assert page_is_up(superadmin_session)
