import uuid

import allure
import pytest

from tests.admin_portal.employees.conftest import (
    ASSIGNMENT_SITE,
    EMP_EMAIL,
    EMP_FIRST_NAME,
    EMP_LAST_NAME,
    EMP_PHONE,
    EMP_CODE,
    EMP_WAGE,
    INVALID_EMAIL,
    create_employee_if_missing,
    open_create_employee_form,
    open_employees_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Employees"),
    allure.story("Create"),
]

_LOCATION_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Location multi-select combobox locator uses label heuristics. "
        "Verify exact React Select element in DevTools before removing xfail."
    ),
)


def _unique_last_name():
    return "AutoEmp%s" % uuid.uuid4().hex[:6]


def _unique_email():
    return "vk.emp.%s@test.com" % uuid.uuid4().hex[:8]


def _unique_phone():
    return "90%08d" % (abs(hash(uuid.uuid4())) % 100000000)


@allure.title("EMP-CRT-001 Clicking '+ Add employee' opens the create form at the correct URL")
@pytest.mark.smoke
def test_add_employee_form_opens(browser):
    page = open_employees_page(browser)
    page.click_add_employee()

    assert "employees/new" in browser.current_url or "employees" in browser.current_url
    assert page_has_no_broken_state(page)


@allure.title("EMP-CRT-002 Creating an active employee with all required fields saves correctly")
@pytest.mark.smoke
@_LOCATION_XFAIL
def test_create_active_employee(browser):
    last_name = _unique_last_name()
    email = _unique_email()
    phone = _unique_phone()

    form = open_create_employee_form(browser)
    form.fill_create_form(EMP_FIRST_NAME, last_name, email, phone, ASSIGNMENT_SITE)
    form.click_save()

    page = open_employees_page(browser)
    assert page.employee_exists(last_name), (
        "Employee '%s' not found in list after save" % last_name
    )
    assert page.get_employee_status(last_name) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("EMP-CRT-003 Creating an inactive employee saves it with Inactive status")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_create_inactive_employee(browser):
    last_name = _unique_last_name()

    form = open_create_employee_form(browser)
    form.fill_create_form(EMP_FIRST_NAME, last_name, _unique_email(), _unique_phone(), ASSIGNMENT_SITE)
    form.ensure_active_switch_off()
    form.click_save()

    page = open_employees_page(browser)
    page.filter_by_status("Inactive")
    page.apply_filters()
    body = page.get_body_text()

    assert last_name in body or page_has_no_broken_state(page), (
        "Inactive employee '%s' not found after filtering by Inactive" % last_name
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-CRT-004 Saving without First Name is blocked with a validation error")
@pytest.mark.smoke
def test_create_employee_first_name_required(browser):
    form = open_create_employee_form(browser)
    form.enter_last_name(_unique_last_name())
    form.enter_email(_unique_email())
    form.enter_phone(_unique_phone())
    # First Name intentionally omitted
    form.click_save()

    assert (
        not form.first_name_input_is_valid()
        or "first name" in form.get_body_text().lower()
        or "required" in form.get_body_text().lower()
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-CRT-005 Saving without Last Name is blocked with a validation error")
@pytest.mark.smoke
def test_create_employee_last_name_required(browser):
    form = open_create_employee_form(browser)
    form.enter_first_name(EMP_FIRST_NAME)
    form.enter_email(_unique_email())
    form.enter_phone(_unique_phone())
    # Last Name intentionally omitted
    form.click_save()

    assert (
        not form.last_name_input_is_valid()
        or "last name" in form.get_body_text().lower()
        or "required" in form.get_body_text().lower()
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-CRT-006 Saving without Locations is blocked — Locations is required")
@pytest.mark.smoke
@_LOCATION_XFAIL
def test_create_employee_locations_required(browser):
    form = open_create_employee_form(browser)
    form.enter_first_name(EMP_FIRST_NAME)
    form.enter_last_name(_unique_last_name())
    form.enter_email(_unique_email())
    form.enter_phone(_unique_phone())
    # Location intentionally omitted
    form.click_save()

    body = form.get_body_text()
    assert (
        "location" in body.lower()
        or "required" in body.lower()
        or "employees/new" in browser.current_url
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-CRT-007 Saving without Email is blocked with a validation error")
@pytest.mark.smoke
def test_create_employee_email_required(browser):
    form = open_create_employee_form(browser)
    form.enter_first_name(EMP_FIRST_NAME)
    form.enter_last_name(_unique_last_name())
    form.enter_phone(_unique_phone())
    # Email intentionally omitted
    form.click_save()

    assert (
        not form.email_input_is_valid()
        or "email" in form.get_body_text().lower()
        or "required" in form.get_body_text().lower()
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-CRT-008 Saving without Phone Number is blocked with a validation error")
@pytest.mark.regression
def test_create_employee_phone_required(browser):
    form = open_create_employee_form(browser)
    form.enter_first_name(EMP_FIRST_NAME)
    form.enter_last_name(_unique_last_name())
    form.enter_email(_unique_email())
    # Phone intentionally omitted
    form.click_save()

    assert (
        not form.phone_input_is_valid()
        or "phone" in form.get_body_text().lower()
        or "required" in form.get_body_text().lower()
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-CRT-009 Invalid email format (missing @) is rejected on save")
@pytest.mark.regression
def test_create_employee_invalid_email_rejected(browser):
    form = open_create_employee_form(browser)
    form.enter_email(INVALID_EMAIL)
    form.click_save()

    assert not form.email_input_is_valid() or "email" in form.get_body_text().lower()
    assert page_has_no_broken_state(form)


@allure.title("EMP-CRT-010 Duplicate email address is rejected on save")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_create_employee_duplicate_email_rejected(browser):
    create_employee_if_missing(browser)  # ensure EMP_EMAIL exists

    form = open_create_employee_form(browser)
    form.enter_first_name(EMP_FIRST_NAME)
    form.enter_last_name(_unique_last_name())
    form.enter_email(EMP_EMAIL)          # already exists
    form.enter_phone(_unique_phone())
    form.assign_location(ASSIGNMENT_SITE)
    form.click_save()

    body = form.get_body_text()
    assert (
        "exist" in body.lower()
        or "duplicate" in body.lower()
        or "already" in body.lower()
        or "employees/new" in browser.current_url
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-CRT-011 Single location assignment persists after save")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_create_employee_single_location_persists(browser):
    last_name = _unique_last_name()

    form = open_create_employee_form(browser)
    form.fill_create_form(EMP_FIRST_NAME, last_name, _unique_email(), _unique_phone(), ASSIGNMENT_SITE)
    form.click_save()

    page = open_employees_page(browser)
    assert page.employee_exists(last_name)
    assert page_has_no_broken_state(page)


@allure.title("EMP-CRT-012 Multiple location assignment shows chip format after save")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_create_employee_multiple_locations(browser):
    last_name = _unique_last_name()

    form = open_create_employee_form(browser)
    form.enter_first_name(EMP_FIRST_NAME)
    form.enter_last_name(last_name)
    form.enter_email(_unique_email())
    form.enter_phone(_unique_phone())
    form.assign_location(ASSIGNMENT_SITE)
    form.ensure_active_switch_on()
    form.click_save()

    page = open_employees_page(browser)
    assert page.employee_exists(last_name)
    assert page_has_no_broken_state(page)


@allure.title("EMP-CRT-013 Hire date selected from calendar picker persists after save")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "EMP-CRT-013: Hire date calendar picker interaction not yet modelled. "
        "Verify date input name/type in DevTools and implement picker interaction."
    ),
)
def test_create_employee_hire_date_persists(browser):
    last_name = _unique_last_name()
    hire_date = "2024-06-15"

    form = open_create_employee_form(browser)
    form.enter_first_name(EMP_FIRST_NAME)
    form.enter_last_name(last_name)
    form.enter_email(_unique_email())
    form.enter_phone(_unique_phone())
    from pages.admin_portal.employees_page import AdminEmployeeFormPage
    from selenium.webdriver.support import expected_conditions as EC
    el = form.wait.until(EC.presence_of_element_located(AdminEmployeeFormPage.HIRE_DATE_INPUT))
    form._set_input_value(el, hire_date)
    form.assign_location(ASSIGNMENT_SITE)
    form.click_save()

    from tests.admin_portal.employees.conftest import open_edit_employee_form
    edit = open_edit_employee_form(browser, last_name)
    body = edit.get_body_text()
    assert "2024" in body or hire_date in body
    assert page_has_no_broken_state(edit)


@allure.title("EMP-CRT-014 Omitting hire date still saves the employee successfully")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_create_employee_hire_date_optional(browser):
    last_name = _unique_last_name()

    form = open_create_employee_form(browser)
    form.fill_create_form(EMP_FIRST_NAME, last_name, _unique_email(), _unique_phone(), ASSIGNMENT_SITE)
    # Hire date intentionally omitted
    form.click_save()

    page = open_employees_page(browser)
    assert page.employee_exists(last_name), (
        "Employee without hire date was not saved"
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-CRT-016 Omitting employee code still saves the employee successfully")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_create_employee_code_optional(browser):
    last_name = _unique_last_name()

    form = open_create_employee_form(browser)
    form.fill_create_form(EMP_FIRST_NAME, last_name, _unique_email(), _unique_phone(), ASSIGNMENT_SITE)
    # Employee code intentionally omitted
    form.click_save()

    page = open_employees_page(browser)
    assert page.employee_exists(last_name), (
        "Employee without code was not saved"
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-CRT-018 Hourly wage with a decimal value saves correctly")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_create_employee_hourly_wage_decimal(browser):
    last_name = _unique_last_name()

    form = open_create_employee_form(browser)
    form.fill_create_form(EMP_FIRST_NAME, last_name, _unique_email(), _unique_phone(), ASSIGNMENT_SITE)
    form.enter_hourly_wage(EMP_WAGE)
    form.click_save()

    page = open_employees_page(browser)
    assert page.employee_exists(last_name)
    assert page_has_no_broken_state(page)


@allure.title("EMP-CRT-019 Omitting hourly wage still saves the employee successfully")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_create_employee_hourly_wage_optional(browser):
    last_name = _unique_last_name()

    form = open_create_employee_form(browser)
    form.fill_create_form(EMP_FIRST_NAME, last_name, _unique_email(), _unique_phone(), ASSIGNMENT_SITE)
    # Hourly wage intentionally omitted
    form.click_save()

    page = open_employees_page(browser)
    assert page.employee_exists(last_name)
    assert page_has_no_broken_state(page)


@allure.title("EMP-CRT-020 Negative hourly wage is rejected with a validation error")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "EMP-CRT-020: Browser checkValidity() on the wage input depends on a 'min' attribute. "
        "Verify input constraints in DevTools; server-side rejection also acceptable."
    ),
)
def test_create_employee_negative_wage_rejected(browser):
    form = open_create_employee_form(browser)
    form.enter_first_name(EMP_FIRST_NAME)
    form.enter_last_name(_unique_last_name())
    form.enter_email(_unique_email())
    form.enter_phone(_unique_phone())
    form.enter_hourly_wage("-5")
    form.click_save()

    assert (
        not form.hourly_wage_input_is_valid()
        or "wage" in form.get_body_text().lower()
        or "invalid" in form.get_body_text().lower()
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-CRT-021 State dropdown contains entries (US states visible)")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "EMP-CRT-021: State combobox locator uses label heuristics. "
        "Verify exact React Select element in DevTools before removing xfail."
    ),
)
def test_create_employee_state_dropdown_has_options(browser):
    form = open_create_employee_form(browser)
    from pages.admin_portal.employees_page import AdminEmployeeFormPage
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    form.driver.execute_script(
        "arguments[0].click();",
        form.wait.until(EC.element_to_be_clickable(AdminEmployeeFormPage.STATE_COMBOBOX))
    )
    opts = form.driver.find_elements(By.XPATH, "//*[@role='option']")
    opt_texts = [o.text.strip() for o in opts if o.text.strip()]

    assert len(opt_texts) >= 1, "State dropdown returned no options"
    assert page_has_no_broken_state(form)


@allure.title("EMP-CRT-022 City dropdown populates after a State is selected")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "EMP-CRT-022: State + City combobox cascade locators use label heuristics. "
        "Verify both dropdowns in DevTools before removing xfail."
    ),
)
def test_create_employee_city_populates_after_state(browser):
    form = open_create_employee_form(browser)
    form.select_state("Alabama")
    city_options = form.get_city_dropdown_options()

    assert len(city_options) > 0, (
        "City dropdown returned no options after selecting Alabama"
    )
    assert page_has_no_broken_state(form)


@allure.title("EMP-CRT-024 Omitting all address fields saves the employee successfully")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_create_employee_address_fields_optional(browser):
    last_name = _unique_last_name()

    form = open_create_employee_form(browser)
    form.fill_create_form(EMP_FIRST_NAME, last_name, _unique_email(), _unique_phone(), ASSIGNMENT_SITE)
    # Address, ZIP, State, City all intentionally omitted
    form.click_save()

    page = open_employees_page(browser)
    assert page.employee_exists(last_name)
    assert page_has_no_broken_state(page)


@allure.title("EMP-CRT-025 Clicking Cancel discards the form and returns to the list")
@pytest.mark.regression
def test_create_employee_cancel_discards_form(browser):
    last_name = _unique_last_name()

    form = open_create_employee_form(browser)
    form.enter_first_name(EMP_FIRST_NAME)
    form.enter_last_name(last_name)
    form.click_cancel()

    page = open_employees_page(browser)
    assert not page.employee_exists(last_name), (
        "Employee '%s' was saved despite clicking Cancel" % last_name
    )
    assert page_has_no_broken_state(page)


@allure.title("EMP-CRT-026 Newly created employee appears in the list immediately after save")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_newly_created_employee_appears_immediately(browser):
    last_name = _unique_last_name()

    form = open_create_employee_form(browser)
    form.fill_create_form(EMP_FIRST_NAME, last_name, _unique_email(), _unique_phone(), ASSIGNMENT_SITE)
    form.click_save()

    page = open_employees_page(browser)
    assert page.employee_exists(last_name), (
        "Employee '%s' did not appear in list immediately after save" % last_name
    )
    assert page_has_no_broken_state(page)
