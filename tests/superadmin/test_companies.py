from pages.superadmin.login_page import LoginPage
from pages.superadmin.sidebar import Sidebar
from pages.superadmin.companies_page import CompaniesPage


COMPANY_NAME = "vktestcompany"
AP_STAGING_URL = "https://staging.nxtwash.com/"


def test_open_companies(browser):

    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()

    login_page.wait_for_url(
        "https://superadmin.nxtwash.com/"
    )

    sidebar = Sidebar(browser)
    sidebar.open_companies()

    companies_page = CompaniesPage(browser)

    assert browser.current_url == "https://superadmin.nxtwash.com/companies"

    assert companies_page.get_text(
        companies_page.PAGE_TITLE
    ) == "Companies"


def test_login_to_vktestcompany_admin_portal_ap_staging(browser):

    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()

    login_page.wait_for_url(
        "https://superadmin.nxtwash.com/"
    )

    sidebar = Sidebar(browser)
    sidebar.open_companies()

    companies_page = CompaniesPage(browser)
    companies_page.wait_for_loaded()

    companies_page.login_to_admin_portal_ap_staging(COMPANY_NAME)
    companies_page.wait_for_ap_staging_overview()

    assert browser.current_url == AP_STAGING_URL
    assert companies_page.get_text(
        companies_page.AP_OVERVIEW_TEXT
    ) == "Overview"
