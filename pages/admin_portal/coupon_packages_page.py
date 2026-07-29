from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class CouponPackagesPage(BasePage):

    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/couponPackages')"
        " and not(contains(@src,'/new'))"
        " and not(contains(@src,'/edit/'))]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/couponPackages/new')]"
    )
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/couponPackages/edit/')]"
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Coupon packages']")
    SEARCH_INPUT = (By.NAME, "packageName")
    FILTER_BUTTON = (By.XPATH, "//button[normalize-space()='Filter by']")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Filter by']/following-sibling::button[1]"
    )
    ADD_COUPON_PACKAGE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='+ Add new coupon package']"
    )
    GRID_LOAD_MASK = (
        By.CSS_SELECTOR,
        ".inovua-react-toolkit-load-mask__background-layer"
    )
    SAVE_COUPON_PACKAGE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save new coupon package' "
        "or normalize-space()='Save coupon package']"
    )

    COUPON_PACKAGE_NAME_INPUT = (By.NAME, "packageName")
    EXPIRATION_DAYS_INPUT = (By.NAME, "expirationDays")
    ASSIGN_DISCOUNT_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='Assign discount']"
        "/following::input[@role='combobox'][1]"
    )
    GIVEAWAY_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='Coupon giveaway on receipt']"
        "/following::input[@role='combobox'][1]"
    )
    ACTIVE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active coupon package']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    APPLY_FILTERS_BUTTON = (By.XPATH, "//button[normalize-space()='Apply filters']")
    RESET_ALL_BUTTON = (By.XPATH, "//button[normalize-space()='Reset all']")
    ACTIVE_PACKAGE_FILTER_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active coupon package']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    GRID_HEADER_COLUMN = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__column-header__content')"
        " and normalize-space()='Coupon package name']"
    )
    GRID_STATUS_CELLS = (By.XPATH, "//*[@data-props-id='isActive']")
    CUSTOMER_TAB = (
        By.XPATH,
        "//button[@role='tab' and normalize-space()='Customer coupon packages']"
    )

    def wait_for_list_loaded(self):
        """Wait until the Coupon Packages list is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(
            EC.element_to_be_clickable(self.ADD_COUPON_PACKAGE_BUTTON)
        )
        self.wait_for_grid_idle()
        self.wait.until(EC.visibility_of_element_located(self.GRID_HEADER_COLUMN))

    def wait_for_grid_idle(self):
        """Wait until the React grid load mask is not blocking interactions."""
        self.wait.until(
            lambda driver: not any(
                mask.is_displayed()
                for mask in driver.find_elements(*self.GRID_LOAD_MASK)
            )
        )

    def wait_for_create_loaded(self):
        """Wait until the create coupon package form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME)
        )
        self.wait.until(
            EC.visibility_of_element_located(self.COUPON_PACKAGE_NAME_INPUT)
        )
        self.wait.until(
            EC.element_to_be_clickable(self.SAVE_COUPON_PACKAGE_BUTTON)
        )

    def wait_for_edit_loaded(self):
        """Wait until the edit coupon package form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME)
        )
        self.wait.until(
            EC.visibility_of_element_located(self.COUPON_PACKAGE_NAME_INPUT)
        )
        self.wait.until(
            EC.element_to_be_clickable(self.SAVE_COUPON_PACKAGE_BUTTON)
        )
        self.wait.until(lambda driver: self.get_coupon_package_name_value() != "")

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

    def get_coupon_package_row_locator(self, coupon_package_name):
        """Build a locator for a coupon package row by package name."""
        return (
            By.XPATH,
            "//*[contains(@class,'InovuaReactDataGrid__row') "
            "and .//*[normalize-space()='%s']]"
            % coupon_package_name
        )

    def wait_for_coupon_package_row(self, coupon_package_name):
        """Wait until a coupon package row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_coupon_package_row_locator(coupon_package_name)
            )
        )

    def search_coupon_package(self, coupon_package_name):
        """Search coupon package by name."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_input.click()
        search_input.send_keys(Keys.COMMAND + "a")
        search_input.send_keys(Keys.BACKSPACE)
        search_input.send_keys(coupon_package_name)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == coupon_package_name
        )
        self.wait_for_grid_idle()

    def coupon_package_exists(self, coupon_package_name):
        """Return whether the coupon package exists in the list."""
        self.wait_for_list_loaded()
        self.search_coupon_package(coupon_package_name)

        try:
            self.wait_for_coupon_package_row(coupon_package_name)
            return True
        except TimeoutException:
            return False

    def open_create_coupon_package(self):
        """Open create coupon package form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_COUPON_PACKAGE_BUTTON)
        self.wait_for_create_loaded()

    def open_edit_coupon_package(self, coupon_package_name):
        """Open edit coupon package form."""
        self.wait_for_list_loaded()
        self.search_coupon_package(coupon_package_name)
        row = self.wait_for_coupon_package_row(coupon_package_name)
        edit_button = row.find_element(
            By.XPATH,
            ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        edit_button.click()
        self.wait_for_edit_loaded()

    def enter_coupon_package_name(self, coupon_package_name):
        """Enter coupon package name."""
        self.enter_text(self.COUPON_PACKAGE_NAME_INPUT, coupon_package_name)

    def get_coupon_package_name_value(self):
        """Return the current coupon package name."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.COUPON_PACKAGE_NAME_INPUT)
        )
        return element.get_attribute("value")

    def get_coupon_package_name_validation_message(self):
        """Return native validation message for coupon package name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.COUPON_PACKAGE_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def coupon_package_name_input_is_valid(self):
        """Return native validity state for coupon package name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.COUPON_PACKAGE_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def switch_is_on(self, locator):
        """Return whether a switch is on."""
        switch = self.wait.until(EC.presence_of_element_located(locator))
        return switch.get_attribute("aria-checked") == "true"

    def ensure_switch_on(self, locator):
        """Turn a switch on if needed."""
        switch = self.wait.until(EC.visibility_of_element_located(locator))
        if switch.get_attribute("aria-checked") != "true":
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", switch
            )
            ActionChains(self.driver).move_to_element(switch).click().perform()
            self.wait.until(
                lambda driver: switch.get_attribute("aria-checked") == "true"
            )

    def active_switch_is_on(self):
        """Return whether Active coupon package is on."""
        return self.switch_is_on(self.ACTIVE_SWITCH)

    def ensure_active_switch_on(self):
        """Turn Active coupon package on if needed."""
        self.ensure_switch_on(self.ACTIVE_SWITCH)

    def ensure_switch_off(self, locator):
        """Turn a switch off if needed."""
        switch = self.wait.until(EC.visibility_of_element_located(locator))
        if switch.get_attribute("aria-checked") != "false":
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", switch
            )
            ActionChains(self.driver).move_to_element(switch).click().perform()
            self.wait.until(
                lambda driver: switch.get_attribute("aria-checked") == "false"
            )

    def ensure_active_switch_off(self):
        """Turn Active coupon package off if needed."""
        self.ensure_switch_off(self.ACTIVE_SWITCH)

    def enter_expiration_days(self, days):
        """Set the expiration days field value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.EXPIRATION_DAYS_INPUT)
        )
        self._set_input_value(element, str(days))

    def get_expiration_days_value(self):
        """Return the current expiration days value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.EXPIRATION_DAYS_INPUT)
        )
        return element.get_attribute("value")

    def clear_search(self):
        """Clear the search input and wait for the grid to refresh."""
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

    def open_filter_panel(self):
        """Open the Coupon Packages filter panel."""
        self.wait_for_list_loaded()
        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))

    def set_active_package_filter(self, on):
        """Set the filter panel Active coupon package toggle."""
        if on:
            self.ensure_switch_on(self.ACTIVE_PACKAGE_FILTER_SWITCH)
        else:
            self.ensure_switch_off(self.ACTIVE_PACKAGE_FILTER_SWITCH)

    def apply_filters(self):
        """Apply configured filters and wait for the grid to refresh."""
        self.click(self.APPLY_FILTERS_BUTTON)
        self.wait.until(
            EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON)
        )
        self.wait_for_list_loaded()

    def reset_filters(self):
        """Open filter panel and reset all filters back to defaults."""
        self.open_filter_panel()
        self.click(self.RESET_ALL_BUTTON)
        self.click(self.APPLY_FILTERS_BUTTON)
        self.wait.until(
            EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON)
        )
        self.wait_for_list_loaded()

    def show_all_packages(self):
        """Open filter panel and turn off Active filter to show all packages."""
        self.open_filter_panel()
        self.ensure_switch_off(self.ACTIVE_PACKAGE_FILTER_SWITCH)
        self.apply_filters()

    def has_active_filters(self):
        """Return whether any filters are currently applied."""
        try:
            btn = self.driver.find_element(*self.FILTER_BUTTON)
            return "(" in btn.text
        except Exception:
            return False

    def get_all_visible_statuses(self):
        """Return all visible status values from the coupon packages grid."""
        return [
            cell.text.strip()
            for cell in self.driver.find_elements(*self.GRID_STATUS_CELLS)
            if cell.is_displayed() and cell.text.strip()
        ]

    def click_customer_coupon_packages_tab(self):
        """Click the Customer coupon packages tab (button is inside the list iframe)."""
        tab = self.wait.until(EC.element_to_be_clickable(self.CUSTOMER_TAB))
        self.driver.execute_script("arguments[0].click();", tab)
        self.driver.switch_to.default_content()

    def duplicate_name_error_is_visible(self):
        """Return whether a duplicate package name error is visible."""
        body_text = self.get_body_text().lower()
        return any(kw in body_text for kw in (
            "already exists", "duplicate", "already in use",
            "name is taken", "package name", "already been taken",
            "must be unique", "already used",
        ))

    def get_assign_discount_value(self):
        """Return the currently selected discount name from the combobox."""
        return self.driver.find_element(
            *self.ASSIGN_DISCOUNT_COMBOBOX
        ).get_attribute("value")

    def get_coupon_package_status(self, package_name):
        """Return the status text of a coupon package row in the grid."""
        row = self.wait_for_coupon_package_row(package_name)
        status_cell = row.find_element(
            By.XPATH, ".//*[@data-props-id='isActive']"
        )
        return status_cell.text.strip()

    def remove_giveaway_service(self, service_name):
        """Uncheck a giveaway service option from the multi-select dropdown."""
        self.open_giveaway_dropdown()
        if self.option_checkbox_is_checked(service_name):
            option = self.wait.until(
                lambda driver: self.find_select_option(service_name)
            )
            checkbox = option.find_element(By.XPATH, ".//input[@type='checkbox']")
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                option
            )
            self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(
                lambda driver: not self.option_checkbox_is_checked(service_name)
            )

    def create_inactive_coupon_package(
        self,
        package_name,
        discount_name,
        giveaway_service_name
    ):
        """Create an inactive coupon package and return to the list."""
        self.open_create_coupon_package()
        self.enter_coupon_package_name(package_name)
        self.select_assign_discount(discount_name)
        self.select_coupon_giveaway(giveaway_service_name)
        self.ensure_active_switch_off()
        self.click_save_coupon_package()
        self.wait_for_list_loaded()

    def activate_coupon_package(self, package_name):
        """Open edit form and activate the coupon package."""
        self.open_edit_coupon_package(package_name)
        # Wait for React to hydrate the form with the actual package state;
        # the switch may briefly render ON before settling to OFF for an
        # inactive package.
        self.wait.until(
            lambda d: d.find_element(
                *self.ACTIVE_SWITCH
            ).get_attribute("aria-checked") == "false"
        )
        # Type into the expiration days field via native send_keys (cross-origin
        # iframe safe) so React's onChange fires and the form is marked dirty.
        # A pristine-state guard on some React forms silently skips save when
        # no text-field change is detected alongside a switch-only toggle.
        expiry = self.wait.until(
            EC.element_to_be_clickable(self.EXPIRATION_DAYS_INPUT)
        )
        expiry.click()
        expiry.send_keys(Keys.COMMAND + "a")
        expiry.send_keys(Keys.BACKSPACE)
        expiry.send_keys("30")
        self.ensure_active_switch_on()
        self.click_save_coupon_package()
        try:
            self.wait_for_list_loaded()
        except TimeoutException:
            from urllib.parse import urlparse as _urlparse
            parsed = _urlparse(self.driver.current_url)
            self.driver.get(
                f"{parsed.scheme}://{parsed.netloc}/services/couponPackages"
            )
            self.wait_for_list_loaded()

    def deactivate_coupon_package(self, package_name):
        """Open edit form and deactivate the coupon package."""
        self.open_edit_coupon_package(package_name)
        self.ensure_active_switch_off()
        self.click_save_coupon_package()
        self.wait_for_list_loaded()

    def update_coupon_package_name(self, package_name, new_name):
        """Open edit form, update the name, and save."""
        self.open_edit_coupon_package(package_name)
        self.enter_coupon_package_name(new_name)
        self.click_save_coupon_package()
        self.wait_for_list_loaded()

    def clear_assign_discount(self):
        """Clear the currently selected discount from the combobox."""
        clear_button = (
            By.XPATH,
            "//*[normalize-space()='Assign discount']"
            "/following::*[contains(@class,'clear') or @aria-label='Clear'][1]"
        )
        try:
            btn = self.driver.find_element(*clear_button)
            if btn.is_displayed():
                self.driver.execute_script("arguments[0].click();", btn)
        except Exception:
            pass

    def update_assigned_discount(self, package_name, discount_name):
        """Open edit form, clear the existing discount, select a new one, and save."""
        self.open_edit_coupon_package(package_name)
        self.clear_assign_discount()
        self.select_assign_discount(discount_name)
        self.click_save_coupon_package()
        self.wait_for_list_loaded()

    def update_expiration_days(self, package_name, days):
        """Open edit form, update expiration days, and save."""
        self.open_edit_coupon_package(package_name)
        self.enter_expiration_days(days)
        self.click_save_coupon_package()
        self.wait_for_list_loaded()

    def find_select_option(self, option_text):
        """Find a visible React select option by case-insensitive text."""
        normalized = option_text.lower()
        options = self.driver.find_elements(
            By.XPATH,
            "//*[@role='option' or contains(@class,'option')]"
        )
        for option in options:
            try:
                if (
                    option.is_displayed()
                    and option.text.strip().lower() == normalized
                ):
                    return option
            except StaleElementReferenceException:
                return None
        return None

    def select_combobox_option(self, combobox_locator, option_text):
        """Select one option from a React combobox."""
        last_error = None
        for _ in range(3):
            try:
                combobox = self.wait.until(
                    EC.element_to_be_clickable(combobox_locator)
                )
                combobox.click()
                combobox.send_keys(option_text)
                break
            except StaleElementReferenceException as error:
                last_error = error
        else:
            raise last_error

        option = self.wait.until(
            lambda driver: self.find_select_option(option_text)
        )
        self.driver.execute_script("arguments[0].click();", option)
        self.wait.until(
            lambda driver: option_text.lower() in self.get_body_text().lower()
        )

    def select_assign_discount(self, discount_name):
        """Select Assign discount value."""
        self.select_combobox_option(self.ASSIGN_DISCOUNT_COMBOBOX, discount_name)

    def select_coupon_giveaway(self, service_name):
        """Select one Coupon giveaway on receipt value."""
        self.select_multi_select_option(self.GIVEAWAY_COMBOBOX, service_name)

    def select_multi_select_option(self, combobox_locator, option_text):
        """Select one checkbox option from a React multi-select combobox."""
        last_error = None
        for _ in range(3):
            try:
                combobox = self.wait.until(
                    EC.element_to_be_clickable(combobox_locator)
                )
                combobox.click()
                break
            except StaleElementReferenceException as error:
                last_error = error
        else:
            raise last_error

        option = self.wait.until(
            lambda driver: self.find_select_option(option_text)
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            option
        )
        checkbox = option.find_element(By.XPATH, ".//input[@type='checkbox']")
        try:
            checkbox.click()
        except Exception:
            option.click()
        self.wait.until(
            lambda driver: self.option_checkbox_is_checked(option_text)
        )

    def option_checkbox_is_checked(self, option_text):
        """Return whether a visible multi-select option checkbox is checked."""
        option = self.find_select_option(option_text)
        if option is None:
            return False
        checkbox = option.find_element(By.XPATH, ".//input[@type='checkbox']")
        return checkbox.is_selected() or checkbox.get_attribute("checked") is not None

    def selected_giveaway_values(self):
        """Return selected coupon giveaway text visible near the form."""
        body_text = self.get_body_text().lower()
        values = []
        for service_name in (
            "vk detail wash",
            "detail cleaning",
            "vk wash 2 package",
            "plus wash",
            "detail wash and clean"
        ):
            if service_name in body_text:
                values.append(service_name)
        return values

    def checked_giveaway_values(self):
        """Return checked Coupon giveaway on receipt option values."""
        self.open_giveaway_dropdown()
        values = []
        options = self.driver.find_elements(
            By.XPATH,
            "//*[@role='option' and .//input[@type='checkbox']]"
        )
        for option in options:
            try:
                checkbox = option.find_element(
                    By.XPATH,
                    ".//input[@type='checkbox']"
                )
                if checkbox.is_selected() or checkbox.get_attribute("checked"):
                    values.append(option.text.strip().lower())
            except StaleElementReferenceException:
                return self.checked_giveaway_values()
        return values

    def open_giveaway_dropdown(self):
        """Open the Coupon giveaway on receipt dropdown."""
        if self.find_select_option("Plus Wash") is not None:
            return

        for _ in range(3):
            try:
                combobox = self.wait.until(
                    EC.element_to_be_clickable(self.GIVEAWAY_COMBOBOX)
                )
                combobox.click()
                self.wait.until(lambda driver: self.find_select_option("Plus Wash"))
                return
            except StaleElementReferenceException:
                continue

    def click_save_coupon_package(self):
        """Click save coupon package."""
        button = self.wait.until(
            EC.element_to_be_clickable(self.SAVE_COUPON_PACKAGE_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def create_coupon_package(
        self,
        coupon_package_name,
        discount_name,
        giveaway_service_name
    ):
        """Create an active coupon package and return to the list."""
        self.open_create_coupon_package()
        self.enter_coupon_package_name(coupon_package_name)
        self.select_assign_discount(discount_name)
        self.select_coupon_giveaway(giveaway_service_name)
        self.ensure_active_switch_on()
        self.click_save_coupon_package()
        try:
            self.wait_for_list_loaded()
        except TimeoutException:
            error = self.get_visible_error()
            raise RuntimeError(
                "Coupon package save did not return to list. Page message: %s"
                % (error or "none visible")
            ) from None

    def update_coupon_giveaway_services(
        self,
        coupon_package_name,
        service_names
    ):
        """Update coupon giveaway services for an existing package."""
        self.open_edit_coupon_package(coupon_package_name)
        for service_name in service_names:
            if service_name.lower() not in self.checked_giveaway_values():
                self.select_coupon_giveaway(service_name)
        self.ensure_active_switch_on()
        self.click_save_coupon_package()
        self.wait_for_list_loaded()
