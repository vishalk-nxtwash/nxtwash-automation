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
    page.clear_active_filters()
    return page


def open_create_employee_form(browser):
    open_admin_path(browser, "/users/employees/new")
    form = AdminEmployeeFormPage(browser)
    form.wait_for_create_loaded()
    return form


def open_edit_employee_form(browser, last_name=EMP_LAST_NAME):
    page = open_employees_page(browser)
    if last_name == EMP_LAST_NAME:
        # The lastName column search bar is non-functional in the current UI
        # (no server-side filter fires on typing/Enter/blur), so name-based
        # open_edit_employee reliably times out on staging with 929+ employees.
        # Use the employee-code filter (always ≤1 row) instead.
        found_row = _find_employee_by_code(page, EMP_CODE, timeout=30)
        if found_row is not None:
            _open_edit_from_row(page, found_row)
            form = AdminEmployeeFormPage(browser)
            form.wait_for_edit_loaded()
            return form
    page.open_edit_employee(last_name)
    form = AdminEmployeeFormPage(browser)
    form.wait_for_edit_loaded()
    return form


def open_shift_page(browser):
    from selenium.common.exceptions import TimeoutException as _TE
    open_admin_path(browser, "/users/employeeShift")
    page = AdminEmployeeShiftPage(browser)
    try:
        page.wait_for_loaded()
    except _TE:
        # Shift iframe can fail to render under resource pressure; reload once.
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
# Upsert helpers
# ---------------------------------------------------------------------------


def _find_employee_by_code(page, emp_code, timeout=30):
    """Filter by employee code (unique field) and return the first grid row.

    Name-based searches are unreliable on the staging grid: when many employees
    share the same last-name prefix, InovuaReactDataGrid's virtual scroller
    omits the target row from the DOM, causing 60-second timeouts even when the
    record exists.  The code filter returns ≤ 1 row, guaranteeing the row is
    always rendered regardless of grid size.

    Searches active employees first (the default view after Reset All), then
    retries with the inactive view in case a previous test deactivated the
    managed employee without restoring it.
    """
    from selenium.webdriver.support import expected_conditions as _EC
    from selenium.webdriver.support.ui import WebDriverWait as _WDW

    def _apply_and_get(include_inactive):
        """Apply code filter; include_inactive=True adds the Inactive status filter."""
        try:
            page.clear_active_filters()
            # Under staging load (929+ employees, parallel workers) the Reset-All
            # API call takes longer than _wait_for_grid_idle's 10-second timeout.
            # If the load mask is still visible when we click the filter button,
            # it intercepts the click and the panel never opens.
            try:
                _WDW(page.driver, 30).until(
                    lambda d: not any(
                        m.is_displayed()
                        for m in d.find_elements(*AdminEmployeesPage.GRID_LOAD_MASK)
                    )
                )
            except Exception:
                pass
            page.open_filter_panel()
            el = _WDW(page.driver, 20).until(
                _EC.element_to_be_clickable(AdminEmployeesPage.FILTER_EMPLOYEE_CODE_INPUT)
            )
            el.click()
            el.clear()
            el.send_keys(emp_code)
            if include_inactive:
                # Toggle the active-employee switch so inactive records are visible.
                page.filter_by_status("Inactive")
            page.apply_filters()
            _WDW(page.driver, timeout).until(
                lambda d: len(d.find_elements(*AdminEmployeesPage.GRID_ROWS)) > 0
            )
            rows = page.driver.find_elements(*AdminEmployeesPage.GRID_ROWS)
            return rows[0] if rows else None
        except Exception:
            return None

    # Pass 1: active-employees view (default after Reset All).
    row = _apply_and_get(include_inactive=False)
    if row is not None:
        return row
    # Pass 2: inactive-employees view — the managed employee may have been
    # deactivated by a test that failed before it could restore it.
    return _apply_and_get(include_inactive=True)


def _open_edit_from_row(page, row):
    """Click the Edit link inside a visible grid row."""
    from selenium.webdriver.common.by import By as _By
    edit_link = row.find_element(_By.XPATH,
        ".//a[@role='button' and .//span[normalize-space()='Edit']]")
    page.driver.execute_script("arguments[0].click();", edit_link)


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

    # Use employee code (unique field) as the primary existence check.
    # Name-based searches hit a virtual-scroll truncation bug: when many
    # employees share the same last-name prefix the target row may not be
    # rendered, causing 60-second false-negatives. The code filter always
    # returns ≤ 1 row so the row is guaranteed to be in the DOM.
    found_row = _find_employee_by_code(page, EMP_CODE, timeout=30)

    if found_row is not None:
        # Employee exists. Open edit to read the current last name.
        # If it is already canonical, just cancel (avoids an unnecessary
        # save round-trip and the >15-second API wait that triggers a
        # spurious warning). If it was renamed by an edit test, restore it.
        try:
            _open_edit_from_row(page, found_row)
            restore_form = AdminEmployeeFormPage(browser)
            restore_form.wait_for_edit_loaded()
            current_last = restore_form.driver.find_element(
                *AdminEmployeeFormPage.LAST_NAME_INPUT
            ).get_attribute("value")
            last_ok = current_last.lower().strip() == last_name.lower()
            active_ok = restore_form.active_switch_is_on()
            if last_ok and active_ok:
                restore_form.click_cancel()
            else:
                if not last_ok:
                    restore_form.enter_last_name(last_name)
                restore_form.ensure_active_switch_on()
                restore_form.click_save()
        except Exception:
            pass
        return open_employees_page(browser)

    # Employee not found by code → CREATE.
    form = open_create_employee_form(browser)
    # Optional dropdowns first — each triggers a React re-render; if they come
    # after text inputs, the re-render can wipe RHF's internal state for text
    # fields (confirmed by staging behaviour). Setting them first means the
    # re-renders fire before any text field is written.
    try:
        form.select_state(EMP_STATE)
        form.select_city(EMP_CITY)
    except Exception:
        pass
    try:
        from selenium.webdriver.support import expected_conditions as EC
        el = form.wait.until(
            EC.presence_of_element_located(AdminEmployeeFormPage.HIRE_DATE_INPUT)
        )
        form._set_input_value(el, EMP_HIRE_DATE)
    except Exception:
        pass
    # Required text fields after optional dropdowns — proven order from
    # test_create_employee_multiple_locations: text first, then locations,
    # then switch; assign_locations and ensure_active_switch_on both trigger
    # re-renders that preserve text values when text was set before them.
    form.enter_first_name(first_name)
    form.enter_last_name(last_name)
    form.enter_email(email)
    form.enter_phone(phone)
    form.enter_employee_code(EMP_CODE)
    try:
        form.enter_address(EMP_ADDRESS)
    except Exception:
        pass
    try:
        form.enter_zip(EMP_ZIP)
    except Exception:
        pass
    form.assign_locations(locations)
    form.ensure_active_switch_on()
    url_before = browser.current_url
    form.click_save()
    # Detect silent failure: URL unchanged means duplicate email — the employee
    # exists but the code filter returned nothing (race or index lag).
    duplicate = browser.current_url == url_before
    if duplicate:
        import logging
        logging.getLogger("nxtwash").warning(
            "Employee create did not navigate away — duplicate email; "
            "retrying lookup by employee code"
        )
        page = open_employees_page(browser)
        found_row2 = _find_employee_by_code(page, EMP_CODE, timeout=30)
        if found_row2 is not None:
            try:
                _open_edit_from_row(page, found_row2)
                restore_form2 = AdminEmployeeFormPage(browser)
                restore_form2.wait_for_edit_loaded()
                current_last2 = restore_form2.driver.find_element(
                    *AdminEmployeeFormPage.LAST_NAME_INPUT
                ).get_attribute("value")
                last2_ok = current_last2.lower().strip() == last_name.lower()
                active2_ok = restore_form2.active_switch_is_on()
                if last2_ok and active2_ok:
                    restore_form2.click_cancel()
                else:
                    if not last2_ok:
                        restore_form2.enter_last_name(last_name)
                    restore_form2.ensure_active_switch_on()
                    restore_form2.click_save()
            except Exception:
                pass
        return open_employees_page(browser)

    # Genuine CREATE — wait for the grid to reflect the new record.
    page = open_employees_page(browser)
    try:
        page.reset_filters()
    except Exception:
        pass
    page.search_employee(last_name)
    page.wait_for_employee_row(last_name, timeout=120)
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
