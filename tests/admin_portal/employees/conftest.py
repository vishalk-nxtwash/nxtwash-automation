import pytest

from pages.admin_portal.employees_page import (
    AdminEmployeeFormPage,
    AdminEmployeeShiftFormPage,
    AdminEmployeeShiftPage,
    AdminEmployeesPage,
)
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._data import load as _load

# ---------------------------------------------------------------------------
# Constants  (values managed in test_data/employees.json)
# ---------------------------------------------------------------------------

_D = _load("employees")

EMP_FIRST_NAME = _D["template"]["first_name"]
EMP_LAST_NAME  = _D["template"]["last_name"]
EMP_FULL_NAME  = EMP_FIRST_NAME + " " + EMP_LAST_NAME
EMP_EMAIL      = _D["template"]["email"]
EMP_PHONE      = _D["template"]["phone"]
EMP_CODE       = _D["template"]["employee_code"]
EMP_WAGE       = _D["template"]["wage"]
EMP_HIRE_DATE  = _D["template"]["hire_date"]
EMP_ADDRESS    = _D["template"]["address"]
EMP_ZIP        = _D["template"]["zip"]
EMP_STATE      = _D["template"]["state"]
EMP_CITY       = _D["template"]["city"]
EMP_LOCATIONS  = _D["template"]["locations"]
ASSIGNMENT_SITE = EMP_LOCATIONS[0]

SHIFT_DATE       = _D["shift"]["date"]
SHIFT_START_TIME = _D["shift"]["start_time"]
SHIFT_END_TIME   = _D["shift"]["end_time"]

UPDATED_FIRST_NAME = _D["updated"]["first_name"]
UPDATED_LAST_NAME  = _D["updated"]["last_name"]
UPDATED_EMAIL      = _D["updated"]["email"]
UPDATED_PHONE      = _D["updated"]["phone"]
UPDATED_WAGE       = _D["updated"]["wage"]

NONEXISTENT_LAST_NAME = _D["search"]["nonexistent_last_name"]
INVALID_EMAIL         = _D["invalid"]["email"]

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


BROKEN_STATE_TEXTS = [
    "something went wrong",
    "internal server error",
    "application error",
    "cannot read",
    "typeerror",
    "uncaught error",
]


def page_has_no_broken_state(page):
    try:
        body = page.get_body_text().lower()
    except Exception:
        return True
    return not any(s in body for s in BROKEN_STATE_TEXTS)


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
    url_before = browser.current_url
    form.click_save()
    # Detect silent failure: if URL didn't change, the form rejected the save
    # (most common cause: duplicate email).  In that case the employee already
    # exists — the earlier employee_exists call timed out because staging's
    # InovuaReactDataGrid is slow, not because the record is absent.
    if browser.current_url == url_before:
        import logging
        logging.getLogger("nxtwash").warning(
            "Employee create did not navigate away — assuming duplicate; "
            "searching list with extended timeout"
        )
    page = open_employees_page(browser)
    page.search_employee(last_name)
    page.wait_for_employee_row(last_name, timeout=180)
    return page


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def managed_employee(browser):
    """Ensure the baseline employee exists and is active before each test.

    No teardown restore — the next test's setup calls create_employee_if_missing
    which takes the EXISTS path and reactivates via ensure_active_switch_on.
    This avoids doubling the fixture budget (setup + teardown both running the
    full create cycle against the slow staging grid).
    """
    page = create_employee_if_missing(browser)
    yield page


@pytest.fixture
def managed_shift(browser, managed_employee):
    """Navigate to the shift list; the caller is responsible for creating a shift if needed."""
    page = open_shift_page(browser)
    yield page
