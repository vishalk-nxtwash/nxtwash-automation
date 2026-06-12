import allure
import pytest

from tests.admin_portal.login.conftest import configured_credentials
from tests.admin_portal.login.conftest import open_login_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("Positive"),
]


def test_login_with_valid_credentials(browser):

    login_page = open_login_page(browser)

    login_page.login()
    login_page.wait_for_overview()

    assert browser.current_url == login_page.config.get_url(login_page.PORTAL)
    assert login_page.get_overview_text() == "Overview"


def test_login_using_enter_key(browser):

    login_page = open_login_page(browser)
    username, password = configured_credentials(login_page)

    login_page.submit_with_enter(username, password)
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"


def test_session_persists_after_refresh(browser):

    login_page = open_login_page(browser)

    login_page.login()
    login_page.wait_for_overview()
    browser.refresh()
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"


def test_authenticated_user_cannot_access_login_page(browser):

    login_page = open_login_page(browser)

    login_page.login()
    login_page.wait_for_overview()
    login_page.open_login_url()
    login_page.wait_until_redirected_away_from_login()

    assert "/login" not in browser.current_url


@pytest.mark.xfail(
    reason="Known product gap: valid email with a leading space is not trimmed.",
    strict=True,
)
def test_login_with_email_leading_space(browser):

    login_page = open_login_page(browser)
    username, password = configured_credentials(login_page)

    login_page.login_with(" " + username, password)
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"


def test_login_with_email_trailing_space(browser):

    login_page = open_login_page(browser)
    username, password = configured_credentials(login_page)

    login_page.login_with(username + " ", password)
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"


def test_login_with_email_case_variation(browser):

    login_page = open_login_page(browser)
    username, password = configured_credentials(login_page)

    login_page.login_with(username.upper(), password)
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"


def test_session_remains_active_in_new_tab(browser):

    login_page = open_login_page(browser)

    login_page.login()
    login_page.wait_for_overview()
    login_page.open_overview_in_new_tab()
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"
