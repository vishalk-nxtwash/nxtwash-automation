import allure

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("Password"),
]


def test_password_field_is_masked_by_default(login_page):
    """SA-LGN-SEC-001 — The password field renders as type='password' (masked) on page load."""
    assert login_page.password_is_masked(), \
        "Password input should have type='password' so it is masked by default"
