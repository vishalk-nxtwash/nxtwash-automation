import os
import subprocess

import pytest
from selenium.webdriver.common.service import Service as _SeleniumService

from core.driver_factory import DriverFactory


# ---------------------------------------------------------------------------
# Selenium's Service._terminate_process() hard-codes process.wait(60).
# When Chrome/ChromeDriver freezes, that 60-second wait blocks every
# subsequent test in the run.  Patching the CLASS (not an instance) means
# the fix applies to every service object, including ones created during a
# failed driver setup that are later garbage-collected via __del__ →
# stop() → _terminate_process().
# ---------------------------------------------------------------------------
def _fast_terminate_process(self) -> None:
    try:
        for stream in (self.process.stdin, self.process.stdout, self.process.stderr):
            try:
                stream.close()
            except AttributeError:
                pass
        self.process.terminate()
        try:
            self.process.wait(3)  # was 60 seconds
        except subprocess.TimeoutExpired:
            self.process.kill()
    except OSError:
        pass


_SeleniumService._terminate_process = _fast_terminate_process


def _is_headless(config):
    """Headless if --headless is passed or HEADLESS env is truthy."""
    if config.getoption("--headless", default=False):
        return True
    return os.getenv("HEADLESS", "").strip().lower() in ("1", "true", "yes")


def browser_scope(fixture_name, config):
    """Decide how often a browser is created.

    Always uses function scope (one browser per test) so that a Chrome crash
    in one test never cascades to the rest of the suite.  Pass --single-window
    to opt into session scope when you explicitly want one shared window.
    """
    if config.getoption("--single-window", default=False):
        return "session"

    return "function"


# ---------------------------------------------------------------------------
# Session-scoped auth state — log in once per xdist worker and capture
# the localStorage + cookies so each function-scoped browser can inject
# them instead of going through the full login flow (~7-10s per test saved).
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def _worker_auth_state(request):
    """Log in once per worker session and capture auth state for injection.

    Yields a dict with 'cookies', 'localStorage', and 'base_url'.
    On any failure yields an empty dict so callers fall back gracefully
    to the normal ensure_admin_logged_in() path.
    """
    headless = _is_headless(request.config)
    driver = None
    try:
        from tests.admin_portal.admin_session import ensure_admin_logged_in
        from core.config_manager import ConfigManager

        driver = DriverFactory.get_driver(headless=headless, detach=False)
        driver.set_page_load_timeout(60)

        config = ConfigManager()
        base_url = config.get_url("admin_portal").rstrip("/")
        driver.get(base_url)
        ensure_admin_logged_in(driver)

        local_storage = driver.execute_script(
            "return Object.entries(window.localStorage)"
            ".reduce(function(acc, kv){ acc[kv[0]] = kv[1]; return acc; }, {});"
        )
        cookies = driver.get_cookies()
        yield {"cookies": cookies, "localStorage": local_storage, "base_url": base_url}
    except Exception:
        yield {}
    finally:
        if driver is not None:
            try:
                driver.set_page_load_timeout(5)
                driver.get("about:blank")
            except Exception:
                pass
            try:
                driver.quit()
            except Exception:
                pass


@pytest.fixture(scope=browser_scope)
def browser(request, _worker_auth_state):

    headless = _is_headless(request.config)

    driver = DriverFactory.get_driver(
        headless=headless,
        detach=False,
    )
    driver.set_page_load_timeout(60)

    # Inject the pre-captured auth state so this browser skips the full
    # login flow.  The browser must first navigate to the portal origin
    # before cookies / localStorage can be written for that origin.
    # Any failure here is silently ignored — ensure_admin_logged_in()
    # will perform a fresh login when the test calls open_admin_path().
    auth = _worker_auth_state
    if auth:
        try:
            driver.get(auth["base_url"])
            for cookie in auth.get("cookies", []):
                try:
                    driver.add_cookie(cookie)
                except Exception:
                    pass
            ls = auth.get("localStorage", {})
            if ls:
                driver.execute_script(
                    """
                    var ls = arguments[0];
                    for (var k in ls) {
                        try { localStorage.setItem(k, ls[k]); } catch(e) {}
                    }
                    """,
                    ls,
                )
        except Exception:
            pass

    yield driver

    # Navigate away before quitting so Chrome doesn't hang on a download
    # dialog or a frozen renderer.  Short page-load timeout prevents this
    # navigation from itself blocking if Chrome is already unresponsive.
    try:
        driver.set_page_load_timeout(5)
        driver.get("about:blank")
    except Exception:  # noqa: BLE001
        pass

    try:
        driver.quit()
    except Exception:  # noqa: BLE001
        pass
