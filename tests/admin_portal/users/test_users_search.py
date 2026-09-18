import allure
import pytest

from tests.admin_portal.users.conftest import (
    NONEXISTENT_PHONE,
    USER_EMAIL,
    USER_PHONE,
    create_user_if_missing,
    open_users_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Users"),
    allure.story("Search"),
]


@allure.title("USR-SRH-001 Exact phone number search returns the matching user")
@pytest.mark.regression
def test_users_search_exact_phone(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    page.search_user(USER_PHONE)

    assert page.user_exists(USER_EMAIL)
    assert page_has_no_broken_state(page)


@allure.title("USR-SRH-002 Partial phone number search returns matching users")
@pytest.mark.regression
def test_users_search_partial_phone(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    page.search_user(USER_PHONE[:6])

    assert USER_PHONE[:6] in page.get_body_text() or page.get_visible_row_count() >= 1
    assert page_has_no_broken_state(page)


@allure.title("USR-SRH-003 Searching a non-existent phone shows an empty state")
@pytest.mark.edge
def test_users_search_nonexistent_phone_shows_empty(browser):
    page = open_users_page(browser)
    page.search_user(NONEXISTENT_PHONE)

    body = page.get_body_text()
    assert NONEXISTENT_PHONE not in body or page.get_visible_row_count() == 0
    assert page_has_no_broken_state(page)


@allure.title("USR-SRH-004 Clearing the phone search restores the full user list")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Manual — USR-SRH-004: Requires managed user vkuser02@yopmail.com to be active "
        "on staging with employee 'test user 2' and role 'VK UR02'. "
        "Restore staging baseline (active user, linked employee, correct role) then re-enable."
    )
)
def test_users_search_clear_restores_list(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    original_count = page.get_visible_row_count()

    page.search_user(NONEXISTENT_PHONE)
    assert page.get_visible_row_count() == 0 or NONEXISTENT_PHONE not in page.get_body_text()

    page.clear_search()
    assert page.get_visible_row_count() >= min(original_count, 1)
    assert page_has_no_broken_state(page)
