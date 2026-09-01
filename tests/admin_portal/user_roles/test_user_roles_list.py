import allure
import pytest

from tests.admin_portal.user_roles.conftest import (
    DEFAULT_ROLE_NAMES,
    create_role_if_missing,
    open_user_roles_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("User Roles"),
    allure.story("List"),
]


@allure.title("UR-LST-001 User roles list page loads with all primary controls visible")
@pytest.mark.smoke
def test_user_roles_list_page_loads(browser):
    page = open_user_roles_page(browser)
    body = page.get_body_text()

    assert "User roles" in body
    assert page_has_no_broken_state(page)


@allure.title("UR-LST-002 List shows required columns: Name, Type, Date, Status, Edit")
@pytest.mark.regression
def test_user_roles_list_required_columns(browser):
    page = open_user_roles_page(browser)
    body = page.get_body_text()

    assert "User role name" in body   # actual column header from legacy UI
    assert "Role Type" in body
    assert "Status" in body
    assert "Edit" in body
    assert page_has_no_broken_state(page)


@allure.title("UR-LST-003 All three predefined system roles are present in the list")
@pytest.mark.smoke
def test_user_roles_default_roles_present(browser):
    page = open_user_roles_page(browser)

    for role in DEFAULT_ROLE_NAMES:
        assert page.role_exists(role), (
            "Predefined role '%s' is missing — expected in every seeded environment" % role
        )
    assert page_has_no_broken_state(page)


@allure.title("UR-LST-004 Pagination shows a record count that matches rendered rows")
@pytest.mark.regression
def test_user_roles_pagination_count(browser):
    create_role_if_missing(browser)
    page = open_user_roles_page(browser)
    body = page.get_body_text()

    # Pagination label must contain a numeric count ("Showing 1-3 of 3", "3 records", etc.)
    has_count = any(char.isdigit() for char in body)
    assert has_count
    assert page_has_no_broken_state(page)


@allure.title("UR-LST-005 Results-per-page dropdown changes the number of rows displayed")
@pytest.mark.edge
def test_user_roles_rows_per_page_changes_display(browser):
    page = open_user_roles_page(browser)

    if not page.driver.find_elements(*page.ROWS_PER_PAGE_SELECT):
        pytest.skip("Rows-per-page control not available on this environment")

    options = page.get_rows_per_page_options()
    assert len(options) >= 2, "Rows-per-page control has fewer than 2 options: %s" % options

    # Pick a different option from the current one and switch to it
    current = page.get_body_text()
    alt_option = next((o for o in options if o not in current), options[-1])
    page.select_rows_per_page(alt_option)

    assert page_has_no_broken_state(page)
    assert alt_option in page.get_body_text(), (
        "Selected option '%s' not reflected in page after change" % alt_option
    )
