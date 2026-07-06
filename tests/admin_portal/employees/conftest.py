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

EMP_FIRST_NAME = "VK"
EMP_LAST_NAME = "AutoEmp01"
EMP_FULL_NAME = EMP_FIRST_NAME + " " + EMP_LAST_NAME
EMP_EMAIL = "vk.auto.emp01@test.com"
EMP_PHONE = "9001003001"
EMP_CODE = "VKE001"
EMP_WAGE = "15.50"
ASSIGNMENT_SITE = "VK AL11"

UPDATED_FIRST_NAME = "VKEdited"
UPDATED_LAST_NAME = "AutoEmp01Edited"
UPDATED_EMAIL = "vk.auto.emp01.edited@test.com"
UPDATED_PHONE = "9001003002"
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
    site=ASSIGNMENT_SITE,
):
    page = open_employees_page(browser)

    if page.employee_exists(last_name):
        form = open_edit_employee_form(browser, last_name)
        # Reset all mutable fields back to baseline
        form.enter_first_name(first_name)
        form.enter_last_name(last_name)
        form.enter_email(email)
        form.enter_phone(phone)
        form.ensure_active_switch_on()
        form.click_save()
        return open_employees_page(browser)

    form = open_create_employee_form(browser)
    form.fill_create_form(first_name, last_name, email, phone, site)
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
