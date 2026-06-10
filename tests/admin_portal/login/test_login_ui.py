from tests.admin_portal.login.conftest import open_login_page


def test_login_page_loads(browser):

    login_page = open_login_page(browser)

    assert login_page.is_login_page()
    assert "Log in" in login_page.get_body_text()


def test_login_logo_is_available(browser):

    login_page = open_login_page(browser)

    assert login_page.logo_is_present()


def test_login_fields_and_button_are_visible(browser):

    login_page = open_login_page(browser)

    assert login_page.email_field_is_visible()
    assert login_page.password_field_is_visible()
    assert login_page.login_button_is_visible()
    assert login_page.login_button_is_enabled()


def test_login_footer_is_displayed(browser):

    login_page = open_login_page(browser)

    assert "NxtWash LLC 2026" in login_page.get_footer_text()
    assert "All right reserved" in login_page.get_footer_text()


def test_login_browser_title(browser):

    login_page = open_login_page(browser)

    assert "Admin Portal NxtWash" == login_page.get_browser_title()
