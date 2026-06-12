import allure
import pytest

from tests.admin_portal.login.conftest import open_login_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("Validation"),
]


def test_login_validation_both_fields_empty(browser):

    login_page = open_login_page(browser)

    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "email" in login_page.visible_error_text().lower()
    assert "Overview" not in login_page.get_body_text()


def test_login_validation_email_empty(browser):

    login_page = open_login_page(browser)

    login_page.enter_password("dummy-password")
    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "email" in login_page.visible_error_text().lower()
    assert "Overview" not in login_page.get_body_text()


def test_login_validation_password_empty(browser):

    login_page = open_login_page(browser)

    login_page.enter_email_or_phone("admin@nxtwash.com")
    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "password" in login_page.visible_error_text().lower()
    assert "Overview" not in login_page.get_body_text()


def test_login_validation_email_spaces_only(browser):

    login_page = open_login_page(browser)

    login_page.login_with("   ", "dummy-password")
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()


def test_login_validation_password_spaces_only(browser):

    login_page = open_login_page(browser)

    login_page.login_with("admin@nxtwash.com", "   ")
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()


@pytest.mark.parametrize(
    "email",
    [
        "abc",
        "abc@",
        "@gmail.com",
        "abc@gmail",
        "abc.gmail.com",
        "abc@@gmail.com",
        "abc @gmail.com",
    ],
)
def test_login_validation_invalid_email_formats(browser, email):

    login_page = open_login_page(browser)

    login_page.login_with(email, "dummy-password")
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()


def test_login_validation_maximum_email_length_does_not_break_ui(browser):

    login_page = open_login_page(browser)
    long_email = "a" * 245 + "@example.com"

    login_page.login_with(long_email, "dummy-password")
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert login_page.email_field_is_visible()
    assert login_page.password_field_is_visible()
    assert login_page.login_button_is_visible()
    assert "Overview" not in login_page.get_body_text()
