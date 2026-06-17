import allure

from tests.admin_portal.login.conftest import configured_credentials
from tests.admin_portal.login.conftest import open_login_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("Negative"),
]


def test_login_invalid_email_valid_password_does_not_authenticate(browser):

    login_page = open_login_page(browser)
    _, valid_password = configured_credentials(login_page)

    login_page.login_with("invalid.user@example.com", valid_password)
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()


def test_login_valid_email_invalid_password_does_not_authenticate(browser):

    login_page = open_login_page(browser)
    valid_username, _ = configured_credentials(login_page)

    login_page.login_with(valid_username, "wrong-password")
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()


def test_login_invalid_email_invalid_password_does_not_authenticate(browser):

    login_page = open_login_page(browser)

    login_page.login_with("not-an-email", "wrong-password")
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()
