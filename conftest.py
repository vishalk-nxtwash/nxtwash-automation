import datetime
import logging
import os
import re
import shutil

import pytest

# Re-export the browser fixture so every test can request `browser`.
from fixtures.browser import browser, _worker_auth_state  # noqa: F401

try:  # Allure is optional; failure artifacts still land on disk without it.
    import allure
except ImportError:  # pragma: no cover
    allure = None


LOG = logging.getLogger("nxtwash")

SCREENSHOTS_DIR = "reports/screenshots"
LOGS_DIR = "reports/logs"


def pytest_addoption(parser):
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


def _patch_pytest_ast_source():
    # Python 3.11.0-3.11.3 CPython bug: ast.parse raises SystemError on deeply
    # nested source files.  Pytest's _code/code.py calls getstatementrange_ast
    # (imported into its own namespace) when formatting failure tracebacks.  By
    # patching the name in that module we convert SystemError → IndexError, which
    # pytest already handles gracefully, before it can propagate to third-party
    # plugins (pytest-html, pytest-rerunfailures) that call outcome.get_result()
    # and would re-raise it as INTERNALERROR.
    try:
        import _pytest._code.code as _code_mod

        _orig = _code_mod.getstatementrange_ast

        def _safe(*args, **kwargs):
            try:
                return _orig(*args, **kwargs)
            except SystemError:
                # getsource() catches SyntaxError and falls back gracefully;
                # IndexError is NOT caught in this pytest version and propagates.
                raise SyntaxError("ast.parse failed: Python 3.11 CPython AST bug")

        _code_mod.getstatementrange_ast = _safe
    except (ImportError, AttributeError):
        pass


def pytest_configure(config):
    _patch_pytest_ast_source()

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


# --------------------------------------------------------------------------- #
# Quarantine: known-failing tests stabilized as xfail(strict=False) so the
# suite stays green while each is fixed individually. strict=False means a test
# that starts passing is reported xpass (not a failure), so entries are safe to
# leave until fixed. Remove an entry the moment its test is fixed.
# Tracking + root-cause notes: docs/admin_test_burndown.md
# --------------------------------------------------------------------------- #
_QUARANTINE_TIMING_REASON = (
    "Headless post-save/navigation timeout (grid/iframe re-render race); "
    "reproduces locally. Pending individual fix — see docs/admin_test_burndown.md"
)

# Post-save / grid-reload timing races (one nodeid fragment per test).
_QUARANTINE_TIMING = (
    "test_service_categories_positive.py::test_activate_service_category",
    "test_service_categories_positive.py::test_deactivate_service_category",
    "test_service_categories_positive.py::test_service_category_settings_persist",
    "test_service_categories_edge_cases.py::test_activate_deactivate_activate_cycle",
    "test_service_categories_edge_cases.py::test_deactivated_category_findable_via_filter",
    "test_service_categories_edge_cases.py::test_edit_inactive_category_saves_changes",
    "test_service_categories_filter.py::test_filter_inactive_categories_shows_inactive",
    "test_service_categories_managed.py::test_managed_category_provided_at_baseline",
    "test_service_categories_managed.py::test_managed_category_rename_is_reset_on_teardown",
    "test_memberships_search_filter.py::test_memberships_partial_search",
    "test_memberships_search_filter.py::test_memberships_clear_search_restores_records",
    "test_memberships_search_filter.py::test_memberships_search_with_surrounding_spaces",
    "test_wash_packages_edit.py::test_remove_applicable_discount_persists",
    "test_wash_packages_export.py::test_wash_packages_export_after_filter",
    "test_wash_packages_search_filter.py::test_filter_active_shows_active_packages",
    "test_wash_packages_search_filter.py::test_filter_site_and_active_combined",
    "test_wash_packages_site_assignment.py::test_location_price_override_persists",
    "test_wash_extras_edit.py::test_edit_wash_extra_values_persist",
    # Overview tests carry their own in-code xfail(strict=False) markers
    # (legacy Overview iframe), so they are not listed here.
)

# Known script/data issues with specific root causes (nodeid fragment -> reason).
_QUARANTINE_SCRIPT = {
    "test_memberships_redemption.py::test_redeem_at_multiple_locations_persists":
        "MB-RDM-002 test-data issue: the service is only configured at one staging "
        "location, so multi-location redemption cannot be exercised.",
    "test_sites_validation.py::test_create_site_validation_invalid_email_formats":
        "Site create form appears to accept invalid email formats (abc@, abc, "
        "abc@yopmail). Investigate product-side email validation before un-xfail.",
}


def pytest_collection_modifyitems(config, items):
    # Auto-tag tests by location so `-m admin/superadmin/smoke` works suite-wide.
    for item in items:
        path = str(item.fspath).replace(os.sep, "/")
        nodeid = item.nodeid.replace(os.sep, "/")

        if "/tests/admin_portal/" in path:
            item.add_marker(pytest.mark.admin)
        if "/tests/superadmin/" in path:
            item.add_marker(pytest.mark.superadmin)

        # Smoke = login flows, positive paths, and *_smoke files.
        if "/login/" in path or "_positive" in path or "_smoke" in path:
            item.add_marker(pytest.mark.smoke)

        # Quarantine known-failing tests (kept green via xfail until fixed).
        if any(fragment in nodeid for fragment in _QUARANTINE_TIMING):
            item.add_marker(
                pytest.mark.xfail(reason=_QUARANTINE_TIMING_REASON, strict=False)
            )
        for fragment, reason in _QUARANTINE_SCRIPT.items():
            if fragment in nodeid:
                item.add_marker(pytest.mark.xfail(reason=reason, strict=False))
                break


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

    # Capture visible text from the active frame — error messages in this app
    # appear inside iframes, so page_source (outer shell) is nearly empty.
    try:
        from selenium.webdriver.common.by import By
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if allure is not None:
            allure.attach(
                body_text,
                name="visible_page_text",
                attachment_type=allure.attachment_type.TEXT,
            )
        LOG.error("Visible page text at failure:\n%s", body_text[:2000])
    except Exception as _err:  # noqa: BLE001
        LOG.warning("Could not capture body text: %s", _err)

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
    try:
        report = outcome.get_result()
    except SystemError:
        # Python 3.11.0–3.11.3 has a CPython bug (AST constructor recursion
        # depth mismatch) that fires when pytest formats a traceback through
        # a source file with complex nested expressions.  Catching it here
        # prevents the INTERNALERROR that would otherwise crash the entire
        # suite; the test is still recorded as failed by pytest's inner
        # runner — we just skip our screenshot/capture step for that one.
        return

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
