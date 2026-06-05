from pages.superadmin.login_page import LoginPage
from pages.superadmin.sidebar import Sidebar
from pages.superadmin.companies_page import CompaniesPage


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