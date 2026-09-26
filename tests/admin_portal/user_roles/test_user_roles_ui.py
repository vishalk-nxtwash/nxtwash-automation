import allure
import pytest

from tests.admin_portal.user_roles.conftest import (
    open_user_roles_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("User Roles"),
    allure.story("UI"),
]


@allure.title("UR-UI-001 User roles page loads with all primary controls")
@pytest.mark.prod_smoke
def test_user_roles_page_loads_with_primary_controls(browser):
    page = open_user_roles_page(browser)
    body = page.get_body_text()

    assert "User roles" in body, "Page heading 'User roles' not found"
    assert page.driver.find_element(*page.SEARCH_INPUT).is_displayed(), (
        "Search input not visible"
    )
    assert page.driver.find_element(*page.FILTER_BUTTON).is_displayed(), (
        "Filter button not visible"
    )
    assert page.driver.find_element(*page.ADD_ROLE_BUTTON).is_displayed(), (
        "Add role button not visible"
    )
    assert page_has_no_broken_state(page)


@allure.title("UR-UI-002 User roles grid shows required column headers")
@pytest.mark.prod_smoke
def test_user_roles_grid_columns_are_visible(browser):
    page = open_user_roles_page(browser)
    body = page.get_body_text()

    assert "User role name" in body, "Column 'User role name' not found"
    assert "Role Type" in body, "Column 'Role Type' not found"
    assert "Status" in body, "Column 'Status' not found"
    assert "Edit" in body, "Column 'Edit' not found"
    assert page_has_no_broken_state(page)
