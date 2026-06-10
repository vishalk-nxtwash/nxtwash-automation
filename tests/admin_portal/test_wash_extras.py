from pages.admin_portal.login_page import AdminLoginPage
from pages.admin_portal.sidebar import AdminSidebar
from pages.admin_portal.wash_extras_page import WashExtrasPage


EXISTING_EXTRA = "Detailing"
MISSING_EXTRA = "wash-extra-does-not-exist-automation"


def open_wash_extras_page(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()
    login_page.login()
    login_page.wait_for_overview()

    sidebar = AdminSidebar(browser)
    sidebar.open_wash_extras()

    wash_extras_page = WashExtrasPage(browser)
    wash_extras_page.wait_for_list_loaded()

    return wash_extras_page


def test_wash_extras_page_loads(browser):

    wash_extras_page = open_wash_extras_page(browser)

    assert "Wash extra name" in wash_extras_page.get_body_text()
    assert "Price" in wash_extras_page.get_body_text()
    assert "Status" in wash_extras_page.get_body_text()


def test_wash_extras_existing_extra_search(browser):

    wash_extras_page = open_wash_extras_page(browser)
    wash_extras_page.search_extra(EXISTING_EXTRA)

    assert wash_extras_page.wait_for_extra_row(EXISTING_EXTRA).is_displayed()


def test_wash_extras_missing_extra_search(browser):

    wash_extras_page = open_wash_extras_page(browser)
    wash_extras_page.search_extra(MISSING_EXTRA)

    assert MISSING_EXTRA not in wash_extras_page.get_body_text()


def test_wash_extras_filter_panel_shows_controls(browser):

    wash_extras_page = open_wash_extras_page(browser)
    wash_extras_page.open_filter_panel()

    assert "Select site" in wash_extras_page.get_body_text()
    assert "Apply filters" in wash_extras_page.get_body_text()
    assert "Reset all" in wash_extras_page.get_body_text()


def test_wash_extras_download_button_is_available(browser):

    wash_extras_page = open_wash_extras_page(browser)

    assert wash_extras_page.download_button_is_clickable()
