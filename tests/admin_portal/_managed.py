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
import logging
import os

import pytest
from selenium.common.exceptions import TimeoutException

# pytest-timeout (--timeout-method=signal) raises this on a global-timeout
# hit, regardless of what code was executing when the signal landed. It is
# pytest's own internal outcome type for `pytest.fail()` -- not an
# Exception subclass, so a plain `except Exception` would not catch it.
from _pytest.outcomes import Failed as _PytestTimeoutFailed

LOG = logging.getLogger("nxtwash")

_IS_CI = bool(
    os.environ.get("CI")
    or os.environ.get("GITHUB_ACTIONS")
    or os.environ.get("JENKINS_URL")
    or os.environ.get("CIRCLECI")
)
AUTOTEST_PREFIX = "CI-AUTOTEST" if _IS_CI else "AUTOTEST"


def managed_name(label):
    """Build a sweeper-identifiable name for a managed record."""
    return "%s %s" % (AUTOTEST_PREFIX, label)


def managed_resource(reset):
    """Return a pytest fixture that keeps a dedicated record at baseline.

    ``reset(browser)`` must ensure the record exists and bring its mutable
    fields to a known baseline, returning the feature page object. It runs both
    before the test (setup) and after it (teardown), so every test starts from a
    clean record and never leaves dirty state behind — even if it fails.

    A timeout in the TEARDOWN reset specifically is swallowed (logged, not
    raised): by that point the test's own body already ran and reported its
    own outcome, so failing the item here would blame the test for a slow
    cleanup step, not a real test failure. The next test's own setup calls
    reset() again with a fresh timeout budget, bringing the record back to
    baseline then — nothing stays dirty either way. A timeout during SETUP
    (above, before the test runs) is NOT swallowed: proceeding into a test
    against an unknown, possibly-not-reset record would be unsafe.

    Confirmed source of these teardown timeouts in practice: the AWS
    self-hosted runner's own intermittent connection slowness occasionally
    pushing one item's setup+call+teardown time past pytest's global
    --timeout (see admin-portal-frozen memory, ROUND 4) -- not a bug in any
    reset() implementation. Only TimeoutException and pytest-timeout's own
    Failed outcome are swallowed; any other exception from reset() during
    teardown still fails the item, so a real bug in a reset() implementation
    is not hidden by this.
    """

    @pytest.fixture
    def _managed_fixture(browser):
        page = reset(browser)
        try:
            yield page
        finally:
            try:
                reset(browser)
            except (TimeoutException, _PytestTimeoutFailed) as exc:
                LOG.warning(
                    "managed_resource teardown reset failed (%s: %s) -- "
                    "swallowing, next test's setup will retry fresh",
                    type(exc).__name__, exc,
                )

    return _managed_fixture
