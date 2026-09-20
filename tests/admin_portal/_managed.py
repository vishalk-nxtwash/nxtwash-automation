"""Shared helpers for managed (self-cleaning) test data.

Most Admin Portal catalog entities (memberships, discounts, gift-card products,
sites, ...) cannot be deleted through the product, so throwaway "create then
delete" data is not possible. Instead each feature keeps a single dedicated
record and **resets it to a known baseline** before and after every test that
mutates it — no delete required, no data accumulation, and parallel-safe as long
as each test owns its own record.

All managed records are named with ``AUTOTEST_PREFIX`` so an orphan sweeper (or a
human) can identify framework-owned data at a glance.

CI/DEV separation (Option A):
  Local dev runs  → prefix "AUTOTEST"        e.g. "AUTOTEST Discount"
  CI pipeline     → prefix "CI-AUTOTEST"     e.g. "CI-AUTOTEST Discount"

CI is detected via standard environment variables (CI, GITHUB_ACTIONS,
JENKINS_URL, CIRCLECI). Set CI=true locally to simulate pipeline naming.

Per-feature usage (the only part that repeats):

    # in tests/admin_portal/<feature>/conftest.py
    from tests.admin_portal._managed import managed_name, managed_resource

    MANAGED_X = managed_name("Widget")        # -> "AUTOTEST Widget" or "CI-AUTOTEST Widget"

    def reset_managed_x(browser):
        page = open_x_page(browser)
        # create the record once if missing, then reset its mutable fields
        ...
        return page

    managed_widget = managed_resource(reset_managed_x)   # the fixture
"""
import os

import pytest

_IS_CI = bool(
    os.environ.get("CI")
    or os.environ.get("GITHUB_ACTIONS")
    or os.environ.get("JENKINS_URL")
    or os.environ.get("CIRCLECI")
)
AUTOTEST_PREFIX = "CI-AUTOTEST" if _IS_CI else "AUTOTEST"


def clear_redux_filters(browser, *table_keys):
    """Delete named entries from Redux Persist's tableFilterReducer before navigation.

    Prevents the SPA from rehydrating with a stale filter (e.g. active-only ON
    from a previous test) that would hide inactive managed records the moment the
    page loads — before any UI-level ``clear_active_filters()`` can fire.

    Each ``table_key`` should match the key used in
    ``tableFilterReducer.tableFilters`` (camelCase, same as the Redux slice).
    Deleting the key makes Redux fall back to the reducer initial state; the
    caller's ``clear_active_filters()`` / ``reset_filters_if_active()`` call
    then normalises that initial state to "no filter active".
    """
    if not table_keys:
        return
    try:
        browser.execute_script(
            """
            try {
                var keys = arguments[0];
                var root = JSON.parse(localStorage.getItem('persist:root') || '{}');
                var tfr = JSON.parse(root.tableFilterReducer || '{}');
                var tf = tfr.tableFilters || {};
                for (var i = 0; i < keys.length; i++) { delete tf[keys[i]]; }
                tfr.tableFilters = tf;
                root.tableFilterReducer = JSON.stringify(tfr);
                localStorage.setItem('persist:root', JSON.stringify(root));
            } catch(e) {}
            """,
            list(table_keys),
        )
    except Exception:
        pass


def managed_name(label):
    """Build a sweeper-identifiable name for a managed record."""
    return "%s %s" % (AUTOTEST_PREFIX, label)


def managed_resource(reset, ensure=None):
    """Return a pytest fixture that keeps a dedicated record at baseline.

    ``reset(browser)`` brings all mutable fields to a known baseline and runs
    in teardown after every test. It also runs in setup when no ``ensure`` is
    provided (backward-compatible behaviour).

    ``ensure(browser)``, when supplied, is the cheaper setup-only alternative:
    it only checks that the record exists and creates it if missing, but skips
    field-level reset. The teardown always runs the full ``reset`` so dirty
    state from one test never leaks to the next.

    Splitting setup/teardown halves fixture overhead for modules whose reset
    involves opening an edit form and re-saving unchanged fields (~30-60 s each).
    """
    _setup = ensure if ensure is not None else reset

    @pytest.fixture
    def _managed_fixture(browser):
        page = _setup(browser)
        try:
            yield page
        finally:
            # Skip teardown when Chrome is dead — reset(browser) would trigger the
            # upsert helper's full retry/create cycle against an unresponsive driver,
            # generating a cascade of ERRORs for zero benefit.  The next test's
            # setup handles restoration from a fresh browser session.
            try:
                browser.execute_script("return 1")
            except Exception:
                return
            reset(browser)

    return _managed_fixture
