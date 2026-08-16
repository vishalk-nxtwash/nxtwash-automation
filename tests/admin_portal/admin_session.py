from urllib.parse import urlparse

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.login_page import AdminLoginPage


ADMIN_PORTAL = "admin_portal"

# How many times to (re)attempt login and to recover from a /login bounce.
LOGIN_ATTEMPTS = 3
NAVIGATION_ATTEMPTS = 2
# Per-navigation cost on the success path, so keep it short — a client-side
# auth redirect back to /login happens almost immediately.
LOGIN_BOUNCE_TIMEOUT = 8


def _session_stored(login_page):
    """Best-effort 'already authenticated' probe (never raises, never blocks)."""
    try:
        return login_page.authenticated_session_is_stored()
    except Exception:  # noqa: BLE001
        return False


def _on_login_page(browser):
    return "/login" in browser.current_url


def _bounced_to_login(browser, timeout=LOGIN_BOUNCE_TIMEOUT):
    """Return True if the SPA redirected us back to /login after navigating."""
    try:
        WebDriverWait(browser, timeout).until(
            lambda driver: "/login" in driver.current_url
        )
        return True
    except TimeoutException:
        return False


def ensure_admin_logged_in(browser, attempts=LOGIN_ATTEMPTS):
    """Ensure the current browser has an authenticated Admin session.

    Uses the Overview screen (a real UI signal) as the source of truth that
    login succeeded, and retries the login if it does not land there. We do not
    gate on localStorage: that probe is unreliable and only used as a fast path.
    """
    login_page = AdminLoginPage(browser)
    base_url = login_page.config.get_url(ADMIN_PORTAL)
    host = urlparse(base_url).netloc

    if host not in browser.current_url:
        browser.get(base_url)

    # Fast path: an active session already off the login page.
    if not _on_login_page(browser) and _session_stored(login_page):
        return

    # _session_stored() can return False after frame switches or error
    # recovery even when the session is still alive (e.g. after a failed
    # create-form save leaves the driver in an unusual frame state).
    # Navigate to the portal root and check whether the SPA bounces us to
    # /login.  If it does not, the session is valid and no login is needed.
    if not _on_login_page(browser):
        browser.get(base_url)
        if not _bounced_to_login(browser):
            return  # Session confirmed alive via SPA redirect probe

    last_error = None
    for _ in range(attempts):
        if not _on_login_page(browser):
            browser.get(base_url)
        try:
            login_page.wait_for_loaded()
            login_page.login()
            login_page.wait_for_overview()
            return
        except (TimeoutException, WebDriverException) as error:
            last_error = error
            try:
                browser.get(base_url)
            except (TimeoutException, WebDriverException):
                pass

    if last_error is not None:
        raise last_error


def open_admin_path(browser, path, attempts=NAVIGATION_ATTEMPTS):
    """Open an Admin Portal path with an authenticated session.

    Retries if the deep-link bounces back to /login, which indicates the
    session was not honored on navigation; we re-establish it and try again.
    """
    login_page = AdminLoginPage(browser)
    base_url = login_page.config.get_url(ADMIN_PORTAL).rstrip("/")

    for attempt in range(1, attempts + 1):
        ensure_admin_logged_in(browser)
        browser.switch_to.default_content()
        browser.get(base_url + path)

        if not _bounced_to_login(browser):
            return

        # Bounced: force a fresh login on the next iteration (we are on /login).
