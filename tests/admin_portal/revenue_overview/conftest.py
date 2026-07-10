import time

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.revenue_overview_page import RevenueOverviewPage
from tests.admin_portal.admin_session import open_admin_path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RVO_SITE = "VK Test carwash 2"
RVO_SITE_2 = "VK AL02"
RVO_DATE_START = "06/01/2026"
RVO_DATE_END = "06/30/2026"
# Past date guaranteed to have no test transactions (site not yet set up)
RVO_ZERO_DATE_START = "01/01/2022"
RVO_ZERO_DATE_END = "01/31/2022"

# Seven date presets including Custom (sheet: RVO-FMD-002, RVO-DTE-001..008).
DATE_PRESETS = [
    "Today",
    "Yesterday",
    "This week",
    "Last week",
    "This month",
    "Last month",
    "Custom",
]

# Expected KPI values for VK Test carwash 2 + VK AL02, This month.
TOTAL_REVENUE_LAST_MONTH = "$300.00"
TOTAL_REVENUE_THIS_MONTH = "$75.00"
WASH_PACKAGE_AMOUNT = "$60.00"
WASH_EXTRA_AMOUNT = "$15.00"

MEM_NEW_SALES_COUNT = 1
MEM_RECHARGES_COUNT = 0
MEM_RESIGNUPS_COUNT = 2
MEM_TOTAL_COUNT = 3          # New Sales + Recharges + Resignups

# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------


def open_rvo_page(browser):
    open_admin_path(browser, "/reports/detailed/revenue")
    page = RevenueOverviewPage(browser)
    page.wait_for_modal()
    return page


def page_has_no_broken_state(page):
    try:
        body = page.get_body_text().lower()
    except Exception:
        return True
    broken_signals = [
        "something went wrong",
        "internal server error",
        "application error",
        "cannot read",
        "typeerror",
        "uncaught error",
    ]
    return not any(s in body for s in broken_signals)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def rvo_modal(browser):
    """Revenue Overview at Phase 1 — filter modal open, no filters applied."""
    return open_rvo_page(browser)


@pytest.fixture
def rvo_page(browser):
    """Revenue Overview metrics screen with VK Test carwash 2 + VK AL02 + This month applied."""
    page = open_rvo_page(browser)
    page.select_site(RVO_SITE)
    page.select_site(RVO_SITE_2, clear_first=False)
    page.select_date_preset("This month")
    # Wait for the date range field to auto-populate (it shows e.g.
    # "Wednesday, 07/01/2026 - Friday, 07/10/2026" after preset is applied).
    try:
        WebDriverWait(page.driver, 10).until(
            lambda d: page.get_date_range_value() != ""
        )
    except Exception:
        time.sleep(2.0)
    page.apply_modal_filters()
    return page


@pytest.fixture
def zero_data_filter(browser):
    """Revenue Overview filtered to a future date — guarantees zero transactions."""
    page = open_rvo_page(browser)
    page.select_site(RVO_SITE)
    page.enter_date_range(RVO_ZERO_DATE_START, RVO_ZERO_DATE_END)
    page.apply_modal_filters()
    return page


@pytest.fixture
def rvo_single_day(browser):
    """Modal open, both sites selected, Single day checkbox checked."""
    page = open_rvo_page(browser)
    page.select_site(RVO_SITE)
    page.select_site(RVO_SITE_2, clear_first=False)
    page.check_single_day()
    return page
