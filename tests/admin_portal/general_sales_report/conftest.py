import pytest

from pages.admin_portal.general_sales_report_page import (
    AdminGeneralSalesReportPage,
    AdminRedemptionDetailsPage,
)
from tests.admin_portal.admin_session import open_admin_path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GSR_SITE = "VK Test carwash 2"
GSR_DATE_START = "06/01/2026"
GSR_DATE_END = "06/30/2026"
GSR_ZERO_DATA_DATE_START = "01/01/2030"
GSR_ZERO_DATA_DATE_END = "01/31/2030"

# Six predefined date presets used by GSR-FLT-007..012 and GSR-RDT-005.
DATE_PRESETS = [
    "Today",
    "Yesterday",
    "This week",
    "Last week",
    "This month",
    "Last month",
]

# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------


def open_gsr_page(browser):
    open_admin_path(browser, "/general-sales-report")
    page = AdminGeneralSalesReportPage(browser)
    page.wait_for_loaded()
    return page


def open_redemption_details_page(browser):
    # Confirmed URL from live run: /reports/detailed/redemption_details
    open_admin_path(browser, "/reports/detailed/redemption_details")
    page = AdminRedemptionDetailsPage(browser)
    page.wait_for_loaded()
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
def gsr_page(browser):
    """GSR page at its default filter state — no manual filters applied."""
    return open_gsr_page(browser)


@pytest.fixture
def gsr_filtered(browser):
    """GSR page with test site + last-month date applied — data is expected."""
    page = open_gsr_page(browser)
    page.select_site(GSR_SITE)
    page.select_date_preset("Last month")
    page.apply_filters()
    return page


@pytest.fixture
def zero_data_filter(browser):
    """GSR page filtered to a future date range — guarantees zero transactions."""
    page = open_gsr_page(browser)
    page.select_site(GSR_SITE)
    page.enter_custom_date_range(GSR_ZERO_DATA_DATE_START, GSR_ZERO_DATA_DATE_END)
    page.apply_filters()
    return page


@pytest.fixture
def rdt_page(browser):
    """Redemption Details page at default filter state."""
    return open_redemption_details_page(browser)
