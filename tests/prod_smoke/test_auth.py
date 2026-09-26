import allure
import pytest

from pages.admin_portal.login_page import AdminLoginPage
from tests.prod_smoke.conftest import page_is_up


pytestmark = [
    allure.epic("Production Smoke"),
    allure.feature("Authentication"),
    pytest.mark.prod_smoke,
]


@pytest.fixture
def unauthenticated_browser(browser):
    """Return a browser with no active session — needed for login-flow tests."""
    browser.delete_all_cookies()
    browser.execute_script("localStorage.clear(); sessionStorage.clear();")
    return browser


@allure.title("PSMO-AUTH-001 Login page loads with all expected UI elements")
@pytest.mark.prod_smoke
def test_login_page_loads(unauthenticated_browser):
    page = AdminLoginPage(unauthenticated_browser)
    page.open()
    page.wait_for_loaded()

    assert page.logo_is_visible(), "NxtWash logo not visible on login page"
    assert page.email_field_is_visible(), "Email field not visible"
    assert page.password_field_is_visible(), "Password field not visible"
    assert page.login_button_is_visible(), "Login button not visible"


@allure.title("PSMO-AUTH-002 Valid production credentials authenticate successfully")
@pytest.mark.prod_smoke
def test_login_with_valid_credentials(unauthenticated_browser):
    page = AdminLoginPage(unauthenticated_browser)
    page.open()
    page.wait_for_loaded()
    page.login()
    page.wait_for_overview()

    assert "/login" not in unauthenticated_browser.current_url, (
        "Still on /login after submitting valid credentials"
    )
    assert page_is_up(unauthenticated_browser)


@allure.title("PSMO-AUTH-003 Authenticated session is maintained across page navigation")
@pytest.mark.prod_smoke
def test_session_persists_after_navigation(browser):
    from tests.admin_portal.admin_session import open_admin_path

    open_admin_path(browser, "/customers")
    open_admin_path(browser, "/")

    assert "/login" not in browser.current_url, (
        "Session was lost — redirected to /login after navigating between pages"
    )
    assert page_is_up(browser)
