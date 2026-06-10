from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class WashBooksPage(BasePage):

    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/washBooks?')]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/washBooks/new')]"
    )
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/washBooks/') "
        "and not(contains(@src,'/services/washBooks/new'))]"
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Wash books']")
    SEARCH_INPUT = (By.NAME, "washbookName")
    FILTER_BUTTON = (By.XPATH, "//button[normalize-space()='Filter by']")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Filter by']/following-sibling::button[1]"
    )
    ADD_WASH_BOOK_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='+ Add new wash book']"
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

    SAVE_WASH_BOOK_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save wash book']"
    )
    SERVICE_SETTINGS_TAB = (
        By.XPATH,
        "//button[@role='tab' and normalize-space()='Service settings']"
    )
    REDEMPTION_SETTINGS_TAB = (
        By.XPATH,
        "//button[@role='tab' and normalize-space()='Redemption settings']"
    )

    WASH_BOOK_NAME_INPUT = (By.NAME, "washbookName")
    NUMBER_OF_WASHES_INPUT = (By.NAME, "numberOfWashes")
    POINTS_AWARDED_INPUT = (By.NAME, "pointsAwarded")
    GLOBAL_PRICE_INPUT = (By.NAME, "washbookPrice")
    COMMISSION_INPUTS = (By.NAME, "commission")
    LOCATION_PRICE_INPUTS = (By.NAME, "price")
    ACTIVE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active wash books']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    CUSTOMER_PORTAL_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Show on customer portal']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    WASH_BOOK_DESCRIPTION_SECTION = (
        By.XPATH,
        "//*[normalize-space()='Wash book description']"
        "/ancestor::div[contains(@style,'cursor: pointer')][1]"
    )
    WASH_BOOK_DESCRIPTION_TEXTAREA = (
        By.XPATH,
        "//textarea[@name='description']"
    )
    ASSIGNMENT_CHECKBOXES = (
        By.XPATH,
        "//*[contains(@class,'inovua-react-toolkit-checkbox') "
        "and contains(@class,'InovuaReactDataGrid__checkbox')]"
    )
    SERVICE_LOCATION_ROWS = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row') "
        "and .//*[contains(@class,'inovua-react-toolkit-checkbox')]]"
    )
    REDEEM_AS_COMBOBOXES = (
        By.XPATH,
        "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
        "//input[@role='combobox']"
    )

    def wait_for_list_loaded(self):
        """Wait until the Wash Books list is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_WASH_BOOK_BUTTON))

    def wait_for_create_loaded(self):
        """Wait until the create wash book form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME)
        )
        self.wait.until(
            EC.visibility_of_element_located(self.WASH_BOOK_NAME_INPUT)
        )
        self.wait.until(EC.element_to_be_clickable(self.SAVE_WASH_BOOK_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until the edit wash book form is visible."""
        long_wait = WebDriverWait(self.driver, 30)
        self.driver.switch_to.default_content()
        long_wait.until(EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME))
        tab = long_wait.until(
            EC.presence_of_element_located(self.SERVICE_SETTINGS_TAB)
        )
        self.driver.execute_script("arguments[0].click();", tab)
        long_wait.until(
            EC.visibility_of_element_located(self.WASH_BOOK_NAME_INPUT)
        )
        long_wait.until(EC.element_to_be_clickable(self.SAVE_WASH_BOOK_BUTTON))
        long_wait.until(lambda driver: self.get_wash_book_name_value() != "")

    def get_body_text(self):
        """Get visible text inside the current iframe."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def _set_input_value(self, element, value):
        """Set a React-controlled input value and dispatch change events."""
        if element.tag_name.lower() == "textarea":
            self.driver.execute_script(
                """
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(
                    new Event('input', { bubbles: true })
                );
                arguments[0].dispatchEvent(
                    new Event('change', { bubbles: true })
                );
                """,
                element,
                value
            )
            return

        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];
            input.focus();
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype,
                'value'
            ).set;
            setter.call(input, value);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            value
        )

    def get_wash_book_row_locator(self, wash_book_name):
        """Build a locator for a wash book row by name."""
        return (
            By.XPATH,
            "//*[@data-props-id='washbookName']"
            "[.//span[normalize-space()='%s']]"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
            % wash_book_name
        )

    def wait_for_wash_book_row(self, wash_book_name):
        """Wait until a wash book row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_wash_book_row_locator(wash_book_name)
            )
        )

    def search_wash_book(self, wash_book_name):
        """Search wash book by name."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        self._set_input_value(search_input, wash_book_name)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == wash_book_name
        )

    def wash_book_exists(self, wash_book_name):
        """Return whether the wash book exists in the list."""
        self.wait_for_list_loaded()
        self.search_wash_book(wash_book_name)

        try:
            self.wait_for_wash_book_row(wash_book_name)
            return True
        except TimeoutException:
            return False

    def get_wash_book_price(self, wash_book_name):
        """Return visible price for a wash book row."""
        row = self.wait_for_wash_book_row(wash_book_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='washbookPrice']"
        ).text.strip()

    def get_wash_book_washes(self, wash_book_name):
        """Return visible number of washes for a wash book row."""
        row = self.wait_for_wash_book_row(wash_book_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='numberOfWashes']"
        ).text.strip()

    def get_wash_book_status(self, wash_book_name):
        """Return visible status for a wash book row."""
        row = self.wait_for_wash_book_row(wash_book_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='isActive']"
        ).text.strip()

    def open_filter_panel(self):
        """Open the Wash Books filter panel."""
        self.wait_for_list_loaded()
        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.FILTER_SITE_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))

    def download_button_is_clickable(self):
        """Return whether the download button can be clicked."""
        return self.wait.until(
            EC.element_to_be_clickable(self.DOWNLOAD_BUTTON)
        ).is_displayed()

    def open_create_wash_book(self):
        """Open create wash book form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_WASH_BOOK_BUTTON)
        self.wait_for_create_loaded()

    def open_edit_wash_book(self, wash_book_name):
        """Open edit wash book form."""
        self.wait_for_list_loaded()
        self.search_wash_book(wash_book_name)
        row = self.wait_for_wash_book_row(wash_book_name)
        edit_button = row.find_element(
            By.XPATH,
            ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        edit_button.click()
        self.wait_for_edit_loaded()

    def enter_wash_book_name(self, wash_book_name):
        """Enter wash book name."""
        self.enter_text(self.WASH_BOOK_NAME_INPUT, wash_book_name)

    def get_wash_book_name_value(self):
        """Return the current wash book name input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.WASH_BOOK_NAME_INPUT)
        )
        return element.get_attribute("value")

    def get_wash_book_name_validation_message(self):
        """Return native validation message for wash book name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.WASH_BOOK_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def wash_book_name_input_is_valid(self):
        """Return native validity state for wash book name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.WASH_BOOK_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def set_number_of_washes(self, washes):
        """Set number of washes."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.NUMBER_OF_WASHES_INPUT)
        )
        self._set_input_value(element, str(washes))

    def get_number_of_washes_value(self):
        """Return number of washes input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.NUMBER_OF_WASHES_INPUT)
        )
        return element.get_attribute("value")

    def set_points_awarded(self, points):
        """Set loyalty points awarded."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_AWARDED_INPUT)
        )
        self._set_input_value(element, str(points))

    def get_points_awarded_value(self):
        """Return points awarded input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_AWARDED_INPUT)
        )
        return element.get_attribute("value")

    def set_global_price(self, price):
        """Set global wash book price."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        self._set_input_value(element, str(price))

    def get_global_price_value(self):
        """Return global wash book price value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return element.get_attribute("value")

    def set_global_commission(self, commission):
        """Set global wash book commission."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.COMMISSION_INPUTS)
        )
        self._set_input_value(elements[0], str(commission))

    def get_global_commission_value(self):
        """Return global wash book commission value."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.COMMISSION_INPUTS)
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
        """Return whether Active wash books switch is on."""
        return self.switch_is_on(self.ACTIVE_SWITCH)

    def customer_portal_switch_is_on(self):
        """Return whether Show on customer portal switch is on."""
        return self.switch_is_on(self.CUSTOMER_PORTAL_SWITCH)

    def ensure_active_switch_on(self):
        """Turn Active wash books on if needed."""
        self.ensure_switch_on(self.ACTIVE_SWITCH)

    def ensure_customer_portal_switch_on(self):
        """Turn Show on customer portal on if needed."""
        self.ensure_switch_on(self.CUSTOMER_PORTAL_SWITCH)

    def open_wash_book_description(self):
        """Expand the Wash book description section."""
        section = self.wait.until(
            EC.presence_of_element_located(self.WASH_BOOK_DESCRIPTION_SECTION)
        )
        textarea = self.driver.find_element(
            *self.WASH_BOOK_DESCRIPTION_TEXTAREA
        )
        if not textarea.is_displayed():
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                section
            )
            try:
                section.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", section)
            self.wait.until(
                EC.visibility_of_element_located(
                    self.WASH_BOOK_DESCRIPTION_TEXTAREA
                )
            )

    def set_wash_book_description(self, description):
        """Set wash book description text."""
        self.open_wash_book_description()
        textarea = self.wait.until(
            EC.visibility_of_element_located(
                self.WASH_BOOK_DESCRIPTION_TEXTAREA
            )
        )
        textarea.clear()
        textarea.send_keys(description)
        self.driver.execute_script(
            """
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            textarea
        )
        self.wait.until(
            lambda driver: textarea.get_attribute("value") == description
        )

    def get_wash_book_description_value(self):
        """Return wash book description text."""
        self.open_wash_book_description()
        textarea = self.wait.until(
            EC.visibility_of_element_located(
                self.WASH_BOOK_DESCRIPTION_TEXTAREA
            )
        )
        return textarea.get_attribute("value")

    def wait_for_service_location_rows(self):
        """Wait until service-setting location rows are hydrated."""
        self.wait.until(
            lambda driver: "VK Test carwash 2" in self.get_body_text()
            and len(self.visible_location_price_inputs()) >= 2
        )

    def visible_location_price_inputs(self):
        """Return visible location price inputs."""
        rows = self.visible_service_location_rows()
        if rows:
            return [
                row.find_element(By.NAME, "price")
                for row in rows
            ]

        return [
            element
            for element in self.driver.find_elements(*self.LOCATION_PRICE_INPUTS)
            if element.is_displayed() and element.is_enabled()
        ]

    def visible_location_commission_inputs(self):
        """Return visible location commission inputs, excluding global commission."""
        rows = self.visible_service_location_rows()
        if rows:
            return [
                row.find_element(By.NAME, "commission")
                for row in rows
            ]

        elements = [
            element
            for element in self.driver.find_elements(*self.COMMISSION_INPUTS)[1:]
            if element.is_displayed() and element.is_enabled()
        ]
        return elements

    def visible_service_location_rows(self):
        """Return visible service location rows, preferring baseline test sites."""
        rows = [
            row
            for row in self.driver.find_elements(*self.SERVICE_LOCATION_ROWS)
            if row.rect["width"] > 0 and row.rect["height"] > 0
        ]
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

        baseline_rows = [
            row
            for row in unique_rows
            if "VK Test carwash 2" in row.text or "VK Test Wash 01" in row.text
        ]

        return baseline_rows or unique_rows

    def visible_assignment_checkboxes(self):
        """Return visible service assignment checkboxes, excluding header."""
        rows = self.visible_service_location_rows()
        if rows:
            return [
                row.find_element(
                    By.XPATH,
                    ".//*[contains(@class,'inovua-react-toolkit-checkbox') "
                    "and contains(@class,'InovuaReactDataGrid__checkbox')]"
                )
                for row in rows
            ]

        checkboxes = [
            checkbox
            for checkbox in self.driver.find_elements(*self.ASSIGNMENT_CHECKBOXES)
            if checkbox.rect["width"] > 0 and checkbox.rect["height"] > 0
        ]
        return checkboxes[1:]

    def visible_assignment_header_checkbox(self):
        """Return visible assignment header checkbox."""
        checkboxes = [
            checkbox
            for checkbox in self.driver.find_elements(*self.ASSIGNMENT_CHECKBOXES)
            if checkbox.rect["width"] > 0 and checkbox.rect["height"] > 0
        ]
        return checkboxes[0]

    def visible_switches(self):
        """Return visible switches on the current tab."""
        return [
            switch
            for switch in self.driver.find_elements(
                By.XPATH,
                "//button[@role='switch']"
            )
            if switch.is_displayed()
        ]

    def visible_location_customer_portal_switches(self):
        """Return visible row-level Show on CP switches."""
        return [
            switch
            for switch in self.visible_switches()
            if switch.rect["x"] > 1000
        ]

    def row_checkbox_is_checked(self, checkbox):
        """Return whether an Inovua checkbox is checked."""
        classes = checkbox.get_attribute("class")
        return (
            "inovua-react-toolkit-checkbox--checked" in classes
            and "inovua-react-toolkit-checkbox--unchecked" not in classes
        )

    def ensure_checkbox_checked(self, checkbox):
        """Check an Inovua checkbox if needed."""
        if not self.row_checkbox_is_checked(checkbox):
            self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(lambda driver: self.row_checkbox_is_checked(checkbox))

    def set_location_price_and_commission_by_index(
        self,
        row_index,
        price,
        commission
    ):
        """Set one location row price and commission."""
        self.wait_for_service_location_rows()
        price_inputs = self.visible_location_price_inputs()
        commission_inputs = self.visible_location_commission_inputs()

        if row_index >= len(price_inputs) or row_index >= len(commission_inputs):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (
                    row_index + 1,
                    min(len(price_inputs), len(commission_inputs))
                )
            )

        self.set_grid_input_value(price_inputs[row_index], price)
        self.set_grid_input_value(commission_inputs[row_index], commission)

    def set_grid_input_value(self, element, value):
        """Set a React grid input value without appending to stale text."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({ block: 'center' });"
            "arguments[0].focus();",
            element
        )
        element.send_keys(Keys.COMMAND, "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(str(value))
        self.driver.execute_script(
            """
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element
        )
        if not self.grid_input_numeric_value_matches(element, value):
            self._set_input_value(element, str(value))
        self.driver.execute_script(
            """
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            element
        )
        self.wait.until(
            lambda driver: self.grid_input_numeric_value_matches(element, value)
        )

    def grid_input_numeric_value_matches(self, element, value):
        """Return whether a possibly formatted numeric input equals value."""
        current_value = element.get_attribute("value") or ""
        try:
            current_number = float(
                "".join(
                    character
                    for character in current_value
                    if character.isdigit() or character in ".-"
                )
            )
            expected_number = float(str(value))
            return current_number == expected_number
        except ValueError:
            return current_value == str(value)

    def assign_location_by_index(self, row_index):
        """Assign one visible location row."""
        self.wait_for_service_location_rows()
        checkboxes = self.visible_assignment_checkboxes()

        if row_index >= len(checkboxes):
            raise AssertionError(
                "Expected at least %s location checkboxes, found %s"
                % (row_index + 1, len(checkboxes))
            )

        self.ensure_checkbox_checked(checkboxes[row_index])

    def assign_all_locations(self):
        """Assign all visible service location rows."""
        self.wait_for_service_location_rows()
        for row_index in range(len(self.visible_assignment_checkboxes())):
            self.assign_location_by_index(row_index)

    def enable_location_customer_portal_by_index(self, row_index):
        """Enable one row-level Show on CP switch."""
        self.wait_for_service_location_rows()
        switches = self.visible_location_customer_portal_switches()

        if row_index >= len(switches):
            raise AssertionError(
                "Expected at least %s Show on CP switches, found %s"
                % (row_index + 1, len(switches))
            )

        switch = switches[row_index]
        if switch.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(
                lambda driver: self.visible_location_customer_portal_switches()[
                    row_index
                ].get_attribute("aria-checked") == "true"
            )

    def location_is_assigned_by_index(self, row_index):
        """Return whether one service location row is assigned."""
        self.wait_for_service_location_rows()
        return self.row_checkbox_is_checked(
            self.visible_assignment_checkboxes()[row_index]
        )

    def get_location_price_by_index(self, row_index):
        """Return one location row price."""
        self.wait_for_service_location_rows()
        return self.visible_location_price_inputs()[row_index].get_attribute("value")

    def get_location_commission_by_index(self, row_index):
        """Return one location row commission."""
        self.wait_for_service_location_rows()
        return self.visible_location_commission_inputs()[row_index].get_attribute(
            "value"
        )

    def location_customer_portal_is_on_by_index(self, row_index):
        """Return whether one row-level Show on CP switch is on."""
        self.wait_for_service_location_rows()
        return (
            self.visible_location_customer_portal_switches()[row_index]
            .get_attribute("aria-checked") == "true"
        )

    def open_service_settings(self):
        """Open Service settings tab."""
        tab = self.wait.until(
            EC.presence_of_element_located(self.SERVICE_SETTINGS_TAB)
        )
        self.driver.execute_script("arguments[0].click();", tab)
        self.wait.until(
            EC.visibility_of_element_located(self.WASH_BOOK_NAME_INPUT)
        )

    def open_redemption_settings(self):
        """Open Redemption settings tab."""
        tab = self.wait.until(
            EC.presence_of_element_located(self.REDEMPTION_SETTINGS_TAB)
        )
        self.driver.execute_script("arguments[0].click();", tab)
        self.wait.until(lambda driver: "Redeem at" in self.get_body_text())
        self.wait.until(
            lambda driver: len(self.visible_redeem_as_comboboxes()) >= 2
        )

    def visible_redemption_checkboxes(self):
        """Return visible redemption checkboxes, excluding header if present."""
        checkboxes = [
            checkbox
            for checkbox in self.driver.find_elements(*self.ASSIGNMENT_CHECKBOXES)
            if checkbox.rect["width"] > 0 and checkbox.rect["height"] > 0
        ]
        if len(checkboxes) > 2:
            return checkboxes[1:3]
        return checkboxes[:2]

    def visible_redeem_as_comboboxes(self):
        """Return visible Redeem as comboboxes."""
        return [
            element
            for element in self.driver.find_elements(*self.REDEEM_AS_COMBOBOXES)
            if element.is_displayed() and element.is_enabled()
        ]

    def assign_redemption_location_by_index(self, row_index):
        """Assign one redemption location row."""
        checkboxes = self.visible_redemption_checkboxes()

        if row_index >= len(checkboxes):
            raise AssertionError(
                "Expected at least %s redemption rows, found %s"
                % (row_index + 1, len(checkboxes))
            )

        self.ensure_checkbox_checked(checkboxes[row_index])

    def select_redeem_as_option(self, row_index, service_name):
        """Select one Redeem as option."""
        comboboxes = self.wait.until(
            EC.presence_of_all_elements_located(self.REDEEM_AS_COMBOBOXES)
        )

        if row_index >= len(comboboxes):
            raise AssertionError(
                "Expected at least %s redeem-as fields, found %s"
                % (row_index + 1, len(comboboxes))
            )

        comboboxes[row_index].click()
        comboboxes[row_index].send_keys(service_name)
        option = self.wait.until(
            EC.element_to_be_clickable(
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

    def click_save_wash_book(self):
        """Click save wash book."""
        button = self.wait.until(
            EC.element_to_be_clickable(self.SAVE_WASH_BOOK_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def fill_wash_book_form(
        self,
        wash_book_name,
        washes,
        points_awarded,
        global_price,
        global_commission
    ):
        """Fill all required wash book service and redemption settings."""
        self.enter_wash_book_name(wash_book_name)
        self.set_number_of_washes(washes)
        self.set_points_awarded(points_awarded)
        self.ensure_active_switch_on()
        self.ensure_customer_portal_switch_on()
        self.set_global_price(global_price)
        self.set_global_commission(global_commission)
        self.assign_all_locations()

        for row_index in range(2):
            self.set_location_price_and_commission_by_index(
                row_index,
                global_price,
                global_commission
            )

        self.open_redemption_settings()
        self.assign_redemption_location_by_index(0)
        self.select_redeem_as_option(0, "vk detail wash")
        self.assign_redemption_location_by_index(1)
        self.select_redeem_as_option(1, "Detail cleaning")
        self.open_service_settings()

    def create_wash_book(
        self,
        wash_book_name,
        washes,
        points_awarded,
        global_price,
        global_commission
    ):
        """Create an active wash book and return to the list."""
        self.open_create_wash_book()
        self.fill_wash_book_form(
            wash_book_name,
            washes,
            points_awarded,
            global_price,
            global_commission
        )
        self.click_save_wash_book()
        self.wait_for_list_loaded()

    def update_wash_book_description(self, wash_book_name, description):
        """Update one wash book description and return to the list."""
        self.open_edit_wash_book(wash_book_name)
        self.set_wash_book_description(description)
        self.click_save_wash_book()
        self.wait_for_list_loaded()
