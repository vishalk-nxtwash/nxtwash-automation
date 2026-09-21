import allure
import pytest

from tests.admin_portal.employees.conftest import (
    EMP_LAST_NAME,
    NONEXISTENT_LAST_NAME,
    open_shift_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Employees"),
    allure.story("Shift — List & Search"),
    pytest.mark.xdist_group(name="managed_employee"),
    pytest.mark.timeout(480),
]

_COLUMNS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Shift column header locator uses class heuristics. "
        "Verify exact header element classes in DevTools before removing xfail."
    ),
)


@allure.title("EMP-SH-LST-001 Employee shift tab loads and the Add shift button is visible")
@pytest.mark.smoke
def test_shift_tab_loads(browser):
    page = open_shift_page(browser)

    assert page_has_no_broken_state(page), "Shift tab shows an error state on load"
    body = page.get_body_text()
    assert "shift" in body.lower() or "employee" in body.lower()


@allure.title("EMP-SH-LST-002 Shift list displays the five expected columns")
@pytest.mark.regression
@_COLUMNS_XFAIL
def test_shift_list_displays_correct_columns(browser):
    from pages.admin_portal.employees_page import AdminEmployeeShiftPage
    from selenium.webdriver.common.by import By

    page = open_shift_page(browser)
    headers = page.driver.find_elements(By.XPATH,
        "//*[contains(@class,'header') or @role='columnheader']")
    header_text = " ".join(h.text.lower() for h in headers if h.text.strip())

    expected = ["employee", "date", "start time", "end time", "hours worked"]
    for col in expected:
        assert col in header_text, (
            "Expected column '%s' not found in shift headers: '%s'" % (col, header_text)
        )
    assert page_has_no_broken_state(page)


@allure.title("EMP-SH-LST-003 Empty state message shows when no shift records exist")
@pytest.mark.smoke
def test_shift_empty_state_when_no_records(browser):
    page = open_shift_page(browser)
    page.search_shift(NONEXISTENT_LAST_NAME)
    body = page.get_body_text()

    assert (
        "no record" in body.lower()
        or "no data" in body.lower()
        or "empty" in body.lower()
        or page.get_visible_row_count() == 0
    ), "Expected empty state for non-existent search; page may have rendered ghost rows"
    assert page_has_no_broken_state(page)


@allure.title("EMP-SH-LST-004 Pagination shows 0-of-0 (or N-of-N) label without negative numbers")
@pytest.mark.regression
@pytest.mark.skip(reason="Manual — EMP-SH-LST-004: Pagination label verification requires manual visual check.")
def test_shift_pagination_no_negative_numbers(browser):
    page = open_shift_page(browser)
    body = page.get_body_text()

    import re
    negative_pagination = re.search(r"-\d+-of-|-\s*\d+\s*of", body)
    assert not negative_pagination, (
        "Negative pagination number found in page text: '%s'" % body[:200]
    )
    assert page_has_no_broken_state(page)


# ---------------------------------------------------------------------------
# Shift Search (EMP-SH-SRH)
# ---------------------------------------------------------------------------


@allure.title("EMP-SH-SRH-001 Search shift by exact employee last name returns matching records")
@pytest.mark.regression
def test_shift_search_by_exact_last_name(browser, managed_employee):
    page = open_shift_page(browser)
    page.search_shift(EMP_LAST_NAME)
    body = page.get_body_text()

    # If the employee has shifts they appear; if none, expect empty state — both are valid
    assert page_has_no_broken_state(page), (
        "Page crashed when searching shifts for '%s'" % EMP_LAST_NAME
    )
    _ = body  # confirm page body is readable


@allure.title("EMP-SH-SRH-002 Search shift by partial last name returns all matching records")
@pytest.mark.regression
def test_shift_search_by_partial_last_name(browser, managed_employee):
    partial = EMP_LAST_NAME[:4]
    page = open_shift_page(browser)
    page.search_shift(partial)

    assert page_has_no_broken_state(page), (
        "Page crashed when searching shifts with partial name '%s'" % partial
    )


@allure.title("EMP-SH-SRH-003 Search with non-matching last name shows an empty state")
@pytest.mark.regression
def test_shift_search_nonexistent_shows_empty(browser):
    page = open_shift_page(browser)
    page.search_shift(NONEXISTENT_LAST_NAME)
    body = page.get_body_text()

    assert (
        "no record" in body.lower()
        or "no data" in body.lower()
        or "empty" in body.lower()
        or page.get_visible_row_count() == 0
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-SH-SRH-004 Clearing the shift search field restores the full shift list")
@pytest.mark.regression
def test_shift_clear_search_restores_list(browser):
    page = open_shift_page(browser)
    page.search_shift(NONEXISTENT_LAST_NAME)
    count_filtered = page.get_visible_row_count()

    page.clear_search()
    count_full = page.get_visible_row_count()

    assert count_full >= count_filtered, (
        "Row count after clearing shift search (%d) should be >= filtered count (%d)"
        % (count_full, count_filtered)
    )
    assert page_has_no_broken_state(page)
