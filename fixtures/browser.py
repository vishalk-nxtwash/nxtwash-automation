import os

import pytest

from core.driver_factory import DriverFactory


def _is_headless(config):
    """Headless if --headless is passed or HEADLESS env is truthy."""
    if config.getoption("--headless", default=False):
        return True
    return os.getenv("HEADLESS", "").strip().lower() in ("1", "true", "yes")


def browser_scope(fixture_name, config):

    if config.getoption("--single-window", default=False):
        return "session"

    return "function"


@pytest.fixture(scope=browser_scope)
def browser(request):

    headless = _is_headless(request.config)
    close_browser = request.config.getoption("--close-browser")

    driver = DriverFactory.get_driver(
        headless=headless,
        detach=not close_browser,
    )

    yield driver

    # Always quit in headless mode (no window to keep) or when requested.
    if close_browser or headless:
        driver.quit()
