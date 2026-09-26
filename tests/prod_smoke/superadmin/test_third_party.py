import allure
import pytest

from pages.superadmin.sales_path_page import SalesPathPage
from pages.superadmin.third_party_setup_page import WebhookSetupPage
from pages.superadmin.third_party_subscribers_page import SubscribersPage
from tests.prod_smoke.conftest import page_is_up


pytestmark = [
    allure.epic("Production Smoke"),
    allure.feature("Superadmin Third Party"),
    pytest.mark.prod_smoke,
]


@pytest.fixture
def sales_path_page(superadmin_session, sidebar):
    sidebar.open_sales_path()
    page = SalesPathPage(superadmin_session)
    page.wait_for_loaded()
    return page


@pytest.fixture
def subscribers_page(superadmin_session, sidebar):
    sidebar.open_subscribers()
    page = SubscribersPage(superadmin_session)
    page.wait_for_loaded()
    return page


@pytest.fixture
def webhook_setup_page(superadmin_session, sidebar):
    sidebar.open_webhook_setup()
    page = WebhookSetupPage(superadmin_session)
    page.wait_for_loaded()
    return page


# ── Sales Path ────────────────────────────────────────────────────────────────

@allure.title("SA-PSMO-SLP-001 Sales Path list loads without error")
@pytest.mark.prod_smoke
def test_sales_path_list_loads(sales_path_page):
    assert page_is_up(sales_path_page.driver)
    assert sales_path_page.get_column_headers(), \
        "Sales Path table should render column headers"


# ── Webhook Subscribers ───────────────────────────────────────────────────────

@allure.title("SA-PSMO-SUB-001 Webhook Subscribers list loads without error")
@pytest.mark.prod_smoke
def test_subscribers_list_loads(subscribers_page):
    assert page_is_up(subscribers_page.driver)
    assert subscribers_page.get_column_headers(), \
        "Subscribers table should render column headers"


# ── Webhook Setup ─────────────────────────────────────────────────────────────

@allure.title("SA-PSMO-SET-001 Webhook Setup list loads without error")
@pytest.mark.prod_smoke
def test_webhook_setup_list_loads(webhook_setup_page):
    assert page_is_up(webhook_setup_page.driver)
    assert webhook_setup_page.get_column_headers(), \
        "Webhook Setup table should render column headers"
