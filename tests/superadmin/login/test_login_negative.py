import allure
import pytest

from core.config_manager import ConfigManager


pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("Negative"),
]


def test_wrong_password_shows_error(login_page, login_credentials):
    """SA-LGN-NG-001 — valid email + wrong password is rejected by the server."""
    valid_email, _ = login_credentials

    login_page.login_with(valid_email, "wrong-password-xyz")
    login_page.wait_for_login_failure()
    login_page.wait_for_auth_error()

    assert login_page.is_login_page(), \
        "Should remain on login page after wrong password"
    assert "Overview" not in login_page.get_body_text()


def test_nonexistent_email_shows_error(login_page):
    """SA-LGN-NG-002 — a non-existent account is rejected by the server."""
    login_page.login_with("nonexistent.user@example.com", "dummy-password")
    login_page.wait_for_login_failure()
    login_page.wait_for_auth_error()

    assert login_page.is_login_page(), \
        "Should remain on login page for a non-existent account"
    assert "Overview" not in login_page.get_body_text()


@pytest.mark.parametrize(
    ("email", "password"),
    [
        ("' OR 1=1 --", "password"),
        ("admin@example.com", "' OR 1=1 --"),
        ("<script>alert(1)</script>", "password"),
        ("admin@example.com", "<script>alert(1)</script>"),
    ],
)
def test_injection_payloads_do_not_authenticate(login_page, email, password):
    """SA-LGN-NG-003 — SQL / XSS payloads are rejected without crashing."""
    login_page.login_with(email, password)
    login_page.wait_for_login_failure()

    assert login_page.is_login_page(), \
        f"Malicious payload ({email!r}, {password!r}) must not grant access"
    assert "Overview" not in login_page.get_body_text()


def test_non_superadmin_account_is_rejected(login_page):
    """SA-LGN-NG-004 — an admin-portal account cannot log in to Superadmin."""
    config = ConfigManager()
    admin_email = config.get_username("admin_portal")
    admin_password = config.get_password("admin_portal")

    login_page.login_with(admin_email, admin_password)
    login_page.wait_for_login_failure()
    login_page.wait_for_auth_error()

    assert login_page.is_login_page(), \
        "Non-superadmin account must be blocked from the Superadmin portal"
    assert "Overview" not in login_page.get_body_text()
