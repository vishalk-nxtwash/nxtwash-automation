import pytest

from pages.superadmin.login_page import LoginPage


@pytest.fixture
def login_page(browser):
    """Provide a clean, unauthenticated Superadmin login page.

    Auth state injected by the session-scoped browser fixture is for the
    admin portal origin and has no effect on the superadmin origin, but
    cookies and localStorage are cleared explicitly to guarantee a
    logged-out starting state regardless of fixture scope changes.
    """
    browser.delete_all_cookies()
    browser.execute_script("localStorage.clear(); sessionStorage.clear();")
    page = LoginPage(browser)
    page.open()
    page.wait_for_loaded()
    return page


@pytest.fixture
def login_credentials(login_page):
    """Return the configured Superadmin (email, password) tuple."""
    return (
        login_page.config.get_username(login_page.PORTAL),
        login_page.config.get_password(login_page.PORTAL),
    )
