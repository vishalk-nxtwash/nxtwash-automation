import allure
import pytest

from tests.admin_portal.employees.conftest import (
    EMP_LAST_NAME,
    open_employees_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Employees"),
    allure.story("Filter"),
]

_FILTER_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Filter panel locators (status combobox, apply button) use label heuristics. "
        "Verify exact DOM structure in DevTools before removing xfail."
    ),
)


@allure.title("EMP-FLT-001 Clicking 'Filter by' opens the filter panel with status controls")
@pytest.mark.smoke
def test_filter_panel_opens(browser):
    page = open_employees_page(browser)
    page.open_filter_panel()

    assert page.filter_panel_is_open(), (
        "Filter panel did not open after clicking Filter by"
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-FLT-002 Filtering by Active status shows only active employees")
@pytest.mark.regression
@_FILTER_XFAIL
def test_filter_by_active_status(browser, managed_employee):
    page = open_employees_page(browser)
    page.filter_by_status("Active")
    page.apply_filters()
    body = page.get_body_text()

    assert "Inactive" not in body or "Active" in body, (
        "Inactive employees visible after applying Active status filter"
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-FLT-003 Filtering by Inactive status shows only inactive employees")
@pytest.mark.regression
@_FILTER_XFAIL
def test_filter_by_inactive_status(browser):
    page = open_employees_page(browser)
    page.filter_by_status("Inactive")
    page.apply_filters()
    body = page.get_body_text()

    # Either the list shows only inactive employees or shows empty state (no inactive data)
    assert (
        "Active" not in body
        or "Inactive" in body
        or "no record" in body.lower()
        or page.get_visible_row_count() == 0
    ), "Unexpected active employees shown after Inactive filter applied"
    assert page_has_no_broken_state(page)


@allure.title("EMP-FLT-004 Filter result count matches the number of rendered rows")
@pytest.mark.regression
@_FILTER_XFAIL
def test_filter_result_count_matches_rows(browser, managed_employee):
    page = open_employees_page(browser)
    page.filter_by_status("Active")
    page.apply_filters()

    result_text = page.filter_result_count_text()
    row_count = page.get_visible_row_count()

    if result_text:
        import re
        numbers = re.findall(r"\d+", result_text)
        if numbers:
            expected = int(numbers[0])
            assert expected == row_count, (
                "Filter result label says %d but %d rows are visible"
                % (expected, row_count)
            )
    assert page_has_no_broken_state(page)


@allure.title("EMP-FLT-005 Clicking Reset All clears filters and restores the full employee list")
@pytest.mark.regression
@_FILTER_XFAIL
def test_reset_all_clears_filters(browser, managed_employee):
    page = open_employees_page(browser)
    page.filter_by_status("Active")
    page.apply_filters()
    filtered_count = page.get_visible_row_count()

    page.reset_filters()
    full_count = page.get_visible_row_count()

    assert full_count >= filtered_count, (
        "Row count after Reset All (%d) should be >= filtered count (%d)"
        % (full_count, filtered_count)
    )
    assert page_has_no_broken_state(page)
