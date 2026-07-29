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


def managed_name(label):
    """Build a sweeper-identifiable name for a managed record."""
    return "%s %s" % (AUTOTEST_PREFIX, label)


def managed_resource(reset):
    """Return a pytest fixture that keeps a dedicated record at baseline.

    ``reset(browser)`` must ensure the record exists and bring its mutable
    fields to a known baseline, returning the feature page object. It runs both
    before the test (setup) and after it (teardown), so every test starts from a
    clean record and never leaves dirty state behind — even if it fails.
    """

    @pytest.fixture
    def _managed_fixture(browser):
        page = reset(browser)
        try:
            yield page
        finally:
            reset(browser)

    return _managed_fixture
