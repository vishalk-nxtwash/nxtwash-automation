from pages.admin_portal.login_page import AdminLoginPage


def open_login_page(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()

    return login_page


def configured_credentials(login_page):

    return (
        login_page.config.get_username(login_page.PORTAL),
        login_page.config.get_password(login_page.PORTAL)
    )
