from pages.admin_portal.login_page import AdminLoginPage


def test_admin_login(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()
    login_page.login()
    login_page.wait_for_overview()

    assert browser.current_url == login_page.config.get_url(
        login_page.PORTAL
    )
    assert login_page.get_overview_text() == "Overview"
