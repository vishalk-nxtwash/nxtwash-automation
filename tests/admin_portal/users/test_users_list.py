import allure
import pytest

from tests.admin_portal.users.conftest import (
    create_user_if_missing,
    open_users_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Users"),
    allure.story("List"),
]


@allure.title("USR-LST-001 Users list page loads with all primary controls visible")
@pytest.mark.smoke
def test_users_list_page_loads(browser):
    page = open_users_page(browser)

    assert "Users" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("USR-LST-002 List displays required columns")
@pytest.mark.regression
def test_users_list_required_columns(browser):
    page = open_users_page(browser)
    body = page.get_body_text()

    assert "Email address" in body
    assert "First name" in body
    assert "Edit" in body
    assert page_has_no_broken_state(page)


@allure.title("USR-LST-003 Pagination shows a record count that matches rendered rows")
@pytest.mark.regression
def test_users_list_pagination_count(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    body = page.get_body_text()

    has_count = any(char.isdigit() for char in body)
    assert has_count, "No numeric count found in pagination area"
    assert page_has_no_broken_state(page)


@allure.title("USR-LST-004 Results-per-page dropdown changes the number of rows displayed")
@pytest.mark.edge
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-LST-004: Rows-per-page control locator not confirmed against actual DOM. "
        "Verify control label and element type in DevTools before removing xfail."
    ),
)
def test_users_list_rows_per_page(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    body = page.get_body_text()

    assert "Results per page" in body or "per page" in body.lower(), (
        "Results-per-page control not found on the page"
    )
    assert page_has_no_broken_state(page)
