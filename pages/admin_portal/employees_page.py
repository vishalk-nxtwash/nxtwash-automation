import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

from pages.common.base_page import BasePage


class AdminEmployeesPage(BasePage):
    """Employees tab list page — /users/employees"""

    EMP_LIST_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/users/employees') "
        "and not(contains(@src,'/users/employees/'))]")
    EMP_CREATE_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/users/employees/new')]")
    EMP_EDIT_FRAME = (By.XPATH,
        "//iframe["
        "contains(@src,'/users/employees') and ("
        "contains(@src,'employeeId=') or "
        "(contains(@src,'/users/employees/') and not(contains(@src,'/users/employees/new')))"
        ")]")

    PAGE_TITLE = (By.XPATH,
        "//*[normalize-space()='Employees' and (self::h1 or self::h2 or "
        "contains(@class,'title') or contains(@class,'heading'))]")
    ADD_EMPLOYEE_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Add employee')] | "
        "//*[contains(normalize-space(),'Add employee') and @role='button']")
    EMPLOYEE_SHIFT_TAB = (By.XPATH,
        "//*[@role='tab' and contains(normalize-space(),'Employee shift')] | "
        "//button[contains(normalize-space(),'Employee shift')]")

    SEARCH_INPUT = (By.XPATH,
        "//input[@placeholder='last name' or @placeholder='Last name' "
        "or @placeholder='Last Name' or @placeholder='Search by last name' "
        "or @name='lastName' or @name='last_name']")

    FILTER_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Filter by')] | "
        "//button[contains(normalize-space(),'Filter')]")
    # Filter panel controls — verified from DevTools:
    # panel has firstName input, employeeCode input, Active employee switch.
    # There is NO status combobox.
    FILTER_FIRST_NAME_INPUT = (By.XPATH, "//input[@name='firstName']")
    FILTER_EMPLOYEE_CODE_INPUT = (By.XPATH, "//input[@name='employeeCode']")
    FILTER_ACTIVE_SWITCH = (By.XPATH, "//button[@role='switch' and @value='on']")
    APPLY_FILTERS_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters'] | "
        "//button[normalize-space()='Apply']")
    RESET_ALL_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Reset all')] | "
        "//button[contains(normalize-space(),'Reset All')]")
    EXPORT_BUTTON = (By.XPATH,
        "//button[normalize-space()='Export'] | "
        "//button[contains(@aria-label,'export') or contains(@aria-label,'Export')] | "
        "//button[normalize-space()='Filter by']/following-sibling::button[1]")

    GRID_ROWS = (By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row')] | "
        "//tr[contains(@class,'row') and not(contains(@class,'header'))]")
    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and not(contains(@style,'display: none'))]")

    def wait_for_loaded(self):
        self.switch_to_frame_with_retry(self.EMP_LIST_FRAME)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        self.wait.until(EC.element_to_be_clickable(self.ADD_EMPLOYEE_BUTTON))

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def search_employee(self, last_name):
        el = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        el.send_keys(last_name)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value") == last_name
        )
        # Allow the grid time to begin filtering before checking LOAD_MASK
        time.sleep(3)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def clear_search(self):
        el = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value") == ""
        )
        time.sleep(3)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    @staticmethod
    def _xpath_string(value):
        """Build a safe XPath string literal handling names with apostrophes."""
        if "'" not in value:
            return "'%s'" % value
        parts = value.split("'")
        return "concat(%s)" % ", \"'\", ".join("'%s'" % p for p in parts)

    def _row_locator(self, last_name):
        # Use translate() for case-insensitive match — staging may title-case
        # the name (e.g. "User 2") even when stored as "user 2".
        safe = self._xpath_string(last_name.lower())
        _U = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        _L = 'abcdefghijklmnopqrstuvwxyz'
        return (By.XPATH,
            "//*[contains(@class,'InovuaReactDataGrid__row') and "
            ".//*[contains(translate(normalize-space(),'%s','%s'),%s)]]" % (_U, _L, safe))

    def wait_for_employee_row(self, last_name, timeout=None):
        # InovuaReactDataGrid rows are present in the DOM but Selenium's
        # is_displayed() returns False due to CSS transforms/clipping used by
        # the virtual scroller. Use presence_of_element_located instead.
        locator = self._row_locator(last_name)
        if timeout:
            from selenium.webdriver.support.ui import WebDriverWait
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        return self.wait.until(EC.presence_of_element_located(locator))

    def employee_exists(self, last_name, timeout=120):
        # Reset filters so inactive employees are visible — required if a previous
        # test deactivated the record and the default list shows active-only.
        try:
            self.reset_filters()
        except Exception:
            pass
        self.search_employee(last_name)
        try:
            self.wait_for_employee_row(last_name, timeout=timeout)
            return True
        except TimeoutException:
            return False

    def get_employee_status(self, last_name):
        self.search_employee(last_name)
        row = self.wait_for_employee_row(last_name)
        try:
            badge = row.find_element(By.XPATH,
                ".//*[normalize-space()='Active' or normalize-space()='Inactive']")
            return badge.text.strip()
        except Exception:
            return ""

    def get_visible_row_count(self):
        for _ in range(3):
            try:
                rows = self.driver.find_elements(*self.GRID_ROWS)
                return len([r for r in rows if r.is_displayed()])
            except StaleElementReferenceException:
                time.sleep(0.2)
        return 0

    def click_add_employee(self):
        el = self.wait.until(EC.element_to_be_clickable(self.ADD_EMPLOYEE_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def open_edit_employee(self, last_name):
        from selenium.common.exceptions import StaleElementReferenceException
        try:
            self.reset_filters()
        except Exception:
            pass
        self.search_employee(last_name)
        for _attempt in range(3):
            try:
                row = self.wait_for_employee_row(last_name, timeout=60)
                edit_link = row.find_element(By.XPATH,
                    ".//a[@role='button' and .//span[normalize-space()='Edit']]")
                self.driver.execute_script("arguments[0].click();", edit_link)
                break
            except StaleElementReferenceException:
                if _attempt == 2:
                    raise

    def click_edit_for_visible_employee(self, last_name):
        """Click Edit on a row already visible after a search — skips re-navigation."""
        from selenium.common.exceptions import StaleElementReferenceException
        for _attempt in range(3):
            try:
                row = self.wait_for_employee_row(last_name, timeout=10)
                edit_link = row.find_element(By.XPATH,
                    ".//a[@role='button' and .//span[normalize-space()='Edit']]")
                self.driver.execute_script("arguments[0].click();", edit_link)
                return
            except StaleElementReferenceException:
                if _attempt == 2:
                    raise

    def filter_panel_is_open(self):
        els = self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)
        try:
            return any(e.is_displayed() for e in els)
        except StaleElementReferenceException:
            return False

    def open_filter_panel(self):
        if self.filter_panel_is_open():
            return
        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.APPLY_FILTERS_BUTTON))

    def filter_by_status(self, status):
        """Toggle the Active employee switch: 'Active' → ON, 'Inactive' → OFF."""
        self.open_filter_panel()
        switch = self.wait.until(EC.presence_of_element_located(self.FILTER_ACTIVE_SWITCH))
        current = switch.get_attribute("aria-checked")
        if status == "Active" and current != "true":
            self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(lambda d: switch.get_attribute("aria-checked") == "true")
        elif status == "Inactive" and current != "false":
            self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(lambda d: switch.get_attribute("aria-checked") == "false")

    def apply_filters(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def reset_filters(self):
        self.open_filter_panel()
        btn = self.wait.until(EC.element_to_be_clickable(self.RESET_ALL_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        # Reset All triggers an immediate data reload (no need to click Apply).
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        # The panel stays open after Reset All; close it so subsequent clicks
        # (e.g. the search input) are not intercepted.
        try:
            WebDriverWait(self.driver, 2).until(
                EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON)
            )
        except Exception:
            filter_btn = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
            self.driver.execute_script("arguments[0].click();", filter_btn)
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON)
                )
            except Exception:
                pass

    def reset_filters_if_active(self):
        try:
            body = self.driver.find_element(By.TAG_NAME, "body").text
            if "Filter by (" in body:
                self.reset_filters()
        except Exception:
            pass

    def clear_active_filters(self):
        """Unconditionally reset all filters regardless of badge state.

        The filter badge count is lazy — it does not render at bare page load,
        so reset_filters_if_active() always skips the reset on first navigation.
        This method opens the panel and resets unconditionally, which is the
        only reliable way to flush a server-side filter state leak.
        """
        try:
            self.reset_filters()
        except Exception:
            pass

    def filter_result_count_text(self):
        try:
            el = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(),'Filter result')]")
            ))
            return el.text.strip()
        except TimeoutException:
            return ""

    def click_export_button(self):
        el = self.wait.until(EC.element_to_be_clickable(self.EXPORT_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def page_header_columns_text(self):
        try:
            headers = self.driver.find_elements(By.XPATH,
                "//*[contains(@class,'header') or @role='columnheader']")
            return [h.text.strip() for h in headers if h.text.strip()]
        except Exception:
            return []


class AdminEmployeeFormPage(BasePage):
    """Employee create/edit form — /users/employees/new or /users/employees/edit/{id}"""

    FIRST_NAME_INPUT = (By.XPATH,
        "//input[@name='firstName' or @name='first_name' or "
        "@placeholder='First name' or @placeholder='First Name']")
    LAST_NAME_INPUT = (By.XPATH,
        "//input[@name='lastName' or @name='last_name' or "
        "@placeholder='Last name' or @placeholder='Last Name']")
    EMAIL_INPUT = (By.XPATH,
        "//input[@name='email' or @name='emailId' or @name='email_id' or "
        "@placeholder='Email' or @placeholder='Email address' or "
        "@placeholder='Email Address' or @placeholder='Email id']")
    PHONE_INPUT = (By.XPATH,
        "//input[@name='phone' or @name='phoneNumber' or "
        "@name='phone_number' or @placeholder='Phone number']")
    EMPLOYEE_CODE_INPUT = (By.XPATH,
        "//input[@name='employeeCode' or @name='empCode' or "
        "@name='employee_code' or @placeholder='Employee code']")
    HOURLY_WAGE_INPUT = (By.XPATH,
        "//input[@name='hourlyWage' or @name='wage' or "
        "@name='hourly_wage' or @placeholder='Hourly wage']")
    HIRE_DATE_INPUT = (By.XPATH,
        "//input[@name='hireDate' or @name='hire_date' or "
        "@placeholder='Hire date' or (@type='date' and not(@name='startTime') "
        "and not(@name='endTime'))]")
    ADDRESS_INPUT = (By.XPATH,
        "//input[@name='address' or @name='street' or @name='streetAddress' or "
        "@placeholder='Address' or @placeholder='Street address']")
    ZIP_INPUT = (By.XPATH,
        "//input[@name='zip' or @name='zipCode' or @name='zip_code' or "
        "@name='postalCode' or @placeholder='ZIP' or @placeholder='Zip code']")

    LOCATIONS_COMBOBOX = (By.XPATH,
        "//*[normalize-space()='Locations' or normalize-space()='Location']"
        "/following::*[@role='combobox'][1]")
    STATE_COMBOBOX = (By.XPATH,
        "//*[normalize-space()='State']/following::*[@role='combobox'][1]")
    CITY_COMBOBOX = (By.XPATH,
        "//*[normalize-space()='City']/following::*[@role='combobox'][1]")

    ACTIVE_SWITCH = (By.XPATH,
        "//*[contains(normalize-space(),'Active employee')]"
        "/ancestor::*[.//button[@role='switch']][1]"
        "//button[@role='switch'] | "
        "//form//button[@role='switch'][1]")

    SAVE_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Save employee')] | "
        "//button[normalize-space()='Save'] | "
        "//*[@data-type='primary' and (contains(normalize-space(),'Save'))]")
    CANCEL_BUTTON = (By.XPATH,
        "//button[normalize-space()='Cancel'] | "
        "//*[@data-type and normalize-space()='Cancel']")

    def wait_for_create_loaded(self):
        self.switch_to_frame_with_retry(AdminEmployeesPage.EMP_CREATE_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))

    def wait_for_edit_loaded(self):
        self.switch_to_frame_with_retry(AdminEmployeesPage.EMP_EDIT_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        self.wait.until(
            lambda d: d.find_element(*self.FIRST_NAME_INPUT).get_attribute("value") != ""
        )

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def _set_input_value(self, element, value):
        self.driver.execute_script("""
            var input = arguments[0]; var value = arguments[1];
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            input.focus();
            setter.call(input, value);
            input.dispatchEvent(new Event('input', {bubbles: true}));
            input.dispatchEvent(new Event('change', {bubbles: true}));
        """, element, value)

    def enter_first_name(self, name):
        el = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_INPUT))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        el.send_keys(name)

    def enter_last_name(self, name):
        el = self.wait.until(EC.element_to_be_clickable(self.LAST_NAME_INPUT))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        el.send_keys(name)

    def clear_first_name(self):
        el = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_INPUT))
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)

    def clear_last_name(self):
        el = self.wait.until(EC.element_to_be_clickable(self.LAST_NAME_INPUT))
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)

    def get_first_name_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
        ).get_attribute("value")

    def get_last_name_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.LAST_NAME_INPUT)
        ).get_attribute("value")

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def clear_email(self):
        el = self.wait.until(EC.element_to_be_clickable(self.EMAIL_INPUT))
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)

    def get_email_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        ).get_attribute("value")

    def enter_phone(self, phone):
        self.enter_text(self.PHONE_INPUT, phone)

    def clear_phone(self):
        el = self.wait.until(EC.element_to_be_clickable(self.PHONE_INPUT))
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)

    def get_phone_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.PHONE_INPUT)
        ).get_attribute("value")

    def enter_address(self, address):
        self.enter_text(self.ADDRESS_INPUT, address)

    def enter_zip(self, zip_code):
        self.enter_text(self.ZIP_INPUT, zip_code)

    def enter_employee_code(self, code):
        self.enter_text(self.EMPLOYEE_CODE_INPUT, code)

    def get_employee_code_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.EMPLOYEE_CODE_INPUT)
        ).get_attribute("value")

    def enter_hourly_wage(self, wage):
        el = self.wait.until(EC.visibility_of_element_located(self.HOURLY_WAGE_INPUT))
        self._set_input_value(el, str(wage))

    def get_hourly_wage_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.HOURLY_WAGE_INPUT)
        ).get_attribute("value")

    def assign_location(self, site_name):
        self.select_react_dropdown_option(self.LOCATIONS_COMBOBOX, site_name)

    def _close_locations_dropdown(self):
        # Send Escape to the combobox's inner input, not document.body.
        # ActionChains.send_keys(ESCAPE) without a focused target misses the
        # React Select handler. Wait for aria-expanded=false to confirm closure.
        try:
            combobox = self.driver.find_element(*self.LOCATIONS_COMBOBOX)
            if combobox.get_attribute("aria-expanded") == "true":
                inner = combobox.find_elements(By.XPATH, ".//input")
                (inner[0] if inner else combobox).send_keys(Keys.ESCAPE)
                WebDriverWait(self.driver, 8).until(
                    lambda d: d.find_element(*self.LOCATIONS_COMBOBOX)
                    .get_attribute("aria-expanded") in (None, "false")
                )
        except Exception:
            time.sleep(0.3)

    def assign_locations(self, site_names):
        # Use clear_first=False so CTRL+A+DEL doesn't wipe previously-selected
        # chips — in a multi-select React Select the input auto-clears between
        # selections, so we only need to clear the very first call (or not at all).
        for name in site_names:
            self.select_react_dropdown_option(
                self.LOCATIONS_COMBOBOX, name, clear_first=False
            )
        self._close_locations_dropdown()

    def remove_all_locations(self):
        """Remove all selected location chips by clicking their X buttons."""
        remove_btns = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'multi-value__remove') or "
            "contains(@class,'chip-remove') or "
            "contains(@aria-label,'remove') or "
            "contains(@aria-label,'Remove')]")
        for btn in remove_btns:
            try:
                self.driver.execute_script("arguments[0].click();", btn)
            except Exception:
                pass

    def get_location_chips_text(self):
        chips = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'multi-value__label') or "
            "contains(@class,'chip__label') or "
            "contains(@class,'tag-label')]")
        return [c.text.strip() for c in chips if c.text.strip()]

    def select_state(self, state_name):
        self.select_react_dropdown_option(self.STATE_COMBOBOX, state_name)

    def select_city(self, city_name):
        self.select_react_dropdown_option(self.CITY_COMBOBOX, city_name)

    def get_city_dropdown_options(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.wait.until(EC.element_to_be_clickable(self.CITY_COMBOBOX))
        )
        opts = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//*[@role='option']")
        ))
        return [o.text.strip() for o in opts if o.text.strip()]

    def ensure_active_switch_on(self):
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "true":
            switch.click()
            self.wait.until(lambda d: switch.get_attribute("aria-checked") == "true")

    def ensure_active_switch_off(self):
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "false":
            switch.click()
            self.wait.until(lambda d: switch.get_attribute("aria-checked") == "false")

    def active_switch_is_on(self):
        switch = self.wait.until(EC.presence_of_element_located(self.ACTIVE_SWITCH))
        return switch.get_attribute("aria-checked") == "true"

    def fill_create_form(self, first_name, last_name, email, phone, site_name):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_phone(phone)
        self.assign_location(site_name)
        self.ensure_active_switch_on()

    def click_save(self):
        import logging
        from selenium.webdriver.common.action_chains import ActionChains
        # Dismiss any open Locations dropdown before clicking Save.
        self._close_locations_dropdown()
        el = self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
        ActionChains(self.driver).move_to_element(el).click().perform()
        # After save the form iframe navigates to the list page, removing all
        # form elements from the DOM. driver.current_url reflects the outer shell
        # (unchanged in iframe-based nav), so we detect success by watching the
        # First Name input disappear instead.
        try:
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located(self.FIRST_NAME_INPUT)
            )
        except Exception:
            body = ""
            try:
                body = self.driver.find_element(By.TAG_NAME, "body").text[:1200]
            except Exception:
                pass
            logging.getLogger("nxtwash").warning(
                "Employee save did not navigate away. Page text: %s", body or "(empty)"
            )

    def click_cancel(self):
        el = self.wait.until(EC.visibility_of_element_located(self.CANCEL_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def _input_is_valid(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.execute_script("return arguments[0].checkValidity();", el)

    def first_name_input_is_valid(self):
        return self._input_is_valid(self.FIRST_NAME_INPUT)

    def last_name_input_is_valid(self):
        return self._input_is_valid(self.LAST_NAME_INPUT)

    def email_input_is_valid(self):
        return self._input_is_valid(self.EMAIL_INPUT)

    def phone_input_is_valid(self):
        return self._input_is_valid(self.PHONE_INPUT)

    def hourly_wage_input_is_valid(self):
        return self._input_is_valid(self.HOURLY_WAGE_INPUT)


class AdminEmployeeShiftPage(BasePage):
    """Employee Shift tab list page — /users/employeeShift"""

    SHIFT_LIST_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/users/employeeShift') "
        "and not(contains(@src,'/users/employeeShift/'))]")
    SHIFT_CREATE_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/users/employeeShift/new')]")
    SHIFT_EDIT_FRAME = (By.XPATH,
        "//iframe["
        "contains(@src,'/users/employeeShift') and ("
        "contains(@src,'shiftId=') or "
        "(contains(@src,'/users/employeeShift/') and not(contains(@src,'/users/employeeShift/new')))"
        ")]")

    SHIFT_PAGE_TITLE = (By.XPATH,
        "//*[contains(normalize-space(),'Employee shift') and "
        "(self::h1 or self::h2 or contains(@class,'title') or contains(@class,'heading'))]")
    ADD_SHIFT_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Add new employee shift')] | "
        "//button[contains(normalize-space(),'Add employee shift')] | "
        "//*[contains(normalize-space(),'Add new employee shift') and @role='button']")
    SHIFT_SEARCH_INPUT = (By.XPATH,
        "//input[@name='lastName' or @name='last_name' "
        "or @placeholder='Last Name' or @placeholder='Search by last name']")

    FILTER_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Filter by')] | "
        "//button[contains(normalize-space(),'Filter')]")
    FILTER_FIRST_NAME = (By.XPATH,
        "//input[@name='firstName' or @name='first_name' "
        "or @placeholder='First name' or @placeholder='First Name']")
    FILTER_SITE_COMBOBOX = (By.XPATH,
        "//*[normalize-space()='Select site' or normalize-space()='Site' "
        "or normalize-space()='Location']/following::*[@role='combobox'][1]")
    FILTER_ACTIVE_SHIFT_SWITCH = (By.XPATH,
        "//*[contains(normalize-space(),'Active shift')]"
        "/following::*[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Active shift')]"
        "/following::button[@role='switch'][1]")
    FILTER_START_DATE = (By.XPATH,
        "//input[@name='startDate' or @name='start_date' "
        "or @placeholder='Start date' or @placeholder='From']")
    FILTER_END_DATE = (By.XPATH,
        "//input[@name='endDate' or @name='end_date' "
        "or @placeholder='End date' or @placeholder='To']")
    APPLY_FILTERS_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters'] | "
        "//button[normalize-space()='Apply']")
    RESET_ALL_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Reset all')] | "
        "//button[contains(normalize-space(),'Reset All')]")
    EXPORT_BUTTON = (By.XPATH,
        "//button[normalize-space()='Export'] | "
        "//button[normalize-space()='Filter by']/following-sibling::button[1]")

    GRID_ROWS = (By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row')] | "
        "//tr[contains(@class,'row') and not(contains(@class,'header'))]")
    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and not(contains(@style,'display: none'))]")

    def wait_for_loaded(self):
        self.switch_to_frame_with_retry(self.SHIFT_LIST_FRAME)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        self.wait.until(EC.visibility_of_element_located(self.ADD_SHIFT_BUTTON))

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_visible_row_count(self):
        for _ in range(3):
            try:
                rows = self.driver.find_elements(*self.GRID_ROWS)
                return len([r for r in rows if r.is_displayed()])
            except StaleElementReferenceException:
                time.sleep(0.2)
        return 0

    def search_shift(self, last_name):
        el = self.wait.until(EC.element_to_be_clickable(self.SHIFT_SEARCH_INPUT))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        el.send_keys(last_name)
        el.send_keys(Keys.RETURN)
        self.wait.until(
            lambda d: d.find_element(*self.SHIFT_SEARCH_INPUT).get_attribute("value") == last_name
        )
        time.sleep(1)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def clear_search(self):
        el = self.wait.until(EC.element_to_be_clickable(self.SHIFT_SEARCH_INPUT))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        self.wait.until(
            lambda d: d.find_element(*self.SHIFT_SEARCH_INPUT).get_attribute("value") == ""
        )
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def click_add_shift(self):
        el = self.wait.until(EC.element_to_be_clickable(self.ADD_SHIFT_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def filter_panel_is_open(self):
        els = self.driver.find_elements(*self.FILTER_FIRST_NAME)
        try:
            return any(e.is_displayed() for e in els)
        except StaleElementReferenceException:
            return False

    def open_filter_panel(self):
        if self.filter_panel_is_open():
            return
        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.FILTER_FIRST_NAME))

    def filter_panel_has_expected_controls(self):
        self.open_filter_panel()
        body = self.get_body_text().lower()
        return all(label in body for label in ["first name", "active shift", "start date", "end date"])

    def filter_by_first_name(self, first_name):
        self.open_filter_panel()
        el = self.wait.until(EC.element_to_be_clickable(self.FILTER_FIRST_NAME))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        el.send_keys(first_name)

    def filter_by_site(self, site_name):
        self.open_filter_panel()
        self.select_react_dropdown_option(self.FILTER_SITE_COMBOBOX, site_name)

    def get_active_shift_filter_state(self):
        self.open_filter_panel()
        switch = self.wait.until(EC.presence_of_element_located(self.FILTER_ACTIVE_SHIFT_SWITCH))
        return switch.get_attribute("aria-checked") == "true"

    def toggle_active_shift_filter(self):
        self.open_filter_panel()
        switch = self.wait.until(EC.element_to_be_clickable(self.FILTER_ACTIVE_SHIFT_SWITCH))
        self.driver.execute_script("arguments[0].click();", switch)

    def apply_filters(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON)
            )
        except Exception:
            pass

    def reset_filters(self):
        from selenium.common.exceptions import StaleElementReferenceException
        self.open_filter_panel()
        for _attempt in range(3):
            try:
                btn = self.wait.until(EC.element_to_be_clickable(self.RESET_ALL_BUTTON))
                self.driver.execute_script("arguments[0].click();", btn)
                break
            except StaleElementReferenceException:
                if _attempt == 2:
                    raise
        # Reset All triggers an immediate data reload (no need to click Apply).
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        # The panel stays open after Reset All; close it so subsequent clicks
        # (e.g. the search input) are not intercepted.
        try:
            WebDriverWait(self.driver, 2).until(
                EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON)
            )
        except Exception:
            filter_btn = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
            self.driver.execute_script("arguments[0].click();", filter_btn)
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON)
                )
            except Exception:
                pass

    def filter_result_count_text(self):
        try:
            el = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[contains(normalize-space(),'Filter result')]")
            ))
            return el.text.strip()
        except TimeoutException:
            return ""

    def click_export_button(self):
        el = self.wait.until(EC.element_to_be_clickable(self.EXPORT_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def open_first_shift_edit(self):
        edit_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH,
             "(.//a[@role='button' and .//span[normalize-space()='Edit']])[1]")
        ))
        self.driver.execute_script("arguments[0].click();", edit_btn)


class AdminEmployeeShiftFormPage(BasePage):
    """Employee Shift create/edit form — /users/employeeShift/new or edit"""

    EMPLOYEE_COMBOBOX = (By.XPATH,
        "//*[normalize-space()='Employee']/following::*[@role='combobox'][1]")
    SITE_COMBOBOX = (By.XPATH,
        "//*[normalize-space()='Site' or normalize-space()='Location' "
        "or normalize-space()='Site/Location']/following::*[@role='combobox'][1]")

    START_TIME_INPUT = (By.XPATH,
        "//input[@name='startTime' or @name='start_time' or "
        "contains(@placeholder,'Start time') or contains(@placeholder,'start')]")
    END_TIME_INPUT = (By.XPATH,
        "//input[@name='endTime' or @name='end_time' or "
        "contains(@placeholder,'End time') or contains(@placeholder,'end')]")
    DATE_INPUT = (By.XPATH,
        "//input[@name='date' or @name='shiftDate' or @name='shift_date']")

    ACTIVE_SWITCH = (By.XPATH,
        "//*[contains(normalize-space(),'Active shift')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch'] | "
        "//form//button[@role='switch'][1]")

    SAVE_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Save shift')] | "
        "//button[normalize-space()='Save'] | "
        "//*[@data-type='primary' and contains(normalize-space(),'Save')]")
    CANCEL_BUTTON = (By.XPATH,
        "//button[normalize-space()='Cancel'] | "
        "//*[@data-type and normalize-space()='Cancel']")

    def wait_for_create_loaded(self):
        self.switch_to_frame_with_retry(AdminEmployeeShiftPage.SHIFT_CREATE_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.EMPLOYEE_COMBOBOX))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))

    def wait_for_edit_loaded(self):
        self.switch_to_frame_with_retry(AdminEmployeeShiftPage.SHIFT_EDIT_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def _set_input_value(self, element, value):
        self.driver.execute_script("""
            var input = arguments[0]; var value = arguments[1];
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            input.focus();
            setter.call(input, value);
            input.dispatchEvent(new Event('input', {bubbles: true}));
            input.dispatchEvent(new Event('change', {bubbles: true}));
        """, element, value)

    def select_employee(self, employee_name):
        self.select_react_dropdown_option(self.EMPLOYEE_COMBOBOX, employee_name)

    def select_site(self, site_name):
        self.select_react_dropdown_option(self.SITE_COMBOBOX, site_name)

    def set_shift_date(self, date_str):
        el = self.wait.until(EC.presence_of_element_located(self.DATE_INPUT))
        self._set_input_value(el, date_str)

    def set_start_time(self, time_str):
        el = self.wait.until(EC.presence_of_element_located(self.START_TIME_INPUT))
        self._set_input_value(el, time_str)

    def set_end_time(self, time_str):
        el = self.wait.until(EC.presence_of_element_located(self.END_TIME_INPUT))
        self._set_input_value(el, time_str)

    def ensure_active_switch_on(self):
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "true":
            switch.click()
            self.wait.until(lambda d: switch.get_attribute("aria-checked") == "true")

    def ensure_active_switch_off(self):
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "false":
            switch.click()
            self.wait.until(lambda d: switch.get_attribute("aria-checked") == "false")

    def active_switch_is_on(self):
        switch = self.wait.until(EC.presence_of_element_located(self.ACTIVE_SWITCH))
        return switch.get_attribute("aria-checked") == "true"

    def get_employee_dropdown_options(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.wait.until(EC.element_to_be_clickable(self.EMPLOYEE_COMBOBOX))
        )
        opts = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//*[@role='option']")
        ))
        return [o.text.strip() for o in opts if o.text.strip()]

    def get_site_dropdown_options(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.wait.until(EC.element_to_be_clickable(self.SITE_COMBOBOX))
        )
        opts = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//*[@role='option']")
        ))
        return [o.text.strip() for o in opts if o.text.strip()]

    def click_save(self):
        el = self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def click_cancel(self):
        el = self.wait.until(EC.visibility_of_element_located(self.CANCEL_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)
