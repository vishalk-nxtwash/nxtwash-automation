import allure

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("Validation"),
]


def test_blank_email_blocks_submission(login_page):
    """SA-LGN-VAL-001 — Submitting with a blank email field does not log the user in."""
    login_page.enter_password(login_page.config.get_password("superadmin"))
    login_page.click_login()
    assert login_page.is_on_login_page(), \
        "Submitting with a blank email should keep the user on the login page"


def test_blank_password_blocks_submission(login_page):
    """SA-LGN-VAL-002 — Submitting with a blank password field does not log the user in."""
    login_page.enter_email(login_page.config.get_username("superadmin"))
    login_page.click_login()
    assert login_page.is_on_login_page(), \
        "Submitting with a blank password should keep the user on the login page"


def test_invalid_email_format_blocks_submission(login_page):
    """SA-LGN-VAL-004 — An email missing '@' is rejected and does not log the user in."""
    login_page.enter_email_native("invalidemail")
    login_page.enter_password(login_page.config.get_password("superadmin"))
    login_page.click_login()
    assert login_page.is_on_login_page(), \
        "An email without '@' should be rejected and keep the user on the login page"
