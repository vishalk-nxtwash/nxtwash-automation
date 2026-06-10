from tests.admin_portal.login.conftest import open_login_page


def test_direct_protected_url_without_login_redirects_to_login(browser):

    login_page = open_login_page(browser)
    browser.delete_all_cookies()
    browser.execute_script("window.localStorage.clear();")
    browser.execute_script("window.sessionStorage.clear();")

    login_page.open_protected_overview()
    login_page.wait_for_loaded()

    assert login_page.is_login_page()


def test_auth_token_is_stored_after_login(browser):

    login_page = open_login_page(browser)

    login_page.login()
    login_page.wait_for_overview()

    assert login_page.authenticated_session_is_stored()
