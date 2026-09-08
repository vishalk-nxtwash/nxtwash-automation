import allure
import pytest


pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Login"),
    allure.story("Password Visibility"),
]


def test_password_is_masked_by_default(login_page):
    """SA-LGN-SEC-001 — the password field type is 'password' on page load."""
    assert login_page.password_input_type() == "password", \
        "Password field should be masked (type='password') by default"


@pytest.mark.xfail(
    reason="Toggle presence unconfirmed per test spec (SA-LGN-UI-006) — "
           "verify the eye-icon locator against the live app before un-xfailing.",
    strict=False,
)
def test_password_visibility_toggle_reveals_text(login_page):
    """SA-LGN-SEC-002 — clicking the eye toggle changes the field type to 'text'."""
    if not login_page.password_visibility_toggle_exists():
        pytest.skip("Password visibility toggle is not present on this build.")

    login_page.enter_password("VisiblePassword123")
    login_page.toggle_password_visibility()

    assert login_page.password_input_type() == "text", \
        "Password field should switch to type='text' after toggling visibility"


def test_password_visibility_toggle_re_masks_password(login_page):
    """SA-LGN-SEC-003 — toggling twice returns the field to type='password'."""
    if not login_page.password_visibility_toggle_exists():
        pytest.skip("Password visibility toggle is not present on this build.")

    login_page.enter_password("VisiblePassword123")
    login_page.toggle_password_visibility()
    login_page.toggle_password_visibility()

    assert login_page.password_input_type() == "password", \
        "Password field should return to type='password' after toggling twice"
