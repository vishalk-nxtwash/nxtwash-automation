import pytest

from pages.admin_portal.login_page import AdminLoginPage


@pytest.fixture
def login_page(browser):
    # Auth injection in the browser fixture pre-authenticates the session.
    # Login tests need an unauthenticated browser — clear state before opening.
    browser.delete_all_cookies()
    browser.execute_script("localStorage.clear(); sessionStorage.clear();")
    page = AdminLoginPage(browser)
    page.open()
    page.wait_for_loaded()
    return page


@pytest.fixture
def login_credentials(login_page):
    return (
        login_page.config.get_username(login_page.PORTAL),
        login_page.config.get_password(login_page.PORTAL)
    )
