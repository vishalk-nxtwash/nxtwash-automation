import pytest

from pages.superadmin.login_page import LoginPage


@pytest.fixture
def login_page(browser):
    """Open the superadmin login page and wait for the form to be fully rendered."""
    page = LoginPage(browser)
    page.open()
    page.wait_for_loaded()
    return page


@pytest.fixture
def logged_in_browser(browser):
    """Log in to superadmin and return the browser positioned at the Overview page."""
    page = LoginPage(browser)
    page.open()
    page.wait_for_loaded()
    page.login()
    page.wait_for_overview()
    return browser
