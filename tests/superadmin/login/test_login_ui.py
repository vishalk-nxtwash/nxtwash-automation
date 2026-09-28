import allure

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("UI"),
]


def test_email_input_is_visible(login_page):
    """SA-LGN-UI-003 — Email input field is visible on the login page."""
    assert login_page.email_input_is_visible(), \
        "Email input field should be visible on the login page"


def test_password_input_is_visible(login_page):
    """SA-LGN-UI-004 — Password input field is visible on the login page."""
    assert login_page.password_input_is_visible(), \
        "Password input field should be visible on the login page"


def test_login_button_visible_and_enabled(login_page):
    """SA-LGN-UI-005 — 'Log in' button is visible and enabled before any input."""
    assert login_page.login_button_is_visible_and_enabled(), \
        "Login button should be visible and enabled on page load"
