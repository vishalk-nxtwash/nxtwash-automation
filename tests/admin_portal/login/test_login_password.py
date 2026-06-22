import allure
import pytest


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("Password"),
]


def test_password_is_masked_by_default(login_page):

    assert login_page.password_input_type() == "password"


@pytest.mark.xfail(
    reason="Known product gap: password visibility icon disappears after typing.",
    strict=True,
)
def test_password_visibility_toggle_shows_password(login_page):

    if not login_page.password_visibility_toggle_exists():
        pytest.skip("Password visibility toggle is not present on login page.")

    login_page.enter_password("VisiblePassword123")
    login_page.toggle_password_visibility()

    assert login_page.password_input_type() == "text"


@pytest.mark.xfail(
    reason="Known product gap: password visibility icon disappears after typing.",
    strict=True,
)
def test_password_visibility_toggle_hides_password_again(login_page):

    if not login_page.password_visibility_toggle_exists():
        pytest.skip("Password visibility toggle is not present on login page.")

    login_page.enter_password("VisiblePassword123")
    login_page.toggle_password_visibility()
    login_page.toggle_password_visibility()

    assert login_page.password_input_type() == "password"


def test_very_long_password_does_not_break_login_ui(login_page):

    login_page.enter_password("A" * 512)

    assert login_page.password_field_is_visible()
    assert login_page.login_button_is_visible()
