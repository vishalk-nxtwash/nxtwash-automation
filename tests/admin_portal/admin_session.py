from core.config_manager import ConfigManager
from pages.admin_portal.login_page import AdminLoginPage


ADMIN_PORTAL = "admin_portal"


def ensure_admin_logged_in(browser):
    """Ensure the current browser has an authenticated Admin session."""
    login_page = AdminLoginPage(browser)
    base_url = login_page.config.get_url(ADMIN_PORTAL)

    if "staging.nxtwash.com" not in browser.current_url:
        browser.get(base_url)

    try:
        if login_page.authenticated_session_is_stored():
            return
    except Exception:
        browser.get(base_url)

    if "/login" not in browser.current_url:
        browser.get(base_url)

    if "/login" in browser.current_url:
        login_page.wait_for_loaded()
        login_page.login()
        login_page.wait_for_overview()
        return

    login_page.wait_for_overview()


def open_admin_path(browser, path):
    """Open an Admin Portal path in the current browser tab."""
    ensure_admin_logged_in(browser)
    base_url = ConfigManager().get_url(ADMIN_PORTAL).rstrip("/")
    browser.switch_to.default_content()
    browser.get(base_url + path)
