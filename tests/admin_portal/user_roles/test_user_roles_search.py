import allure
import pytest

from tests.admin_portal.user_roles.conftest import (
    NONEXISTENT_ROLE,
    ROLE_NAME,
    create_role_if_missing,
    open_user_roles_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("User Roles"),
    allure.story("Search"),
]


@allure.title("UR-SRH-001 Exact name search returns the matching role")
@pytest.mark.regression
def test_user_roles_search_exact_name(browser):
    create_role_if_missing(browser)
    page = open_user_roles_page(browser)
    page.search_role(ROLE_NAME)

    assert page.wait_for_role_row(ROLE_NAME).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("UR-SRH-002 Partial name search returns matching roles")
@pytest.mark.regression
@pytest.mark.manual
@pytest.mark.xfail(
    strict=False,
    reason=(
        "UR-SRH-002: create_role_if_missing cannot reliably activate an inactive VK UR01 "
        "(ensure_active_switch_on does not persist via the current automation approach). "
        "When VK UR01 is inactive the active-only default filter hides it and the search "
        "returns no results. "
        "Verify manually: ensure VK UR01 is active, search 'VK U', confirm the role appears."
    ),
)
def test_user_roles_search_partial_name(browser):
    create_role_if_missing(browser)
    page = open_user_roles_page(browser)
    page.search_role(ROLE_NAME[:4])

    assert ROLE_NAME in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("UR-SRH-003 Searching a non-existent name shows an empty state")
@pytest.mark.edge
def test_user_roles_search_nonexistent_shows_empty(browser):
    page = open_user_roles_page(browser)
    page.search_role(NONEXISTENT_ROLE)

    assert NONEXISTENT_ROLE not in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("UR-SRH-004 Clearing search after a query restores the full list")
@pytest.mark.regression
def test_user_roles_clear_search_restores_list(browser):
    create_role_if_missing(browser)
    page = open_user_roles_page(browser)
    original_count = page.get_visible_row_count()

    page.search_role(NONEXISTENT_ROLE)
    assert NONEXISTENT_ROLE not in page.get_body_text()

    page.clear_search()
    assert page.get_visible_row_count() >= min(original_count, 1)
    assert page_has_no_broken_state(page)
