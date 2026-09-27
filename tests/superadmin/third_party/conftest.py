import warnings

import pytest
from selenium.common.exceptions import TimeoutException
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


# Managed subscriber (reset-to-baseline, rename-reset variant — see
# tests/admin_portal/_managed.py). Subscribers cannot be deleted, so the edit
# tests share ONE record, identified by id, and reset it before and after each
# test. Names produced by the edit tests ("<base> Edited ...") are recognised
# as this record so an aborted run self-heals instead of orphaning it.
_SUBSCRIBER_BASELINE = {"thirdPartyName": SUBSCRIBER_NAME, "abbreviation": SUBSCRIBER_ABBR, "isActive": True}


def _is_managed_subscriber(name):
    return name == SUBSCRIBER_NAME or name.startswith(SUBSCRIBER_NAME + " Edited")


def _wait_for_subscriber_api(page, subscriber_id, expected, timeout=20):
    """Block until the backend record matches ``expected``; return last seen."""
    seen = {}

    def _matches(_driver):
        seen.update(page.get_by_id_with_api(subscriber_id))
        return all(seen.get(k) == v for k, v in expected.items())

    try:
        WebDriverWait(page.driver, timeout, poll_frequency=1).until(_matches)
    except TimeoutException:
        pass
    return {k: seen.get(k) for k in expected}


def reset_managed_subscriber(browser):
    """Ensure the managed subscriber exists at baseline; return its id."""
    page = SubscribersPage(browser)
    matches = [s for s in page.list_with_api() if _is_managed_subscriber(s["thirdPartyName"])]
    # Prefer the record holding the canonical name (renaming another record to
    # it would 499 on uniqueness), then the newest.
    matches.sort(key=lambda s: (s["thirdPartyName"] != SUBSCRIBER_NAME, -s["thirdPartyId"]))

    if not matches:
        browser.get(_BASE_URL + "/third-party/subscribers/create")
        cp = CreateSubscriberPage(browser)
        cp.wait_for_loaded()
        cp.enter_name(SUBSCRIBER_NAME)
        cp.enter_abbreviation(SUBSCRIBER_ABBR)
        cp.click_save_new()
        cp.confirm_yes_if_present()
        WebDriverWait(browser, 20, poll_frequency=1).until(
            lambda d: any(s["thirdPartyName"] == SUBSCRIBER_NAME for s in page.list_with_api())
        )
        matches = [s for s in page.list_with_api() if s["thirdPartyName"] == SUBSCRIBER_NAME]

    subscriber_id = matches[0]["thirdPartyId"]
    record = page.get_by_id_with_api(subscriber_id)
    if any(record.get(k) != v for k, v in _SUBSCRIBER_BASELINE.items()):
        browser.get("%s/third-party/subscribers/%s" % (_BASE_URL, subscriber_id))
        ep = EditSubscriberPage(browser)
        ep.wait_for_loaded()
        WebDriverWait(browser, 15).until(lambda d: ep.get_name() != "")
        ep.set_name(SUBSCRIBER_NAME)
        ep.set_abbreviation(SUBSCRIBER_ABBR)
        ep.set_active_toggle(True)
        ep.click_save_changes()
        ep.confirm_yes_if_present()
        seen = _wait_for_subscriber_api(page, subscriber_id, _SUBSCRIBER_BASELINE)
        assert seen == _SUBSCRIBER_BASELINE, \
            "Could not reset managed subscriber %s to baseline: %s" % (subscriber_id, seen)
    return subscriber_id


@pytest.fixture
def managed_subscriber_id(browser):
    """Id of the managed subscriber, at baseline before and after the test."""
    _login_and_wait(browser)
    subscriber_id = reset_managed_subscriber(browser)
    try:
        yield subscriber_id
    finally:
        try:
            reset_managed_subscriber(browser)
        except Exception as exc:  # noqa: BLE001
            warnings.warn("Managed subscriber teardown reset failed: %s" % exc)


@pytest.fixture
def edit_subscriber_page(managed_subscriber_id, browser):
    """Open the Edit form of the managed subscriber directly by id."""
    browser.get("%s/third-party/subscribers/%s" % (_BASE_URL, managed_subscriber_id))
    page = EditSubscriberPage(browser)
    page.wait_for_loaded(expected_name=SUBSCRIBER_NAME)
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
    # Filter first — row_exists on an unfiltered paginated list misses page-2+ records
    webhook_setup_page.filter_by_company_name(SETUP_COMPANY)

    if not webhook_setup_page.row_exists(SETUP_COMPANY, timeout=10):
        webhook_setup_page.wait_for_loaded()
        webhook_setup_page.click_add_setup()
        cp = CreateSetupPage(browser)
        cp.wait_for_loaded()
        cp.select_subscriber(SETUP_SUBSCRIBER)
        cp.select_company(SETUP_COMPANY)
        cp.enter_url(SETUP_URL)
        cp.enter_key(SETUP_KEY)
        # Server requires at least one event type — select the first
        from pages.superadmin.third_party_setup_page import EVENT_TYPE_NAMES
        cp.set_event(EVENT_TYPE_NAMES[0], True)
        cp.click_save_new()
        cp.confirm_yes_if_present(timeout=5)
        # Wait for any navigation away from /create
        WebDriverWait(browser, 30).until(
            lambda d: "/create" not in d.current_url
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

    Handles three cases:
      1. Record exists and is enabled  → open it directly.
      2. Record exists but is disabled → re-enable it, then open.
      3. Record does not exist         → create it, then open.
    """
    from selenium.webdriver.common.by import By as _By

    def _filter_all_states():
        """Open filter with both enabled/active toggles OFF so all records show."""
        sales_path_page.open_filters()
        for toggle_loc, label_xp in [
            (sales_path_page.ENABLED_TOGGLE,
             "//div[normalize-space()='Enabled Sales Path']/following-sibling::label[1]"),
            (sales_path_page.ACTIVE_TOGGLE,
             "//div[normalize-space()='Active Sales Path']/following-sibling::label[1]"),
        ]:
            els = browser.find_elements(*toggle_loc)
            if els and els[0].is_selected():
                lbls = browser.find_elements(_By.XPATH, label_xp)
                if lbls:
                    browser.execute_script("arguments[0].click();", lbls[0])
        sales_path_page.enter_text(sales_path_page.COMPANY_NAME_FILTER, SALES_PATH_COMPANY)
        sales_path_page.apply_filters()

    def _re_enable_and_return():
        """Enable isEnabled on the currently-open edit page, save, and return the page."""
        ep = EditSalesPathPage(browser)
        ep.wait_for_loaded()
        is_en_els = browser.find_elements(_By.NAME, "isEnabled")
        if is_en_els and not is_en_els[0].is_selected():
            browser.execute_script("""
                var inp = arguments[0], id = inp.id;
                var lbl = id ? document.querySelector('label[for="' + id + '"]') : null;
                if (!lbl) lbl = inp.closest('label');
                if (!lbl) lbl = inp.parentElement;
                if (lbl) lbl.click(); else inp.click();
            """, is_en_els[0])
            ep.click_save_changes()
            ep.confirm_yes_if_present(timeout=5)
            WebDriverWait(browser, 20).until(
                lambda d: "/sales-path" in d.current_url and "/create" not in d.current_url
                and browser.find_elements(_By.XPATH, "//*[normalize-space()='Sales Path List']")
            )
            sales_path_page.wait_for_loaded()
            sales_path_page.filter_by_company_name(SALES_PATH_COMPANY)
            sales_path_page.open_edit(SALES_PATH_COMPANY)
            ep = EditSalesPathPage(browser)
            ep.wait_for_loaded()
        return ep

    # ── 1. Standard filter (enabled + active ON) ─────────────────────────────
    sales_path_page.filter_by_company_name(SALES_PATH_COMPANY)
    if sales_path_page.row_exists(SALES_PATH_COMPANY, timeout=8):
        sales_path_page.open_edit(SALES_PATH_COMPANY)
        # open_edit is a JS click — wait for the SPA to reach the edit route
        # before handing the page over, or tests read the list URL.
        ep = EditSalesPathPage(browser)
        ep.wait_for_loaded()
        return ep

    # ── 2. Record disabled — find it with toggles OFF ─────────────────────────
    sales_path_page.wait_for_loaded()
    _filter_all_states()
    if sales_path_page.row_exists(SALES_PATH_COMPANY, timeout=8):
        sales_path_page.open_edit(SALES_PATH_COMPANY)
        return _re_enable_and_return()

    # ── 3. Record doesn't exist — create it ──────────────────────────────────
    sales_path_page.wait_for_loaded()
    sales_path_page.click_add_sales_path()
    cp = CreateSalesPathPage(browser)
    cp.wait_for_loaded()
    cp.select_company(SALES_PATH_COMPANY)
    cp.click_save_new()
    cp.confirm_yes_if_present(timeout=5)
    try:
        WebDriverWait(browser, 15).until(lambda d: "/create" not in d.current_url)
    except Exception:
        # Creation blocked (possibly existing disabled record) — go back to list
        browser.get("https://superadmin.nxtwash.com/sales-path")
        sales_path_page.wait_for_loaded()
    _filter_all_states()
    sales_path_page.open_edit(SALES_PATH_COMPANY)
    return _re_enable_and_return()
