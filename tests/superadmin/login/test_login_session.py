import allure


pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("Session"),
]


def test_unauthenticated_access_redirects_to_login(browser, login_page):
    """SA-LGN-SEC-004 — opening a protected URL without a session redirects to login.

    Auth state is wiped via the login_page fixture before this navigation.
    """
    browser.delete_all_cookies()
    browser.execute_script("localStorage.clear(); sessionStorage.clear();")

    login_page.open_protected_url()
    login_page.wait_for_loaded()

    assert login_page.is_login_page(), \
        "Unauthenticated access to the Superadmin root should redirect to /login"


def test_clearing_session_redirects_to_login_on_navigation(browser, login_page):
    """SA-LGN-SEC-005 — after auth tokens are removed, protected pages redirect to login.

    Clears localStorage to simulate a logout (token removal) and verifies the
    app does not serve cached content from the authenticated session.
    """
    login_page.login()
    login_page.wait_for_overview()

    browser.delete_all_cookies()
    browser.execute_script("localStorage.clear(); sessionStorage.clear();")
    login_page.open_protected_url()
    login_page.wait_for_loaded()

    assert login_page.is_login_page(), \
        "After session tokens are cleared, navigating to a protected URL must redirect to /login"
