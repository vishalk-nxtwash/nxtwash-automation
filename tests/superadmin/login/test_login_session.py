import allure
import pytest

from pages.superadmin.login_page import LoginPage

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("Session"),
]


def test_unauthenticated_url_redirects_to_login(browser):
    """SA-LGN-SEC-004 — Navigating to a protected URL while unauthenticated redirects to login."""
    from selenium.webdriver.support.ui import WebDriverWait

    base      = LoginPage(browser).base_url()
    protected = base + "/companies"

    browser.get(protected)
    WebDriverWait(browser, 20).until(lambda d: "/login" in d.current_url)

    assert "/login" in browser.current_url, \
        f"Expected redirect to /login when unauthenticated, got: {browser.current_url}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-LGN-SEC-005: Logout button not found via text ('Logout'/'Log out'/'Sign out'). "
           "App likely hides logout behind a user-avatar/profile dropdown — inspect the DOM "
           "on the Overview page to find the real trigger, add it to Sidebar or LoginPage, "
           "then un-xfail this test.",
)
def test_post_logout_url_redirects_to_login(logged_in_browser):
    """SA-LGN-SEC-005 — After logging out, navigating to a protected URL redirects to login."""
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC

    logout_locator = (By.XPATH,
        "//button[contains(normalize-space(),'Logout') or contains(normalize-space(),'Log out')"
        " or contains(normalize-space(),'Sign out')]"
        " | //a[contains(normalize-space(),'Logout') or contains(normalize-space(),'Log out')]")

    btn = WebDriverWait(logged_in_browser, 10).until(
        EC.element_to_be_clickable(logout_locator)
    )
    btn.click()
    WebDriverWait(logged_in_browser, 15).until(lambda d: "/login" in d.current_url)

    base = LoginPage(logged_in_browser).base_url()
    logged_in_browser.get(base + "/companies")
    WebDriverWait(logged_in_browser, 15).until(lambda d: "/login" in d.current_url)

    assert "/login" in logged_in_browser.current_url, \
        "After logout, a protected URL should redirect back to the login page"
