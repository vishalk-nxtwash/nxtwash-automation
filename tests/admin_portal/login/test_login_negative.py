import allure


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("Negative"),
]


def test_login_invalid_email_valid_password_does_not_authenticate(login_page, login_credentials):

    _, valid_password = login_credentials

    login_page.login_with("invalid.user@example.com", valid_password)
    login_page.wait_for_login_failure()
    login_page.wait_for_auth_error()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()


def test_login_valid_email_invalid_password_does_not_authenticate(login_page, login_credentials):

    valid_username, _ = login_credentials

    login_page.login_with(valid_username, "wrong-password")
    login_page.wait_for_login_failure()
    login_page.wait_for_auth_error()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()


def test_login_invalid_email_invalid_password_does_not_authenticate(login_page):

    login_page.login_with("not-an-email", "wrong-password")
    login_page.wait_for_login_failure()
    login_page.wait_for_auth_error()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()
