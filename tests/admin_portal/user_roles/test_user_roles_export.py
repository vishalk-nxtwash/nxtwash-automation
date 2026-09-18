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


@allure.title("UR-EXP-001 Export panel opens and export can be submitted without error")
@pytest.mark.edge
def test_user_roles_export_button_clickable(browser):
    page = open_user_roles_page(browser)

    if page.driver.execute_script(page._JS_FIND_EXPORT_BTN) is None:
        pytest.skip("Export button not available on this environment")

    with allure.step("Click the download icon to open the export panel"):
        page.click_export_button()

    with allure.step("Submit the export form"):
        page.submit_export()

    assert page_has_no_broken_state(page)
