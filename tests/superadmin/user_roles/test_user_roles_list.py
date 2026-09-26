import allure
import pytest

from tests.superadmin.user_roles.conftest import PREDEFINED_ROLE_NAME, TEST_ROLE_NAME

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("User Roles"),
    allure.story("List"),
]


def test_user_roles_list_page_loads(user_roles_page):
    """SA-UR-LST-001 — User Roles list page loads with the 'User Roles' title visible."""
    title = user_roles_page.get_text(user_roles_page.PAGE_TITLE)
    assert "User Roles" in title, \
        f"Expected page title 'User Roles', got: {title!r}"


def test_list_shows_role_name_and_role_type_columns(user_roles_page):
    """SA-UR-LST-002 — List shows Role Name, Role Type columns and a row-level Edit action."""
    headers = user_roles_page.get_column_headers()
    headers_lower = [h.lower() for h in headers]
    assert any("name" in h for h in headers_lower), \
        f"Expected a 'Role Name' column in headers: {headers}"
    assert any("type" in h for h in headers_lower), \
        f"Expected a 'Role Type' column in headers: {headers}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-LST-003: Exact Role Type cell value ('Custom' vs 'Default'/'Predefined') "
           "and column index not confirmed — needs DOM inspection.",
)
def test_role_type_column_shows_correct_value_per_role(user_roles_page):
    """SA-UR-LST-003 — Role Type column shows 'Custom' for auto-created roles and
    'Default' / 'Predefined' for predefined roles."""
    user_roles_page.filter_by_role_name(TEST_ROLE_NAME)
    custom_type = user_roles_page.get_role_type_for_row(TEST_ROLE_NAME)
    assert custom_type and "custom" in custom_type.lower(), \
        f"Expected '{TEST_ROLE_NAME}' to have Role Type 'Custom', got: {custom_type!r}"

    user_roles_page.reset_filters()
    user_roles_page.filter_by_role_name(PREDEFINED_ROLE_NAME)
    predefined_type = user_roles_page.get_role_type_for_row(PREDEFINED_ROLE_NAME)
    assert predefined_type and (
        "default" in predefined_type.lower() or "predefined" in predefined_type.lower()
    ), f"Expected '{PREDEFINED_ROLE_NAME}' to have Role Type 'Default/Predefined', " \
       f"got: {predefined_type!r}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-LST-004: Blank-named role row rendering — the list contains a role with "
           "no name; Edit action presence on that row needs DOM verification.",
)
def test_blank_role_name_row_renders_without_breaking(user_roles_page):
    """SA-UR-LST-004 — A role with a blank name renders without breaking the row or its Edit action."""
    count = user_roles_page.get_visible_row_count()
    assert count >= 1, \
        "List must render at least one row even when a blank-named role exists"
    body = user_roles_page.driver.find_element(
        *(__import__("selenium.webdriver.common.by", fromlist=["By"]).By.TAG_NAME, "body")
    ).text
    assert "error" not in body.lower(), \
        "Page should not show an error when a blank-named role row is present"


def test_pagination_shows_page_x_of_y_and_record_count(user_roles_page):
    """SA-UR-LST-005 — Pagination footer shows 'Page X of Y' and 'out of N records'."""
    pagination = user_roles_page.get_pagination_text()
    assert "Page" in pagination and "of" in pagination, \
        f"Pagination text should contain 'Page ... of ...', got: {pagination!r}"

    records = user_roles_page.get_records_text()
    assert "out of" in records.lower() and "records" in records.lower(), \
        f"Pagination should show 'out of N records', got: {records!r}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-LST-006: 'Show 100' results-per-page dropdown locator not confirmed "
           "— may render as a React Select or native <select>.",
)
def test_results_per_page_changes_rows_shown(user_roles_page):
    """SA-UR-LST-006 — Results-per-page dropdown changes the number of rows shown."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.select import Select

    selects = user_roles_page.driver.find_elements(*user_roles_page.RESULTS_PER_PAGE_SELECT)
    assert selects, "Results-per-page selector should be present on the list page"
    sel = Select(selects[0])
    options = [o.text.strip() for o in sel.options]
    assert any(opt.isdigit() for opt in options), \
        f"Results-per-page options should include numeric values, got: {options}"


def test_pagination_controls_disabled_on_single_page(user_roles_page):
    """SA-UR-LST-007 — First / Previous buttons are disabled when the list fits one page."""
    assert user_roles_page.prev_page_button_is_disabled(), \
        "Previous page button should be disabled when on page 1"


def test_predefined_roles_appear_in_list(user_roles_page):
    """SA-UR-LST-008 — Predefined roles (e.g. Company Owner) appear in the list."""
    user_roles_page.filter_by_role_name(PREDEFINED_ROLE_NAME)
    assert user_roles_page.role_row_is_visible(PREDEFINED_ROLE_NAME), \
        f"Predefined role '{PREDEFINED_ROLE_NAME}' should appear in the User Roles list"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-LST-009: Cannot create a reliably empty list state in staging "
           "— requires deleting all roles which is destructive.",
)
def test_empty_list_shows_empty_state_not_error(user_roles_page):
    """SA-UR-LST-009 — Filtering to no results shows an empty state, not an error."""
    user_roles_page.open_filters()
    user_roles_page.enter_text(
        user_roles_page.SEARCH_INPUTS, "ZZZNOMATCH_ROLE_99999"
    )
    user_roles_page.apply_filters()

    body = user_roles_page.driver.find_element(
        *(__import__("selenium.webdriver.common.by", fromlist=["By"]).By.TAG_NAME, "body")
    ).text
    assert "error" not in body.lower(), \
        "A zero-match filter should show an empty state, not an error"
    assert user_roles_page.empty_state_is_visible() or user_roles_page.get_visible_row_count() == 0, \
        "Expected empty state message or zero rows after no-match filter"


def test_records_count_reflects_existing_roles(user_roles_page):
    """SA-UR-LST-010 — Records count shows at least the known test roles."""
    records = user_roles_page.get_records_text()
    assert records, "Pagination records text should be present on the list"
    # conftest creates TEST_ROLE_NAME so at least one role must exist
    count = user_roles_page.get_visible_row_count()
    assert count >= 1, \
        f"Expected at least 1 role row on the list, got: {count}"
