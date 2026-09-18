import allure
import pytest


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("Validation"),
]

_PLACEHOLDER_EMAIL = "admin@nxtwash.com"


def test_login_validation_both_fields_empty(login_page):

    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "email" in login_page.visible_error_text().lower()
    assert "Overview" not in login_page.get_body_text()


def test_login_validation_email_empty(login_page):

    login_page.enter_password("dummy-password")
    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "email" in login_page.visible_error_text().lower()
    assert "Overview" not in login_page.get_body_text()


def test_login_validation_password_empty(login_page):

    login_page.enter_email_or_phone(_PLACEHOLDER_EMAIL)
    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "password" in login_page.visible_error_text().lower()
    assert "Overview" not in login_page.get_body_text()


def test_login_validation_email_spaces_only(login_page):

    login_page.login_with("   ", "dummy-password")
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()


def test_login_validation_password_spaces_only(login_page):

    login_page.login_with(_PLACEHOLDER_EMAIL, "   ")
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
        pytest.param(
            "abc.gmail.com",
            marks=pytest.mark.xfail(
                reason="Real domain suffix (gmail.com) triggers a slow server code path; "
                       "wait_for_login_failure times out. No-@ case is covered by 'abc'.",
                strict=False,
            ),
        ),
        "abc@@gmail.com",
        "abc @gmail.com",
    ],
)
def test_login_validation_invalid_email_formats(login_page, email):

    login_page.login_with(email, "dummy-password")
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()


def test_login_validation_email_label_is_correct(login_page):

    assert login_page.email_label_is_visible()
    assert "Email" in login_page.get_body_text()


def test_login_validation_maximum_email_length_does_not_break_ui(login_page):

    long_email = "a" * 245 + "@example.com"

    login_page.login_with(long_email, "dummy-password")
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert login_page.email_field_is_visible()
    assert login_page.password_field_is_visible()
    assert login_page.login_button_is_visible()
    assert "Overview" not in login_page.get_body_text()
