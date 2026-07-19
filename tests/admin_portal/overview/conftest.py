# Overview test suite
#
# ENVIRONMENT NOTE — legacy iframe gap
# ─────────────────────────────────────
# The Overview dashboard is rendered inside a legacy iframe
# (//iframe[contains(@src,'legacy')]).  In the current staging/test
# environment this iframe loads empty, so all assertions that call
# overview_page.get_legacy_dashboard_text() will find an empty string
# and fail — hence the widespread @pytest.mark.xfail(strict=False) markers.
#
# When the iframe environment is working (production or a correctly seeded
# staging tenant), remove the xfail markers from all tests in this package
# to promote them to live regression tests.  The test logic itself is
# already correct; only the environment is the blocker.

import pytest

from pages.admin_portal.overview_page import AdminOverviewPage
from tests.admin_portal.admin_session import open_admin_path

# ── Filter test data ──────────────────────────────────────────────────────────
# Site used across all filter and widget tests.
OVERVIEW_SITE = "Vk test carwash 2"

# Primary date preset used in filter tests.
OVERVIEW_DATE_PRESET = "Last Month"

# Explicit date range equivalent to "Last Month" relative to July 2026.
# Update these when tests need a specific historical window.
OVERVIEW_DATE_FROM = "2026-06-01"
OVERVIEW_DATE_TO = "2026-06-30"


@pytest.fixture
def overview_page(browser):
    open_admin_path(browser, "/")
    page = AdminOverviewPage(browser)
    page.wait_for_loaded()
    return page
