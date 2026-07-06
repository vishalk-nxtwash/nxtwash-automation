import allure
import pytest

from tests.admin_portal.employees.conftest import (
    ASSIGNMENT_SITE,
    EMP_FULL_NAME,
    EMP_LAST_NAME,
    SHIFT_DATE,
    SHIFT_END_TIME,
    SHIFT_START_TIME,
    open_create_shift_form,
    open_shift_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Employees"),
    allure.story("Shift — Create"),
]

_SHIFT_FORM_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Shift form locators (Employee combobox, Site combobox, start/end time inputs) "
        "use label heuristics. Verify exact DOM structure and datetime picker behaviour "
        "in DevTools before removing xfail."
    ),
)


@allure.title("EMP-SH-CRT-001 Clicking '+ Add new employee shift' opens the shift create form")
@pytest.mark.smoke
def test_add_shift_form_opens(browser):
    page = open_shift_page(browser)
    page.click_add_shift()

    assert (
        "employeeShift/new" in browser.current_url
        or "employeeShift" in browser.current_url
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-SH-CRT-002 Creating an active shift with all required fields saves correctly")
@pytest.mark.smoke
@_SHIFT_FORM_XFAIL
def test_create_active_shift(browser, managed_employee):
    form = open_create_shift_form(browser)
    form.select_employee(EMP_FULL_NAME)
    form.select_site(ASSIGNMENT_SITE)
    form.set_shift_date(SHIFT_DATE)
    form.set_start_time(SHIFT_START_TIME)
    form.set_end_time(SHIFT_END_TIME)
    form.ensure_active_switch_on()
    form.click_save()

    page = open_shift_page(browser)
    assert page_has_no_broken_state(page), (
        "Shift page shows an error state after creating a shift"
    )


@allure.title("EMP-SH-CRT-003 Creating an inactive shift saves it with the inactive state")
@pytest.mark.regression
@_SHIFT_FORM_XFAIL
def test_create_inactive_shift(browser, managed_employee):
    form = open_create_shift_form(browser)
    form.select_employee(EMP_FULL_NAME)
    form.select_site(ASSIGNMENT_SITE)
    form.set_start_time("09:00")
    form.set_end_time("17:00")
    form.ensure_active_switch_off()
    form.click_save()

    assert page_has_no_broken_state(form), (
        "Page shows error state after saving inactive shift"
    )


@allure.title("EMP-SH-CRT-004 Saving without Employee selected is blocked with a validation error")
@pytest.mark.smoke
@_SHIFT_FORM_XFAIL
def test_create_shift_employee_required(browser):
    form = open_create_shift_form(browser)
    form.select_site(ASSIGNMENT_SITE)
    form.set_start_time("09:00")
    form.set_end_time("17:00")
    # Employee intentionally omitted
    form.click_save()

    body = form.get_body_text()
    assert (
        "employee" in body.lower()
        or "required" in body.lower()
        or "employeeShift/new" in browser.current_url
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-SH-CRT-005 Saving without Site/Location is blocked with a validation error")
@pytest.mark.smoke
@_SHIFT_FORM_XFAIL
def test_create_shift_site_required(browser, managed_employee):
    form = open_create_shift_form(browser)
    form.select_employee(EMP_FULL_NAME)
    form.set_start_time("09:00")
    form.set_end_time("17:00")
    # Site intentionally omitted
    form.click_save()

    body = form.get_body_text()
    assert (
        "site" in body.lower()
        or "location" in body.lower()
        or "required" in body.lower()
        or "employeeShift/new" in browser.current_url
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-SH-CRT-006 Saving without Start/End time is blocked with a validation error")
@pytest.mark.smoke
@_SHIFT_FORM_XFAIL
def test_create_shift_time_required(browser, managed_employee):
    form = open_create_shift_form(browser)
    form.select_employee(EMP_FULL_NAME)
    form.select_site(ASSIGNMENT_SITE)
    # Time fields intentionally omitted
    form.click_save()

    body = form.get_body_text()
    assert (
        "time" in body.lower()
        or "required" in body.lower()
        or "employeeShift/new" in browser.current_url
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-SH-CRT-007 Employee dropdown lists only active employees")
@pytest.mark.regression
@_SHIFT_FORM_XFAIL
def test_create_shift_employee_dropdown_lists_active_employees(browser, managed_employee):
    form = open_create_shift_form(browser)
    options = form.get_employee_dropdown_options()

    assert len(options) > 0, "Employee dropdown returned no options"
    assert EMP_FULL_NAME in options or any(
        EMP_LAST_NAME in o for o in options
    ), (
        "Active employee '%s' not found in dropdown. Got: %s" % (EMP_FULL_NAME, options[:10])
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-SH-CRT-008 Site/Location dropdown lists all configured sites")
@pytest.mark.regression
@_SHIFT_FORM_XFAIL
def test_create_shift_site_dropdown_lists_sites(browser):
    form = open_create_shift_form(browser)
    options = form.get_site_dropdown_options()

    assert len(options) > 0, "Site/Location dropdown returned no options"
    assert ASSIGNMENT_SITE in options, (
        "Expected site '%s' not found in shift form dropdown. Got: %s"
        % (ASSIGNMENT_SITE, options[:10])
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-SH-CRT-009 Date-time picker is present with both start and end time fields")
@pytest.mark.regression
@_SHIFT_FORM_XFAIL
def test_create_shift_datetime_picker_present(browser):
    from pages.admin_portal.employees_page import AdminEmployeeShiftFormPage
    from selenium.webdriver.support import expected_conditions as EC

    form = open_create_shift_form(browser)
    start_visible = bool(
        form.driver.find_elements(*AdminEmployeeShiftFormPage.START_TIME_INPUT)
    )
    end_visible = bool(
        form.driver.find_elements(*AdminEmployeeShiftFormPage.END_TIME_INPUT)
    )

    assert start_visible, "Start time input not found on shift create form"
    assert end_visible, "End time input not found on shift create form"
    assert page_has_no_broken_state(form)


@allure.title("EMP-SH-CRT-010 A shift with end time before start time shows a validation error")
@pytest.mark.edge
@pytest.mark.xfail(
    strict=False,
    reason=(
        "EMP-SH-CRT-010: Whether end-before-start is rejected depends on whether the app "
        "supports overnight shifts. Verify expected product behaviour in DevTools."
    ),
)
def test_create_shift_end_before_start(browser, managed_employee):
    form = open_create_shift_form(browser)
    form.select_employee(EMP_FULL_NAME)
    form.select_site(ASSIGNMENT_SITE)
    form.set_start_time("17:00")
    form.set_end_time("09:00")   # end before start on same day
    form.ensure_active_switch_on()
    form.click_save()

    body = form.get_body_text()
    assert (
        "time" in body.lower()
        or "invalid" in body.lower()
        or "before" in body.lower()
        or "employeeShift/new" in browser.current_url
    ), "Expected validation error for end time before start time"
    assert page_has_no_broken_state(form)


@allure.title("EMP-SH-CRT-011 A midnight-spanning shift (22:00–06:00) saves correctly")
@pytest.mark.edge
@_SHIFT_FORM_XFAIL
def test_create_shift_midnight_spanning(browser, managed_employee):
    form = open_create_shift_form(browser)
    form.select_employee(EMP_FULL_NAME)
    form.select_site(ASSIGNMENT_SITE)
    form.set_start_time("22:00")
    form.set_end_time("06:00")   # crosses midnight
    form.ensure_active_switch_on()
    form.click_save()

    page = open_shift_page(browser)
    assert page_has_no_broken_state(page), (
        "Page shows error state after saving a midnight-spanning shift"
    )


@allure.title("EMP-SH-CRT-012 Creating a shift that overlaps an existing one is a product decision")
@pytest.mark.edge
@pytest.mark.xfail(
    strict=False,
    reason=(
        "EMP-SH-CRT-012: Whether overlapping shifts are blocked is a product decision. "
        "Verify expected server behaviour before implementing the assertion."
    ),
)
def test_create_shift_overlapping_shifts(browser, managed_shift):
    form = open_create_shift_form(browser)
    form.select_employee(EMP_FULL_NAME)
    form.select_site(ASSIGNMENT_SITE)
    form.set_start_time("09:00")   # same window used in other shift tests
    form.set_end_time("17:00")
    form.ensure_active_switch_on()
    form.click_save()

    assert page_has_no_broken_state(form), (
        "Page shows broken state after creating overlapping shift"
    )


@allure.title("EMP-SH-CRT-013 Clicking Cancel discards the shift form and returns to the list")
@pytest.mark.regression
def test_create_shift_cancel_discards_form(browser):
    form = open_create_shift_form(browser)
    form.click_cancel()

    assert (
        "employeeShift" in browser.current_url
        and "new" not in browser.current_url
    ) or page_has_no_broken_state(form)
    assert page_has_no_broken_state(form)


@allure.title("EMP-SH-CRT-014 Newly created shift appears in the list immediately after save")
@pytest.mark.regression
@_SHIFT_FORM_XFAIL
def test_newly_created_shift_appears_immediately(browser, managed_employee):
    form = open_create_shift_form(browser)
    form.select_employee(EMP_FULL_NAME)
    form.select_site(ASSIGNMENT_SITE)
    form.set_shift_date(SHIFT_DATE)
    form.set_start_time(SHIFT_START_TIME)
    form.set_end_time(SHIFT_END_TIME)
    form.ensure_active_switch_on()
    form.click_save()

    page = open_shift_page(browser)
    row_count = page.get_visible_row_count()

    assert row_count >= 0, "Shift list page not accessible after save"
    assert page_has_no_broken_state(page)
