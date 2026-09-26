import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.superadmin.login_page import LoginPage
from pages.superadmin.sales_path_page import (
    CreateSalesPathPage,
    EditSalesPathPage,
    SalesPathPage,
)
from pages.superadmin.sidebar import Sidebar
from pages.superadmin.third_party_setup_page import (
    CreateSetupPage,
    EditSetupPage,
    WebhookSetupPage,
)
from pages.superadmin.third_party_subscribers_page import (
    CreateSubscriberPage,
    EditSubscriberPage,
    SubscribersPage,
)

_BASE_URL = "https://superadmin.nxtwash.com"

# ── Automation test record constants ─────────────────────────────────────────

# Webhook Subscribers
SUBSCRIBER_NAME = "VK Auto Test Sub"
SUBSCRIBER_ABBR = "VT"

# Pre-existing staging records (never modified by automation)
REF_SUBSCRIBER_NAME = "Tether"
REF_SUBSCRIBER_ABBR = "TE"

# Webhook Setup
SETUP_COMPANY = "vkautomationcompanytest"
SETUP_SUBSCRIBER = "Tether"
SETUP_URL = "https://webhook-test.nxtwash.com/api/test"
SETUP_KEY = "vkautotestkey12345abcdef"

# Sales Path
SALES_PATH_COMPANY = "vkautomationcompanytest"


# ── Login helper ──────────────────────────────────────────────────────────────

def _login_and_wait(browser):
    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()
    login_page.wait_for_url("https://superadmin.nxtwash.com/")


# ── Webhook Subscribers fixtures ──────────────────────────────────────────────

@pytest.fixture
def subscribers_page(browser):
    """Log in and navigate to the Webhook Subscribers list."""
    _login_and_wait(browser)
    Sidebar(browser).open_subscribers()
    page = SubscribersPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def create_subscriber_page(subscribers_page, browser):
    """Navigate from the list to the Add Webhook Subscriber form."""
    subscribers_page.click_add_subscriber()
    page = CreateSubscriberPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def edit_subscriber_page(subscribers_page, browser):
    """Navigate to the Edit form for the automation test subscriber.

    Creates the record first if it does not yet exist on staging.
    """
    if not subscribers_page.row_exists(SUBSCRIBER_NAME):
        subscribers_page.click_add_subscriber()
        cp = CreateSubscriberPage(browser)
        cp.wait_for_loaded()
        cp.enter_name(SUBSCRIBER_NAME)
        cp.enter_abbreviation(SUBSCRIBER_ABBR)
        cp.click_save_new()
        WebDriverWait(browser, 30).until(
            EC.url_contains("/third-party/subscribers")
        )
        subscribers_page.wait_for_loaded()

    subscribers_page.open_edit(SUBSCRIBER_NAME)
    page = EditSubscriberPage(browser)
    page.wait_for_loaded()
    return page


# ── Webhook Setup fixtures ────────────────────────────────────────────────────

@pytest.fixture
def webhook_setup_page(browser):
    """Log in and navigate to the Webhook Setup list."""
    _login_and_wait(browser)
    Sidebar(browser).open_webhook_setup()
    page = WebhookSetupPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def create_setup_page(webhook_setup_page, browser):
    """Navigate from the list to the Add Webhook Setup form."""
    webhook_setup_page.click_add_setup()
    page = CreateSetupPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def edit_setup_page(webhook_setup_page, browser):
    """Navigate to the Edit form for the automation test setup.

    Creates the record first if it does not yet exist on staging.
    """
    if not webhook_setup_page.row_exists(SETUP_COMPANY, timeout=30):
        webhook_setup_page.click_add_setup()
        cp = CreateSetupPage(browser)
        cp.wait_for_loaded()
        cp.select_subscriber(SETUP_SUBSCRIBER)
        cp.select_company(SETUP_COMPANY)
        cp.enter_url(SETUP_URL)
        cp.enter_key(SETUP_KEY)
        cp.click_save_new()
        WebDriverWait(browser, 30).until(
            EC.url_contains("/third-party/setup")
        )
        webhook_setup_page.wait_for_loaded()

    webhook_setup_page.filter_by_company_name(SETUP_COMPANY)
    webhook_setup_page.open_edit(SETUP_COMPANY)
    page = EditSetupPage(browser)
    page.wait_for_loaded()
    return page


# ── Sales Path fixtures ───────────────────────────────────────────────────────

@pytest.fixture
def sales_path_page(browser):
    """Log in and navigate to the Sales Path list."""
    _login_and_wait(browser)
    Sidebar(browser).open_sales_path()
    page = SalesPathPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def create_sales_path_page(sales_path_page, browser):
    """Navigate from the list to the Add Sales Path form."""
    sales_path_page.click_add_sales_path()
    page = CreateSalesPathPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def edit_sales_path_page(sales_path_page, browser):
    """Navigate to the Edit form for the automation test sales path.

    Creates the record first if it does not yet exist on staging.
    """
    if not sales_path_page.row_exists(SALES_PATH_COMPANY, timeout=30):
        sales_path_page.click_add_sales_path()
        cp = CreateSalesPathPage(browser)
        cp.wait_for_loaded()
        cp.select_company(SALES_PATH_COMPANY)
        cp.click_save_new()
        WebDriverWait(browser, 30).until(
            EC.url_contains("/sales-path")
        )
        sales_path_page.wait_for_loaded()

    sales_path_page.filter_by_company_name(SALES_PATH_COMPANY)
    sales_path_page.open_edit(SALES_PATH_COMPANY)
    page = EditSalesPathPage(browser)
    page.wait_for_loaded()
    return page
