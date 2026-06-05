from pages.superadmin.login_page import LoginPage
from pages.superadmin.sidebar import Sidebar
from pages.superadmin.companies_page import CompaniesPage
from pages.superadmin.create_company_page import CreateCompanyPage


def test_open_create_company(browser):

    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()

    login_page.wait_for_url(
        "https://superadmin.nxtwash.com/"
    )

    sidebar = Sidebar(browser)
    sidebar.open_companies()

    companies_page = CompaniesPage(browser)
    companies_page.click_add_company()

    create_company_page = CreateCompanyPage(browser)

    create_company_page.wait_for_url(
        "https://superadmin.nxtwash.com/companies/create"
    )

    assert browser.current_url == (
        "https://superadmin.nxtwash.com/companies/create"
    )

    assert create_company_page.get_text(
        create_company_page.COMPANY_BASE_SETTINGS_TITLE
    ) == "Company Base Settings"