import datetime
import logging
import os
import re
import shutil

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

    # Ship the Allure "Categories" definition into the results dir so buckets
    # like "Known product defects" render even after results are cleared.
    alluredir = config.getoption("--alluredir", default=None)
    categories_src = os.path.join(
        os.path.dirname(__file__), "allure-categories.json"
    )
    if alluredir and os.path.exists(categories_src):
        os.makedirs(alluredir, exist_ok=True)
        shutil.copyfile(
            categories_src, os.path.join(alluredir, "categories.json")
        )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(LOGS_DIR, "test_run.log")),
        ],
    )
    config.addinivalue_line(
        "markers",
        "visual: capture an end-of-test screenshot into the Allure report "
        "(on pass or fail), for visually validating a flow against the spec",
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


def _attach_screenshot(driver, name):
    """Save a PNG to ``screenshots/`` and attach it to the Allure report.

    Shared by the on-demand ``screenshot`` fixture and the failure/visual hooks.
    Returns the file path, or None if capture failed.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    base = "%s_%s" % (_safe_name(name), timestamp)
    png_path = os.path.join(SCREENSHOTS_DIR, base + ".png")

    try:
        driver.save_screenshot(png_path)
        if allure is not None:
            allure.attach.file(
                png_path,
                name=name,
                attachment_type=allure.attachment_type.PNG,
            )
        return png_path
    except Exception as error:  # noqa: BLE001
        LOG.warning("Could not capture screenshot '%s': %s", name, error)
        return None


@pytest.fixture
def screenshot(browser):
    """Capture a named screenshot into the Allure report at any point in a test.

    Usage:
        def test_x(browser, screenshot):
            ...
            screenshot("filtered grid")   # appears as a step + attachment
    """
    def _capture(name):
        if allure is not None:
            with allure.step("Screenshot: %s" % name):
                return _attach_screenshot(browser, name)
        return _attach_screenshot(browser, name)

    return _capture


def _capture_failure(item, driver):
    """Save a screenshot + page source on failure and attach to Allure."""
    try:
        url = driver.current_url
    except Exception:  # noqa: BLE001
        url = "unknown"
    LOG.error("Test FAILED: %s (url: %s)", item.nodeid, url)

    _attach_screenshot(driver, "failure-%s" % _safe_name(item.nodeid))

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base = "%s_%s" % (_safe_name(item.nodeid), timestamp)
    html_path = os.path.join(LOGS_DIR, base + ".html")

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

    if report.when != "call":
        return

    driver = item.funcargs.get("browser")
    if driver is None:
        return

    if report.failed:
        _capture_failure(item, driver)
    elif item.get_closest_marker("visual"):
        # Record the final on-screen state for visual spec validation.
        _attach_screenshot(driver, "final-state")
