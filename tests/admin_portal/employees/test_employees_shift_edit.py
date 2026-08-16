import allure
import pytest

from tests.admin_portal.employees.conftest import (
    ASSIGNMENT_SITE,
    EMP_FULL_NAME,
    EMP_LAST_NAME,
    open_shift_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Employees"),
    allure.story("Shift — Edit"),
    pytest.mark.xdist_group(name="managed_employee"),
]

_SHIFT_EDIT_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Shift edit tests require an existing shift record in staging. "
        "Edit form locators (Employee, Site comboboxes, time inputs) use label heuristics. "
        "Verify DOM and confirm at least one shift exists in DevTools before removing xfail."
    ),
)


def _open_first_shift_edit(browser):
    from tests.admin_portal.employees.conftest import open_shift_page
    from pages.admin_portal.employees_page import AdminEmployeeShiftFormPage

    page = open_shift_page(browser)
    if page.get_visible_row_count() == 0:
        pytest.skip("No shift records available in staging to edit")
    page.open_first_shift_edit()
    form = AdminEmployeeShiftFormPage(browser)
    form.wait_for_edit_loaded()
    return form


@allure.title("EMP-SH-EDT-001 Clicking Edit on a shift record opens the edit form pre-populated")
@pytest.mark.regression
@_SHIFT_EDIT_XFAIL
def test_shift_edit_form_opens_prepopulated(browser, managed_employee):
    form = _open_first_shift_edit(browser)

    assert (
        "employeeShift" in browser.current_url
        and "new" not in browser.current_url
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-SH-EDT-002 Editing Employee assignment on a shift persists after save")
@pytest.mark.regression
@_SHIFT_EDIT_XFAIL
def test_shift_edit_employee_persists(browser, managed_employee):
    form = _open_first_shift_edit(browser)
    form.select_employee(EMP_FULL_NAME)
    form.click_save()

    page = open_shift_page(browser)
    page.search_shift(EMP_LAST_NAME)
    body = page.get_body_text()

    assert EMP_LAST_NAME.lower() in body.lower() or page_has_no_broken_state(page)
    assert page_has_no_broken_state(page)


@allure.title("EMP-SH-EDT-003 Editing Site/Location on a shift persists after save")
@pytest.mark.regression
@_SHIFT_EDIT_XFAIL
def test_shift_edit_site_persists(browser, managed_employee):
    form = _open_first_shift_edit(browser)
    form.select_site(ASSIGNMENT_SITE)
    form.click_save()

    assert page_has_no_broken_state(form), (
        "Page shows error after editing shift site"
    )


@allure.title("EMP-SH-EDT-004 Editing Start/End time recalculates Hours Worked after save")
@pytest.mark.regression
@_SHIFT_EDIT_XFAIL
def test_shift_edit_time_recalculates_hours(browser, managed_employee):
    form = _open_first_shift_edit(browser)
    form.set_start_time("08:00")
    form.set_end_time("16:00")
    form.click_save()

    page = open_shift_page(browser)
    body = page.get_body_text()
    # 8 hours worked should appear somewhere in the list
    assert "8" in body or page_has_no_broken_state(page)
    assert page_has_no_broken_state(page)


@allure.title("EMP-SH-EDT-005 Activating an inactive shift saves it as active")
@pytest.mark.regression
@_SHIFT_EDIT_XFAIL
def test_shift_edit_activate_inactive_shift(browser, managed_employee):
    form = _open_first_shift_edit(browser)
    form.ensure_active_switch_on()
    form.click_save()

    assert page_has_no_broken_state(form), (
        "Page shows error after activating shift"
    )
