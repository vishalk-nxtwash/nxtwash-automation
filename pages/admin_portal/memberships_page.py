from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class MembershipsPage(BasePage):

    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/memberships?')]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/memberships/new')]"
    )
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/memberships/') "
        "and not(contains(@src,'/services/memberships/new'))]"
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Memberships']")
    SEARCH_INPUT = (By.NAME, "membershipName")
    FILTER_BUTTON = (By.XPATH, "//button[normalize-space()='Filter by']")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Filter by']/following-sibling::button[1]"
    )
    ADD_MEMBERSHIP_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='+ Add new membership']"
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

    SAVE_MEMBERSHIP_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save membership']"
    )
    MEMBERSHIP_SETTINGS_TAB = (
        By.XPATH,
        "//button[@role='tab' and normalize-space()='Membership settings']"
    )
    REDEMPTION_SETTINGS_TAB = (
        By.XPATH,
        "//button[@role='tab' and normalize-space()='Redemption settings']"
    )
    DISCOUNT_SETTINGS_TAB = (
        By.XPATH,
        "//button[@role='tab' and normalize-space()='Discount settings']"
    )
    MEMBERSHIP_NAME_INPUT = (By.NAME, "membershipName")
    PREPAID_RADIO = (
        By.XPATH,
        "//input[@name='isRecurring' and @value='prepaid']"
    )
    PREPAID_LABEL = (
        By.XPATH,
        "//*[normalize-space()='Prepaid']"
    )
    RECURRING_RADIO = (
        By.XPATH,
        "//input[@name='isRecurring' and @value='recurring']"
    )
    GLOBAL_PRICE_INPUT = (By.NAME, "membershipPrice")
    GLOBAL_COMMISSION_INPUTS = (By.NAME, "commission")
    PREPAID_MONTHS_INPUT = (By.NAME, "prepaidMonths")
    POINTS_AWARDED_INPUT = (By.NAME, "pointsAwarded")
    ACTIVE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active service']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    CUSTOMER_PORTAL_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Show on customer portal']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    LOCATION_ROWS = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row') "
        "and .//*[contains(@class,'inovua-react-toolkit-checkbox')]]"
    )
    REDEMPTION_ROWS = (
        By.XPATH,
        "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
        "//*[contains(@class,'InovuaReactDataGrid__row') "
        "and .//*[contains(@class,'inovua-react-toolkit-checkbox')]]"
    )
    REDEMPTION_CHECKBOXES = (
        By.XPATH,
        "//*[contains(@class,'inovua-react-toolkit-checkbox') "
        "and contains(@class,'InovuaReactDataGrid__checkbox')]"
    )
    REDEEM_AS_COMBOBOX = (
        By.XPATH,
        "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
        "//input[@role='combobox']"
    )
    APPLICABLE_DISCOUNTS_COMBOBOX = (
        By.XPATH,
        "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
        "//*[normalize-space()='Discounts applied to this service']"
        "/following::input[@role='combobox'][1]"
    )
    SELECTED_DISCOUNT_LABEL = (
        By.XPATH,
        "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
        "//*[contains(@class,'form-select__multi-value__label') "
        "and normalize-space()='%s']"
    )

    def wait_for_list_loaded(self):
        """Wait until the Memberships list is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(
            EC.element_to_be_clickable(self.ADD_MEMBERSHIP_BUTTON)
        )

    def wait_for_create_loaded(self):
        """Wait until the create membership form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME)
        )
        self.wait.until(
            EC.visibility_of_element_located(self.MEMBERSHIP_NAME_INPUT)
        )
        self.wait.until(EC.element_to_be_clickable(self.SAVE_MEMBERSHIP_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until the edit membership form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME))
        self.wait.until(
            EC.visibility_of_element_located(self.MEMBERSHIP_NAME_INPUT)
        )
        self.wait.until(EC.element_to_be_clickable(self.SAVE_MEMBERSHIP_BUTTON))
        self.wait.until(lambda driver: self.get_membership_name_value() != "")

    def get_body_text(self):
        """Get visible text inside the current iframe."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_membership_row_locator(self, membership_name):
        """Build a locator for a membership row by name."""
        return (
            By.XPATH,
            "//*[@data-props-id='membershipName']"
            "[.//span[normalize-space()='%s']]"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
            % membership_name
        )

    def wait_for_membership_row(self, membership_name):
        """Wait until a membership row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_membership_row_locator(membership_name)
            )
        )

    def membership_exists(self, membership_name):
        """Return whether the membership exists in the list."""
        self.wait_for_list_loaded()
        self.search_membership(membership_name)

        try:
            self.wait_for_membership_row(membership_name)
            return True
        except TimeoutException:
            return False

    def search_membership(self, membership_name):
        """Search membership by name."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        self._set_input_value(search_input, membership_name)
        self.wait.until(
            lambda driver: self.driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == membership_name
        )

    def get_membership_type(self, membership_name):
        """Return visible type for a membership row."""
        row = self.wait_for_membership_row(membership_name)
        for props_id in ("membershipType", "type"):
            cells = row.find_elements(
                By.XPATH,
                ".//*[@data-props-id='%s']" % props_id
            )
            if cells:
                return cells[0].text.strip()

        row_text = row.text
        if "Prepaid" in row_text:
            return "Prepaid"
        if "Recurring" in row_text:
            return "Recurring"

        raise AssertionError("Membership type column was not found")

    def get_membership_price(self, membership_name):
        """Return visible price for a membership row."""
        row = self.wait_for_membership_row(membership_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='membershipPrice']"
        ).text.strip()

    def get_membership_status(self, membership_name):
        """Return visible status for a membership row."""
        row = self.wait_for_membership_row(membership_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='isActive']"
        ).text.strip()

    def open_filter_panel(self):
        """Open the Memberships filter panel."""
        self.wait_for_list_loaded()
        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.FILTER_SITE_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))

    def download_button_is_clickable(self):
        """Return whether the download button can be clicked."""
        return self.wait.until(
            EC.element_to_be_clickable(self.DOWNLOAD_BUTTON)
        ).is_displayed()

    def open_create_membership(self):
        """Open create membership form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_MEMBERSHIP_BUTTON)
        self.wait_for_create_loaded()

    def open_edit_membership(self, membership_name):
        """Open edit membership form."""
        self.wait_for_list_loaded()
        self.search_membership(membership_name)
        row = self.wait_for_membership_row(membership_name)
        edit_button = row.find_element(
            By.XPATH,
            ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        edit_button.click()
        self.wait_for_edit_loaded()

    def enter_membership_name(self, membership_name):
        """Enter membership name."""
        self.enter_text(self.MEMBERSHIP_NAME_INPUT, membership_name)

    def get_membership_name_value(self):
        """Return the current membership name input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.MEMBERSHIP_NAME_INPUT)
        )
        return element.get_attribute("value")

    def get_membership_name_validation_message(self):
        """Return native validation message for membership name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.MEMBERSHIP_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def membership_name_input_is_valid(self):
        """Return native validity state for membership name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.MEMBERSHIP_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
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

    def select_prepaid_membership_type(self):
        """Select Prepaid membership type."""
        radio = self.wait.until(EC.presence_of_element_located(self.PREPAID_RADIO))
        if not radio.is_selected():
            radio.click()
            self.wait.until(
                lambda driver: driver.find_element(
                    *self.PREPAID_RADIO
                ).is_selected()
            )

    def prepaid_membership_type_is_selected(self):
        """Return whether Prepaid membership type is selected."""
        radio = self.wait.until(EC.presence_of_element_located(self.PREPAID_RADIO))
        return radio.is_selected()

    def set_prepaid_months(self, months):
        """Set prepaid membership duration months."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.PREPAID_MONTHS_INPUT)
        )
        element.clear()
        element.send_keys(str(months))

    def get_prepaid_months_value(self):
        """Return prepaid membership duration months value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.PREPAID_MONTHS_INPUT)
        )
        return element.get_attribute("value")

    def set_points_awarded(self, points):
        """Set loyalty points awarded on purchase/sale."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_AWARDED_INPUT)
        )
        element.clear()
        element.send_keys(str(points))
        self.wait.until(
            lambda driver: driver.find_element(
                *self.POINTS_AWARDED_INPUT
            ).get_attribute("value") == str(points)
        )

    def get_points_awarded_value(self):
        """Return loyalty points awarded on purchase/sale value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_AWARDED_INPUT)
        )
        return element.get_attribute("value")

    def set_global_price(self, price):
        """Set membership global price."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        element.clear()
        element.send_keys(str(price))

    def get_global_price_value(self):
        """Return membership global price input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return element.get_attribute("value")

    def set_global_commission(self, commission):
        """Set membership global commission."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        elements[0].clear()
        elements[0].send_keys(str(commission))

    def get_global_commission_value(self):
        """Return membership global commission input value."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        return elements[0].get_attribute("value")

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

    def customer_portal_switch_is_on(self):
        """Return whether Show on customer portal switch is on."""
        return self.switch_is_on(self.CUSTOMER_PORTAL_SWITCH)

    def ensure_active_switch_on(self):
        """Turn Active service on if needed."""
        self.ensure_switch_on(self.ACTIVE_SWITCH)

    def ensure_customer_portal_switch_on(self):
        """Turn Show on customer portal on if needed."""
        self.ensure_switch_on(self.CUSTOMER_PORTAL_SWITCH)

    def open_membership_settings(self):
        """Open Membership settings tab."""
        tab = self.wait.until(
            EC.presence_of_element_located(self.MEMBERSHIP_SETTINGS_TAB)
        )
        self.driver.execute_script("arguments[0].click();", tab)
        self.wait.until(
            EC.visibility_of_element_located(self.MEMBERSHIP_NAME_INPUT)
        )

    def open_redemption_settings(self):
        """Open Redemption settings tab."""
        tab = self.wait.until(
            EC.presence_of_element_located(self.REDEMPTION_SETTINGS_TAB)
        )
        self.driver.execute_script("arguments[0].click();", tab)
        self.wait.until(
            lambda driver: "Redeem at" in self.get_body_text()
        )
        self.wait.until(
            lambda driver: any(
                element.is_displayed()
                for element in driver.find_elements(*self.REDEEM_AS_COMBOBOX)
            )
        )

    def open_discount_settings(self):
        """Open Discount settings tab."""
        tab = self.wait.until(
            EC.presence_of_element_located(self.DISCOUNT_SETTINGS_TAB)
        )
        self.driver.execute_script("arguments[0].click();", tab)
        self.wait.until(
            lambda driver: "Applicable discounts" in self.get_body_text()
        )
        self.wait.until(
            lambda driver: any(
                element.is_displayed()
                for element in driver.find_elements(
                    *self.APPLICABLE_DISCOUNTS_COMBOBOX
                )
            )
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

    def get_location_checkbox_by_index(self, row_index):
        """Return assignment checkbox for one visible location row."""
        rows = self.get_location_rows()

        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (row_index + 1, len(rows))
            )

        return rows[row_index].find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
        )

    def location_is_assigned_by_index(self, row_index):
        """Return whether one visible location row is assigned."""
        checkbox = self.get_location_checkbox_by_index(row_index)
        return self.row_checkbox_is_checked(checkbox)

    def assign_location_by_index_with_price_and_commission(
        self,
        row_index,
        price,
        commission
    ):
        """Assign one visible location row and set price/commission."""
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

    def set_location_price_and_commission_by_index(
        self,
        row_index,
        price,
        commission
    ):
        """Set one visible location row price/commission without assigning it."""
        price_inputs = [
            element
            for element in self.wait.until(
                EC.presence_of_all_elements_located((By.NAME, "price"))
            )
            if element.is_displayed() and element.is_enabled()
        ]
        commission_inputs = [
            element
            for element in self.wait.until(
                EC.presence_of_all_elements_located((By.NAME, "commission"))
            )[1:]
            if element.is_displayed() and element.is_enabled()
        ]

        if row_index >= len(price_inputs) or row_index >= len(commission_inputs):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (
                    row_index + 1,
                    min(len(price_inputs), len(commission_inputs))
                )
            )

        price_input = price_inputs[row_index]
        commission_input = commission_inputs[row_index]
        self.set_grid_input_value(price_input, price)
        self.set_grid_input_value(commission_input, commission)

    def set_grid_input_value(self, element, value):
        """Set a grid input using native typing, with JS fallback."""
        try:
            element.click()
            element.clear()
            element.send_keys(str(value))
        except Exception:
            self._set_input_value(element, str(value))

    def fill_required_unassigned_location_values(self):
        """Fill required grid inputs for unassigned locations without assigning."""
        for row_index in range(1, len(self.get_location_rows())):
            self.set_location_price_and_commission_by_index(row_index, "0", "0")

    def get_redemption_rows(self):
        """Return unique visible redemption location rows."""
        rows = self.wait.until(
            EC.presence_of_all_elements_located(self.REDEMPTION_ROWS)
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

    def assign_redemption_location_by_index(self, row_index):
        """Assign one redemption location row by zero-based row index."""
        checkboxes = [
            checkbox
            for checkbox in self.wait.until(
                EC.presence_of_all_elements_located(self.REDEMPTION_CHECKBOXES)
            )
            if checkbox.rect["width"] > 0 and checkbox.rect["height"] > 0
        ]

        if row_index >= len(checkboxes):
            raise AssertionError(
                "Expected at least %s redemption rows, found %s"
                % (row_index + 1, len(checkboxes))
            )

        checkbox_index = row_index + 1 if len(checkboxes) > row_index + 1 else row_index
        checkbox = checkboxes[checkbox_index]

        if not self.row_checkbox_is_checked(checkbox):
            rect = checkbox.rect
            self.driver.execute_script(
                """
                const target = document.elementFromPoint(arguments[0], arguments[1]);
                const checkbox = target.closest('.inovua-react-toolkit-checkbox');
                checkbox.click();
                """,
                rect["x"] + rect["width"] / 2,
                rect["y"] + rect["height"] / 2
            )
            self.wait.until(
                lambda driver: self.row_checkbox_is_checked(
                    [
                        checkbox
                        for checkbox in driver.find_elements(
                            *self.REDEMPTION_CHECKBOXES
                        )
                        if (
                            checkbox.rect["width"] > 0
                            and checkbox.rect["height"] > 0
                        )
                    ][checkbox_index]
                )
            )

    def redemption_location_is_assigned_by_index(self, row_index):
        """Return whether one redemption location row is assigned."""
        checkboxes = [
            checkbox
            for checkbox in self.wait.until(
                EC.presence_of_all_elements_located(self.REDEMPTION_CHECKBOXES)
            )
            if checkbox.rect["width"] > 0 and checkbox.rect["height"] > 0
        ]

        checkbox_index = row_index + 1 if len(checkboxes) > row_index + 1 else row_index

        if checkbox_index >= len(checkboxes):
            raise AssertionError(
                "Expected at least %s redemption rows, found %s"
                % (row_index + 1, len(checkboxes))
            )

        checkbox = checkboxes[checkbox_index]
        return self.row_checkbox_is_checked(checkbox)

    def select_redeem_as_option(self, service_name, row_index=0):
        """Select Redeem as option in Redemption settings."""
        comboboxes = self.wait.until(
            lambda driver: [
                element
                for element in driver.find_elements(*self.REDEEM_AS_COMBOBOX)
                if element.is_displayed() and element.is_enabled()
            ]
        )

        if row_index >= len(comboboxes):
            raise AssertionError(
                "Expected at least %s redeem-as fields, found %s"
                % (row_index + 1, len(comboboxes))
            )

        comboboxes[row_index].click()
        comboboxes[row_index].send_keys(service_name)
        option = self.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@role='option' and translate(normalize-space(), "
                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='%s']"
                    % service_name.lower()
                )
            )
        )
        self.driver.execute_script("arguments[0].click();", option)
        self.wait.until(
            lambda driver: service_name.lower() in self.get_body_text().lower()
        )

    def configure_redemption_settings(
        self,
        redemption_row_index,
        redeem_as_service
    ):
        """Set required redemption location and redeem-as service."""
        self.open_redemption_settings()
        self.assign_redemption_location_by_index(redemption_row_index)
        self.select_redeem_as_option(redeem_as_service, redemption_row_index)

    def discount_is_selected(self, discount_name):
        """Return whether an applicable discount is selected."""
        return bool(
            self.driver.find_elements(
                self.SELECTED_DISCOUNT_LABEL[0],
                self.SELECTED_DISCOUNT_LABEL[1] % discount_name
            )
        )

    def select_applicable_discount(self, discount_name):
        """Ensure an applicable discount is selected."""
        self.open_discount_settings()

        if self.discount_is_selected(discount_name):
            return

        combobox = self.wait.until(
            EC.element_to_be_clickable(self.APPLICABLE_DISCOUNTS_COMBOBOX)
        )
        combobox.click()

        option = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[@role='option' and translate(normalize-space(), "
                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='%s']"
                    % discount_name.lower()
                )
            )
        )
        self.driver.execute_script("arguments[0].click();", option)
        self.wait.until(lambda driver: self.discount_is_selected(discount_name))

    def update_loyalty_points_and_discount(
        self,
        membership_name,
        points_awarded,
        discount_name
    ):
        """Update membership loyalty points and applicable discount."""
        self.open_edit_membership(membership_name)
        self.set_points_awarded(points_awarded)
        self.select_applicable_discount(discount_name)
        self.click_save_membership()
        self.wait_for_list_loaded()

    def get_location_price_by_index(self, row_index):
        """Return one visible location row price by zero-based row index."""
        rows = self.get_location_rows()
        price_input = rows[row_index].find_element(By.NAME, "price")
        return price_input.get_attribute("value")

    def get_location_commission_by_index(self, row_index):
        """Return one visible location row commission by zero-based row index."""
        rows = self.get_location_rows()
        commission_input = rows[row_index].find_element(By.NAME, "commission")
        return commission_input.get_attribute("value")

    def click_save_membership(self):
        """Click save membership."""
        self.click(self.SAVE_MEMBERSHIP_BUTTON)

    def fill_membership_form(
        self,
        membership_name,
        global_price,
        global_commission,
        first_location_price,
        first_location_commission,
        prepaid_months="1"
    ):
        """Fill membership settings for a prepaid membership."""
        self.enter_membership_name(membership_name)
        self.select_prepaid_membership_type()
        self.set_prepaid_months(prepaid_months)
        self.ensure_active_switch_on()
        self.ensure_customer_portal_switch_on()
        self.set_global_price(global_price)
        self.set_global_commission(global_commission)
        self.set_location_price_and_commission_by_index(
            0,
            first_location_price,
            first_location_commission
        )
        self.fill_required_unassigned_location_values()
        self.assign_location_by_index_with_price_and_commission(
            0,
            first_location_price,
            first_location_commission
        )
        self.configure_redemption_settings(0, "VK detail wash")

    def create_membership(
        self,
        membership_name,
        global_price,
        global_commission,
        first_location_price,
        first_location_commission
    ):
        """Create an active prepaid membership and return to list."""
        self.open_create_membership()
        self.fill_membership_form(
            membership_name,
            global_price,
            global_commission,
            first_location_price,
            first_location_commission
        )
        self.click_save_membership()
        self.wait_for_list_loaded()
