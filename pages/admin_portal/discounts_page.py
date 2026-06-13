from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class DiscountsPage(BasePage):

    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/discounts?')]"
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

    def wait_for_list_loaded(self):
        """Wait until the Discounts list is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_DISCOUNT_BUTTON))

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
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.DISCOUNT_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_DISCOUNT_BUTTON))
        self.wait.until(lambda driver: self.get_discount_name_value() != "")

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
        self._set_input_value(search_input, discount_name)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == discount_name
        )

    def clear_discount_search(self):
        """Clear the discount search box."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        self._set_input_value(search_input, "")
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == ""
        )

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
        self.click(self.FILTER_BUTTON)
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

    def select_service_category(self, service_category, fallback=None):
        """Select discount service category from the React select."""
        combobox = self.wait.until(
            EC.element_to_be_clickable(self.SERVICE_CATEGORY_COMBOBOX)
        )
        combobox.click()

        option = self.find_select_option(service_category)

        if option is None and fallback is not None:
            option = self.find_select_option(fallback)

        if option is None:
            raise AssertionError(
                "Service category option was not found: %s" % service_category
            )

        self.driver.execute_script("arguments[0].click();", option)
        selected_label = fallback if fallback is not None else service_category
        self.wait.until(
            lambda driver: selected_label.lower() in self.get_body_text().lower()
        )

    def find_select_option(self, option_text):
        """Return a visible select option by case-insensitive text."""
        xpath = (
            "//*[@role='option' and translate(normalize-space(), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='%s']"
            % option_text.lower()
        )
        option_locator = (
            By.XPATH,
            xpath
        )

        try:
            return self.wait.until(
                lambda driver: self.get_clickable_option_after_scroll(xpath)
            )
        except TimeoutException:
            return None

    def get_clickable_option_after_scroll(self, option_xpath):
        """Return a select option, scrolling the open menu if needed."""
        options = self.driver.find_elements(By.XPATH, option_xpath)

        if options:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({ block: 'nearest' });",
                options[0]
            )
            if options[0].is_displayed() and options[0].is_enabled():
                return options[0]

        menus = self.driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'form-select__menu-list')]"
        )
        if menus:
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight;",
                menus[0]
            )

        options = self.driver.find_elements(By.XPATH, option_xpath)
        if options and options[0].is_displayed() and options[0].is_enabled():
            return options[0]

        return False

    def select_amount_discount_type(self):
        """Select Amount discount type."""
        radio = self.wait.until(EC.presence_of_element_located(self.AMOUNT_RADIO))
        if not radio.is_selected():
            radio.click()
            self.wait.until(
                lambda driver: driver.find_element(
                    *self.AMOUNT_RADIO
                ).is_selected()
            )

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
        discount_input.clear()
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
        option = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[@role='option' and translate(normalize-space(), "
                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='%s']"
                    % discount_type.lower()
                )
            )
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
                lambda driver: switch.get_attribute("aria-checked") == "true"
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
        self.wait.until(lambda driver: time_text in start_date.get_attribute("value"))

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
