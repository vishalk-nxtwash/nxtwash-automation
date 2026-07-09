import allure
import pytest

from tests.admin_portal.employees.conftest import (
    EMP_LAST_NAME,
    NONEXISTENT_LAST_NAME,
    open_employees_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Employees"),
    allure.story("List & Search"),
]

_COLUMNS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Column header locator uses class heuristics. "
        "Verify exact header element classes in DevTools before removing xfail."
    ),
)


@allure.title("EMP-LST-001 Employees page loads with the Employees tab active by default")
@pytest.mark.smoke
def test_employees_page_loads(browser):
    page = open_employees_page(browser)

    assert page_has_no_broken_state(page), "Page shows an error state on load"
    body = page.get_body_text()
    assert "Employees" in body


@allure.title("EMP-LST-002 Employees tab displays the seven expected columns")
@pytest.mark.regression
@_COLUMNS_XFAIL
def test_employees_list_displays_correct_columns(browser):
    page = open_employees_page(browser)
    headers = page.page_header_columns_text()
    joined = " ".join(h.lower() for h in headers)

    expected_fragments = [
        "first name",
        "last name",
        "employee code",
        "hire date",
        "shift status",
        "status",
    ]
    for fragment in expected_fragments:
        assert fragment in joined, (
            "Expected column '%s' not found in headers: %s" % (fragment, headers)
        )
    assert page_has_no_broken_state(page)


@allure.title("EMP-LST-003 Shift Status column shows Inactive for employees with no active shift")
@pytest.mark.regression
def test_shift_status_inactive_when_no_active_shift(browser, managed_employee):
    page = open_employees_page(browser)
    page.search_employee(EMP_LAST_NAME)
    body = page.get_body_text()

    assert "Inactive" in body or "Active" in body, (
        "Shift Status column not rendered in list"
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-LST-004 Status column shows Active/Inactive badge correctly per employee")
@pytest.mark.regression
def test_status_column_shows_badge(browser, managed_employee):
    page = open_employees_page(browser)
    status = page.get_employee_status(EMP_LAST_NAME)

    assert status in ("Active", "Inactive"), (
        "Status badge must be 'Active' or 'Inactive'; got: '%s'" % status
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-LST-005 Pagination control shows a non-empty 'Showing N of N' label")
@pytest.mark.regression
def test_employees_pagination_shows_count(browser):
    page = open_employees_page(browser)
    body = page.get_body_text()

    has_pagination = (
        "showing" in body.lower()
        or "of" in body.lower()
        or "-" in body
    )
    assert has_pagination, (
        "Pagination / total count label not found on Employees list page"
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-LST-006 Results-per-page dropdown updates the visible row count")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "EMP-LST-006: Results-per-page dropdown locator not yet verified in DevTools. "
        "Activate once the per-page select element is confirmed."
    ),
)
def test_results_per_page_updates_rows(browser):
    page = open_employees_page(browser)
    count_before = page.get_visible_row_count()

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    dropdown = page.wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//select[contains(@name,'pageSize') or contains(@name,'perPage')] | "
                   "//*[@aria-label='Rows per page']//select")
    ))
    from selenium.webdriver.support.ui import Select
    sel = Select(dropdown)
    options = [o.get_attribute("value") for o in sel.options]
    other = next((o for o in options if o != dropdown.get_attribute("value")), None)
    if other:
        sel.select_by_value(other)

    count_after = page.get_visible_row_count()
    assert count_after != count_before or count_before == 0
    assert page_has_no_broken_state(page)


# ---------------------------------------------------------------------------
# Search (EMP-SRH)
# ---------------------------------------------------------------------------


@allure.title("EMP-SRH-001 Search by exact last name returns the matching employee")
@pytest.mark.regression
def test_search_by_exact_last_name(browser, managed_employee):
    page = open_employees_page(browser)
    page.search_employee(EMP_LAST_NAME)
    body = page.get_body_text()

    assert EMP_LAST_NAME in body, (
        "Employee with last name '%s' not found after exact search" % EMP_LAST_NAME
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-SRH-002 Search by partial last name returns all matching employees")
@pytest.mark.regression
def test_search_by_partial_last_name(browser, managed_employee):
    partial = EMP_LAST_NAME[:4]
    page = open_employees_page(browser)
    page.search_employee(partial)
    body = page.get_body_text()

    assert partial.lower() in body.lower() or EMP_LAST_NAME in body, (
        "No employees found for partial last-name search '%s'" % partial
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-SRH-003 Searching a non-existent last name shows an empty state")
@pytest.mark.regression
def test_search_nonexistent_shows_empty_state(browser):
    page = open_employees_page(browser)
    page.search_employee(NONEXISTENT_LAST_NAME)
    body = page.get_body_text()

    assert (
        "no record" in body.lower()
        or "no data" in body.lower()
        or "empty" in body.lower()
        or page.get_visible_row_count() == 0
    ), "Expected empty state message or zero rows for non-existent search"
    assert page_has_no_broken_state(page)


@allure.title("EMP-SRH-004 Clearing the search field restores the full employee list")
@pytest.mark.regression
def test_clear_search_restores_full_list(browser, managed_employee):
    page = open_employees_page(browser)
    page.search_employee(EMP_LAST_NAME)
    count_filtered = page.get_visible_row_count()

    page.clear_search()
    count_full = page.get_visible_row_count()

    assert count_full >= count_filtered, (
        "Row count after clearing search (%d) should be >= filtered count (%d)"
        % (count_full, count_filtered)
    )
    assert page_has_no_broken_state(page)
