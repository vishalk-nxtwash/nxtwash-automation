import allure
import pytest

from tests.admin_portal.login.conftest import open_login_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("Password"),
]


def test_password_is_masked_by_default(browser):

    login_page = open_login_page(browser)

    assert login_page.password_input_type() == "password"


@pytest.mark.xfail(
    reason="Known product gap: password visibility icon disappears after typing.",
    strict=True,
)
def test_password_visibility_toggle_shows_password(browser):

    login_page = open_login_page(browser)

    if not login_page.password_visibility_toggle_exists():
        pytest.skip("Password visibility toggle is not present on login page.")

    login_page.enter_password("VisiblePassword123")
    login_page.toggle_password_visibility()

    assert login_page.password_input_type() == "text"


@pytest.mark.xfail(
    reason="Known product gap: password visibility icon disappears after typing.",
    strict=True,
)
def test_password_visibility_toggle_hides_password_again(browser):

    login_page = open_login_page(browser)

    if not login_page.password_visibility_toggle_exists():
        pytest.skip("Password visibility toggle is not present on login page.")

    login_page.enter_password("VisiblePassword123")
    login_page.toggle_password_visibility()
    login_page.toggle_password_visibility()

    assert login_page.password_input_type() == "password"


def test_very_long_password_does_not_break_login_ui(browser):

    login_page = open_login_page(browser)

    login_page.enter_password("A" * 512)

    assert login_page.password_field_is_visible()
    assert login_page.login_button_is_visible()
