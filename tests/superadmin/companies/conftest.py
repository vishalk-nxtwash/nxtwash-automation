import pytest

from pages.superadmin.companies_page import CompaniesPage
from pages.superadmin.create_company_page import CreateCompanyPage
from pages.superadmin.edit_company_page import EditCompanyPage
from pages.superadmin.login_page import LoginPage
from pages.superadmin.sidebar import Sidebar

# Pre-existing staging company — never created by automation.
# Update email / phone if the actual staging values differ.
COMPANY_NAME = "vkautomationcompanytest"

PRIMARY_COMPANY = {
    "name": "vkautomationcompanytest",
    # Actual staging values — fill in to unlock field-value assertions in edit tests.
    # Leave empty to run only the "field is non-empty" checks (always active).
    "email": "",
    "phone": "",
}


@pytest.fixture
def companies_page(browser):
    """Log in to Superadmin and return a loaded Companies list page."""
    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()
    login_page.wait_for_url("https://superadmin.nxtwash.com/")

    Sidebar(browser).open_companies()

    page = CompaniesPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def edit_company_page(companies_page, browser):
    """Navigate to the edit form for the primary test company."""
    companies_page.filter_by_company_name(COMPANY_NAME)
    companies_page.open_company_edit(COMPANY_NAME)

    page = EditCompanyPage(browser)
    page.wait_for_loaded(COMPANY_NAME)
    return page


@pytest.fixture
def create_company_page(companies_page, browser):
    """Navigate from Companies list to the Create Company form."""
    companies_page.click_add_company()

    page = CreateCompanyPage(browser)
    page.wait_for_loaded()
    return page
