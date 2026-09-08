import allure


pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("Validation"),
]

_VALID_EMAIL = "admin@example.com"


def test_blank_email_blocks_submission(login_page):
    """SA-LGN-VAL-001 — an empty email field prevents form submission."""
    login_page.enter_password("dummy-password")
    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page(), \
        "Should remain on login page when email field is blank"
    assert "Overview" not in login_page.get_body_text()


def test_blank_password_blocks_submission(login_page):
    """SA-LGN-VAL-002 — an empty password field prevents form submission."""
    login_page.enter_email(_VALID_EMAIL)
    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page(), \
        "Should remain on login page when password field is blank"
    assert "Overview" not in login_page.get_body_text()


def test_both_fields_blank_blocks_submission(login_page):
    """SA-LGN-VAL-003 — both fields empty prevents form submission."""
    login_page.click_login()
    login_page.wait_for_login_failure()

    assert login_page.is_login_page(), \
        "Should remain on login page when both fields are blank"
    assert "Overview" not in login_page.get_body_text()


def test_invalid_email_format_blocks_submission(login_page):
    """SA-LGN-VAL-004 — browser-level email validation rejects a missing '@'."""
    login_page.login_with("not-a-valid-email", "dummy-password")
    login_page.wait_for_login_failure()

    assert login_page.is_login_page(), \
        "Browser email format validation should block submission for 'not-a-valid-email'"
    assert "Overview" not in login_page.get_body_text()


def test_email_field_label_is_visible(login_page):
    """SA-LGN-VAL-005 — the email field is identified by a visible label.

    The app uses a <label> element ('Email') rather than an HTML placeholder
    attribute. Asserting the label is visible covers the same spec intent.
    """
    assert login_page.email_label_is_visible(), \
        "Email label should be visible to identify the email input field"
    assert "Email" in login_page.get_body_text(), \
        "Expected 'Email' label text to be present on the login page"
