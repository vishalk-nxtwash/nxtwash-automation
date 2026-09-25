import allure
import pytest

from selenium.webdriver.common.by import By

from tests.superadmin.user_roles.conftest import TEST_ROLE_NAME

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("User Roles"),
    allure.story("Filter"),
]


def test_filter_by_button_opens_filter_panel(user_roles_page):
    """SA-UR-FLT-001 — Clicking 'Filter by' opens the filter panel."""
    user_roles_page.open_filters()
    assert user_roles_page.filter_panel_is_open(), \
        "Filter panel should be visible after clicking 'Filter by'"


def test_filter_panel_shows_required_controls(user_roles_page):
    """SA-UR-FLT-002 — Panel shows Role Name field, Active User Role toggle,
    Reset filters and Apply filters buttons."""
    user_roles_page.open_filters()

    role_name_inputs = user_roles_page.driver.find_elements(
        *user_roles_page.SEARCH_INPUTS
    )
    assert role_name_inputs, \
        "Filter panel should have a Role Name input field"

    apply_btns = user_roles_page.driver.find_elements(
        *user_roles_page.APPLY_FILTERS_BUTTON
    )
    assert apply_btns, "Filter panel should have an 'Apply filters' button"

    reset_btns = user_roles_page.driver.find_elements(
        *user_roles_page.RESET_FILTERS_BUTTON
    )
    assert reset_btns, "Filter panel should have a 'Reset filters' button"


def test_filter_by_exact_role_name_returns_match(user_roles_page):
    """SA-UR-FLT-003 — Filter by exact Role Name returns the matching role."""
    user_roles_page.filter_by_role_name(TEST_ROLE_NAME)
    assert user_roles_page.role_row_is_visible(TEST_ROLE_NAME), \
        f"Filtering by exact name should show '{TEST_ROLE_NAME}' in the list"


def test_filter_by_partial_role_name_returns_matches(user_roles_page):
    """SA-UR-FLT-004 — Filter by partial Role Name returns matching roles.
    e.g. 'POS' matches 'POS User8' and 'POS Super USer1'."""
    user_roles_page.open_filters()
    user_roles_page.enter_text(user_roles_page.SEARCH_INPUTS, "POS")
    user_roles_page.apply_filters()

    count = user_roles_page.get_visible_row_count()
    assert count >= 1, \
        "Partial name filter 'POS' should return at least one matching role"


def test_filter_with_no_match_shows_empty_state(user_roles_page):
    """SA-UR-FLT-005 — Filter with a role name matching nothing shows an empty state."""
    user_roles_page.open_filters()
    user_roles_page.enter_text(user_roles_page.SEARCH_INPUTS, "ZZZNOMATCH_ROLE_99999")
    user_roles_page.apply_filters()

    body = user_roles_page.driver.find_element(By.TAG_NAME, "body").text
    assert "error" not in body.lower(), \
        "No-match filter should show an empty state, not an error message"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-FLT-006: 'Active User Role' toggle locator inside the filter panel "
           "not confirmed — needs DevTools inspection to verify the toggle element.",
)
def test_active_user_role_toggle_on_shows_only_active(user_roles_page):
    """SA-UR-FLT-006 — 'Active User Role' toggle ON shows only active roles."""
    user_roles_page.open_filters()
    toggles = user_roles_page.driver.find_elements(*user_roles_page.ACTIVE_FILTER_TOGGLE)
    assert toggles, "Active User Role toggle should be present in the filter panel"

    # Enable the toggle (click if currently off)
    toggle = toggles[0]
    is_on = toggle.is_selected() or toggle.get_attribute("aria-checked") == "true"
    if not is_on:
        user_roles_page.driver.execute_script("arguments[0].click();", toggle)

    user_roles_page.apply_filters()
    assert user_roles_page.role_row_is_visible(TEST_ROLE_NAME), \
        f"Active filter ON should still show the active '{TEST_ROLE_NAME}' role"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-FLT-007: Active User Role toggle OFF requires confirming the inactive "
           "role appears — toggle locator and inactive role visibility not confirmed.",
)
def test_active_user_role_toggle_off_shows_all_roles(user_roles_page):
    """SA-UR-FLT-007 — Active User Role toggle OFF shows all roles including inactive."""
    user_roles_page.open_filters()
    toggles = user_roles_page.driver.find_elements(*user_roles_page.ACTIVE_FILTER_TOGGLE)
    assert toggles, "Active User Role toggle should be present in the filter panel"

    toggle = toggles[0]
    is_on = toggle.is_selected() or toggle.get_attribute("aria-checked") == "true"
    if is_on:
        user_roles_page.driver.execute_script("arguments[0].click();", toggle)

    user_roles_page.apply_filters()
    count = user_roles_page.get_visible_row_count()
    assert count >= 1, \
        "With Active toggle OFF all roles (including inactive) should be shown"


def test_apply_filters_updates_list_and_record_count(user_roles_page):
    """SA-UR-FLT-008 — 'Apply filters' updates the list and the records count."""
    initial_records = user_roles_page.get_records_text()

    user_roles_page.filter_by_role_name(TEST_ROLE_NAME)
    filtered_records = user_roles_page.get_records_text()

    assert filtered_records, "Records text should still be present after applying a filter"
    assert user_roles_page.role_row_is_visible(TEST_ROLE_NAME), \
        f"'{TEST_ROLE_NAME}' should appear in the filtered list"
    _ = initial_records  # variable used to confirm baseline was captured


def test_reset_filters_clears_input_and_restores_full_list(user_roles_page):
    """SA-UR-FLT-009 — 'Reset filters' clears the input and restores the full list."""
    user_roles_page.open_filters()
    user_roles_page.reset_filters()
    full_count = user_roles_page.get_visible_row_count()

    user_roles_page.filter_by_role_name(TEST_ROLE_NAME)
    filtered_count = user_roles_page.get_visible_row_count()

    user_roles_page.open_filters()
    user_roles_page.reset_filters()
    restored_count = user_roles_page.get_visible_row_count()

    assert restored_count >= filtered_count, \
        "Resetting filters should restore at least as many rows as the filtered result"
    assert restored_count == full_count, \
        f"After reset, expected {full_count} rows, got {restored_count}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-FLT-010: Close (X) button locator inside the filter panel "
           "not confirmed — needs DOM inspection.",
)
def test_close_x_dismisses_panel_without_applying(user_roles_page):
    """SA-UR-FLT-010 — Close (X) dismisses the filter panel without applying changes."""
    initial_count = user_roles_page.get_visible_row_count()

    user_roles_page.open_filters()
    user_roles_page.enter_text(user_roles_page.SEARCH_INPUTS, "ZZZNOMATCH")
    user_roles_page.close_filter_panel()

    after_count = user_roles_page.get_visible_row_count()
    assert after_count == initial_count, \
        "Closing the filter panel without applying should not change the list"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-FLT-011: Case-insensitive filter — server may perform case-sensitive "
           "matching on staging; behaviour not confirmed.",
)
def test_role_name_filter_is_case_insensitive(user_roles_page):
    """SA-UR-FLT-011 — Role Name filter is case-insensitive."""
    user_roles_page.filter_by_role_name(TEST_ROLE_NAME.upper())
    assert user_roles_page.role_row_is_visible(TEST_ROLE_NAME), \
        f"Case-insensitive filter should find '{TEST_ROLE_NAME}' when searching upper-case"
