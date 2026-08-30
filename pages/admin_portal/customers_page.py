import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class CustomersPage(BasePage):

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
    FILTER_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Filter by')]")
    FILTER_BUTTON_ACTIVE = (By.XPATH, "//button[contains(normalize-space(),'Filter by (')]")
    RESET_FILTERS_BUTTON = (By.XPATH, "//button[normalize-space()='Reset filters']")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[.//svg[contains(@class,'lucide-download')"
        " or contains(@class,'download')"
        " or contains(@class,'arrow-down')]]"
        " | //button[@aria-label[contains(.,'ownload') or contains(.,'xport')]]"
        " | //button[@title[contains(.,'ownload') or contains(.,'xport')]]",
    )
    ADD_CUSTOMER_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Add customer')]",
    )
    GRID_ROWS = (By.XPATH, "//table//tr[td]")
    GRID_LOAD_MASK = (
        By.CSS_SELECTOR,
        ".inovua-react-toolkit-load-mask__background-layer",
    )
    EDIT_LINK = (By.XPATH, "//*[normalize-space()='Edit']")

    # ── Filter panel ──────────────────────────────────────────────────────────
    APPLY_FILTERS_BUTTON = (By.XPATH, "//button[normalize-space()='Apply filters']")
    RESET_ALL_BUTTON = (By.XPATH, "//button[normalize-space()='Reset all']")
    FILTER_ACTIVE_ACCOUNTS_SWITCH = (By.NAME, "isActive")
    FILTER_FIRST_NAME = (By.NAME, "searchString")
    FILTER_LAST_NAME = (By.NAME, "lastName")
    FILTER_EMAIL = (By.NAME, "emailId")
    FILTER_RFID = (
        By.XPATH,
        "//input[@name='rfidTag' or @name='rfid' or @name='RFID' or @name='rfid_tag']"
        " | //*[normalize-space()='RFID']/following::input[@type='text' or not(@type)][1]",
    )
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
        "//button[@form='customer-form'"
        " or contains(normalize-space(),'Add new customer')"
        " or contains(normalize-space(),'Save customer')"
        " or contains(normalize-space(),'Update customer')"
        " or contains(normalize-space(),'Save new')"
        " or normalize-space()='Save changes']",
    )
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    EMAIL_INPUT = (By.NAME, "emailId")
    ACTIVE_SWITCH = (By.NAME, "isActive")
    ALLOW_INVOICING_SWITCH = (By.NAME, "allowInvoicing")
    SEND_TEXT_SWITCH = (By.NAME, "isSendText")
    SEND_EMAIL_SWITCH = (By.NAME, "isSendEmail")
    SITE_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='Assign to Loc/Site'"
        " or normalize-space()='Site'"
        " or normalize-space()='Site/Location'"
        " or normalize-space()='Location']"
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
        "//*[@role='tab' and (normalize-space()='Customer info'"
        " or normalize-space()='Customer information')]"
        " | //*[normalize-space()='Customer info' or normalize-space()='Customer information']",
    )
    CARS_SETTINGS_TAB = (
        By.XPATH,
        "//*[@role='tab'][normalize-space()='Cars settings']"
        " | //button[normalize-space()='Cars settings']"
        " | //li[normalize-space()='Cars settings']"
        " | //a[normalize-space()='Cars settings']"
        " | //*[normalize-space()='Cars settings']",
    )
    PAYMENT_SETTINGS_TAB = (
        By.XPATH,
        "//*[@role='tab'][normalize-space()='Payment settings']"
        " | //button[normalize-space()='Payment settings']"
        " | //li[normalize-space()='Payment settings']"
        " | //a[normalize-space()='Payment settings']"
        " | //*[normalize-space()='Payment settings']",
    )

    # ── Cars settings ─────────────────────────────────────────────────────────
    ADD_CAR_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Add car')"
        " or contains(normalize-space(),'Add Car')"
        " or contains(normalize-space(),'+ Add car')"
        " or contains(normalize-space(),'New car')"
        " or contains(normalize-space(),'New Car')"
        " or contains(normalize-space(),'Add vehicle')]",
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
    CARS_GRID_ROWS = (By.XPATH, "//table//tr[td]")

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
        "//*[contains(normalize-space(),'Transaction history')"
        " or contains(normalize-space(),'Payment history')]",
    )
    TRANSACTION_ALL_TIME_FILTER = (
        By.XPATH,
        "//*[normalize-space()='All time']",
    )

    # ─────────────────────────────────────────────────────────────────────────
    # Frame management
    # ─────────────────────────────────────────────────────────────────────────

    def _switch_to_car_form_frame(self):
        """Switch into the iframe hosting the add/edit car form.

        The add-car route (/customers/edit/{id}/cars/new/{id}) renders its
        content inside a legacy iframe. Try known src patterns first, then
        fall back to enumerating all iframes and switching to the first one
        that has non-empty body text.
        """
        self.driver.switch_to.default_content()
        for pattern in ("cars/new", "/customers/edit"):
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.XPATH, "//iframe[contains(@src,'%s')]" % pattern)
                    )
                )
                return
            except TimeoutException:
                pass
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: len(d.find_elements(By.TAG_NAME, "iframe")) > 0
            )
        except TimeoutException:
            return
        for frame in self.driver.find_elements(By.TAG_NAME, "iframe"):
            try:
                self.driver.switch_to.frame(frame)
                if self.driver.find_element(By.TAG_NAME, "body").text.strip():
                    return
                self.driver.switch_to.default_content()
            except Exception:  # noqa: BLE001
                self.driver.switch_to.default_content()

    def _wait_for_success_toast_gone(self):
        """If a Success notification is visible, wait for it to disappear.

        The server's search index is updated asynchronously after a save. The
        Success toast is the closest UI proxy for "save acknowledged"; once it
        fades out the index has usually caught up, preventing 0-result filter
        queries on freshly created records.
        """
        try:
            toast = WebDriverWait(self.driver, 0.8).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[contains(normalize-space(),'Success')]")
                )
            )
            WebDriverWait(self.driver, 8).until(EC.invisibility_of_element(toast))
        except TimeoutException:
            pass

    def wait_for_list_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_CUSTOMER_BUTTON))
        self._wait_for_grid_idle()
        self._wait_for_success_toast_gone()

    def _wait_for_grid_idle(self):
        self.wait.until(
            lambda d: not any(
                m.is_displayed() for m in d.find_elements(*self.GRID_LOAD_MASK)
            )
        )

    def wait_for_create_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_CUSTOMER_BUTTON))

    def wait_for_edit_loaded(self):
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
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.DOWNLOAD_BUTTON)
            )
            return btn.is_displayed()
        except TimeoutException:
            return False

    def add_customer_button_is_clickable(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.ADD_CUSTOMER_BUTTON)
        ).is_displayed()

    def pagination_controls_are_visible(self):
        text = self.get_body_text()
        return "Page" in text or "page" in text

    def results_per_page_control_is_visible(self):
        text = self.get_body_text()
        return "Show" in text or "out of" in text

    def every_visible_row_has_edit_action(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//table//tr[td and .//button[.//*[normalize-space()='Edit']]]",
                ))
            )
            return True
        except TimeoutException:
            return False

    def get_visible_row_count(self):
        from selenium.common.exceptions import StaleElementReferenceException as _Stale
        rows = self.driver.find_elements(*self.GRID_ROWS)
        count = 0
        any_stale = False
        for r in rows:
            try:
                if r.is_displayed():
                    count += 1
            except _Stale:
                any_stale = True
        if any_stale and count == 0 and rows:
            time.sleep(0.4)
            count = 0
            for r in self.driver.find_elements(*self.GRID_ROWS):
                try:
                    if r.is_displayed():
                        count += 1
                except _Stale:
                    pass
        return count

    # ─────────────────────────────────────────────────────────────────────────
    # Search
    # ─────────────────────────────────────────────────────────────────────────

    def _react_clear_and_type(self, locator, value):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        el.send_keys(value)
        self.wait.until(
            lambda d: d.find_element(*locator).get_attribute("value") == value
        )
        time.sleep(0.4)
        self._wait_for_grid_idle()

    def search_by_license_plate(self, plate):
        self._react_clear_and_type(self.LICENSE_PLATE_SEARCH, plate)

    def search_by_phone(self, phone):
        # Use JS-based value setter so React's onChange fires reliably in CI.
        # We do not wait for exact value match because tel inputs reformat digits
        # (e.g. "1001001" → "(100) 100-1") while React still filters on the raw value.
        el = self.wait.until(EC.element_to_be_clickable(self.PHONE_SEARCH))
        el.click()
        self._set_input_value(el, phone)
        time.sleep(0.4)
        self._wait_for_grid_idle()

    def clear_license_plate_search(self):
        el = self.wait.until(EC.element_to_be_clickable(self.LICENSE_PLATE_SEARCH))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        self.wait.until(
            lambda d: d.find_element(*self.LICENSE_PLATE_SEARCH).get_attribute("value") == ""
        )
        self._wait_for_grid_idle()

    def wait_for_customer_row_by_text(self, text):
        return self.wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//table//tr[td and .//*[contains(normalize-space(),'%s')]]" % text,
            ))
        )

    def customer_row_visible(self, text):
        try:
            self.wait_for_customer_row_by_text(text)
            return True
        except TimeoutException:
            return False

    def open_edit_customer_from_row(self, row_text):
        from selenium.common.exceptions import StaleElementReferenceException as _Stale
        self.wait_for_list_loaded()
        for attempt in range(3):
            try:
                row = self.wait_for_customer_row_by_text(row_text)
                edit_btn = row.find_element(
                    By.XPATH, ".//button[.//*[normalize-space()='Edit']]"
                )
                self.driver.execute_script("arguments[0].click();", edit_btn)
                break
            except _Stale:
                if attempt == 2:
                    raise
                time.sleep(0.4)
        self.wait_for_edit_loaded()

    # ─────────────────────────────────────────────────────────────────────────
    # Filter panel
    # ─────────────────────────────────────────────────────────────────────────

    def _reset_active_filter_if_present(self):
        """If a filter badge is active, clear it so the next filter call starts clean."""
        if not any(
            b.is_displayed()
            for b in self.driver.find_elements(*self.FILTER_BUTTON_ACTIVE)
        ):
            return
        # Try clicking Reset filters if the panel is already open
        try:
            btn = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable(self.RESET_FILTERS_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.3)
            self._wait_for_grid_idle()
            return
        except TimeoutException:
            pass
        # Panel is closed — open it by clicking the badge button, then reset
        active_btns = [
            b for b in self.driver.find_elements(*self.FILTER_BUTTON_ACTIVE)
            if b.is_displayed()
        ]
        if not active_btns:
            return
        self.driver.execute_script("arguments[0].click();", active_btns[0])
        try:
            btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.RESET_FILTERS_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.3)
            self._wait_for_grid_idle()
        except TimeoutException:
            pass

    def open_filter_panel(self):
        self.wait_for_list_loaded()
        # Clear any stale filter from previous tests before setting new ones.
        self._reset_active_filter_if_present()
        visible_inputs = [
            el for el in self.driver.find_elements(*self.FILTER_FIRST_NAME)
            if el.is_displayed()
        ]
        if visible_inputs:
            return
        btn = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
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
        return switch.is_selected()

    def ensure_active_filter_off(self):
        """Turn off the 'Active accounts only' filter toggle if it is on."""
        # Open the panel first — switch is not in the DOM while the panel is closed.
        self.open_filter_panel()
        try:
            # aria-checked lives on the wrapper ancestor, not the <input> itself.
            wrapper = WebDriverWait(self.driver, 5).until(
                lambda d: d.find_element(
                    By.XPATH,
                    "//input[@name='isActive']/ancestor::*[@aria-checked][1]"
                )
            )
            if wrapper.get_attribute("aria-checked") == "false":
                return
            self._click_react_switch(wrapper, False)
        except TimeoutException:
            pass

    def _filter_type_in(self, locator, value):
        self.open_filter_panel()
        el = self.wait.until(EC.element_to_be_clickable(locator))
        self._set_input_value(el, value)

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
        try:
            # Blur the focused filter input so React commits any typed value
            # before the Apply handler reads it. JS blur() fires the native
            # blur event, which React's onBlur picks up in both headed and
            # headless Chrome.
            self.driver.execute_script(
                "if (document.activeElement) document.activeElement.blur();"
            )
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON)
            )
            # JS click is coordinate-independent — works correctly in headless
            # Chrome even when the Apply button sits inside a scrollable panel.
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.5)  # Give the grid time to start re-rendering
        except TimeoutException:
            pass
        self._wait_for_grid_idle()

    def reset_filters(self):
        try:
            btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.RESET_FILTERS_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.3)
            self._wait_for_grid_idle()
            return
        except TimeoutException:
            pass
        # Fallback: clear each text field manually.
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
                    el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
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
        el = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_INPUT))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        el.send_keys(name)

    def enter_last_name(self, name):
        el = self.wait.until(EC.element_to_be_clickable(self.LAST_NAME_INPUT))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        el.send_keys(name)

    def enter_email(self, email):
        el = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        self._set_input_value(el, email)

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
        return switch.is_selected()

    def _click_react_switch(self, switch, desired_checked):
        """Toggle the react-switch outer span.

        Uses HTMLElement.click() via JS — coordinate-independent. Waits for
        aria-checked to hold a valid value before clicking (ensures the element
        is fully rendered, not just present). Verifies state via aria-checked on
        the wrapper — more authoritative than the hidden input's is_selected().
        Retries up to 2 more times with increasing pauses.
        """
        _WRAPPER_LOC = (
            By.XPATH,
            "//input[@name='isActive']/ancestor::*[@aria-checked][1]",
        )
        _FALLBACK_LOC = (By.XPATH, "//input[@name='isActive']/..")

        def _find_wrapper():
            try:
                def _ready(d):
                    try:
                        el = d.find_element(*_WRAPPER_LOC)
                        return el if el.get_attribute("aria-checked") in ("true", "false") else False
                    except Exception:
                        return False
                return WebDriverWait(self.driver, 2).until(_ready)
            except TimeoutException:
                return self.driver.find_element(*_FALLBACK_LOC)

        def _state_matches(d):
            try:
                w = d.find_element(*_WRAPPER_LOC)
                return (w.get_attribute("aria-checked") == "true") == desired_checked
            except Exception:
                return False

        def _fire_click():
            w = _find_wrapper()
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", w
            )
            time.sleep(0.2)
            self.driver.execute_script("arguments[0].click();", w)

        def _dismiss_alert():
            try:
                WebDriverWait(self.driver, 0.5).until(EC.alert_is_present())
                self.driver.switch_to.alert.accept()
                time.sleep(0.3)
            except TimeoutException:
                pass

        for attempt in range(3):
            if attempt > 0:
                time.sleep(0.4 * attempt)  # 0.4 s, 0.8 s between retries
            _fire_click()
            _dismiss_alert()
            try:
                WebDriverWait(self.driver, 3).until(_state_matches)
                return
            except TimeoutException:
                pass

    def ensure_active_switch_on(self):
        switch = self.wait.until(EC.presence_of_element_located(self.ACTIVE_SWITCH))
        if switch.is_selected():
            return
        self._click_react_switch(switch, True)

    def ensure_active_switch_off(self):
        switch = self.wait.until(EC.presence_of_element_located(self.ACTIVE_SWITCH))
        if not switch.is_selected():
            return
        self._click_react_switch(switch, False)

    def allow_invoicing_is_on(self):
        switch = self.wait.until(EC.presence_of_element_located(self.ALLOW_INVOICING_SWITCH))
        return switch.is_selected()

    def toggle_allow_invoicing(self):
        switch = self.wait.until(EC.presence_of_element_located(self.ALLOW_INVOICING_SWITCH))
        self.driver.execute_script("arguments[0].click();", switch)

    def click_save_customer(self):
        from selenium.webdriver.common.action_chains import ActionChains
        el = self.wait.until(EC.element_to_be_clickable(self.SAVE_CUSTOMER_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
        # Primary: requestSubmit() fires the browser's native submit event
        # which React Hook Form hooks into via its onSubmit handler.
        had_form = self.driver.execute_script(
            "var f=arguments[0].closest('form');"
            "if(f){f.requestSubmit(arguments[0]);return true;}return false;",
            el,
        )
        if not had_form:
            ActionChains(self.driver).move_to_element(el).click().perform()

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)
        # The form shows "Are you sure you want to cancel?" when data was entered.
        # Click "Yes" to confirm; if no dialog appears, continue silently.
        try:
            confirm = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//*[@role='dialog']//button[normalize-space()='Yes']",
                ))
            )
            confirm.click()
        except TimeoutException:
            pass

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
        aria_invalid = el.get_attribute("aria-invalid")
        if aria_invalid == "true":
            return False
        # React forms use custom validation messages in adjacent DOM elements,
        # not the HTML5 `required` attribute. Walk up to find a sibling error node.
        has_react_error = self.driver.execute_script("""
            var el = arguments[0];
            for (var p = el.parentElement; p && p !== document.body; p = p.parentElement) {
                var kids = Array.from(p.children);
                var err = kids.find(function(c) {
                    return c !== el && c.offsetHeight > 0 && (
                        (c.className && (c.className.indexOf('error') >= 0 ||
                                         c.className.indexOf('invalid') >= 0)) ||
                        c.getAttribute('role') === 'alert' ||
                        (c.textContent.trim().toLowerCase().indexOf('required') >= 0 &&
                         c.textContent.trim().length < 80)
                    );
                });
                if (err) { return true; }
            }
            return false;
        """, el)
        if has_react_error:
            return False
        return self.driver.execute_script("return arguments[0].checkValidity();", el)

    def _validation_message(self, locator):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        native = self.driver.execute_script("return arguments[0].validationMessage;", el)
        if native:
            return native
        # Fall back to React custom validation message from adjacent DOM element.
        return self.driver.execute_script("""
            var el = arguments[0];
            for (var p = el.parentElement; p && p !== document.body; p = p.parentElement) {
                var kids = Array.from(p.children);
                var err = kids.find(function(c) {
                    return c !== el && c.offsetHeight > 0 && (
                        (c.className && (c.className.indexOf('error') >= 0 ||
                                         c.className.indexOf('invalid') >= 0)) ||
                        c.getAttribute('role') === 'alert' ||
                        (c.textContent.trim().toLowerCase().indexOf('required') >= 0 &&
                         c.textContent.trim().length < 80)
                    );
                });
                if (err) { return err.textContent.trim(); }
            }
            return '';
        """, el) or ""

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
            tab = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(locator)
            )
            disabled = tab.get_attribute("disabled")
            aria_disabled = tab.get_attribute("aria-disabled")
            return disabled is not None or aria_disabled == "true"
        except TimeoutException:
            # Tab not present in the DOM (e.g. create-new form) = inaccessible.
            return True

    def cars_settings_tab_is_disabled(self):
        return self.tab_is_disabled(self.CARS_SETTINGS_TAB)

    def payment_settings_tab_is_disabled(self):
        return self.tab_is_disabled(self.PAYMENT_SETTINGS_TAB)

    def open_cars_settings_tab(self):
        self.click(self.CARS_SETTINGS_TAB)
        # Wait for tab switch: Customer Info fields should leave the visible body.
        try:
            self.wait.until(
                lambda d: "First Name" not in d.find_element(
                    By.TAG_NAME, "body"
                ).text
            )
        except TimeoutException:
            pass
        self.wait.until(EC.element_to_be_clickable(self.ADD_CAR_BUTTON))

    def open_payment_settings_tab(self):
        self.click(self.PAYMENT_SETTINGS_TAB)
        # Wait until the Customer Info fields leave the body — confirms tab switched.
        try:
            self.wait.until(
                lambda d: "First Name" not in d.find_element(By.TAG_NAME, "body").text
            )
        except TimeoutException:
            pass
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
            self.wait.until(EC.visibility_of_element_located(self.LICENSE_PLATE_INPUT))
            return True
        except TimeoutException:
            return False

    def rfid_field_is_visible(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.CAR_RFID_INPUT))
            return True
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
        # Give the form / iframe a moment to begin rendering before switching.
        time.sleep(1.0)
        self._switch_to_car_form_frame()
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
        self.wait_for_edit_loaded()

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

    def open_first_visible_edit(self):
        """Click the Edit button on the first visible table row and wait for the edit form."""
        row = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//table//tr[td]"))
        )
        edit_btn = row.find_element(
            By.XPATH, ".//button[.//*[normalize-space()='Edit']]"
        )
        self.driver.execute_script("arguments[0].click();", edit_btn)
        self.wait_for_edit_loaded()

    def car_row_visible(self, plate):
        try:
            self.wait.until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//table//tr[td and .//*[contains(normalize-space(),'%s')]]" % plate,
                ))
            )
            return True
        except TimeoutException:
            return False

    def get_car_row(self, plate):
        """Return the cars-list table row containing the given license plate."""
        return self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//table//tr[td and .//*[contains(normalize-space(),'%s')]]" % plate,
            ))
        )

    def car_row_has_text(self, plate, text):
        """Return True if the car row for the given plate contains specific text."""
        try:
            row = self.get_car_row(plate)
            return text.lower() in row.text.lower()
        except Exception:  # noqa: BLE001
            return False

    def _confirm_action_dialog(self):
        """Accept a Yes/Confirm dialog that may appear after a destructive action."""
        try:
            btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//*[@role='dialog']//button[normalize-space()='Yes'"
                    " or normalize-space()='Confirm'"
                    " or normalize-space()='OK']",
                ))
            )
            self.driver.execute_script("arguments[0].click();", btn)
        except TimeoutException:
            pass

    def blacklist_car_from_row(self, plate):
        """Click the Blacklist button on the car row for the given plate."""
        row = self.get_car_row(plate)
        btn = row.find_element(
            By.XPATH, ".//button[contains(normalize-space(),'Blacklist')]"
        )
        self.driver.execute_script("arguments[0].click();", btn)
        self._confirm_action_dialog()

    def deactivate_car_from_row(self, plate):
        """Click the Deactivate button on the car row for the given plate."""
        row = self.get_car_row(plate)
        btn = row.find_element(
            By.XPATH, ".//button[contains(normalize-space(),'Deactivate')]"
        )
        self.driver.execute_script("arguments[0].click();", btn)
        self._confirm_action_dialog()

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
            // React tracks the last-seen value via _valueTracker. If the tracker
            // already holds the current DOM value, React treats the dispatched
            // 'change' event as a no-op and submits the original value. Reset the
            // tracker to the current (old) value so React sees a real change.
            const tracker = input._valueTracker;
            if (tracker) { tracker.setValue(input.value); }
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
        self._wait_for_list_after_save()

    def create_customer(self, first_name, last_name, site, email=""):
        """Minimal create — required fields only. Use create_full_customer for all fields."""
        self.open_create_customer()
        self.fill_customer_form(first_name, last_name, site, email)
        self.ensure_active_switch_on()
        self.click_save_customer()
        self._wait_for_list_after_save()

    def _wait_for_list_after_save(self):
        """Wait for the customers list after a create/save.

        Staging sometimes doesn't auto-redirect within the default 45 s timeout.
        If that happens, check for a visible error on the form page first (e.g.
        duplicate email), then navigate explicitly to /customers so the list can
        load regardless.
        """
        try:
            self.wait_for_list_loaded()
            return
        except TimeoutException:
            pass
        # Before navigating away, surface any error the form is displaying.
        # This catches silent failures like "email already in use" that would
        # otherwise be lost when we redirect to /customers.
        form_error = self.get_visible_error()
        if form_error:
            raise RuntimeError(
                "Customer save rejected. Form shows: %s" % form_error[:300]
            ) from None
        # Explicit fallback: navigate to the list manually.
        current_url = self.driver.current_url
        base = "/".join(current_url.split("/")[:3])
        self.driver.get(base + "/customers")
        try:
            self.wait_for_list_loaded()
        except TimeoutException:
            error = self.get_visible_error()
            raise RuntimeError(
                "Customer save did not return to list. Page message: %s"
                % (error or "none visible")
            ) from None

    def click_download_button(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.DOWNLOAD_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
