import allure
import pytest

from tests.admin_portal.users.conftest import (
    open_users_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Users"),
    allure.story("UI"),
]


@allure.title("USR-UI-001 Users page loads with all primary controls")
@pytest.mark.prod_smoke
def test_users_page_loads_with_primary_controls(browser):
    page = open_users_page(browser)
    body = page.get_body_text()

    assert "Users" in body, "Page heading 'Users' not found"
    assert page.driver.find_element(*page.SEARCH_INPUT).is_displayed(), (
        "Search input not visible"
    )
    assert page.driver.find_element(*page.FILTER_BUTTON).is_displayed(), (
        "Filter button not visible"
    )
    assert page.driver.find_element(*page.ADD_USER_BUTTON).is_displayed(), (
        "Add user button not visible"
    )
    assert page_has_no_broken_state(page)


@allure.title("USR-UI-002 Users grid shows required column headers")
@pytest.mark.prod_smoke
def test_users_grid_columns_are_visible(browser):
    page = open_users_page(browser)
    body = page.get_body_text()

    assert "Email address" in body, "Column 'Email address' not found"
    assert "First name" in body, "Column 'First name' not found"
    assert "Status" in body, "Column 'Status' not found"
    assert "Edit" in body, "Column 'Edit' not found"
    assert page_has_no_broken_state(page)
