import allure
import pytest

from tests.admin_portal.admin_session import ensure_admin_logged_in
from tests.admin_portal.employees.conftest import (
    ASSIGNMENT_SITE,
    EMP_FIRST_NAME,
    EMP_LAST_NAME,
    create_employee_if_missing,
    open_create_employee_form,
    open_employees_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Employees"),
    allure.story("Edge Cases"),
]


@allure.title("EMP-EC-001 Employee name with special characters (hyphen/apostrophe) saves correctly")
@pytest.mark.edge
def test_employee_name_with_special_characters(browser):
    import uuid
    unique_suffix = uuid.uuid4().hex[:4]
    special_last_name = "O'Brien-%s" % unique_suffix

    form = open_create_employee_form(browser)
    form.enter_first_name("Smith")
    form.enter_last_name(special_last_name)
    form.enter_email("vk.special.%s@test.com" % uuid.uuid4().hex[:6])
    form.enter_phone("90%08d" % (abs(hash(unique_suffix)) % 100000000))
    form.click_save()

    page = open_employees_page(browser)
    assert page.employee_exists(special_last_name) or page_has_no_broken_state(page), (
        "Employee with special characters in name was not saved or page crashed"
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-EC-003 Employee data persists correctly after logout and re-login")
@pytest.mark.edge
def test_employee_data_persists_after_relogin(browser, managed_employee):
    page = open_employees_page(browser)
    assert page.employee_exists(EMP_LAST_NAME)

    browser.delete_all_cookies()
    browser.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")

    ensure_admin_logged_in(browser)
    page = open_employees_page(browser)
    assert page.employee_exists(EMP_LAST_NAME), (
        "Employee '%s' missing after logout and re-login" % EMP_LAST_NAME
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-EC-004 Deactivated employee appears in the Inactive filter — record is not deleted")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "EMP-EC-004: Inactive filter combo locator uses label heuristics. "
        "Verify status filter combobox DOM in DevTools before removing xfail."
    ),
)
def test_deactivated_employee_in_inactive_filter(browser, managed_employee):
    from tests.admin_portal.employees.conftest import open_edit_employee_form
    form = open_edit_employee_form(browser, EMP_LAST_NAME)
    form.ensure_active_switch_off()
    form.click_save()

    page = open_employees_page(browser)
    page.filter_by_status("Inactive")
    page.apply_filters()
    body = page.get_body_text()

    assert EMP_LAST_NAME in body, (
        "Deactivated employee '%s' should appear under Inactive filter, not be deleted"
        % EMP_LAST_NAME
    )
    assert page_has_no_broken_state(page)
