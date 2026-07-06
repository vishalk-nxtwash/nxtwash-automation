import allure
import pytest

from tests.admin_portal.user_roles.conftest import (
    open_user_roles_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("User Roles"),
    allure.story("Export"),
]


@allure.title("UR-EXP-001 Export button is clickable and does not break the page")
@pytest.mark.edge
@pytest.mark.xfail(
    strict=False,
    reason=(
        "UR-EXP-001: Export button locator targets text 'Export'/'Download'. "
        "Verify exact button label and element type in DevTools before removing xfail."
    ),
)
def test_user_roles_export_button_clickable(browser):
    page = open_user_roles_page(browser)
    page.click_export_button()
    page.wait_for_loaded()

    assert page_has_no_broken_state(page)
