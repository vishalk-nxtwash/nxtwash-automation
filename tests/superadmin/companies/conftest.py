import warnings

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.superadmin.companies_page import CompaniesPage
from pages.superadmin.create_company_page import CreateCompanyPage
from pages.superadmin.edit_company_page import EditCompanyPage
from pages.superadmin.login_page import LoginPage
from pages.superadmin.sidebar import Sidebar

# Test company used for all companies-module tests.
# NxtWash enforces lowercase-no-spaces company names (the form normalizes any input),
# so "VK automation Company Test" is stored and displayed as "vkautomationcompanytest".
TEST_COMPANY = "vkautomationcompanytest"

_COMPANY_SETUP = {
    "site_name": "vkautotestco",
    "password": "VkAuto@2024!",
    "address1": "123 Automation Street",
    "zip": "78701",
    "country": "United States",
    "state": "Texas",
    "city": "Austin",
}


def _first_visible_react_option(driver, timeout=10):
    """Return the first visible [@role='option'] element in the DOM."""
    return WebDriverWait(driver, timeout).until(
        lambda d: next(
            (
                el
                for el in d.find_elements(By.XPATH, "//*[@role='option']")
                if el.is_displayed() and el.text.strip()
            ),
            None,
        )
    )


def _try_fill(driver, locators, value, timeout=5):
    """Try each locator in turn; fill and return True on first hit, False if none found."""
    for loc in locators:
        try:
            el = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located(loc)
            )
            driver.execute_script("arguments[0].select();", el)
            el.send_keys(value)
            return True
        except Exception:
            continue
    return False


@pytest.fixture(scope="session", autouse=True)
def ensure_test_company_exists(request):
    """Create TEST_COMPANY in staging before any test in this module runs.

    Uses its own browser instance so it does not interfere with the
    function-scoped ``browser`` fixture used by individual tests.
    If the company already exists the fixture returns immediately.
    On any failure a warning is issued (tests that need the company will
    fail individually rather than all being blocked at setup).
    """
    from core.driver_factory import DriverFactory

    headless = request.config.getoption("--headless", default=False)
    driver = DriverFactory.get_driver(headless=headless, detach=False)
    driver.set_page_load_timeout(60)

    try:
        # ── Login ─────────────────────────────────────────────────────────────
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login()
        login_page.wait_for_overview()

        # ── Navigate to Companies list ────────────────────────────────────────
        Sidebar(driver).open_companies()
        companies_page = CompaniesPage(driver)
        companies_page.wait_for_loaded()

        # ── Check if company already exists (8-second tolerance) ───────────────
        companies_page.open_filters()
        companies_page.enter_text(companies_page.COMPANY_NAME_FILTER, TEST_COMPANY)
        companies_page.apply_filters()

        try:
            WebDriverWait(driver, 8).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//*[normalize-space()='{TEST_COMPANY}']")
                )
            )
            return  # company found — nothing to create
        except Exception:
            pass  # not found → proceed to create

        # ── Open Create Company form ───────────────────────────────────────────
        companies_page.click_add_company()
        create_page = CreateCompanyPage(driver)
        create_page.wait_for_loaded()

        # ── Company Name (required) ───────────────────────────────────────────
        create_page.fill_company_name(TEST_COMPANY)

        # ── Site Name (required) ──────────────────────────────────────────────
        create_page.fill_site_name(_COMPANY_SETUP["site_name"])

        # ── Password (required) ───────────────────────────────────────────────
        create_page.fill_password(_COMPANY_SETUP["password"])

        # ── Email — label-relative XPath is confirmed to work on staging ────────
        _try_fill(
            driver,
            [
                (By.XPATH, "//*[normalize-space(text())='Email']/following::input[1]"),
                (By.XPATH, "//input[@type='email']"),
                (By.NAME, "email"),
                (By.NAME, "adminEmail"),
            ],
            "vkautocompanytest@nxtwash.com",
            timeout=4,
        )

        # ── Phone — label-relative XPath first ───────────────────────────────
        _try_fill(
            driver,
            [
                (By.XPATH,
                 "//*[normalize-space(text())='Phone number']/following::input[1]"),
                (By.XPATH, "//input[@type='tel']"),
                (By.NAME, "phone"),
                (By.NAME, "phoneNumber"),
            ],
            "5551234567",
            timeout=4,
        )

        # ── Address 1 (required) ──────────────────────────────────────────────
        create_page.fill_address1(_COMPANY_SETUP["address1"])

        # ── Zip (required) ────────────────────────────────────────────────────
        create_page.fill_zip(_COMPANY_SETUP["zip"])

        # ── Database: pick first available option ──────────────────────────────
        create_page.click(create_page._DATABASE_CTRL)
        first_db = _first_visible_react_option(driver)
        driver.execute_script("arguments[0].click();", first_db)

        # ── Location (country → state → city cascade) ─────────────────────────
        create_page.select_country(_COMPANY_SETUP["country"])
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(create_page._STATE_CTRL)
        )
        create_page.select_state(_COMPANY_SETUP["state"])
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(create_page._CITY_CTRL)
        )
        create_page.select_city(_COMPANY_SETUP["city"])

        # ── Timezone: pick first available option ─────────────────────────────
        create_page.click(create_page._TIMEZONE_CTRL)
        first_tz = _first_visible_react_option(driver)
        driver.execute_script("arguments[0].click();", first_tz)

        # ── Submit ────────────────────────────────────────────────────────────
        create_page.submit()

        # Wait for navigation away from the create page (success) or for a known
        # error keyword to appear (so we don't wait the full 30 s on rejection).
        WebDriverWait(driver, 30).until(
            lambda d: "/companies/create" not in d.current_url
            or "already" in d.find_element(By.TAG_NAME, "body").text.lower()
            or "duplicate" in d.find_element(By.TAG_NAME, "body").text.lower()
        )

        # After the wait exits, verify we actually navigated away. If we're still
        # on the create page the submission was rejected (duplicate site-name,
        # validation error, etc.) and the company was NOT created.
        if "/companies/create" in driver.current_url:
            body_snip = driver.find_element(By.TAG_NAME, "body").text[:400]
            warnings.warn(
                f"ensure_test_company_exists: form submission stayed on create page — "
                f"'{TEST_COMPANY}' was NOT created. Page text: {body_snip}",
                stacklevel=2,
            )

    except Exception as exc:
        # Warn rather than fail — individual tests that need the company will
        # report their own errors; do not block the whole suite.
        warnings.warn(
            f"ensure_test_company_exists: could not guarantee '{TEST_COMPANY}' "
            f"exists in staging. Tests that depend on it may fail.\nReason: {exc}",
            stacklevel=2,
        )
    finally:
        try:
            driver.set_page_load_timeout(5)
            driver.get("about:blank")
        except Exception:
            pass
        try:
            driver.quit()
        except Exception:
            pass


# ── Per-test fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def companies_page(browser):
    """Log in to Superadmin and return a loaded Companies list page."""
    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()
    login_page.wait_for_overview()

    sidebar = Sidebar(browser)
    sidebar.open_companies()

    page = CompaniesPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def create_company_page(companies_page, browser):
    """Navigate from the Companies list to the Create Company form."""
    companies_page.click_add_company()

    page = CreateCompanyPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def edit_company_page(companies_page, browser):
    """Navigate to the edit page for the staging test company."""
    companies_page.filter_by_company_name(TEST_COMPANY)
    companies_page.open_company_edit(TEST_COMPANY)

    page = EditCompanyPage(browser)
    page.wait_for_loaded(TEST_COMPANY)
    return page
