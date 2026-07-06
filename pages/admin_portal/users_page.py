from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class AdminUsersPage(BasePage):
    """List page — /users/users."""

    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/users/users?') "
        "or (contains(@src,'/users/users') "
        "and not(contains(@src,'/users/users/')))]",
    )
    CREATE_FRAME = (By.XPATH, "//iframe[contains(@src,'/users/users/new')]")
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'users/users') and contains(@src,'userId=')]",
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Users']")
    ADD_USER_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Add user')] | "
        "//span[@data-type='primary' and contains(normalize-space(),'Add user')]",
    )
    # Main search is phone-only
    SEARCH_INPUT = (
        By.XPATH,
        "//input[@name='phone' or @name='phoneNumber' or @placeholder='Search by phone']",
    )
    FILTER_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Filter by')]")
    EXPORT_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Filter by']/following-sibling::button[1]",
    )
    APPLY_FILTERS_BUTTON = (By.XPATH, "//button[normalize-space()='Apply filters']")
    RESET_ALL_BUTTON = (By.XPATH, "//button[normalize-space()='Reset all']")

    # Filter panel inputs
    FILTER_FIRST_NAME = (By.XPATH, "//input[@name='firstName' or @name='first_name']")
    FILTER_LAST_NAME = (By.XPATH, "//input[@name='lastName' or @name='last_name']")
    FILTER_EMAIL = (
        By.XPATH,
        "//input[@name='email' or @name='emailId' or @name='email_id']",
    )
    FILTER_EMPLOYEE_CODE = (
        By.XPATH,
        "//input[@name='employeeCode' or @name='employee_code' or @name='empCode']",
    )
    FILTER_SITE_CONTROL = (
        By.XPATH,
        "//*[normalize-space()='Select site']/following::*[@role='combobox'][1] | "
        "//*[normalize-space()='Site']/following::*[@role='combobox'][1]",
    )
    ACTIVE_FILTER_SWITCH = (
        By.XPATH,
        "//*[contains(normalize-space(),'Active')]"
        "/following::*[@role='switch' or self::input[@type='checkbox']][1]",
    )

    GRID_LOAD_MASK = (
        By.CSS_SELECTOR,
        ".inovua-react-toolkit-load-mask__background-layer",
    )

    def wait_for_loaded(self):
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME))
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_USER_BUTTON))
        self._wait_for_grid_idle()

    def _wait_for_grid_idle(self):
        self.wait.until(
            lambda d: not any(
                m.is_displayed() for m in d.find_elements(*self.GRID_LOAD_MASK)
            )
        )

    def get_body_text(self):
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except Exception:
            self.driver.switch_to.default_content()
            return self.driver.find_element(By.TAG_NAME, "body").text

    # ── Search ────────────────────────────────────────────────────────────────

    def search_user(self, phone):
        el = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        el.click()
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(phone)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value") == phone
        )
        self._wait_for_grid_idle()

    def clear_search(self):
        el = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        el.click()
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value") == ""
        )
        self._wait_for_grid_idle()

    # ── Row helpers ───────────────────────────────────────────────────────────

    def _user_email_cell_locator(self, email):
        # Inovua DataGrid: email and edit are sibling cells — no common row ancestor.
        # Use contains() so minor tooltip/whitespace variations don't break the match.
        return (
            By.XPATH,
            "//*[contains(@class,'InovuaReactDataGrid__cell') and contains(normalize-space(),'%s')]"
            % email,
        )

    def _user_row_locator(self, email):
        return self._user_email_cell_locator(email)

    def wait_for_user_row(self, email):
        return self.wait.until(
            EC.visibility_of_element_located(self._user_email_cell_locator(email))
        )

    def get_user_status(self, email):
        # No status column — infer from visibility: default list shows active users only.
        cells = self.driver.find_elements(*self._user_email_cell_locator(email))
        if any(c.is_displayed() for c in cells):
            return "Active"
        return "Inactive"

    def get_visible_row_count(self):
        # Count visible edit links — one per row.
        links = self.driver.find_elements(
            By.XPATH,
            "//a[contains(@class,'table__edit') and not(contains(@class,'wrapper'))]",
        )
        return len([lnk for lnk in links if lnk.is_displayed()])

    # ── Navigation ────────────────────────────────────────────────────────────

    def click_add_user(self):
        el = self.wait.until(EC.element_to_be_clickable(self.ADD_USER_BUTTON))
        el.click()
        self.driver.switch_to.default_content()

    _EDIT_LINK = (
        By.XPATH,
        "//a[contains(@class,'table__edit') and not(contains(@class,'wrapper'))]",
    )

    def open_edit_user(self, email):
        # Check if user is visible; if not it may be inactive.
        cells = self.driver.find_elements(*self._user_email_cell_locator(email))
        if not any(c.is_displayed() for c in cells):
            self.toggle_active_filter()
            self.apply_filters()
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: any(
                        c.is_displayed()
                        for c in d.find_elements(*self._user_email_cell_locator(email))
                    )
                )
            except TimeoutException:
                raise TimeoutException("User row not found for email: %s" % email)
        # Confirm email cell visible, then click the first VISIBLE edit link.
        # (Inovua DataGrid keeps hidden-row elements in DOM; must skip them.)
        self.wait_for_user_row(email)
        self.wait.until(
            lambda d: any(
                lnk.is_displayed()
                for lnk in d.find_elements(*self._EDIT_LINK)
            )
        )
        visible = [
            lnk for lnk in self.driver.find_elements(*self._EDIT_LINK)
            if lnk.is_displayed()
        ]
        self.driver.execute_script("arguments[0].click();", visible[0])
        self.driver.switch_to.default_content()

    # ── Filter panel ──────────────────────────────────────────────────────────

    def open_filter_panel(self):
        visible = [
            el for el in self.driver.find_elements(*self.FILTER_FIRST_NAME)
            if el.is_displayed()
        ]
        if visible:
            return
        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.FILTER_FIRST_NAME))

    def filter_panel_has_expected_controls(self):
        self.open_filter_panel()
        body = self.get_body_text()
        expected = ["First name", "Last name", "Email", "Site", "Active"]
        return all(label.lower() in body.lower() for label in expected)

    def _enter_filter_field(self, locator, value):
        self.open_filter_panel()
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(value)

    def filter_by_first_name(self, name):
        self._enter_filter_field(self.FILTER_FIRST_NAME, name)

    def filter_by_last_name(self, name):
        self._enter_filter_field(self.FILTER_LAST_NAME, name)

    def filter_by_email(self, email):
        self._enter_filter_field(self.FILTER_EMAIL, email)

    def filter_by_employee_code(self, code):
        self._enter_filter_field(self.FILTER_EMPLOYEE_CODE, code)

    def filter_by_site(self, site_name):
        self.open_filter_panel()
        self.select_react_dropdown_option(self.FILTER_SITE_CONTROL, site_name)

    def toggle_active_filter(self):
        self.open_filter_panel()
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_FILTER_SWITCH))
        try:
            switch.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", switch)

    def apply_filters(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.element_to_be_clickable(self.ADD_USER_BUTTON))
        self._wait_for_grid_idle()

    def reset_filters(self):
        self.open_filter_panel()
        btn = self.wait.until(EC.presence_of_element_located(self.RESET_ALL_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.element_to_be_clickable(self.ADD_USER_BUTTON))

    def get_site_filter_options(self):
        self.open_filter_panel()
        self.driver.execute_script(
            "arguments[0].click();",
            self.wait.until(EC.element_to_be_clickable(self.FILTER_SITE_CONTROL)),
        )
        options = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@role='option']"))
        )
        return [o.text.strip() for o in options if o.text.strip()]

    # ── Export ────────────────────────────────────────────────────────────────

    def search_user_by_email(self, email):
        """Use the filter panel to narrow the list to a specific email, then apply."""
        self.open_filter_panel()
        self._enter_filter_field(self.FILTER_EMAIL, email)
        self.apply_filters()

    def user_exists(self, email):
        self.search_user_by_email(email)
        try:
            self.wait_for_user_row(email)
            return True
        except TimeoutException:
            return False

    def click_export_button(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.EXPORT_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)


class AdminUserFormPage(BasePage):
    """Create / Edit form — /users/users/new and /users/users/edit/{id}."""

    # ── Form fields ───────────────────────────────────────────────────────────
    EMPLOYEE_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='Employee']/following::*[@role='combobox'][1] | "
        "//input[@name='employeeId']/preceding::*[@role='combobox'][1]",
    )
    PASSWORD_INPUT = (By.XPATH, "//input[@name='pass' or @name='password'] | //input[@type='password'][1]")
    CONFIRM_PASSWORD_INPUT = (
        By.XPATH,
        "//input[@name='confirmPass' or @name='confirmPassword' or @name='confirm_password'] | "
        "//input[@type='password'][2]",
    )
    EMAIL_INPUT = (
        By.XPATH,
        "//input[@name='email' or @name='emailId' or @type='email']",
    )
    PHONE_INPUT = (
        By.XPATH,
        "//input[@name='phone' or @name='phoneNumber']",
    )
    ROLE_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='User role' or normalize-space()='Role']"
        "/following::*[@role='combobox'][1] | "
        "//input[@name='roleId']/preceding::*[@role='combobox'][1]",
    )
    ACTIVE_SWITCH = (
        By.XPATH,
        "//*[contains(normalize-space(),'Active')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch'] | "
        "//form//button[@role='switch'][1]",
    )
    SAVE_BUTTON = (
        By.XPATH,
        "//span[@data-type='primary' and (normalize-space()='Save user' "
        "or normalize-space()='Save')] | "
        "//button[normalize-space()='Save user' or normalize-space()='Save new user']",
    )
    CANCEL_BUTTON = (
        By.XPATH,
        "//span[@data-type and normalize-space()='Cancel'] | "
        "//button[normalize-space()='Cancel']",
    )
    CHANGE_PASSWORD_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Change password')] | "
        "//span[contains(normalize-space(),'Change password')]",
    )

    # Password change sub-form fields (modal or inline)
    NEW_PASSWORD_INPUT = (
        By.XPATH,
        "//input[@name='newPassword' or @name='new_password']",
    )
    NEW_CONFIRM_PASSWORD_INPUT = (
        By.XPATH,
        "//input[@name='confirmNewPassword' or @name='confirmPassword' "
        "or @name='confirm_new_password']",
    )

    # Password visibility toggle (eye icon)
    PASSWORD_TOGGLE = (
        By.XPATH,
        "//input[@name='password']/following-sibling::*[contains(@class,'eye') "
        "or @type='button'] | "
        "//input[@name='password']/parent::*//*[contains(@class,'toggle') "
        "or contains(@class,'eye')]",
    )
    CONFIRM_PASSWORD_TOGGLE = (
        By.XPATH,
        "//input[@name='confirmPassword']/following-sibling::*[contains(@class,'eye') "
        "or @type='button'] | "
        "//input[@name='confirmPassword']/parent::*//*[contains(@class,'toggle') "
        "or contains(@class,'eye')]",
    )

    def wait_for_create_loaded(self):
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(AdminUsersPage.CREATE_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))

    def wait_for_edit_loaded(self):
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(AdminUsersPage.EDIT_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        self.wait.until(
            lambda d: d.find_element(*self.EMAIL_INPUT).get_attribute("value") != ""
        )

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    # ── Field interactions ────────────────────────────────────────────────────

    def select_employee(self, employee_name):
        self.select_react_dropdown_option(self.EMPLOYEE_COMBOBOX, employee_name)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def enter_confirm_password(self, password):
        self.enter_text(self.CONFIRM_PASSWORD_INPUT, password)

    def enter_email(self, email):
        el = self.wait.until(EC.element_to_be_clickable(self.EMAIL_INPUT))
        el.click()
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(email)

    def clear_email(self):
        el = self.wait.until(EC.element_to_be_clickable(self.EMAIL_INPUT))
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)

    def get_email_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        ).get_attribute("value")

    def enter_phone(self, phone):
        el = self.wait.until(EC.element_to_be_clickable(self.PHONE_INPUT))
        el.click()
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(phone)

    def clear_phone(self):
        el = self.wait.until(EC.element_to_be_clickable(self.PHONE_INPUT))
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)

    def get_phone_value(self):
        raw = self.wait.until(
            EC.visibility_of_element_located(self.PHONE_INPUT)
        ).get_attribute("value")
        return "".join(c for c in raw if c.isdigit())

    def select_role(self, role_name):
        self.select_react_dropdown_option(self.ROLE_COMBOBOX, role_name)

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

    def fill_create_form(self, employee_name, password, email, phone, role_name):
        self.select_employee(employee_name)
        self.enter_password(password)
        self.enter_confirm_password(password)
        self.enter_email(email)
        self.enter_phone(phone)
        self.select_role(role_name)
        self.ensure_active_switch_on()

    def click_save(self):
        url_before = self.driver.current_url
        el = self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)
        # Wait for the SPA to navigate away from the form (save completed).
        # If validation blocks the save, the URL won't change — silently timeout.
        try:
            WebDriverWait(self.driver, 5).until(lambda d: d.current_url != url_before)
            self.driver.switch_to.default_content()
        except Exception:
            pass

    def click_cancel(self):
        el = self.wait.until(EC.visibility_of_element_located(self.CANCEL_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    # ── Validation helpers ────────────────────────────────────────────────────

    def _input_is_valid(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.execute_script("return arguments[0].checkValidity();", el)

    def _validation_message(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.execute_script("return arguments[0].validationMessage;", el)

    def email_input_is_valid(self):
        return self._input_is_valid(self.EMAIL_INPUT)

    def phone_input_is_valid(self):
        return self._input_is_valid(self.PHONE_INPUT)

    def password_input_is_valid(self):
        return self._input_is_valid(self.PASSWORD_INPUT)

    def confirm_password_input_is_valid(self):
        return self._input_is_valid(self.CONFIRM_PASSWORD_INPUT)

    # ── Password visibility toggle ────────────────────────────────────────────

    def toggle_password_visibility(self):
        el = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_TOGGLE))
        self.driver.execute_script("arguments[0].click();", el)

    def toggle_confirm_password_visibility(self):
        el = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_PASSWORD_TOGGLE))
        self.driver.execute_script("arguments[0].click();", el)

    def password_field_type(self):
        el = self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
        return el.get_attribute("type")

    def confirm_password_field_type(self):
        el = self.wait.until(EC.presence_of_element_located(self.CONFIRM_PASSWORD_INPUT))
        return el.get_attribute("type")

    # ── Change password flow ──────────────────────────────────────────────────

    def click_change_password_button(self):
        el = self.wait.until(EC.element_to_be_clickable(self.CHANGE_PASSWORD_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def enter_new_password(self, password):
        self.enter_text(self.NEW_PASSWORD_INPUT, password)

    def enter_new_confirm_password(self, password):
        self.enter_text(self.NEW_CONFIRM_PASSWORD_INPUT, password)

    def change_password_fields_visible(self):
        return len(self.driver.find_elements(*self.NEW_PASSWORD_INPUT)) > 0

    def password_fields_absent(self):
        pwd_els = self.driver.find_elements(*self.PASSWORD_INPUT)
        confirm_els = self.driver.find_elements(*self.CONFIRM_PASSWORD_INPUT)
        change_btn = self.driver.find_elements(*self.CHANGE_PASSWORD_BUTTON)
        return len(change_btn) > 0 and len(pwd_els) == 0 and len(confirm_els) == 0

    # ── Role / employee dropdown inspection ───────────────────────────────────

    def get_role_dropdown_options(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.wait.until(EC.element_to_be_clickable(self.ROLE_COMBOBOX)),
        )
        opts = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@role='option']"))
        )
        return [o.text.strip() for o in opts if o.text.strip()]

    def get_employee_dropdown_options(self):
        self.driver.execute_script(
            "arguments[0].click();",
            self.wait.until(EC.element_to_be_clickable(self.EMPLOYEE_COMBOBOX)),
        )
        opts = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@role='option']"))
        )
        return [o.text.strip() for o in opts if o.text.strip()]
