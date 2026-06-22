import allure
import pytest


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("Security"),
]


@pytest.mark.parametrize(
    ("email", "password"),
    [
        ("' OR 1=1 --", "password"),
        ("admin@example.com", "' OR 1=1 --"),
        ("<script>alert(1)</script>", "password"),
        ("admin@example.com", "<script>alert(1)</script>"),
    ]
)
def test_login_security_payloads_do_not_authenticate(login_page, email, password):

    login_page.login_with(email, password)
    login_page.wait_for_login_failure()

    assert login_page.is_login_page()
    assert "Overview" not in login_page.get_body_text()
