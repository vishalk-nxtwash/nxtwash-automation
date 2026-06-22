from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class ServiceCategoriesPage(BasePage):

    FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/serviceCategories')]"
    )
    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/serviceCategories')"
        " and not(contains(@src,'/services/serviceCategories/'))]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/serviceCategories/new')]"
    )
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/serviceCategories/') "
        "and not(contains(@src,'/new'))]"
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Service categories']")
    SEARCH_INPUT = (By.NAME, "categoryName")
    FILTER_BUTTON = (By.XPATH, "//button[normalize-space()='Filter by']")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Filter by']/following-sibling::button[1]"
    )
    ADD_CATEGORY_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='+ Add new category']"
    )
    EDIT_ACTIONS = (By.XPATH, "//*[normalize-space()='Edit']")
    GRID_ROWS = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row') "
        "and .//*[@data-props-id='categoryName']]"
    )
    SAVE_NEW_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save new category']"
    )
    SAVE_CHANGES_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Save')]"
    )
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    CATEGORY_NAME_INPUT = (By.NAME, "categoryName")
    ACTIVE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active service']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']"
    )
    RESET_ALL_BUTTON = (By.XPATH, "//button[normalize-space()='Reset all']")
    ACTIVE_FILTER_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active service category']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    GRID_STATUS_CELLS = (By.XPATH, "//*[@data-props-id='isActive']")

    # ------------------------------------------------------------------ waits

    def switch_to_module_frame(self):
        """Switch into the Service Categories iframe."""
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.FRAME))

    def wait_for_list_loaded(self):
        """Wait until the Service Categories list is visible."""
        from selenium.webdriver.support.ui import WebDriverWait
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_CATEGORY_BUTTON))

    def wait_for_create_loaded(self):
        """Wait until the create category form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_NEW_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until the edit category form is visible."""
        from selenium.webdriver.support.ui import WebDriverWait
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME))
        self.wait.until(EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_CHANGES_BUTTON))
        WebDriverWait(self.driver, 30).until(
            lambda driver: self.get_category_name_value() != ""
        )

    # ----------------------------------------------------------- body / checks

    def get_body_text(self):
        """Get visible text inside the current frame."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def search_input_is_visible(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        ).is_displayed()

    def filter_button_is_clickable(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.FILTER_BUTTON)
        ).is_displayed()

    def download_button_is_clickable(self):
        return self.wait.until(
            EC.presence_of_element_located(self.DOWNLOAD_BUTTON)
        ).is_displayed()

    def add_category_button_is_clickable(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.ADD_CATEGORY_BUTTON)
        ).is_displayed()

    def save_new_button_is_clickable(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.SAVE_NEW_BUTTON)
        ).is_displayed()

    def cancel_button_is_visible(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.CANCEL_BUTTON)
        ).is_displayed()

    # -------------------------------------------------------------------- grid

    def get_visible_category_rows(self):
        """Return visible service category rows."""
        return [
            row for row in self.driver.find_elements(*self.GRID_ROWS)
            if row.is_displayed()
        ]

    def get_visible_category_names(self):
        """Return visible category names from the grid."""
        names = []
        for row in self.get_visible_category_rows():
            try:
                names.append(
                    row.find_element(
                        By.XPATH,
                        ".//*[@data-props-id='categoryName']"
                    ).text.strip()
                )
            except Exception:  # noqa: BLE001
                continue
        return [name for name in names if name]

    def get_visible_category_statuses(self):
        """Return visible status values from the grid."""
        statuses = []
        for row in self.get_visible_category_rows():
            try:
                statuses.append(
                    row.find_element(
                        By.XPATH, ".//*[@data-props-id='isActive']"
                    ).text.strip()
                )
            except Exception:  # noqa: BLE001
                continue
        return [s for s in statuses if s]

    def every_visible_row_has_edit_action(self):
        rows = self.get_visible_category_rows()
        edits = [
            e for e in self.driver.find_elements(*self.EDIT_ACTIONS)
            if e.is_displayed()
        ]
        return bool(rows) and len(edits) >= len(rows)

    def pagination_controls_are_visible(self):
        text = self.get_body_text()
        return "Page" in text and "Results per page" in text

    def results_per_page_control_is_visible(self):
        return "Results per page" in self.get_body_text()

    # ------------------------------------------------------------------ React

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

    # -------------------------------------------------------------------- rows

    def get_category_row_locator(self, category_name):
        return (
            By.XPATH,
            "//*[@data-props-id='categoryName']"
            "[.//span[normalize-space()='%s']]"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
            % category_name
        )

    def wait_for_category_row(self, category_name):
        """Wait until a category row is visible in the current grid view."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_category_row_locator(category_name)
            )
        )

    # ------------------------------------------------- inactive category access

    def _show_inactive_categories(self):
        """Apply the inactive filter so hidden inactive rows become visible.

        Clears any active search first — the Filter button is unavailable when
        the grid is in an empty-results state (no-match search applied).
        """
        self.clear_category_search()
        self.open_filter_panel()
        self.set_active_category_filter(False)
        self.apply_filters()

    def _reset_to_default_view(self):
        """Remove any filter and return to the default list view."""
        try:
            self.reset_filters()
            self.wait_for_list_loaded()
        except Exception:  # noqa: BLE001
            pass

    def category_exists(self, category_name):
        """Return True if the category exists (checks active then inactive view)."""
        self.wait_for_list_loaded()
        self.search_category(category_name)
        try:
            self.wait_for_category_row(category_name)
            return True
        except TimeoutException:
            pass

        try:
            self._show_inactive_categories()
            self.search_category(category_name)
            self.wait_for_category_row(category_name)
            return True
        except TimeoutException:
            return False
        finally:
            self._reset_to_default_view()

    def get_category_status(self, category_name):
        """Return status text for a category row, falling back to inactive filter."""
        used_fallback = False
        try:
            row = self.wait_for_category_row(category_name)
        except TimeoutException:
            used_fallback = True
            self._show_inactive_categories()
            self.search_category(category_name)
            row = self.wait_for_category_row(category_name)
        status = row.find_element(
            By.XPATH, ".//*[@data-props-id='isActive']"
        ).text.strip()
        if used_fallback:
            self._reset_to_default_view()
        return status

    def open_create_category(self):
        """Open create category form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_CATEGORY_BUTTON)
        self.wait_for_create_loaded()

    def open_edit_category(self, category_name):
        """Open edit category form, falling back to inactive filter if needed."""
        self.wait_for_list_loaded()
        self.search_category(category_name)
        try:
            row = self.wait_for_category_row(category_name)
        except TimeoutException:
            self._show_inactive_categories()
            self.search_category(category_name)
            row = self.wait_for_category_row(category_name)
        edit_button = row.find_element(
            By.XPATH,
            ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        edit_button.click()
        self.wait_for_edit_loaded()

    # ------------------------------------------------------------------ search

    def search_category(self, category_name):
        """Search category by name."""
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )
        self._set_input_value(search_input, category_name)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == category_name
        )

    def clear_category_search(self):
        """Clear category search and wait until input is empty."""
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        )
        self._set_input_value(search_input, "")
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == ""
        )

    # ------------------------------------------------------------------ filter

    def open_filter_panel(self):
        """Open the filter panel and wait for it to render."""
        import time
        self.wait_for_list_loaded()
        btn = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        try:
            self.wait.until(
                lambda driver: (
                    len(driver.find_elements(*self.APPLY_FILTERS_BUTTON)) > 0
                    or len(driver.find_elements(*self.RESET_ALL_BUTTON)) > 0
                    or len(driver.find_elements(*self.ACTIVE_FILTER_SWITCH)) > 0
                )
            )
        except Exception:  # noqa: BLE001
            time.sleep(1.5)

    def set_active_category_filter(self, on):
        """Toggle the active/inactive switch in the filter panel."""
        desired = "true" if on else "false"

        candidates = self.driver.find_elements(*self.ACTIVE_FILTER_SWITCH)
        if candidates:
            switch = candidates[0]
            if switch.get_attribute("aria-checked") != desired:
                self.driver.execute_script("arguments[0].click();", switch)
                self.wait.until(
                    lambda driver: driver.find_elements(
                        *self.ACTIVE_FILTER_SWITCH
                    )[0].get_attribute("aria-checked") == desired
                )
            return

        checkbox_locator = (By.XPATH, "//input[@type='checkbox']")
        checkboxes = self.driver.find_elements(*checkbox_locator)
        if checkboxes:
            cb = checkboxes[0]
            if cb.is_selected() != on:
                self.driver.execute_script("arguments[0].click();", cb)

    def apply_filters(self):
        """Apply filters — clicks Apply button if present, else auto-applies."""
        apply_btns = self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)
        if apply_btns:
            self.driver.execute_script("arguments[0].click();", apply_btns[0])
            self.wait.until(
                EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON)
            )
        self.wait_for_list_loaded()

    def reset_filters(self):
        """Open filter panel and reset all filters."""
        self.open_filter_panel()
        reset_btns = self.driver.find_elements(*self.RESET_ALL_BUTTON)
        if reset_btns:
            self.driver.execute_script("arguments[0].click();", reset_btns[0])

    # ------------------------------------------------------------------ switch

    def active_switch_is_on(self):
        """Return whether active switch is checked."""
        switch = self.wait.until(
            EC.presence_of_element_located(self.ACTIVE_SWITCH)
        )
        return switch.get_attribute("aria-checked") == "true"

    def ensure_active_switch_on(self):
        """Turn active switch on, using direct .click() to fire React events."""
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "true":
            switch.click()
            self.wait.until(
                lambda driver: driver.find_element(
                    *self.ACTIVE_SWITCH
                ).get_attribute("aria-checked") == "true"
            )

    def ensure_active_switch_off(self):
        """Turn active switch off, using direct .click() to fire React events."""
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "false":
            switch.click()
            self.wait.until(
                lambda driver: driver.find_element(
                    *self.ACTIVE_SWITCH
                ).get_attribute("aria-checked") == "false"
            )

    # -------------------------------------------------------------------- form

    def enter_category_name(self, category_name):
        """Enter category name."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT)
        )
        self._set_input_value(element, category_name)

    def get_category_name_value(self):
        """Return current category name input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT)
        )
        return (element.get_attribute("value") or "").strip()

    def get_category_name_validation_message(self):
        """Return native validation message for category name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def category_name_input_is_valid(self):
        """Return native validity state for category name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def click_save_new(self):
        """Save new category."""
        self.click(self.SAVE_NEW_BUTTON)

    def click_save_changes(self):
        """Save category changes.

        Patches window.confirm to auto-accept — the app shows a native confirm
        dialog when deactivating, which headless Chrome auto-dismisses with
        false (cancel), preventing the save from completing.
        """
        import time
        self.driver.execute_script("window.confirm = () => true;")
        time.sleep(0.5)
        self.click(self.SAVE_CHANGES_BUTTON)

    def click_cancel(self):
        """Cancel create/edit category."""
        self.click(self.CANCEL_BUTTON)

    # ----------------------------------------------------------------- helpers

    def create_category(self, category_name):
        """Create an active category and return to list."""
        self.open_create_category()
        self.enter_category_name(category_name)
        self.ensure_active_switch_on()
        self.click_save_new()
        self.wait_for_list_loaded()

    def create_inactive_category(self, category_name):
        """Create a category with Active switch OFF and return to list."""
        self.open_create_category()
        self.enter_category_name(category_name)
        self.ensure_active_switch_off()
        self.click_save_new()
        self.wait_for_list_loaded()

    def update_category_name(self, old_name, new_name):
        """Rename a category and return to list."""
        self.open_edit_category(old_name)
        self.enter_category_name(new_name)
        self.ensure_active_switch_on()
        self.click_save_changes()
        self.wait_for_list_loaded()
