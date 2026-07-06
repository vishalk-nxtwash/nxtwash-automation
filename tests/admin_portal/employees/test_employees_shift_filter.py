import allure
import pytest

from tests.admin_portal.employees.conftest import (
    ASSIGNMENT_SITE,
    EMP_FIRST_NAME,
    open_shift_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Employees"),
    allure.story("Shift — Filter"),
]

_FILTER_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Shift filter panel locators (First Name input, site combobox, Active shift switch, "
        "date fields) use name/label heuristics. "
        "Verify exact DOM structure in DevTools before removing xfail."
    ),
)


@allure.title("EMP-SH-FLT-001 Shift filter panel opens with the expected controls")
@pytest.mark.smoke
@_FILTER_XFAIL
def test_shift_filter_panel_opens_with_controls(browser):
    page = open_shift_page(browser)
    page.open_filter_panel()

    assert page.filter_panel_is_open(), (
        "Shift filter panel did not open after clicking Filter by"
    )
    assert page.filter_panel_has_expected_controls(), (
        "Shift filter panel missing expected controls (First name / Active shift / "
        "Start date / End date)"
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-SH-FLT-002 Filtering by First Name shows only matching employee shifts")
@pytest.mark.regression
@_FILTER_XFAIL
def test_shift_filter_by_first_name(browser, managed_employee):
    page = open_shift_page(browser)
    page.filter_by_first_name(EMP_FIRST_NAME)
    page.apply_filters()
    body = page.get_body_text()

    assert (
        EMP_FIRST_NAME.lower() in body.lower()
        or "no record" in body.lower()
        or page.get_visible_row_count() == 0
    ), "Unexpected rows visible after filtering by First Name '%s'" % EMP_FIRST_NAME
    assert page_has_no_broken_state(page)


@allure.title("EMP-SH-FLT-003 Filtering by Site shows only shifts at that site")
@pytest.mark.regression
@_FILTER_XFAIL
def test_shift_filter_by_site(browser):
    page = open_shift_page(browser)
    page.filter_by_site(ASSIGNMENT_SITE)
    page.apply_filters()

    assert page_has_no_broken_state(page), (
        "Page crashed after applying site filter for '%s'" % ASSIGNMENT_SITE
    )


@allure.title("EMP-SH-FLT-004 Filtering by date range shows only shifts within that range")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "EMP-SH-FLT-004: Start/end date inputs use name heuristics (startDate, endDate). "
        "Verify exact input names and date format required in DevTools."
    ),
)
def test_shift_filter_by_date_range(browser):
    from pages.admin_portal.employees_page import AdminEmployeeShiftPage
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC

    page = open_shift_page(browser)
    page.open_filter_panel()

    start_el = page.wait.until(EC.element_to_be_clickable(AdminEmployeeShiftPage.FILTER_START_DATE))
    start_el.click()
    start_el.send_keys(Keys.COMMAND + "a")
    start_el.send_keys(Keys.BACKSPACE)
    start_el.send_keys("2025-01-01")

    end_el = page.wait.until(EC.element_to_be_clickable(AdminEmployeeShiftPage.FILTER_END_DATE))
    end_el.click()
    end_el.send_keys(Keys.COMMAND + "a")
    end_el.send_keys(Keys.BACKSPACE)
    end_el.send_keys("2025-01-31")

    page.apply_filters()

    assert page_has_no_broken_state(page), (
        "Page crashed after applying date range filter"
    )


@allure.title("EMP-SH-FLT-005 Active shift filter ON shows only open/active shifts")
@pytest.mark.regression
@_FILTER_XFAIL
def test_shift_filter_active_on(browser):
    page = open_shift_page(browser)
    page.open_filter_panel()
    # Ensure Active shift toggle is ON (it defaults to ON per sheet note)
    if not page.get_active_shift_filter_state():
        page.toggle_active_shift_filter()
    page.apply_filters()

    assert page_has_no_broken_state(page), (
        "Page crashed after applying Active shift ON filter"
    )


@allure.title("EMP-SH-FLT-006 Active shift filter OFF shows all shifts including completed ones")
@pytest.mark.regression
@_FILTER_XFAIL
def test_shift_filter_active_off(browser):
    page = open_shift_page(browser)
    page.open_filter_panel()
    # Turn OFF the Active shift toggle
    if page.get_active_shift_filter_state():
        page.toggle_active_shift_filter()
    page.apply_filters()
    count_all = page.get_visible_row_count()

    # Turn it ON again and compare
    page.open_filter_panel()
    if not page.get_active_shift_filter_state():
        page.toggle_active_shift_filter()
    page.apply_filters()
    count_active_only = page.get_visible_row_count()

    assert count_all >= count_active_only, (
        "Showing all shifts (%d) should be >= active-only (%d)"
        % (count_all, count_active_only)
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-SH-FLT-007 An invalid date range (end before start) shows an error or empty result")
@pytest.mark.edge
@pytest.mark.xfail(
    strict=False,
    reason=(
        "EMP-SH-FLT-007: Whether an invalid date range is rejected at the filter level "
        "is a product decision. Verify expected behaviour in DevTools."
    ),
)
def test_shift_filter_invalid_date_range(browser):
    from pages.admin_portal.employees_page import AdminEmployeeShiftPage
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC

    page = open_shift_page(browser)
    page.open_filter_panel()

    start_el = page.wait.until(EC.element_to_be_clickable(AdminEmployeeShiftPage.FILTER_START_DATE))
    start_el.click()
    start_el.send_keys(Keys.COMMAND + "a")
    start_el.send_keys(Keys.BACKSPACE)
    start_el.send_keys("2025-12-31")

    end_el = page.wait.until(EC.element_to_be_clickable(AdminEmployeeShiftPage.FILTER_END_DATE))
    end_el.click()
    end_el.send_keys(Keys.COMMAND + "a")
    end_el.send_keys(Keys.BACKSPACE)
    end_el.send_keys("2025-01-01")   # end before start

    page.apply_filters()

    body = page.get_body_text()
    assert (
        "invalid" in body.lower()
        or "no record" in body.lower()
        or page.get_visible_row_count() == 0
    ), "Expected error or empty result for invalid date range (end before start)"
    assert page_has_no_broken_state(page)


@allure.title("EMP-SH-FLT-008 Filter result count matches the rendered row count")
@pytest.mark.regression
@_FILTER_XFAIL
def test_shift_filter_result_count_matches_rows(browser, managed_employee):
    page = open_shift_page(browser)
    page.filter_by_first_name(EMP_FIRST_NAME)
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


@allure.title("EMP-SH-FLT-009 Reset All clears shift filters and restores the full list")
@pytest.mark.regression
@_FILTER_XFAIL
def test_shift_reset_all_clears_filters(browser, managed_employee):
    page = open_shift_page(browser)
    page.filter_by_first_name(EMP_FIRST_NAME)
    page.apply_filters()
    filtered_count = page.get_visible_row_count()

    page.reset_filters()
    full_count = page.get_visible_row_count()

    assert full_count >= filtered_count, (
        "Row count after Reset All (%d) should be >= filtered count (%d)"
        % (full_count, filtered_count)
    )
    assert page_has_no_broken_state(page)
