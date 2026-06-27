import re

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class DiscountsPage(BasePage):

    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/discounts')"
        " and not(contains(@src,'/new'))"
        " and not(contains(@src,'/edit/'))]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/discounts/new')]"
    )
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/discounts/edit/')]"
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Discounts']")
    SEARCH_INPUT = (By.NAME, "discountName")
    FILTER_BUTTON = (By.XPATH, "//button[normalize-space()='Filter by']")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Filter by']/following-sibling::button[1]"
    )
    ADD_DISCOUNT_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='+ Add new discount']"
    )
    GRID_LOAD_MASK = (
        By.CSS_SELECTOR,
        ".inovua-react-toolkit-load-mask__background-layer"
    )
    SAVE_DISCOUNT_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save discount']"
    )
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']"
    )
    RESET_ALL_BUTTON = (By.XPATH, "//button[normalize-space()='Reset all']")
    FILTER_SITE_INPUT = (
        By.XPATH,
        "//*[normalize-space()='Select site']/following::input[1]"
    )
    ACTIVE_FILTER_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active discount']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    FILTER_RESULT_AMOUNT = (
        By.XPATH,
        "//*[contains(@class,'filterFooterAmount')]"
    )
    FILTER_OPTION = (
        By.XPATH,
        "//*[contains(@class,'select__option') and not(contains(@class,'No options'))]"
    )
    GRID_STATUS_CELLS = (By.XPATH, "//*[@data-props-id='isActive']")

    DISCOUNT_NAME_INPUT = (By.NAME, "discountName")
    SERVICE_CATEGORY_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='Select service category']"
        "/following::input[@role='combobox'][1]"
    )
    AMOUNT_RADIO = (
        By.XPATH,
        "//input[@name='discountTypeId' and @value='1']"
    )
    PERCENTAGE_RADIO = (
        By.XPATH,
        "//input[@name='discountTypeId' and @value='2']"
    )
    DISCOUNT_AMOUNT_INPUT = (By.NAME, "discountValue")
    DATE_INPUTS = (
        By.XPATH,
        "//input[@placeholder='Select date']"
    )
    ACTIVE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active service']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    ALL_LOCATIONS_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Allow discount at all locations']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    LOCATION_ROWS = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row') "
        "and .//*[contains(@class,'inovua-react-toolkit-checkbox')]]"
    )
    SELECTED_CATEGORY = (
        By.XPATH,
        "//*[normalize-space()='Select service category']"
        "/following::*[contains(@class,'form-select__single-value')][1]"
    )

    def wait_for_list_loaded(self):
        """Wait until the Discounts list is visible."""
        from selenium.webdriver.support.ui import WebDriverWait
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_DISCOUNT_BUTTON))
        self.wait_for_grid_idle()

    def wait_for_grid_idle(self):
        """Wait until the React grid load mask is not blocking interactions."""
        self.wait.until(
            lambda driver: not any(
                mask.is_displayed()
                for mask in driver.find_elements(*self.GRID_LOAD_MASK)
            )
        )

    def wait_for_create_loaded(self):
        """Wait until the create discount form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.DISCOUNT_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_DISCOUNT_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until the edit discount form is visible."""
        from selenium.webdriver.support.ui import WebDriverWait
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.DISCOUNT_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_DISCOUNT_BUTTON))
        WebDriverWait(self.driver, 30).until(
            lambda driver: self.get_discount_name_value() != ""
        )

    def get_body_text(self):
        """Get visible text inside the current iframe."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def _set_input_value(self, element, value):
        """Set a React-controlled input value and dispatch change events."""
        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype,
                'value'
            ).set;
            input.focus();
            setter.call(input, value);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            value
        )

    def get_discount_row_locator(self, discount_name):
        """Build a locator for a discount row by name."""
        return (
            By.XPATH,
            "//*[@data-props-id='discountName']"
            "[.//span[normalize-space()='%s']]"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
            % discount_name
        )

    def wait_for_discount_row(self, discount_name):
        """Wait until a discount row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_discount_row_locator(discount_name)
            )
        )

    def search_discount(self, discount_name):
        """Search discount by name."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_input.click()
        search_input.send_keys(Keys.COMMAND + "a")
        search_input.send_keys(Keys.BACKSPACE)
        search_input.send_keys(discount_name)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == discount_name
        )
        self.wait_for_grid_idle()

    def clear_discount_search(self):
        """Clear the discount search box."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_input.click()
        search_input.send_keys(Keys.COMMAND + "a")
        search_input.send_keys(Keys.BACKSPACE)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == ""
        )
        self.wait_for_grid_idle()

    def discount_exists(self, discount_name):
        """Return whether the discount exists in the list."""
        self.wait_for_list_loaded()
        self.search_discount(discount_name)

        try:
            self.wait_for_discount_row(discount_name)
            return True
        except TimeoutException:
            return False

    def get_discount_status(self, discount_name):
        """Return visible status for a discount row."""
        row = self.wait_for_discount_row(discount_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='isActive']"
        ).text.strip()

    def open_filter_panel(self):
        """Open the Discounts filter panel."""
        self.wait_for_list_loaded()
        btn = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.visibility_of_element_located(self.FILTER_SITE_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))

    def download_button_is_clickable(self):
        """Return whether the download button can be clicked."""
        return self.wait.until(
            EC.element_to_be_clickable(self.DOWNLOAD_BUTTON)
        ).is_displayed()

    def get_visible_discount_names(self):
        """Return visible discount names from the list grid."""
        cells = self.driver.find_elements(
            By.XPATH,
            "//*[@data-props-id='discountName']//span[normalize-space()]"
        )
        return [
            cell.text.strip()
            for cell in cells
            if cell.is_displayed() and cell.text.strip()
        ]

    def get_visible_discount_statuses(self):
        """Return visible discount status values (e.g. 'Active') from the grid."""
        return [
            cell.text.strip()
            for cell in self.driver.find_elements(*self.GRID_STATUS_CELLS)
            if cell.is_displayed() and cell.text.strip()
        ]

    def set_active_discount_filter(self, on):
        """Set the filter panel 'Active discount' switch to the desired state."""
        switch = self.wait.until(
            EC.presence_of_element_located(self.ACTIVE_FILTER_SWITCH)
        )
        desired = "true" if on else "false"
        if switch.get_attribute("aria-checked") != desired:
            self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(
                lambda driver: switch.get_attribute("aria-checked") == desired
            )

    def select_filter_site(self, site_name=None):
        """Pick a site in the filter panel (first option if name omitted).

        Returns the chosen site label, or None if no matching options appear.
        """
        from selenium.common.exceptions import TimeoutException as _TE
        box = self.wait.until(EC.element_to_be_clickable(self.FILTER_SITE_INPUT))
        self.driver.execute_script("arguments[0].click();", box)
        if site_name:
            box.send_keys(site_name)
            try:
                option = WebDriverWait(self.driver, 20).until(
                    lambda d: self._find_react_option(site_name)
                )
                label = option.text.strip()
                self.driver.execute_script("arguments[0].click();", option)
                return label
            except _TE:
                return None
        # No site_name given — click the first available option
        try:
            option = self.wait.until(EC.visibility_of_element_located(self.FILTER_OPTION))
            label = option.text.strip()
            self.driver.execute_script("arguments[0].click();", option)
            return label
        except _TE:
            return None

    def get_filter_result_count(self):
        """Return the live 'Filter result: N Discounts' count from the panel."""
        text = self.wait.until(
            EC.visibility_of_element_located(self.FILTER_RESULT_AMOUNT)
        ).text
        match = re.search(r"\d+", text)
        return int(match.group()) if match else 0

    def apply_filters(self):
        """Apply the configured filters and wait for the grid to refresh."""
        self.click(self.APPLY_FILTERS_BUTTON)
        self.wait.until(
            EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON)
        )
        self.wait_for_list_loaded()

    def reset_filters(self):
        """Open the filter panel and reset all filters back to defaults."""
        self.open_filter_panel()
        self.click(self.RESET_ALL_BUTTON)

    def open_create_discount(self):
        """Open create discount form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_DISCOUNT_BUTTON)
        self.wait_for_create_loaded()

    def open_edit_discount(self, discount_name):
        """Open edit discount form."""
        self.wait_for_list_loaded()
        self.search_discount(discount_name)

        for attempt in range(2):
            try:
                row = self.wait_for_discount_row(discount_name)
                edit_button = row.find_element(
                    By.XPATH,
                    ".//*[normalize-space()='Edit']/ancestor::a[1]"
                )
                self.driver.execute_script("arguments[0].click();", edit_button)
                break
            except StaleElementReferenceException:
                if attempt == 1:
                    raise
                self.search_discount(discount_name)

        self.wait_for_edit_loaded()

    def enter_discount_name(self, discount_name):
        """Enter discount name."""
        self.enter_text(self.DISCOUNT_NAME_INPUT, discount_name)

    def get_discount_name_value(self):
        """Return the current discount name input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.DISCOUNT_NAME_INPUT)
        )
        return element.get_attribute("value")

    def get_discount_name_validation_message(self):
        """Return native validation message for discount name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.DISCOUNT_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def discount_name_input_is_valid(self):
        """Return native validity state for discount name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.DISCOUNT_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def open_service_category_dropdown(self):
        """Click the service category combobox to open its dropdown."""
        combobox = self.wait.until(
            EC.element_to_be_clickable(self.SERVICE_CATEGORY_COMBOBOX)
        )
        combobox.click()

    def select_service_category(self, service_category, fallback=None):
        """Select discount service category from the React select."""
        self.open_service_category_dropdown()

        option = self.find_select_option(service_category)
        selected_label = service_category

        if option is None and fallback is not None:
            option = self.find_select_option(fallback)
            selected_label = fallback

        if option is None:
            raise AssertionError(
                "Service category option was not found: %s" % service_category
            )

        self.driver.execute_script("arguments[0].click();", option)
        self.wait.until(
            lambda driver: (
                (body := self.get_body_text()) is not None
                and selected_label.lower() in body.lower()
            )
        )

    def find_select_option(self, option_text):
        """Return a visible React Select option by case-insensitive text."""
        try:
            return self.wait.until(
                lambda d: self._find_react_option(option_text)
            )
        except Exception:
            return None

    def _is_radio_selected(self, locator):
        try:
            return self.driver.find_element(*locator).is_selected()
        except StaleElementReferenceException:
            return False

    def select_amount_discount_type(self):
        """Select Amount discount type."""
        radio = self.wait.until(EC.presence_of_element_located(self.AMOUNT_RADIO))
        if not radio.is_selected():
            self.driver.execute_script("arguments[0].click();", radio)
            self.wait.until(lambda driver: self._is_radio_selected(self.AMOUNT_RADIO))

    def amount_discount_type_is_selected(self):
        """Return whether Amount discount type is selected."""
        radio = self.wait.until(EC.presence_of_element_located(self.AMOUNT_RADIO))
        return radio.is_selected()

    def set_discount_amount(self, amount):
        """Set discount amount."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.DISCOUNT_AMOUNT_INPUT)
        )
        element.clear()
        element.send_keys(str(amount))
        self.wait.until(
            lambda driver: driver.find_element(
                *self.DISCOUNT_AMOUNT_INPUT
            ).get_attribute("value") == str(amount)
        )

    def get_discount_amount_value(self):
        """Return discount amount input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.DISCOUNT_AMOUNT_INPUT)
        )
        return element.get_attribute("value")

    def set_location_discount_value_by_index(self, row_index, value):
        """Set one visible location row discount value."""
        rows = self.get_location_rows()

        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (row_index + 1, len(rows))
            )

        discount_input = rows[row_index].find_element(By.NAME, "discountValue")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", discount_input
        )
        discount_input.send_keys(Keys.COMMAND + "a")
        discount_input.send_keys(Keys.BACKSPACE)
        discount_input.send_keys(str(value))
        self.wait.until(
            lambda driver: rows[row_index].find_element(
                By.NAME,
                "discountValue"
            ).get_attribute("value") == str(value)
        )

    def select_location_discount_type_by_index(self, row_index, discount_type):
        """Select one visible location row discount type."""
        rows = self.get_location_rows()

        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (row_index + 1, len(rows))
            )

        row = rows[row_index]
        combobox = row.find_element(By.XPATH, ".//input[@role='combobox']")
        combobox.click()
        combobox.send_keys(discount_type)
        option = WebDriverWait(self.driver, 20).until(
            lambda d: self._find_react_option(discount_type)
        )
        self.driver.execute_script("arguments[0].click();", option)
        self.wait.until(
            lambda driver: discount_type.lower()
            in self.get_location_rows()[row_index].text.lower()
        )

    def get_location_rows(self):
        """Return unique visible location assignment rows."""
        rows = self.wait.until(
            EC.presence_of_all_elements_located(self.LOCATION_ROWS)
        )
        unique_rows = []
        seen_locations = set()

        for row in rows:
            lines = [
                line.strip()
                for line in row.text.splitlines()
                if line.strip()
            ]
            location_key = "\n".join(lines[:2])

            if not location_key or location_key in seen_locations:
                continue

            seen_locations.add(location_key)
            unique_rows.append(row)

        return unique_rows

    def row_checkbox_is_checked(self, checkbox):
        """Return whether an Inovua checkbox is checked."""
        classes = checkbox.get_attribute("class")
        return (
            "inovua-react-toolkit-checkbox--checked" in classes
            and "inovua-react-toolkit-checkbox--unchecked" not in classes
        )

    def assign_location_by_index(self, row_index):
        """Assign one visible location row."""
        rows = self.get_location_rows()

        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (row_index + 1, len(rows))
            )

        checkbox = rows[row_index].find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox') "
            "and contains(@class,'InovuaReactDataGrid__checkbox')]"
        )

        if not self.row_checkbox_is_checked(checkbox):
            self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(lambda driver: self.row_checkbox_is_checked(checkbox))

    def location_is_assigned_by_index(self, row_index):
        """Return whether one visible location row is assigned."""
        rows = self.get_location_rows()
        checkbox = rows[row_index].find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox') "
            "and contains(@class,'InovuaReactDataGrid__checkbox')]"
        )
        return self.row_checkbox_is_checked(checkbox)

    def get_location_discount_value_by_index(self, row_index):
        """Return one visible location row discount value."""
        rows = self.get_location_rows()
        return rows[row_index].find_element(
            By.NAME,
            "discountValue"
        ).get_attribute("value")

    def fill_required_unassigned_location_values(self):
        """Fill required discount values for unassigned locations."""
        for row_index in range(1, len(self.get_location_rows())):
            self.set_location_discount_value_by_index(row_index, "0")
            self.select_location_discount_type_by_index(row_index, "Amount")

    def switch_is_on(self, locator):
        """Return whether a switch is on."""
        switch = self.wait.until(EC.presence_of_element_located(locator))
        return switch.get_attribute("aria-checked") == "true"

    def ensure_switch_on(self, locator):
        """Turn a switch on if needed."""
        switch = self.wait.until(EC.presence_of_element_located(locator))
        if switch.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(
                lambda driver: driver.find_element(
                    *locator
                ).get_attribute("aria-checked") == "true"
            )

    def active_switch_is_on(self):
        """Return whether Active service switch is on."""
        return self.switch_is_on(self.ACTIVE_SWITCH)

    def all_locations_switch_is_on(self):
        """Return whether Allow discount at all locations switch is on."""
        return self.switch_is_on(self.ALL_LOCATIONS_SWITCH)

    def ensure_active_switch_on(self):
        """Turn Active service on if needed."""
        self.ensure_switch_on(self.ACTIVE_SWITCH)

    def ensure_all_locations_switch_on(self):
        """Turn Allow discount at all locations on if needed."""
        self.ensure_switch_on(self.ALL_LOCATIONS_SWITCH)

    def set_discount_start(self, day, time_text):
        """Set discount start date in the visible date picker."""
        start_date = self.wait.until(
            EC.element_to_be_clickable(self.DATE_INPUTS)
        )
        start_date.click()

        day_locator = (
            By.XPATH,
            "//div[contains(@class,'react-datepicker__day--%03d') "
            "and not(contains(@class,'outside-month'))]"
            % int(day)
        )
        self.wait.until(EC.element_to_be_clickable(day_locator)).click()

        time_locator = (
            By.XPATH,
            "//li[contains(@class,'react-datepicker__time-list-item') "
            "and normalize-space()='%s']"
            % time_text
        )
        self.wait.until(EC.element_to_be_clickable(time_locator)).click()
        start_date.send_keys(Keys.ESCAPE)
        self.wait.until(
            lambda driver: time_text in self._get_date_input_by_index(0).get_attribute("value")
        )

    def get_discount_start_value(self):
        """Return discount start date value."""
        start_date = self.wait.until(
            EC.visibility_of_element_located(self.DATE_INPUTS)
        )
        return start_date.get_attribute("value")

    def click_save_discount(self):
        """Click save discount."""
        button = self.wait.until(
            EC.element_to_be_clickable(self.SAVE_DISCOUNT_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def fill_discount_form(
        self,
        discount_name,
        service_category,
        discount_amount,
        start_day,
        start_time,
        service_category_fallback=None
    ):
        """Fill the discount form with the requested active amount discount."""
        self.enter_discount_name(discount_name)
        self.select_service_category(service_category, service_category_fallback)
        self.select_amount_discount_type()
        self.set_discount_amount(discount_amount)
        self.set_discount_start(start_day, start_time)
        self.ensure_active_switch_on()
        self.set_location_discount_value_by_index(0, discount_amount)
        self.select_location_discount_type_by_index(0, "Amount")
        self.fill_required_unassigned_location_values()
        self.assign_location_by_index(0)

    def create_discount(
        self,
        discount_name,
        service_category,
        discount_amount,
        start_day,
        start_time,
        service_category_fallback=None
    ):
        """Create an active all-location amount discount and return to list."""
        self.open_create_discount()
        self.fill_discount_form(
            discount_name,
            service_category,
            discount_amount,
            start_day,
            start_time,
            service_category_fallback
        )
        self.click_save_discount()
        self.wait_for_list_loaded()

    def update_discount(
        self,
        discount_name,
        service_category,
        discount_amount,
        start_day,
        start_time,
        service_category_fallback=None
    ):
        """Update an existing discount and return to list."""
        self.open_edit_discount(discount_name)
        self.fill_discount_form(
            discount_name,
            service_category,
            discount_amount,
            start_day,
            start_time,
            service_category_fallback
        )
        self.click_save_discount()
        self.wait_for_list_loaded()

    def select_percentage_discount_type(self):
        """Select Percentage discount type."""
        radio = self.wait.until(EC.presence_of_element_located(self.PERCENTAGE_RADIO))
        if not radio.is_selected():
            self.driver.execute_script("arguments[0].click();", radio)
            self.wait.until(lambda driver: self._is_radio_selected(self.PERCENTAGE_RADIO))

    def percentage_discount_type_is_selected(self):
        """Return whether Percentage discount type is selected."""
        radio = self.wait.until(EC.presence_of_element_located(self.PERCENTAGE_RADIO))
        return radio.is_selected()

    def ensure_active_switch_off(self):
        """Turn Active service switch off if needed."""
        switch = self.wait.until(EC.presence_of_element_located(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") == "true":
            self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(
                lambda driver: driver.find_element(
                    *self.ACTIVE_SWITCH
                ).get_attribute("aria-checked") == "false"
            )

    def ensure_all_locations_switch_off(self):
        """Turn Allow discount at all locations switch off if needed."""
        switch = self.wait.until(
            EC.presence_of_element_located(self.ALL_LOCATIONS_SWITCH)
        )
        if switch.get_attribute("aria-checked") == "true":
            self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(
                lambda driver: driver.find_element(
                    *self.ALL_LOCATIONS_SWITCH
                ).get_attribute("aria-checked") == "false"
            )

    def _get_date_input_by_index(self, index):
        """Return a date input element by zero-based index."""
        inputs = self.wait.until(
            EC.presence_of_all_elements_located(self.DATE_INPUTS)
        )
        if index >= len(inputs):
            raise AssertionError(
                "Expected at least %d date inputs, found %d" % (index + 1, len(inputs))
            )
        return inputs[index]

    def set_discount_end(self, day, time_text):
        """Set discount end date in the second date picker."""
        end_date = self._get_date_input_by_index(1)
        self.driver.execute_script("arguments[0].click();", end_date)
        day_locator = (
            By.XPATH,
            "//div[contains(@class,'react-datepicker__day--%03d') "
            "and not(contains(@class,'outside-month'))]"
            % int(day)
        )
        self.wait.until(EC.element_to_be_clickable(day_locator)).click()
        time_locator = (
            By.XPATH,
            "//li[contains(@class,'react-datepicker__time-list-item') "
            "and normalize-space()='%s']"
            % time_text
        )
        self.wait.until(EC.element_to_be_clickable(time_locator)).click()
        end_date.send_keys(Keys.ESCAPE)
        self.wait.until(lambda driver: time_text in end_date.get_attribute("value"))

    def get_discount_end_value(self):
        """Return discount end date input value."""
        return self._get_date_input_by_index(1).get_attribute("value")

    def get_selected_service_category(self):
        """Return the currently selected service category label."""
        return self.wait.until(
            EC.visibility_of_element_located(self.SELECTED_CATEGORY)
        ).text.strip()

    def click_download_button(self):
        """Click the export/download button."""
        self.wait.until(EC.element_to_be_clickable(self.DOWNLOAD_BUTTON)).click()

    def fill_percentage_discount_form(
        self,
        discount_name,
        service_category,
        discount_amount,
        start_day,
        start_time,
        service_category_fallback=None
    ):
        """Fill the discount form for a percentage discount."""
        self.enter_discount_name(discount_name)
        self.select_service_category(service_category, service_category_fallback)
        self.select_percentage_discount_type()
        self.set_discount_amount(discount_amount)
        self.set_discount_start(start_day, start_time)
        self.ensure_active_switch_on()
        self.set_location_discount_value_by_index(0, discount_amount)
        self.select_location_discount_type_by_index(0, "Percentage")
        self.fill_required_unassigned_location_values()
        self.assign_location_by_index(0)

    def create_percentage_discount(
        self,
        discount_name,
        service_category,
        discount_amount,
        start_day,
        start_time,
        service_category_fallback=None
    ):
        """Create a percentage discount and return to list."""
        self.open_create_discount()
        self.fill_percentage_discount_form(
            discount_name,
            service_category,
            discount_amount,
            start_day,
            start_time,
            service_category_fallback
        )
        self.click_save_discount()
        self.wait_for_list_loaded()

    def fill_discount_form_all_locations(
        self,
        discount_name,
        service_category,
        discount_amount,
        start_day,
        start_time,
        service_category_fallback=None
    ):
        """Fill the discount form targeting all locations."""
        self.enter_discount_name(discount_name)
        self.select_service_category(service_category, service_category_fallback)
        self.select_amount_discount_type()
        self.set_discount_amount(discount_amount)
        self.set_discount_start(start_day, start_time)
        self.ensure_active_switch_on()
        self.ensure_all_locations_switch_on()

    def create_discount_all_locations(
        self,
        discount_name,
        service_category,
        discount_amount,
        start_day,
        start_time,
        service_category_fallback=None
    ):
        """Create an all-locations amount discount and return to list."""
        self.open_create_discount()
        self.fill_discount_form_all_locations(
            discount_name,
            service_category,
            discount_amount,
            start_day,
            start_time,
            service_category_fallback
        )
        self.click_save_discount()
        self.wait_for_list_loaded()

    def unassign_location_by_index(self, row_index):
        """Unassign one visible location row (uncheck if currently checked)."""
        rows = self.get_location_rows()
        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (row_index + 1, len(rows))
            )
        checkbox = rows[row_index].find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox') "
            "and contains(@class,'InovuaReactDataGrid__checkbox')]"
        )
        if self.row_checkbox_is_checked(checkbox):
            self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(lambda driver: not self.row_checkbox_is_checked(checkbox))
