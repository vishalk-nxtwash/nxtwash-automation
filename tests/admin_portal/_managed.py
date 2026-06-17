"""Shared helpers for managed (self-cleaning) test data.

Most Admin Portal catalog entities (memberships, discounts, gift-card products,
sites, ...) cannot be deleted through the product, so throwaway "create then
delete" data is not possible. Instead each feature keeps a single dedicated
record and **resets it to a known baseline** before and after every test that
mutates it — no delete required, no data accumulation, and parallel-safe as long
as each test owns its own record.

All managed records are named with ``AUTOTEST_PREFIX`` so an orphan sweeper (or a
human) can identify framework-owned data at a glance.

Per-feature usage (the only part that repeats):

    # in tests/admin_portal/<feature>/conftest.py
    from tests.admin_portal._managed import managed_name, managed_resource

    MANAGED_X = managed_name("Widget")        # -> "AUTOTEST Widget"

    def reset_managed_x(browser):
        page = open_x_page(browser)
        # create the record once if missing, then reset its mutable fields
        ...
        return page

    managed_widget = managed_resource(reset_managed_x)   # the fixture
"""
import logging

import pytest

LOG = logging.getLogger("nxtwash")

AUTOTEST_PREFIX = "AUTOTEST"


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
        # Setup reset is strict: the test needs a known baseline to start.
        page = reset(browser)
        try:
            yield page
        finally:
            # Teardown reset is best-effort: a flaky cleanup (e.g. a slow
            # save/list-reload under parallel load) must not turn an otherwise
            # passing test into an ERROR. The next test's setup reset
            # re-establishes the baseline regardless.
            try:
                reset(browser)
            except Exception as error:  # noqa: BLE001
                LOG.warning(
                    "Managed teardown reset failed (non-fatal): %s", error
                )

    return _managed_fixture
