import allure
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.cash_report_page import CashReportPage
from pages.admin_portal.card_declines_page import CardDeclinesPage
from pages.admin_portal.general_sales_report_page import AdminGeneralSalesReportPage
from pages.admin_portal.labor_shifts_page import LaborShiftsPage
from pages.admin_portal.performance_metrics_page import PerformanceMetricsPage
from pages.admin_portal.redemptions_page import RedemptionsPage
from pages.admin_portal.revenue_overview_page import RevenueOverviewPage
from pages.admin_portal.transactions_page import TransactionsPage
from pages.admin_portal.wash_activity_page import WashActivityPage
from tests.admin_portal.admin_session import open_admin_path
from tests.prod_smoke.conftest import page_is_up


pytestmark = [
    allure.epic("Production Smoke"),
    allure.feature("Reports"),
    pytest.mark.prod_smoke,
]


@allure.title("PSMO-RPT-001 Revenue Overview report page loads")
@pytest.mark.prod_smoke
def test_revenue_overview_loads(browser):
    open_admin_path(browser, "/reports/detailed/revenue")
    page = RevenueOverviewPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-RPT-002 Cash Report filter modal opens on page load")
@pytest.mark.prod_smoke
def test_cash_report_loads(browser):
    open_admin_path(browser, "/reports/detailed/cash_report")
    page = CashReportPage(browser)
    page.wait_for_modal()

    assert page_is_up(browser)
    assert page.modal_is_open(), "Cash Report filter modal did not open"


@allure.title("PSMO-RPT-003 Card Declines filter modal opens on page load")
@pytest.mark.prod_smoke
def test_card_declines_loads(browser):
    open_admin_path(browser, "/reports/detailed/cc_declines")
    page = CardDeclinesPage(browser)
    page.wait_for_modal()

    assert page_is_up(browser)
    assert page.modal_is_open(), "Card Declines filter modal did not open"


@allure.title("PSMO-RPT-004 Transactions report page loads with filter button")
@pytest.mark.prod_smoke
def test_transactions_report_loads(browser):
    open_admin_path(browser, "/transactions/report")
    page = TransactionsPage(browser)

    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located(page.PAGE_TITLE)
    )
    assert page_is_up(browser)


@allure.title("PSMO-RPT-005 Wash Activity filter modal opens on page load")
@pytest.mark.prod_smoke
def test_wash_activity_loads(browser):
    open_admin_path(browser, "/reports/detailed/cars_washed")
    page = WashActivityPage(browser)
    page.wait_for_modal()

    assert page_is_up(browser)
    assert page.modal_is_open(), "Wash Activity filter modal did not open"


@allure.title("PSMO-RPT-006 Labor & Shifts filter modal opens on page load")
@pytest.mark.prod_smoke
def test_labor_shifts_loads(browser):
    open_admin_path(browser, "/reports/detailed/employee_labor")
    page = LaborShiftsPage(browser)
    page.wait_for_modal()

    assert page_is_up(browser)
    assert page.modal_is_open(), "Labor & Shifts filter modal did not open"


@allure.title("PSMO-RPT-007 General Sales Report page loads")
@pytest.mark.prod_smoke
def test_general_sales_report_loads(browser):
    open_admin_path(browser, "/general-sales-report")
    page = AdminGeneralSalesReportPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-RPT-008 Performance Metrics page loads")
@pytest.mark.prod_smoke
def test_performance_metrics_loads(browser):
    open_admin_path(browser, "/performance-metrics")
    page = PerformanceMetricsPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-RPT-009 Redemptions report page loads")
@pytest.mark.prod_smoke
def test_redemptions_report_loads(browser):
    open_admin_path(browser, "/reports/detailed/redemption_details")
    page = RedemptionsPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)
