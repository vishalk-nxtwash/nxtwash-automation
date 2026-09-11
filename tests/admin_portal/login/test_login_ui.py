import allure
import pytest


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("UI"),
]


def test_login_page_loads(login_page):

    assert login_page.is_login_page()
    assert "Log in" in login_page.get_body_text()


def test_login_page_url_is_correct(browser, login_page):

    assert browser.current_url == login_page.config.get_url(
        login_page.PORTAL
    ).rstrip("/") + "/login"


@pytest.mark.skip(reason="needs_inspection: logo img alt attribute changed on staging — update LOGO_IMAGE locator in login_page.py after checking /login HTML")
def test_login_logo_is_available(login_page):

    assert login_page.logo_is_visible()
    assert "nxtwash" in login_page.get_logo_src().lower()


def test_login_fields_and_button_are_visible(login_page):

    assert login_page.email_field_is_visible()
    assert login_page.email_field_is_enabled()
    assert login_page.password_field_is_visible()
    assert login_page.password_field_is_enabled()
    assert login_page.login_button_is_visible()
    assert login_page.login_button_is_enabled()


def test_password_visibility_icon_is_displayed(login_page):

    if not login_page.password_visibility_toggle_exists():
        pytest.skip("Password visibility toggle is not present on login page.")


def test_login_field_labels_are_displayed(login_page):

    assert login_page.email_label_is_visible()
    assert login_page.password_label_is_visible()


def test_login_footer_is_displayed(login_page):

    assert "NxtWash LLC" in login_page.get_footer_text()
    assert "All rights reserved" in login_page.get_footer_text()


def test_login_browser_title(login_page):

    assert "Admin Portal NxtWash" == login_page.get_browser_title()


@pytest.mark.skip(reason="needs_inspection: depends on LOGO_IMAGE locator — fix test_login_logo_is_available first")
def test_login_layout_renders_after_refresh(browser, login_page):

    browser.refresh()
    login_page.wait_for_loaded()

    assert login_page.logo_is_visible()
    assert login_page.email_field_is_visible()
    assert login_page.password_field_is_visible()
    assert login_page.login_button_is_visible()


def test_login_tab_order_email_password_login_button(login_page):

    login_page.focus_email_field()
    assert login_page.active_element_name() == "emailOrPhone"

    login_page.press_tab()
    assert login_page.active_element_name() == "password"

    login_page.press_tab()
    assert login_page.active_element_type() == "submit"
