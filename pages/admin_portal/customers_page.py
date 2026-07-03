from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class CustomersPage(BasePage):

    # ── Frame locators ────────────────────────────────────────────────────────
    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/customers') and not(contains(@src,'/customers/'))]"
        " | //iframe[contains(@src,'/customers?')]",
    )
    CREATE_FRAME = (By.XPATH, "//iframe[contains(@src,'/customers/new')]")
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/customers/')"
        " and not(contains(@src,'/customers/new'))"
        " and not(contains(@src,'/cars/new'))]",
    )
    CAR_FORM_FRAME = (By.XPATH, "//iframe[contains(@src,'/cars/new')]")

    # ── List view ─────────────────────────────────────────────────────────────
    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Customers']")
    LICENSE_PLATE_SEARCH = (
        By.XPATH,
        "//input[@name='licensePlate']"
        " | //input[contains(@placeholder,'license') or contains(@placeholder,'License')]",
    )
    PHONE_SEARCH = (
        By.XPATH,
        "//input[@name='phoneNumber'] | //input[@name='phone']"
        " | //input[contains(@placeholder,'phone') or contains(@placeholder,'Phone')]",
    )
    FILTER_BUTTON = (By.XPATH, "//button[normalize-space()='Filter by']")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Filter by']/following-sibling::button[1]",
    )
    ADD_CUSTOMER_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Add customer')]",
    )
    GRID_ROWS = (By.XPATH, "//*[contains(@class,'InovuaReactDataGrid__row')]")
    GRID_LOAD_MASK = (
        By.CSS_SELECTOR,
        ".inovua-react-toolkit-load-mask__background-layer",
    )
    EDIT_LINK = (By.XPATH, "//*[normalize-space()='Edit']")

    # ── Filter panel ──────────────────────────────────────────────────────────
    APPLY_FILTERS_BUTTON = (By.XPATH, "//button[normalize-space()='Apply filters']")
    RESET_ALL_BUTTON = (By.XPATH, "//button[normalize-space()='Reset all']")
    FILTER_ACTIVE_ACCOUNTS_SWITCH = (
        By.XPATH,
        "//*[contains(normalize-space(),'active accounts')"
        " or contains(normalize-space(),'Active accounts')]"
        "/ancestor::*[contains(@class,'flex-toggler')]//button[@role='switch']",
    )
    FILTER_FIRST_NAME = (By.NAME, "searchString")
    FILTER_LAST_NAME = (By.NAME, "lastName")
    FILTER_EMAIL = (By.NAME, "emailId")
    FILTER_RFID = (By.NAME, "rfidTag")
    FILTER_SITE = (
        By.XPATH,
        "//*[normalize-space()='Site' or normalize-space()='Location'"
        " or normalize-space()='Assign to Loc/Site']"
        "/following::input[1]",
    )
    FILTER_SIGNUP_FROM = (
        By.XPATH,
        "//*[contains(normalize-space(),'Sign up date')]"
        "/following::input[@type='date' or @type='text'][1]",
    )
    FILTER_SIGNUP_TO = (
        By.XPATH,
        "//*[contains(normalize-space(),'Sign up date')]"
        "/following::input[@type='date' or @type='text'][2]",
    )
    FILTER_ALLOW_INVOICING = (
        By.XPATH,
        "//*[contains(normalize-space(),'Allow invoicing')]"
        "/following::*[@role='combobox' or self::select][1]",
    )
    FILTER_CARD_ON_FILE = (
        By.XPATH,
        "//*[contains(normalize-space(),'Card on file')]"
        "/following::*[@role='combobox' or self::select][1]",
    )
    FILTER_DECLINED = (
        By.XPATH,
        "//*[normalize-space()='Declined']/following::*[@role='combobox' or self::select][1]",
    )

    # ── Create / Edit form ────────────────────────────────────────────────────
    SAVE_CUSTOMER_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Add new customer')"
        " or contains(normalize-space(),'Save customer')"
        " or contains(normalize-space(),'Update customer')]",
    )
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    EMAIL_INPUT = (By.NAME, "emailId")
    ACTIVE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active customer']"
        "/ancestor::*[contains(@class,'flex-toggler')]//button[@role='switch']",
    )
    ALLOW_INVOICING_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Allow invoicing']"
        "/ancestor::*[contains(@class,'flex-toggler')]//button[@role='switch']",
    )
    SEND_TEXT_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Send text']"
        "/ancestor::*[contains(@class,'flex-toggler')]//button[@role='switch']",
    )
    SEND_EMAIL_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Send email']"
        "/ancestor::*[contains(@class,'flex-toggler')]//button[@role='switch']",
    )
    SITE_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='Assign to Loc/Site' or normalize-space()='Site']"
        "/following::input[@role='combobox'][1]",
    )
    DOB_INPUT = (
        By.XPATH,
        "//*[normalize-space()='Date of birth']/following::input[1]",
    )
    PHONE_INPUT = (
        By.XPATH,
        "//input[@name='phone'] | //input[@name='phoneNumber']"
        " | //input[@name='phone_number']"
        " | //*[normalize-space()='Phone']/following::input[1]",
    )
    ADDRESS_INPUT = (
        By.XPATH,
        "//input[@name='address'] | //textarea[@name='address']"
        " | //*[normalize-space()='Address']/following::input[1]",
    )
    ZIP_INPUT = (
        By.XPATH,
        "//input[@name='zip'] | //input[@name='zipCode'] | //input[@name='zip_code']"
        " | //*[normalize-space()='Zip']/following::input[1]"
        " | //*[normalize-space()='ZIP']/following::input[1]",
    )
    STATE_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='State']/following::input[@role='combobox'][1]",
    )
    CITY_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='City']/following::input[@role='combobox'][1]",
    )

    # ── Tabs ──────────────────────────────────────────────────────────────────
    CUSTOMER_INFO_TAB = (
        By.XPATH,
        "//button[@role='tab' and (normalize-space()='Customer info'"
        " or normalize-space()='Customer information')]",
    )
    CARS_SETTINGS_TAB = (
        By.XPATH,
        "//button[@role='tab' and (normalize-space()='Cars settings'"
        " or normalize-space()='Cars')]",
    )
    PAYMENT_SETTINGS_TAB = (
        By.XPATH,
        "//button[@role='tab' and (normalize-space()='Payment settings'"
        " or normalize-space()='Payment')]",
    )

    # ── Cars settings ─────────────────────────────────────────────────────────
    ADD_CAR_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Add') and contains(normalize-space(),'car')]"
        " | //button[contains(normalize-space(),'+ Add car')]",
    )
    LICENSE_PLATE_INPUT = (By.NAME, "licensePlate")
    CAR_RFID_INPUT = (
        By.XPATH,
        "//input[@name='rfid'] | //input[@name='RFID']",
    )
    SAVE_CAR_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Add new car')"
        " or contains(normalize-space(),'Save car')"
        " or contains(normalize-space(),'Update car')]",
    )
    ASSIGN_MEMBERSHIP_BUTTON = (
        By.XPATH,
        "//span[@data-type='primary' and normalize-space()='Assign membership']"
        " | //button[normalize-space()='Assign membership']",
    )
    BLACKLIST_CAR_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Blacklist')]",
    )
    DEACTIVATE_CAR_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Deactivate')]",
    )
    CARS_GRID_ROWS = (
        By.XPATH,
        "//div[@role='tab' and (normalize-space()='Cars settings' or normalize-space()='Cars')]"
        "/following::*[contains(@class,'InovuaReactDataGrid__row')]",
    )

    # ── Payment settings ──────────────────────────────────────────────────────
    CREDIT_CARD_SECTION = (
        By.XPATH,
        "//*[contains(normalize-space(),'Credit card info')"
        " or contains(normalize-space(),'Credit card')]"
        "[not(self::th) and not(self::td)]",
    )
    SAVE_CARD_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Save card')"
        " or contains(normalize-space(),'Add card')]",
    )
    TRANSACTION_HISTORY_SECTION = (
        By.XPATH,
        "//*[contains(normalize-space(),'Transaction history')]",
    )
    TRANSACTION_ALL_TIME_FILTER = (
        By.XPATH,
        "//*[normalize-space()='All time']",
    )

    # ─────────────────────────────────────────────────────────────────────────
    # Frame management
    # ─────────────────────────────────────────────────────────────────────────

    def wait_for_list_loaded(self):
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME))
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_CUSTOMER_BUTTON))
        self._wait_for_grid_idle()

    def _wait_for_grid_idle(self):
        self.wait.until(
            lambda d: not any(
                m.is_displayed() for m in d.find_elements(*self.GRID_LOAD_MASK)
            )
        )

    def wait_for_create_loaded(self):
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME))
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_CUSTOMER_BUTTON))

    def wait_for_edit_loaded(self):
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME))
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_CUSTOMER_BUTTON))
        self.wait.until(lambda d: self.get_first_name_value() != "")

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    # ─────────────────────────────────────────────────────────────────────────
    # List controls
    # ─────────────────────────────────────────────────────────────────────────

    def search_input_is_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.LICENSE_PLATE_SEARCH)
            ).is_displayed()
        except TimeoutException:
            return False

    def phone_search_input_is_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.PHONE_SEARCH)
            ).is_displayed()
        except TimeoutException:
            return False

    def filter_button_is_clickable(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.FILTER_BUTTON)
        ).is_displayed()

    def download_button_is_clickable(self):
        btn = self.wait.until(EC.presence_of_element_located(self.DOWNLOAD_BUTTON))
        return btn.is_displayed()

    def add_customer_button_is_clickable(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.ADD_CUSTOMER_BUTTON)
        ).is_displayed()

    def pagination_controls_are_visible(self):
        text = self.get_body_text()
        return "Page" in text or "page" in text

    def results_per_page_control_is_visible(self):
        text = self.get_body_text()
        return "Results per page" in text or "results per page" in text

    def every_visible_row_has_edit_action(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(@class,'InovuaReactDataGrid__row')"
                    " and .//*[normalize-space()='Edit']]",
                ))
            )
            return True
        except TimeoutException:
            return False

    def get_visible_row_count(self):
        rows = [r for r in self.driver.find_elements(*self.GRID_ROWS) if r.is_displayed()]
        return len(rows)

    # ─────────────────────────────────────────────────────────────────────────
    # Search
    # ─────────────────────────────────────────────────────────────────────────

    def _react_clear_and_type(self, locator, value):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(value)
        self.wait.until(
            lambda d: d.find_element(*locator).get_attribute("value") == value
        )
        self._wait_for_grid_idle()

    def search_by_license_plate(self, plate):
        self._react_clear_and_type(self.LICENSE_PLATE_SEARCH, plate)

    def search_by_phone(self, phone):
        # tel inputs reformat the value (e.g. 1001001 → (100) 100-1),
        # so we can't use _react_clear_and_type which waits for exact value match.
        el = self.wait.until(EC.element_to_be_clickable(self.PHONE_SEARCH))
        el.click()
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(phone)
        self._wait_for_grid_idle()

    def clear_license_plate_search(self):
        el = self.wait.until(EC.element_to_be_clickable(self.LICENSE_PLATE_SEARCH))
        el.click()
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        self.wait.until(
            lambda d: d.find_element(*self.LICENSE_PLATE_SEARCH).get_attribute("value") == ""
        )
        self._wait_for_grid_idle()

    def wait_for_customer_row_by_text(self, text):
        return self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//*[contains(@class,'InovuaReactDataGrid__row')"
                " and .//*[contains(normalize-space(),'%s')]]" % text,
            ))
        )

    def customer_row_visible(self, text):
        try:
            self.wait_for_customer_row_by_text(text)
            return True
        except TimeoutException:
            return False

    def open_edit_customer_from_row(self, row_text):
        self.wait_for_list_loaded()
        row = self.wait_for_customer_row_by_text(row_text)
        edit_link = row.find_element(
            By.XPATH, ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        # JS click bypasses iframe coordinate interception issues.
        self.driver.execute_script("arguments[0].click();", edit_link)
        self.wait_for_edit_loaded()

    # ─────────────────────────────────────────────────────────────────────────
    # Filter panel
    # ─────────────────────────────────────────────────────────────────────────

    def open_filter_panel(self):
        self.wait_for_list_loaded()
        visible_inputs = [
            el for el in self.driver.find_elements(*self.FILTER_FIRST_NAME)
            if el.is_displayed()
        ]
        if visible_inputs:
            return
        btn = self.wait.until(EC.presence_of_element_located(self.FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.visibility_of_element_located(self.FILTER_FIRST_NAME))

    def filter_panel_controls_are_visible(self):
        self.open_filter_panel()
        body = self.get_body_text()
        return (
            "First Name" in body
            and "Last Name" in body
            and "Email" in body
        )

    def active_accounts_toggle_is_on(self):
        self.open_filter_panel()
        switch = self.wait.until(
            EC.presence_of_element_located(self.FILTER_ACTIVE_ACCOUNTS_SWITCH)
        )
        return switch.get_attribute("aria-checked") == "true"

    def _filter_type_in(self, locator, value):
        self.open_filter_panel()
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(value)

    def filter_by_first_name(self, name):
        self._filter_type_in(self.FILTER_FIRST_NAME, name)

    def filter_by_last_name(self, name):
        self._filter_type_in(self.FILTER_LAST_NAME, name)

    def filter_by_email(self, email):
        self._filter_type_in(self.FILTER_EMAIL, email)

    def filter_by_rfid(self, rfid):
        self._filter_type_in(self.FILTER_RFID, rfid)

    def filter_by_site(self, site_name):
        self.open_filter_panel()
        self.click(self.FILTER_SITE)
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[normalize-space()='%s']" % site_name)
            )
        ).click()

    def filter_by_signup_date_range(self, date_from, date_to):
        self.open_filter_panel()
        from_el = self.wait.until(EC.visibility_of_element_located(self.FILTER_SIGNUP_FROM))
        to_el = self.wait.until(EC.visibility_of_element_located(self.FILTER_SIGNUP_TO))
        self._set_input_value(from_el, date_from)
        self._set_input_value(to_el, date_to)

    def filter_by_boolean_dropdown(self, locator, value):
        self.open_filter_panel()
        self.select_react_dropdown_option(locator, value)

    def get_filter_result_count_text(self):
        try:
            el = self.driver.find_element(*self.FILTER_RESULT_COUNT)
            return el.text.strip()
        except Exception:  # noqa: BLE001
            return ""

    FILTER_RESULT_COUNT = (
        By.XPATH,
        "//*[contains(normalize-space(),'result') and contains(normalize-space(),'customer')]",
    )

    def apply_filters(self):
        # Filter auto-applies as fields are filled — just wait for the grid to settle.
        self._wait_for_grid_idle()

    def reset_filters(self):
        # No reset button exists — clear each text field manually.
        for locator in [
            self.FILTER_FIRST_NAME,
            self.FILTER_LAST_NAME,
            self.FILTER_EMAIL,
            self.FILTER_RFID,
        ]:
            try:
                el = self.driver.find_element(*locator)
                if el.is_displayed() and el.get_attribute("value"):
                    el.click()
                    el.send_keys(Keys.COMMAND + "a")
                    el.send_keys(Keys.BACKSPACE)
            except Exception:  # noqa: BLE001
                pass
        self._wait_for_grid_idle()

    # ─────────────────────────────────────────────────────────────────────────
    # Create / Edit form
    # ─────────────────────────────────────────────────────────────────────────

    def open_create_customer(self):
        self.wait_for_list_loaded()
        self.click(self.ADD_CUSTOMER_BUTTON)
        self.wait_for_create_loaded()

    def enter_first_name(self, name):
        self.enter_text(self.FIRST_NAME_INPUT, name)

    def enter_last_name(self, name):
        self.enter_text(self.LAST_NAME_INPUT, name)

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def get_first_name_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.FIRST_NAME_INPUT)
        ).get_attribute("value")

    def get_last_name_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.LAST_NAME_INPUT)
        ).get_attribute("value")

    def get_email_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        ).get_attribute("value")

    def enter_phone(self, phone):
        try:
            el = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT))
            self.enter_text(self.PHONE_INPUT, phone)
        except TimeoutException:
            pass  # phone field may not exist on all form variants

    def enter_address(self, address):
        try:
            self.enter_text(self.ADDRESS_INPUT, address)
        except TimeoutException:
            pass

    def enter_zip(self, zip_code):
        try:
            self.enter_text(self.ZIP_INPUT, zip_code)
        except TimeoutException:
            pass

    def enter_dob(self, dob_value):
        """Set date of birth. dob_value must be in YYYY-MM-DD format."""
        try:
            el = self.wait.until(EC.visibility_of_element_located(self.DOB_INPUT))
            self._set_input_value(el, dob_value)
        except TimeoutException:
            pass

    def select_site(self, site_name):
        self.select_react_dropdown_option(self.SITE_COMBOBOX, site_name)

    def select_state(self, state_name):
        self.select_react_dropdown_option(self.STATE_COMBOBOX, state_name)

    def state_dropdown_is_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.STATE_COMBOBOX)
            ).is_displayed()
        except TimeoutException:
            return False

    def city_dropdown_is_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.CITY_COMBOBOX)
            ).is_displayed()
        except TimeoutException:
            return False

    def city_dropdown_has_no_options(self):
        try:
            self.click(self.CITY_COMBOBOX)
            body = self.get_body_text()
            return "No options" in body or "no option" in body.lower()
        except TimeoutException:
            return True

    def active_switch_is_on(self):
        switch = self.wait.until(EC.presence_of_element_located(self.ACTIVE_SWITCH))
        return switch.get_attribute("aria-checked") == "true"

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

    def allow_invoicing_is_on(self):
        switch = self.wait.until(EC.presence_of_element_located(self.ALLOW_INVOICING_SWITCH))
        return switch.get_attribute("aria-checked") == "true"

    def toggle_allow_invoicing(self):
        switch = self.wait.until(EC.element_to_be_clickable(self.ALLOW_INVOICING_SWITCH))
        switch.click()

    def click_save_customer(self):
        self.click(self.SAVE_CUSTOMER_BUTTON)

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)

    def save_customer_button_is_clickable(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.SAVE_CUSTOMER_BUTTON)
        ).is_displayed()

    def cancel_button_is_visible(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.CANCEL_BUTTON)
        ).is_displayed()

    # ─────────────────────────────────────────────────────────────────────────
    # Validation helpers
    # ─────────────────────────────────────────────────────────────────────────

    def _input_is_valid(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        return self.driver.execute_script("return arguments[0].checkValidity();", el)

    def _validation_message(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        return self.driver.execute_script("return arguments[0].validationMessage;", el)

    def first_name_input_is_valid(self):
        return self._input_is_valid(self.FIRST_NAME_INPUT)

    def last_name_input_is_valid(self):
        return self._input_is_valid(self.LAST_NAME_INPUT)

    def get_first_name_validation_message(self):
        return self._validation_message(self.FIRST_NAME_INPUT)

    def get_last_name_validation_message(self):
        return self._validation_message(self.LAST_NAME_INPUT)

    # ─────────────────────────────────────────────────────────────────────────
    # Tabs
    # ─────────────────────────────────────────────────────────────────────────

    def tab_is_disabled(self, locator):
        try:
            tab = self.wait.until(EC.presence_of_element_located(locator))
            disabled = tab.get_attribute("disabled")
            aria_disabled = tab.get_attribute("aria-disabled")
            return disabled is not None or aria_disabled == "true"
        except TimeoutException:
            return False

    def cars_settings_tab_is_disabled(self):
        return self.tab_is_disabled(self.CARS_SETTINGS_TAB)

    def payment_settings_tab_is_disabled(self):
        return self.tab_is_disabled(self.PAYMENT_SETTINGS_TAB)

    def open_cars_settings_tab(self):
        self.click(self.CARS_SETTINGS_TAB)
        self.wait.until(EC.element_to_be_clickable(self.ADD_CAR_BUTTON))

    def open_payment_settings_tab(self):
        self.click(self.PAYMENT_SETTINGS_TAB)
        # CREDIT_CARD_SECTION may be hidden in the DOM before the tab loads, so
        # presence_of_element_located returns immediately. Instead wait until the
        # Customer Info fields (First Name) have left the visible body text —
        # that confirms the tab panel has actually switched.
        self.wait.until(
            lambda d: "First Name" not in d.find_element(By.TAG_NAME, "body").text
        )
        # Give lazy-loaded payment content a moment to render.
        try:
            self.wait.until(
                lambda d: any(
                    t in d.find_element(By.TAG_NAME, "body").text
                    for t in ["Credit card", "Transaction", "Card", "Add card", "Save card"]
                )
            )
        except TimeoutException:
            pass  # Payment tab may be empty for customers with no payment data

    # ─────────────────────────────────────────────────────────────────────────
    # Cars settings
    # ─────────────────────────────────────────────────────────────────────────

    def add_car_button_is_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.ADD_CAR_BUTTON)
            ).is_displayed()
        except TimeoutException:
            return False

    def save_car_button_is_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.SAVE_CAR_BUTTON)
            ).is_displayed()
        except TimeoutException:
            return False

    def license_plate_field_is_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.LICENSE_PLATE_INPUT)
            ).is_displayed()
        except TimeoutException:
            return False

    def rfid_field_is_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.CAR_RFID_INPUT)
            ).is_displayed()
        except TimeoutException:
            return False

    def license_plate_field_is_required(self):
        el = self.wait.until(EC.visibility_of_element_located(self.LICENSE_PLATE_INPUT))
        return el.get_attribute("required") is not None

    def rfid_field_is_required(self):
        el = self.wait.until(EC.visibility_of_element_located(self.CAR_RFID_INPUT))
        return el.get_attribute("required") is not None

    def open_add_car_form(self):
        self.click(self.ADD_CAR_BUTTON)
        # Clicking "+ Add car" navigates the outer shell to /cars/new — the old
        # edit iframe is gone. Switch back to top level then into the new frame.
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.CAR_FORM_FRAME))
        self.wait.until(EC.visibility_of_element_located(self.LICENSE_PLATE_INPUT))

    def enter_license_plate(self, plate):
        self.enter_text(self.LICENSE_PLATE_INPUT, plate)

    def enter_car_rfid(self, rfid):
        self.enter_text(self.CAR_RFID_INPUT, rfid)

    def get_license_plate_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.LICENSE_PLATE_INPUT)
        ).get_attribute("value")

    def click_save_car(self):
        self.click(self.SAVE_CAR_BUTTON)
        # After saving the car form, the shell navigates back to the edit customer
        # page. Switch back to top level and re-enter the edit iframe.
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME))

    def license_plate_input_is_valid(self):
        return self._input_is_valid(self.LICENSE_PLATE_INPUT)

    def rfid_input_is_valid(self):
        return self._input_is_valid(self.CAR_RFID_INPUT)

    def assign_membership_button_is_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.ASSIGN_MEMBERSHIP_BUTTON)
            ).is_displayed()
        except TimeoutException:
            return False

    def car_row_visible(self, plate):
        try:
            self.wait.until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//*[contains(@class,'InovuaReactDataGrid__row')"
                    " and .//*[contains(normalize-space(),'%s')]]" % plate,
                ))
            )
            return True
        except TimeoutException:
            return False

    # ─────────────────────────────────────────────────────────────────────────
    # Payment settings
    # ─────────────────────────────────────────────────────────────────────────

    def credit_card_section_is_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.CREDIT_CARD_SECTION)
            ).is_displayed()
        except TimeoutException:
            return False

    def save_card_button_is_visible(self):
        try:
            return self.wait.until(
                EC.presence_of_element_located(self.SAVE_CARD_BUTTON)
            ).is_displayed()
        except TimeoutException:
            return False

    def transaction_history_is_visible(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.TRANSACTION_HISTORY_SECTION)
            ).is_displayed()
        except TimeoutException:
            return False

    # ─────────────────────────────────────────────────────────────────────────
    # React input helper (shared with WashPackagesPage pattern)
    # ─────────────────────────────────────────────────────────────────────────

    def _set_input_value(self, element, value):
        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            ).set;
            input.focus();
            setter.call(input, value);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            value,
        )

    # ─────────────────────────────────────────────────────────────────────────
    # High-level helpers
    # ─────────────────────────────────────────────────────────────────────────

    def fill_customer_form(self, first_name, last_name, site, email=""):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        if email:
            self.enter_email(email)
        self.ensure_active_switch_on()
        self.select_site(site)

    def create_full_customer(
        self,
        first_name,
        last_name,
        site,
        email="",
        phone="",
        dob="",
        address="",
        zip_code="",
        state="",
        city="",
    ):
        """Open the create form and fill every provided field before saving."""
        self.open_create_customer()
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        if email:
            self.enter_email(email)
        if phone:
            self.enter_phone(phone)
        if dob:
            self.enter_dob(dob)
        if address:
            self.enter_address(address)
        if zip_code:
            self.enter_zip(zip_code)
        self.ensure_active_switch_on()
        self.select_site(site)
        if state:
            try:
                self.select_state(state)
                if city:
                    self.select_react_dropdown_option(self.CITY_COMBOBOX, city)
            except Exception:  # noqa: BLE001
                pass  # state/city cascade may vary by environment
        self.click_save_customer()
        try:
            self.wait_for_list_loaded()
        except TimeoutException:
            return

    def create_customer(self, first_name, last_name, site, email=""):
        """Minimal create — required fields only. Use create_full_customer for all fields."""
        self.open_create_customer()
        self.fill_customer_form(first_name, last_name, site, email)
        self.click_save_customer()
        try:
            self.wait_for_list_loaded()
        except TimeoutException:
            return

    def click_download_button(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.DOWNLOAD_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
