import pytest

from tests.admin_portal.login.conftest import open_login_page


def test_login_validation_both_fields_empty(browser):

    login_page = open_login_page(browser)

    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()


def test_login_validation_email_empty(browser):

    login_page = open_login_page(browser)

    login_page.enter_password("dummy-password")
    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()


def test_login_validation_password_empty(browser):

    login_page = open_login_page(browser)

    login_page.enter_email_or_phone("admin@nxtwash.com")
    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()


@pytest.mark.parametrize("email", ["abc", "abc@", "abc@gmail"])
def test_login_validation_invalid_email_formats(browser, email):

    login_page = open_login_page(browser)

    login_page.login_with(email, "dummy-password")
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()
