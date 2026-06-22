from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class WashExtrasPage(BasePage):

    FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/washExtras')]"
    )
    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/washExtras?')]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/washExtras/new')]"
    )
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/washExtras/') "
        "and not(contains(@src,'/services/washExtras/new'))]"
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Wash extras']")
    SEARCH_INPUT = (By.NAME, "serviceName")
    # The button text includes a live filter count, e.g. "Filter by (1)".
    # Use contains() so it matches regardless of the count suffix.
    FILTER_BUTTON = (
        By.XPATH,
        "//button[contains("
        "translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"
        ",'filter by')]"
    )
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Filter by']/following-sibling::button[1]"
    )
    ADD_EXTRA_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='+ Add new wash extra']"
    )
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']"
    )
    RESET_ALL_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Reset all')]")
    FILTER_SITE_INPUT = (
        By.XPATH,
        "//*[normalize-space()='Select site']/following::input[1]"
    )

    SAVE_EXTRA_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save wash extra']"
    )
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    SERVICE_NAME_INPUT = (By.NAME, "serviceName")
    BARCODE_INPUT = (By.NAME, "barcode")
    POINTS_AWARDED_INPUT = (By.NAME, "pointsAwarded")
    POINTS_REDEEMED_INPUT = (By.NAME, "pointsRedeemed")
    GLOBAL_PRICE_INPUT = (By.NAME, "servicePrice")
    GLOBAL_COMMISSION_INPUTS = (By.NAME, "commission")
    ACTIVE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active service']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    DISCOUNT_SETTINGS_TAB = (
        By.XPATH,
        "//button[@role='tab' and normalize-space()='Discount settings']"
    )
    SERVICE_SETTINGS_TAB = (
        By.XPATH,
        "//button[@role='tab' and normalize-space()='Service settings']"
    )
    APPLICABLE_DISCOUNTS_TITLE = (
        By.XPATH,
        "//*[normalize-space()='Applicable discounts']"
    )
    DISCOUNTS_COMBOBOX = (
        By.XPATH,
        "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
        "//input[@role='combobox']"
    )
    LOCATION_ROWS = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row') "
        "and .//*[contains(@class,'inovua-react-toolkit-checkbox')]]"
    )

    def wait_for_list_loaded(self):
        """Wait until the Wash Extras list is visible."""
        long_wait = WebDriverWait(self.driver, 30)
        self.driver.switch_to.default_content()
        long_wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_EXTRA_BUTTON))

    def wait_for_create_loaded(self):
        """Wait until the create extra form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.SERVICE_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_EXTRA_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until the edit extra form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME))
        self.wait.until(EC.visibility_of_element_located(self.SERVICE_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_EXTRA_BUTTON))
        self.wait.until(lambda driver: self.get_service_name_value() != "")

    def get_body_text(self):
        """Get visible text inside the current iframe."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_extra_row_locator(self, extra_name):
        """Build a locator for a wash extra row by service name."""
        return (
            By.XPATH,
            "//*[@data-props-id='serviceName']"
            "[.//span[normalize-space()='%s']]"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
            % extra_name
        )

    def wait_for_extra_row(self, extra_name):
        """Wait until an extra row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_extra_row_locator(extra_name)
            )
        )

    def extra_exists(self, extra_name):
        """Return whether the wash extra exists in the list."""
        self.wait_for_list_loaded()
        self.search_extra(extra_name)

        try:
            self.wait_for_extra_row(extra_name)
            return True
        except TimeoutException:
            return False

    def search_extra(self, extra_name):
        """Search wash extra by service name."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )
        self._set_input_value(element, extra_name)
        self.wait.until(
            lambda driver: self.driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == extra_name
        )

    def get_extra_price(self, extra_name):
        """Return visible price for a wash extra row."""
        row = self.wait_for_extra_row(extra_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='servicePrice']"
        ).text.strip()

    def get_extra_status(self, extra_name):
        """Return visible status for a wash extra row."""
        row = self.wait_for_extra_row(extra_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='isActive']"
        ).text.strip()

    def open_filter_panel(self):
        """Open the Wash Extras filter panel."""
        self.wait_for_list_loaded()
        button = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)
        self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))

    def download_button_is_clickable(self):
        """Return whether the download button can be clicked."""
        button = self.wait.until(EC.presence_of_element_located(self.DOWNLOAD_BUTTON))
        return button.is_displayed()

    def open_create_extra(self):
        """Open create wash extra form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_EXTRA_BUTTON)
        self.wait_for_create_loaded()

    def open_edit_extra(self, extra_name):
        """Open edit wash extra form."""
        self.wait_for_list_loaded()
        self.search_extra(extra_name)
        row = self.wait_for_extra_row(extra_name)
        edit_button = row.find_element(
            By.XPATH,
            ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        edit_button.click()
        self.wait_for_edit_loaded()

    def enter_service_name(self, service_name):
        """Enter wash extra service name."""
        self.enter_text(self.SERVICE_NAME_INPUT, service_name)

    def get_service_name_value(self):
        """Return the current wash extra service name input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.SERVICE_NAME_INPUT)
        )
        return element.get_attribute("value")

    def get_service_name_validation_message(self):
        """Return native validation message for service name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.SERVICE_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def service_name_input_is_valid(self):
        """Return native validity state for service name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.SERVICE_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def active_switch_is_on(self):
        """Return whether active switch is checked."""
        switch = self.wait.until(
            EC.presence_of_element_located(self.ACTIVE_SWITCH)
        )
        return switch.get_attribute("aria-checked") == "true"

    def ensure_active_switch_on(self):
        """Turn active switch on if needed."""
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))

        if switch.get_attribute("aria-checked") != "true":
            switch.click()
            self.wait.until(
                lambda driver: switch.get_attribute("aria-checked") == "true"
            )

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

    def set_global_price(self, price):
        """Set wash extra global price."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        self._set_input_value(element, str(price))

    def get_global_price_value(self):
        """Return wash extra global price input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return element.get_attribute("value")

    def set_global_commission(self, commission):
        """Set wash extra global commission."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        self._set_input_value(elements[0], str(commission))

    def get_global_commission_value(self):
        """Return wash extra global commission input value."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        return elements[0].get_attribute("value")

    def open_service_settings(self):
        """Open Service settings tab."""
        self.click(self.SERVICE_SETTINGS_TAB)
        self.wait.until(EC.visibility_of_element_located(self.SERVICE_NAME_INPUT))

    def open_discount_settings(self):
        """Open Discount settings tab."""
        tab = self.wait.until(
            EC.presence_of_element_located(self.DISCOUNT_SETTINGS_TAB)
        )
        self.driver.execute_script("arguments[0].click();", tab)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(self.DISCOUNTS_COMBOBOX)
        )

    def get_selected_discount_locator(self, discount_name):
        """Build a locator for a selected discount chip label."""
        normalized_name = discount_name.lower()
        return (
            By.XPATH,
            "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
            "//*[contains(@class,'form-select__multi-value__label') "
            "and translate(normalize-space(), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='%s']"
            % normalized_name
        )

    def discount_is_selected(self, discount_name):
        """Return whether a discount is selected in Discount settings."""
        return len(
            self.driver.find_elements(
                *self.get_selected_discount_locator(discount_name)
            )
        ) > 0

    def select_applicable_discount(self, discount_name):
        """Select a discount if it is not already selected."""
        if self.discount_is_selected(discount_name):
            return

        self.select_react_dropdown_option(
            self.DISCOUNTS_COMBOBOX, discount_name, clear_first=False
        )
        self.wait.until(
            EC.visibility_of_element_located(
                self.get_selected_discount_locator(discount_name)
            )
        )

    def get_selected_discount_names(self):
        """Return selected discount chip names in Discount settings."""
        labels = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
            "//*[contains(@class,'form-select__multi-value__label')]"
        )
        return [label.text.strip() for label in labels if label.text.strip()]

    def remove_selected_discount(self, discount_name):
        """Remove a selected discount chip if present."""
        if not self.discount_is_selected(discount_name):
            return

        chip_label = self.wait.until(
            EC.visibility_of_element_located(
                self.get_selected_discount_locator(discount_name)
            )
        )
        remove_button = chip_label.find_element(
            By.XPATH,
            "./following-sibling::*"
            "[contains(@class,'form-select__multi-value__remove')]"
        )
        self.driver.execute_script("arguments[0].click();", remove_button)
        self.wait.until(lambda driver: not self.discount_is_selected(discount_name))

    def replace_applicable_discount(self, old_discount_name, new_discount_name):
        """Replace one applicable discount with another."""
        self.remove_selected_discount(old_discount_name)
        self.select_applicable_discount(new_discount_name)

    def get_location_rows(self):
        """Return unique visible location assignment rows.

        Waits for rows that are both visible (non-zero rect) AND have their
        price input mounted, so child find_element calls don't raise
        NoSuchElementException on partially-rendered rows.
        """
        long_wait = WebDriverWait(self.driver, 30)
        long_wait.until(
            EC.presence_of_all_elements_located(self.LOCATION_ROWS)
        )
        long_wait.until(
            lambda driver: any(
                row.find_elements(By.NAME, "price")
                for row in self.driver.find_elements(*self.LOCATION_ROWS)
                if row.rect["height"] > 0
            )
        )
        return [
            row
            for row in self.driver.find_elements(*self.LOCATION_ROWS)
            if row.rect["height"] > 0 and row.find_elements(By.NAME, "price")
        ]

    def row_checkbox_is_checked(self, checkbox):
        """Return whether an Inovua checkbox is checked."""
        classes = checkbox.get_attribute("class")
        return (
            "inovua-react-toolkit-checkbox--checked" in classes
            and "inovua-react-toolkit-checkbox--unchecked" not in classes
        )

    def assign_location_row_with_price_and_commission(
        self,
        row,
        price,
        commission
    ):
        """Assign one location row and set row-level price/commission."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", row)
        checkbox = row.find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
        )

        if not self.row_checkbox_is_checked(checkbox):
            self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(lambda driver: self.row_checkbox_is_checked(checkbox))

        price_input = row.find_element(By.NAME, "price")
        commission_input = row.find_element(By.NAME, "commission")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            price_input
        )
        self._set_input_value(price_input, str(price))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            commission_input
        )
        self._set_input_value(commission_input, str(commission))

    def assign_all_locations_with_price_and_commission(self, price, commission):
        """Assign all visible locations and set price/commission for each."""
        rows = self.get_location_rows()

        for row in rows:
            self.assign_location_row_with_price_and_commission(
                row,
                price,
                commission
            )

    def _numeric_matches(self, element, value):
        """Return True if the element's value equals value numerically (handles "10.00" == "10")."""
        current = element.get_attribute("value") or ""
        try:
            return float(current) == float(str(value))
        except ValueError:
            return current == str(value)

    def set_location_price_by_index(self, row_index, price):
        """Set one visible location row price by zero-based row index.

        Uses send_keys instead of _set_input_value so React's synthetic event
        system registers the keystroke and the value persists on save.
        """
        from selenium.webdriver.common.keys import Keys

        rows = self.get_location_rows()

        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (row_index + 1, len(rows))
            )

        row = rows[row_index]
        self.driver.execute_script("arguments[0].scrollIntoView(true);", row)
        checkbox = row.find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
        )

        if not self.row_checkbox_is_checked(checkbox):
            self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(lambda driver: self.row_checkbox_is_checked(checkbox))

        price_input = row.find_element(By.NAME, "price")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});"
            "arguments[0].focus();",
            price_input
        )
        price_input.send_keys(Keys.COMMAND, "a")
        price_input.send_keys(Keys.BACKSPACE)
        price_input.send_keys(str(price))
        self.driver.execute_script(
            """
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            price_input
        )
        # If send_keys didn't set the value, fall back to the JS setter.
        try:
            WebDriverWait(self.driver, 3).until(
                lambda driver: self._numeric_matches(price_input, price)
            )
        except TimeoutException:
            self._set_input_value(price_input, str(price))
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));",
                price_input
            )
        WebDriverWait(self.driver, 30).until(
            lambda driver: self._numeric_matches(price_input, price)
        )

    def get_location_price_by_index(self, row_index):
        """Return one visible location row price by zero-based row index."""
        rows = self.get_location_rows()

        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (row_index + 1, len(rows))
            )

        price_input = rows[row_index].find_element(By.NAME, "price")
        WebDriverWait(self.driver, 30).until(
            lambda driver: price_input.get_attribute("value") != ""
        )
        return price_input.get_attribute("value")

    def all_locations_are_assigned_with_price_and_commission(
        self,
        price,
        commission
    ):
        """Return whether visible location rows match expected assignment data."""
        for row in self.get_location_rows():
            checkbox = row.find_element(
                By.XPATH,
                ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
            )
            price_input = row.find_element(By.NAME, "price")
            commission_input = row.find_element(By.NAME, "commission")

            if not self.row_checkbox_is_checked(checkbox):
                return False

            if price_input.get_attribute("value") != str(price):
                return False

            if commission_input.get_attribute("value") != str(commission):
                return False

        return True

    def fill_extra_form(self, service_name, global_price, global_commission):
        """Fill service settings fields for a wash extra."""
        self.enter_service_name(service_name)
        self.ensure_active_switch_on()
        self.set_global_price(global_price)
        self.set_global_commission(global_commission)
        self.assign_all_locations_with_price_and_commission(
            global_price,
            global_commission
        )

    def click_save_extra(self):
        """Click save wash extra."""
        self.click(self.SAVE_EXTRA_BUTTON)

    def click_cancel(self):
        """Cancel create/edit wash extra."""
        self.click(self.CANCEL_BUTTON)

    def create_extra(
        self,
        service_name,
        global_price,
        global_commission,
        discount_name
    ):
        """Create an active wash extra and return to the list."""
        self.open_create_extra()
        self.fill_extra_form(service_name, global_price, global_commission)
        self.open_discount_settings()
        self.select_applicable_discount(discount_name)
        self.click_save_extra()
        self.wait_for_list_loaded()

    def ensure_active_switch_off(self):
        """Turn the active switch off if needed."""
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") == "true":
            switch.click()
            self.wait.until(
                lambda driver: switch.get_attribute("aria-checked") != "true"
            )

    def clear_extra_search(self):
        """Clear the wash extra search field."""
        element = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
        self._set_input_value(element, "")

    def apply_filters(self):
        """Click Apply filters."""
        self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON)).click()

    def reset_filters(self):
        """Click Reset all to clear active filters."""
        self.wait.until(EC.element_to_be_clickable(self.RESET_ALL_BUTTON)).click()

    def set_filter_site(self, site_name):
        """Type a site name into the filter panel and select the matching option."""
        self.select_react_dropdown_option(self.FILTER_SITE_INPUT, site_name)

    def get_visible_extra_names(self):
        """Return a list of all visible wash extra names in the grid."""
        elements = self.driver.find_elements(
            By.XPATH,
            "//*[@data-props-id='serviceName']//span[normalize-space()]"
        )
        return [el.text.strip() for el in elements if el.text.strip()]

    def enter_barcode(self, barcode):
        """Enter a barcode value."""
        element = self.wait.until(EC.visibility_of_element_located(self.BARCODE_INPUT))
        self._set_input_value(element, str(barcode))

    def get_barcode_value(self):
        """Return the current barcode input value."""
        element = self.wait.until(EC.visibility_of_element_located(self.BARCODE_INPUT))
        return element.get_attribute("value")

    def set_points_awarded(self, points):
        """Set the loyalty points awarded value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_AWARDED_INPUT)
        )
        self._set_input_value(element, str(points))

    def get_points_awarded_value(self):
        """Return the loyalty points awarded input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_AWARDED_INPUT)
        )
        return element.get_attribute("value")

    def set_points_to_redeem(self, points):
        """Set the loyalty points to redeem value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_REDEEMED_INPUT)
        )
        self._set_input_value(element, str(points))

    def get_points_to_redeem_value(self):
        """Return the loyalty points to redeem input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_REDEEMED_INPUT)
        )
        return element.get_attribute("value")

    def set_location_commission_by_index(self, row_index, commission):
        """Set one visible location row commission by zero-based index."""
        rows = self.get_location_rows()
        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (row_index + 1, len(rows))
            )
        row = rows[row_index]
        self.driver.execute_script("arguments[0].scrollIntoView(true);", row)
        checkbox = row.find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
        )
        if not self.row_checkbox_is_checked(checkbox):
            self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(lambda driver: self.row_checkbox_is_checked(checkbox))
        commission_input = row.find_element(By.NAME, "commission")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            commission_input
        )
        self._set_input_value(commission_input, str(commission))
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));",
            commission_input
        )
        # Short confirmation — invalid inputs (e.g. negative) may be rejected
        # by the browser, so we don't block if the value doesn't match.
        try:
            WebDriverWait(self.driver, 3).until(
                lambda driver: commission_input.get_attribute("value") == str(commission)
            )
        except TimeoutException:
            pass

    def get_location_commission_by_index(self, row_index):
        """Return one visible location row commission by zero-based index."""
        rows = self.get_location_rows()
        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (row_index + 1, len(rows))
            )
        commission_input = rows[row_index].find_element(By.NAME, "commission")
        WebDriverWait(self.driver, 30).until(
            lambda driver: commission_input.get_attribute("value") != ""
        )
        return commission_input.get_attribute("value")

    def assign_all_locations_via_header_checkbox(self):
        """Click the 'Assign to' header checkbox to select all location rows at once."""
        header_checkbox = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'InovuaReactDataGrid__header')]"
                    "//*[contains(@class,'inovua-react-toolkit-checkbox')]"
                )
            )
        )
        self.driver.execute_script("arguments[0].click();", header_checkbox)
        self.wait.until(
            lambda driver: self.all_location_rows_are_assigned()
        )

    def all_location_rows_are_assigned(self):
        """Return True if every visible location row is checked."""
        for row in self.get_location_rows():
            checkbox = row.find_element(
                By.XPATH,
                ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
            )
            if not self.row_checkbox_is_checked(checkbox):
                return False
        return True

    def global_price_input_is_valid(self):
        """Return the native validity state of the global price input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def get_global_price_validation_message(self):
        """Return the native validation message for the global price input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def location_price_input_is_valid_by_index(self, row_index):
        """Return the native validity state of a location price input by index."""
        rows = self.get_location_rows()
        price_input = rows[row_index].find_element(By.NAME, "price")
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            price_input
        )

    def get_selected_discount_count(self):
        """Return how many discounts are currently selected in Discount settings."""
        labels = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
            "//*[contains(@class,'form-select__multi-value__label')]"
        )
        return len([lb for lb in labels if lb.text.strip()])

    def discount_dropdown_options(self):
        """Return a list of discount option texts visible in the open dropdown."""
        options = self.driver.find_elements(
            By.XPATH,
            "//*[@role='option']"
        )
        return [opt.text.strip() for opt in options if opt.text.strip()]

    def remove_applicable_discount(self, discount_name):
        """Remove a selected discount chip by name."""
        self.remove_selected_discount(discount_name)

    def update_extra_name_location_prices_and_discount(
        self,
        old_name,
        new_name,
        first_location_price,
        second_location_price,
        old_discount_name,
        new_discount_name
    ):
        """Update wash extra name, first two location prices, and discount."""
        self.open_edit_extra(old_name)
        self.enter_service_name(new_name)
        self.ensure_active_switch_on()
        self.set_location_price_by_index(0, first_location_price)
        self.set_location_price_by_index(1, second_location_price)
        self.open_discount_settings()
        self.replace_applicable_discount(old_discount_name, new_discount_name)
        self.click_save_extra()
        self.wait_for_list_loaded()
