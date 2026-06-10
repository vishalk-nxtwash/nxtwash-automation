from pages.admin_portal.login_page import AdminLoginPage
from pages.admin_portal.sidebar import AdminSidebar
from pages.admin_portal.wash_packages_page import WashPackagesPage


EXISTING_PACKAGE = "Plus Wash"
MISSING_PACKAGE = "wash-package-does-not-exist-automation"
ASSIGNMENT_SITE = "VK Test carwash 2"


def open_wash_packages_page(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()
    login_page.login()
    login_page.wait_for_overview()

    sidebar = AdminSidebar(browser)
    sidebar.open_wash_packages()

    wash_packages_page = WashPackagesPage(browser)
    wash_packages_page.wait_for_list_loaded()

    return wash_packages_page


def test_wash_packages_page_loads(browser):

    wash_packages_page = open_wash_packages_page(browser)

    assert "Wash package name" in wash_packages_page.get_body_text()
    assert "Price" in wash_packages_page.get_body_text()
    assert "Status" in wash_packages_page.get_body_text()


def test_wash_packages_existing_package_search(browser):

    wash_packages_page = open_wash_packages_page(browser)
    wash_packages_page.search_package(EXISTING_PACKAGE)

    assert wash_packages_page.wait_for_package_row(EXISTING_PACKAGE).is_displayed()


def test_wash_packages_missing_package_search(browser):

    wash_packages_page = open_wash_packages_page(browser)
    wash_packages_page.search_package(MISSING_PACKAGE)

    assert MISSING_PACKAGE not in wash_packages_page.get_body_text()


def test_wash_packages_filter_panel_shows_controls(browser):

    wash_packages_page = open_wash_packages_page(browser)
    wash_packages_page.open_filter_panel()

    assert "Select site" in wash_packages_page.get_body_text()
    assert "Apply filters" in wash_packages_page.get_body_text()
    assert "Reset all" in wash_packages_page.get_body_text()


def test_wash_packages_download_button_is_available(browser):

    wash_packages_page = open_wash_packages_page(browser)

    assert wash_packages_page.download_button_is_clickable()
