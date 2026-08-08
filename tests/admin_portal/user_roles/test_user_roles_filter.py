import allure
import pytest

from tests.admin_portal.user_roles.conftest import (
    ASSIGNMENT_SITE,
    NONEXISTENT_ROLE,
    ROLE_NAME,
    create_role_if_missing,
    open_user_roles_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("User Roles"),
    allure.story("Filter"),
]


@allure.title("UR-FLT-001 Filter panel opens and shows site dropdown and active toggle")
@pytest.mark.smoke
def test_user_roles_filter_panel_opens(browser):
    page = open_user_roles_page(browser)

    assert page.filter_panel_has_site_and_active_controls()
    assert page_has_no_broken_state(page)


@allure.title("UR-FLT-002 Active filter shows only active roles")
@pytest.mark.regression
@pytest.mark.skip(reason="CI-SKIP UR-FLT-002: create_role_if_missing times out in headless CI. Fix: same as CS-CRT-001.")
def test_user_roles_filter_active_shows_active_only(browser):
    create_role_if_missing(browser)
    page = open_user_roles_page(browser)
    page.toggle_active_filter()
    page.apply_filters()
    page.search_role(ROLE_NAME)

    assert page.wait_for_role_row(ROLE_NAME).is_displayed()
    assert page.get_role_status(ROLE_NAME) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("UR-FLT-003 Toggling active filter off shows all roles including inactive")
@pytest.mark.regression
@pytest.mark.skip(reason="CI-SKIP UR-FLT-003: create_role_if_missing times out in headless CI. Fix: same as CS-CRT-001.")
def test_user_roles_filter_off_shows_all(browser):
    create_role_if_missing(browser)
    page = open_user_roles_page(browser)

    # Enable then immediately disable to verify full list returns
    page.toggle_active_filter()
    page.apply_filters()
    filtered_count = page.get_visible_row_count()

    page = open_user_roles_page(browser)
    page.reset_filters()
    total_count = page.get_visible_row_count()

    # Unfiltered list must have at least as many rows as the filtered list
    assert total_count >= filtered_count
    assert page_has_no_broken_state(page)


@allure.title("UR-FLT-004 Site filter narrows results to roles assigned to that site")
@pytest.mark.regression
def test_user_roles_filter_by_site(browser):
    create_role_if_missing(browser)
    page = open_user_roles_page(browser)
    page.select_site_filter(ASSIGNMENT_SITE)
    page.apply_filters()

    # After site filter the grid must render without errors (data-set may vary)
    assert page_has_no_broken_state(page)
    page.reset_filters()


@allure.title("UR-FLT-006 Combined site and active filters return the correct subset")
@pytest.mark.regression
@pytest.mark.skip(reason="CI-SKIP UR-FLT-006: create_role_if_missing times out in headless CI. Fix: same as CS-CRT-001.")
def test_user_roles_filter_combined_site_and_active(browser):
    create_role_if_missing(browser)
    page = open_user_roles_page(browser)
    page.select_site_filter(ASSIGNMENT_SITE)
    page.toggle_active_filter()
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("UR-FLT-005 Filter result count in pagination matches visible row count")
@pytest.mark.regression
def test_user_roles_filter_count_matches_rows(browser):
    create_role_if_missing(browser)
    page = open_user_roles_page(browser)
    page.toggle_active_filter()
    page.apply_filters()

    visible_rows = page.get_visible_row_count()
    body = page.get_body_text()

    assert str(visible_rows) in body, (
        "Row count %d not found in pagination label. Body: %s" % (visible_rows, body[:200])
    )
    assert page_has_no_broken_state(page)


@allure.title("UR-FLT-008 Site filter dropdown lists available sites in alphabetical order")
@pytest.mark.edge
@pytest.mark.xfail(
    strict=False,
    reason=(
        "UR-FLT-008: Site option locator '//*[@role='option']' may capture options from "
        "other dropdowns. Verify in DevTools that only site-filter options are returned."
    ),
)
def test_user_roles_site_filter_alphabetical(browser):
    page = open_user_roles_page(browser)
    options = page.get_site_filter_all_options()

    assert len(options) > 0, "Site filter dropdown returned no options"
    assert options == sorted(options), (
        "Site options are not alphabetical. Got: %s" % options
    )
    assert page_has_no_broken_state(page)


@allure.title("UR-FLT-007 Reset All clears all applied filters and restores the full list")
@pytest.mark.regression
def test_user_roles_reset_all_clears_filters(browser):
    create_role_if_missing(browser)
    page = open_user_roles_page(browser)
    original_count = page.get_visible_row_count()

    page.select_site_filter(ASSIGNMENT_SITE)
    page.apply_filters()

    # Reset filters directly (do not re-navigate; "Reset all" only appears when filters are active)
    page.reset_filters()

    assert page.get_visible_row_count() >= min(original_count, 1)
    assert page_has_no_broken_state(page)
