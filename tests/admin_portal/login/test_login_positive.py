import allure
import pytest


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("Positive"),
]


@pytest.mark.prod_smoke
def test_login_with_valid_credentials(browser, login_page):

    login_page.login()
    login_page.wait_for_overview()

    assert browser.current_url == login_page.config.get_url(login_page.PORTAL)
    assert login_page.get_overview_text() == "Overview"


def test_login_using_enter_key(login_page, login_credentials):

    username, password = login_credentials

    login_page.submit_with_enter(username, password)
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"


@pytest.mark.prod_smoke
def test_session_persists_after_refresh(browser, login_page):

    login_page.login()
    login_page.wait_for_overview()
    browser.refresh()
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"


def test_authenticated_user_cannot_access_login_page(browser, login_page):

    login_page.login()
    login_page.wait_for_overview()
    login_page.open_login_url()
    login_page.wait_until_redirected_away_from_login()

    assert "/login" not in browser.current_url


@pytest.mark.xfail(
    reason="Known product gap: valid email with a leading space is not trimmed.",
    strict=True,
)
def test_login_with_email_leading_space(login_page, login_credentials):

    username, password = login_credentials

    login_page.login_with(" " + username, password)
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"


def test_login_with_email_trailing_space(login_page, login_credentials):

    username, password = login_credentials

    login_page.login_with(username + " ", password)
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"


def test_login_with_email_case_variation(login_page, login_credentials):

    username, password = login_credentials

    login_page.login_with(username.upper(), password)
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"


def test_session_remains_active_in_new_tab(login_page):

    login_page.login()
    login_page.wait_for_overview()
    login_page.open_overview_in_new_tab()
    login_page.wait_for_overview()

    assert login_page.get_overview_text() == "Overview"
