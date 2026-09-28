import allure
import pytest

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("Negative"),
]


def test_wrong_password_shows_error(login_page):
    """SA-LGN-NG-001 — A valid email with the wrong password shows a server auth error."""
    login_page.enter_email(login_page.config.get_username("superadmin"))
    login_page.enter_password("WrongPassword!999")
    login_page.click_login()
    login_page.wait_for_auth_error()
    assert login_page.is_on_login_page(), \
        "Wrong password should keep the user on the login page with an error"


def test_nonexistent_email_shows_error(login_page):
    """SA-LGN-NG-002 — A non-existent email address shows a server auth error."""
    login_page.enter_email("no.such.user.xyz999@nxtwash.com")
    login_page.enter_password("SomePassword!123")
    login_page.click_login()
    login_page.wait_for_auth_error()
    assert login_page.is_on_login_page(), \
        "Non-existent email should keep the user on the login page with an error"


def test_sql_xss_payload_in_email_does_not_crash(login_page):
    """SA-LGN-NG-003 — SQL/XSS payload in the email field is safely rejected (no crash/redirect)."""
    login_page.enter_email_native("' OR '1'='1; <script>alert(1)</script>")
    login_page.enter_password("SomePassword!123")
    login_page.click_login()
    assert login_page.is_on_login_page(), \
        "SQL/XSS payload should not bypass login or cause a crash"
    assert not login_page.body_contains("overview"), \
        "SQL/XSS payload must not result in successful login"


@pytest.mark.xfail(
    strict=False,
    reason="SA-LGN-NG-004: Requires a known non-superadmin account. Falls back to "
           "admin_portal credentials — xfails if those are not configured or also "
           "have superadmin access.",
)
def test_non_superadmin_account_cannot_login(login_page):
    """SA-LGN-NG-004 — An account without superadmin access cannot log in to the superadmin portal."""
    from core.config_manager import ConfigManager
    config = ConfigManager()
    try:
        email    = config.get_username("admin_portal")
        password = config.get_password("admin_portal")
    except RuntimeError:
        pytest.xfail("Admin-portal credentials not configured — cannot exercise NG-004")

    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_login()
    login_page.wait_for_auth_error()
    assert login_page.is_on_login_page(), \
        "A non-superadmin account should be rejected and stay on the login page"
