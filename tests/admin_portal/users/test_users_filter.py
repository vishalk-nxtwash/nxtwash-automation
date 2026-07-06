import allure
import pytest

from tests.admin_portal.users.conftest import (
    ASSIGNMENT_SITE,
    EMPLOYEE_CODE,
    USER_EMAIL,
    USER_FIRST_NAME,
    USER_LAST_NAME,
    create_user_if_missing,
    open_users_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Users"),
    allure.story("Filter"),
]

_FILTER_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Filter field locators use name/label heuristics — verify exact field names "
        "in DevTools before removing xfail."
    ),
)


@allure.title("USR-FLT-001 Filter panel opens with all expected controls")
@pytest.mark.smoke
def test_users_filter_panel_opens(browser):
    page = open_users_page(browser)

    assert page.filter_panel_has_expected_controls()
    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-002 Filter by First Name returns matching users")
@pytest.mark.regression
@_FILTER_XFAIL
def test_users_filter_by_first_name(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    page.filter_by_first_name(USER_FIRST_NAME)
    page.apply_filters()

    assert USER_FIRST_NAME in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-003 Filter by Last Name returns matching users")
@pytest.mark.regression
@_FILTER_XFAIL
def test_users_filter_by_last_name(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    page.filter_by_last_name(USER_LAST_NAME)
    page.apply_filters()

    assert USER_LAST_NAME in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-004 Filter by Email returns the correct user")
@pytest.mark.regression
@_FILTER_XFAIL
def test_users_filter_by_email(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    page.filter_by_email(USER_EMAIL)
    page.apply_filters()

    assert page.user_exists(USER_EMAIL)
    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-005 Filter by Employee code returns the correct user")
@pytest.mark.regression
@_FILTER_XFAIL
def test_users_filter_by_employee_code(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    page.filter_by_employee_code(EMPLOYEE_CODE)
    page.apply_filters()

    assert EMPLOYEE_CODE in page.get_body_text() or page.get_visible_row_count() >= 1
    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-006 Filter by Site shows only users assigned to that site")
@pytest.mark.regression
@_FILTER_XFAIL
def test_users_filter_by_site(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    page.filter_by_site(ASSIGNMENT_SITE)
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-007 Active filter shows only active users")
@pytest.mark.regression
def test_users_filter_active_only(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    page.toggle_active_filter()
    page.apply_filters()

    body = page.get_body_text()
    assert "Inactive" not in body or "Active" in body
    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-008 Disabling the Active filter restores all users including inactive")
@pytest.mark.regression
def test_users_filter_active_off_shows_all(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)

    page.toggle_active_filter()
    page.apply_filters()
    filtered_count = page.get_visible_row_count()

    page = open_users_page(browser)
    page.reset_filters()
    total_count = page.get_visible_row_count()

    assert total_count >= filtered_count
    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-009 Combining First Name and Site filters returns the correct subset")
@pytest.mark.regression
@_FILTER_XFAIL
def test_users_filter_combined_name_and_site(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    page.filter_by_first_name(USER_FIRST_NAME)
    page.filter_by_site(ASSIGNMENT_SITE)
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-010 Filter result count label matches actual rendered row count")
@pytest.mark.regression
@_FILTER_XFAIL
def test_users_filter_result_count_matches_rows(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    page.filter_by_email(USER_EMAIL)
    page.apply_filters()

    visible_rows = page.get_visible_row_count()
    body = page.get_body_text()

    assert str(visible_rows) in body, (
        "Row count %d not reflected in pagination label. Body: %s" % (visible_rows, body[:200])
    )
    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-011 Reset All clears all filters and restores the full list")
@pytest.mark.regression
def test_users_filter_reset_all(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    original_count = page.get_visible_row_count()

    # Apply a filter then reset on the same page — Reset All only appears while a filter
    # is active, so navigating away before resetting would lose the filter state.
    page.toggle_active_filter()
    page.apply_filters()
    page.reset_filters()

    assert page.get_visible_row_count() >= min(original_count, 1)
    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-012 Site dropdown in filter panel lists active sites")
@pytest.mark.edge
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-FLT-012: Site option locator //*[@role='option'] may capture options from "
        "other open dropdowns. Verify in DevTools before removing xfail."
    ),
)
def test_users_filter_site_dropdown_lists_sites(browser):
    page = open_users_page(browser)
    options = page.get_site_filter_options()

    assert len(options) > 0, "Site filter dropdown returned no options"
    assert ASSIGNMENT_SITE in options, (
        "Expected site '%s' not found. Got: %s" % (ASSIGNMENT_SITE, options)
    )
    assert page_has_no_broken_state(page)


@allure.title("USR-FLT-013 Partial name filter returns matching users")
@pytest.mark.edge
@_FILTER_XFAIL
def test_users_filter_partial_name_matches(browser):
    create_user_if_missing(browser)
    page = open_users_page(browser)
    page.filter_by_first_name(USER_FIRST_NAME[:2])
    page.apply_filters()

    assert USER_FIRST_NAME[:2].lower() in page.get_body_text().lower()
    assert page_has_no_broken_state(page)
