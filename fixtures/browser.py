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


@pytest.fixture(scope=browser_scope)
def browser(request):

    headless = _is_headless(request.config)

    driver = DriverFactory.get_driver(
        headless=headless,
        detach=False,
    )
    driver.set_page_load_timeout(60)

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
