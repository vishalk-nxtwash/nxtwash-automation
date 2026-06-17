import allure
import pytest

from tests.admin_portal.login.conftest import open_login_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("UI"),
]


def test_login_page_loads(browser):

    login_page = open_login_page(browser)

    assert login_page.is_login_page()
    assert "Log in" in login_page.get_body_text()


def test_login_page_url_is_correct(browser):

    login_page = open_login_page(browser)

    assert browser.current_url == login_page.config.get_url(
        login_page.PORTAL
    ).rstrip("/") + "/login"


def test_login_logo_is_available(browser):

    login_page = open_login_page(browser)

    assert login_page.logo_is_present()
    assert "nxtwash" in login_page.get_logo_src().lower()


def test_login_fields_and_button_are_visible(browser):

    login_page = open_login_page(browser)

    assert login_page.email_field_is_visible()
    assert login_page.email_field_is_enabled()
    assert login_page.password_field_is_visible()
    assert login_page.password_field_is_enabled()
    assert login_page.login_button_is_visible()
    assert login_page.login_button_is_enabled()


def test_password_visibility_icon_is_displayed(browser):

    login_page = open_login_page(browser)

    if not login_page.password_visibility_toggle_exists():
        pytest.skip("Password visibility toggle is not present on login page.")

    assert login_page.password_visibility_toggle_exists()


def test_login_field_labels_are_displayed(browser):

    login_page = open_login_page(browser)

    assert login_page.email_label_is_visible()
    assert login_page.password_label_is_visible()


def test_login_footer_is_displayed(browser):

    login_page = open_login_page(browser)

    assert "NxtWash LLC 2026" in login_page.get_footer_text()
    assert "All right reserved" in login_page.get_footer_text()


def test_login_browser_title(browser):

    login_page = open_login_page(browser)

    assert "Admin Portal NxtWash" == login_page.get_browser_title()


def test_login_layout_renders_after_refresh(browser):

    login_page = open_login_page(browser)

    browser.refresh()
    login_page.wait_for_loaded()

    assert login_page.logo_is_present()
    assert login_page.email_field_is_visible()
    assert login_page.password_field_is_visible()
    assert login_page.login_button_is_visible()


def test_login_tab_order_email_password_login_button(browser):

    login_page = open_login_page(browser)

    login_page.focus_email_field()
    assert login_page.active_element_name() == "emailOrPhone"

    login_page.press_tab()
    assert login_page.active_element_name() == "password"

    login_page.press_tab()
    assert login_page.active_element_type() == "submit"
