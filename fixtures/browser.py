import os

import pytest

from core.driver_factory import DriverFactory


def _is_headless(config):
    """Headless if --headless is passed or HEADLESS env is truthy."""
    if config.getoption("--headless", default=False):
        return True
    return os.getenv("HEADLESS", "").strip().lower() in ("1", "true", "yes")


def browser_scope(fixture_name, config):
    """Decide how often a browser is created.

    Reuse one browser per worker in CI (headless) or when --single-window is
    set: tests self-navigate and `admin_session` reuses the stored login
    session (its fast path skips re-login when a session already exists), so a
    fresh browser per test only adds cold Chrome start-up + a full re-login on
    every test. Reusing it keeps login to once-per-worker.

    Locally (non-headless) the default stays per-test, so each test opens in its
    own window for easier debugging — pass --single-window to opt into reuse.
    """
    if config.getoption("--single-window", default=False):
        return "session"

    if _is_headless(config):
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
