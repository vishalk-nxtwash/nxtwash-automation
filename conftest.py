import datetime
import logging
import os
import re

import pytest

# Re-export the browser fixture so every test can request `browser`.
from fixtures.browser import browser  # noqa: F401

try:  # Allure is optional; failure artifacts still land on disk without it.
    import allure
except ImportError:  # pragma: no cover
    allure = None


LOG = logging.getLogger("nxtwash")

SCREENSHOTS_DIR = "screenshots"
LOGS_DIR = "logs"


def pytest_addoption(parser):
    parser.addoption(
        "--close-browser",
        action="store_true",
        default=False,
        help="Close the browser after test execution (default: stay open)",
    )
    parser.addoption(
        "--single-window",
        action="store_true",
        default=False,
        help="Reuse one browser window for grouped screen suites",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome in headless mode (recommended for CI)",
    )
    parser.addoption(
        "--env",
        action="store",
        default=None,
        choices=["staging", "production"],
        help="Target environment (default: staging, or TEST_ENV)",
    )


def pytest_configure(config):
    # Propagate the chosen environment so ConfigManager picks it up everywhere.
    env = config.getoption("--env") or os.getenv("TEST_ENV", "staging")
    os.environ["TEST_ENV"] = env

    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(LOGS_DIR, "test_run.log")),
        ],
    )
    LOG.info("Test run starting against '%s' environment", env)


def pytest_collection_modifyitems(config, items):
    # Auto-tag tests by location so `-m admin/superadmin/smoke` works suite-wide.
    for item in items:
        path = str(item.fspath).replace(os.sep, "/")

        if "/tests/admin_portal/" in path:
            item.add_marker(pytest.mark.admin)
        if "/tests/superadmin/" in path:
            item.add_marker(pytest.mark.superadmin)

        # Smoke = login flows, positive paths, and *_smoke files.
        if "/login/" in path or "_positive" in path or "_smoke" in path:
            item.add_marker(pytest.mark.smoke)


def _safe_name(nodeid):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid)


def _capture_failure(item, driver):
    """Save a screenshot + page source on failure and attach to Allure."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base = "%s_%s" % (_safe_name(item.nodeid), timestamp)

    try:
        url = driver.current_url
    except Exception:  # noqa: BLE001
        url = "unknown"
    LOG.error("Test FAILED: %s (url: %s)", item.nodeid, url)

    png_path = os.path.join(SCREENSHOTS_DIR, base + ".png")
    html_path = os.path.join(LOGS_DIR, base + ".html")

    try:
        driver.save_screenshot(png_path)
        if allure is not None:
            allure.attach.file(
                png_path,
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
    except Exception as error:  # noqa: BLE001
        LOG.warning("Could not capture screenshot: %s", error)

    try:
        page_source = driver.page_source
        with open(html_path, "w", encoding="utf-8") as handle:
            handle.write(page_source)
        if allure is not None:
            allure.attach(
                page_source,
                name="page_source",
                attachment_type=allure.attachment_type.HTML,
            )
            allure.attach(
                url, name="url", attachment_type=allure.attachment_type.TEXT
            )
    except Exception as error:  # noqa: BLE001
        LOG.warning("Could not capture page source: %s", error)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser")
        if driver is not None:
            _capture_failure(item, driver)
