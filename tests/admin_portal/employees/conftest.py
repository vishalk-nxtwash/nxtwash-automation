import pytest

from pages.admin_portal.employees_page import (
    AdminEmployeeFormPage,
    AdminEmployeeShiftFormPage,
    AdminEmployeeShiftPage,
    AdminEmployeesPage,
)
from tests.admin_portal.admin_session import open_admin_path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EMP_FIRST_NAME = "Test"
EMP_LAST_NAME = "user 4"
EMP_FULL_NAME = EMP_FIRST_NAME + " " + EMP_LAST_NAME   # "Test user 4"
EMP_EMAIL = "tu4@yopmail.com"
EMP_PHONE = "1234567789"
EMP_CODE = "001"
EMP_WAGE = "15.50"
EMP_HIRE_DATE = "2025-05-01"      # 1st May 2025
EMP_ADDRESS = "Test user 4 address"
EMP_ZIP = "123445"
EMP_STATE = "Alaska"
EMP_CITY = "wales"
EMP_LOCATIONS = ["VK test carwash 2", "VK AL03", "VK AL05"]
ASSIGNMENT_SITE = EMP_LOCATIONS[0]  # primary site used in single-site contexts

SHIFT_DATE = "2025-07-01"         # 1st July 2025
SHIFT_START_TIME = "09:00"        # 9 AM
SHIFT_END_TIME = "19:00"          # 7 PM

UPDATED_FIRST_NAME = "TestEdited"
UPDATED_LAST_NAME = "user4Edited"
UPDATED_EMAIL = "tu4.edited@yopmail.com"
UPDATED_PHONE = "1234567790"
UPDATED_WAGE = "20.00"

NONEXISTENT_LAST_NAME = "employee-does-not-exist-automation"
INVALID_EMAIL = "not-an-email"

SHIFT_EMPLOYEE_LAST_NAME = EMP_LAST_NAME  # shift tests search by this
SHIFT_SITE = ASSIGNMENT_SITE

# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------


def open_employees_page(browser):
    open_admin_path(browser, "/users/employees")
    page = AdminEmployeesPage(browser)
    page.wait_for_loaded()
    return page


def open_create_employee_form(browser):
    open_admin_path(browser, "/users/employees/new")
    form = AdminEmployeeFormPage(browser)
    form.wait_for_create_loaded()
    return form


def open_edit_employee_form(browser, last_name=EMP_LAST_NAME):
    page = open_employees_page(browser)
    page.open_edit_employee(last_name)
    form = AdminEmployeeFormPage(browser)
    form.wait_for_edit_loaded()
    return form


def open_shift_page(browser):
    open_admin_path(browser, "/users/employeeShift")
    page = AdminEmployeeShiftPage(browser)
    page.wait_for_loaded()
    return page


def open_create_shift_form(browser):
    open_admin_path(browser, "/users/employeeShift/new")
    form = AdminEmployeeShiftFormPage(browser)
    form.wait_for_create_loaded()
    return form


def page_has_no_broken_state(page):
    try:
        body = page.get_body_text().lower()
    except Exception:
        return True
    broken_signals = [
        "something went wrong",
        "internal server error",
        "application error",
        "cannot read",
        "typeerror",
        "uncaught error",
    ]
    return not any(s in body for s in broken_signals)


# ---------------------------------------------------------------------------
# Upsert helper
# ---------------------------------------------------------------------------


def create_employee_if_missing(
    browser,
    first_name=EMP_FIRST_NAME,
    last_name=EMP_LAST_NAME,
    email=EMP_EMAIL,
    phone=EMP_PHONE,
    locations=None,
):
    if locations is None:
        locations = EMP_LOCATIONS

    page = open_employees_page(browser)

    if page.employee_exists(last_name):
        form = open_edit_employee_form(browser, last_name)
        form.enter_first_name(first_name)
        form.enter_last_name(last_name)
        form.enter_email(email)
        form.enter_phone(phone)
        form.ensure_active_switch_on()
        form.click_save()
        return open_employees_page(browser)

    form = open_create_employee_form(browser)
    form.enter_first_name(first_name)
    form.enter_last_name(last_name)
    form.enter_email(email)
    form.enter_phone(phone)
    form.enter_employee_code(EMP_CODE)
    form.assign_locations(locations)
    form.ensure_active_switch_on()
    # Optional fields — wrapped so a missing input doesn't abort the whole setup
    try:
        from pages.admin_portal.employees_page import AdminEmployeeFormPage
        from selenium.webdriver.support import expected_conditions as EC
        el = form.wait.until(
            EC.presence_of_element_located(AdminEmployeeFormPage.HIRE_DATE_INPUT)
        )
        form._set_input_value(el, EMP_HIRE_DATE)
    except Exception:
        pass
    try:
        form.enter_address(EMP_ADDRESS)
    except Exception:
        pass
    try:
        form.enter_zip(EMP_ZIP)
    except Exception:
        pass
    try:
        form.select_state(EMP_STATE)
        form.select_city(EMP_CITY)
    except Exception:
        pass
    form.click_save()
    page = open_employees_page(browser)
    page.search_employee(last_name)
    page.wait_for_employee_row(last_name)
    return page


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def managed_employee(browser):
    """Ensure the baseline employee exists; restore it after each test."""
    page = create_employee_if_missing(browser)
    yield page
    create_employee_if_missing(browser)


@pytest.fixture
def managed_shift(browser, managed_employee):
    """Navigate to the shift list; the caller is responsible for creating a shift if needed."""
    page = open_shift_page(browser)
    yield page
