import time

from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
    GRID_LOAD_MASK = (
        By.CSS_SELECTOR,
        ".inovua-react-toolkit-load-mask__background-layer"
    )
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
        self.switch_to_frame_with_retry(self.FRAME)

    def wait_for_list_loaded(self):
        """Wait until the Service Categories list is visible.

        Uses the general FRAME locator (not LIST_FRAME) so this works whether
        React re-mounted the iframe with a new src (in which case src updates)
        or navigated in-place via React Router (in which case the parent DOM
        src attribute stays at the old edit/create URL).  PAGE_TITLE is only
        present on the list page, so it acts as the reliable transition signal.

        Also resets any stale inactive filter: soft-nav through the inactive
        list to an edit form and back leaves React Router's filter state intact,
        so we normalise to the Active-only default view on every list load.
        """
        self.switch_to_frame_with_retry(self.FRAME)
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_CATEGORY_BUTTON))
        if self._has_active_filter():
            self.clear_category_search()
            self.reset_filters()
        self.wait_for_grid_idle()

    wait_for_loaded = wait_for_list_loaded

    def wait_for_grid_idle(self):
        """Wait until the React grid load mask is not blocking interactions."""
        self.wait.until(
            lambda driver: not any(
                mask.is_displayed()
                for mask in driver.find_elements(*self.GRID_LOAD_MASK)
            )
        )

    def wait_for_create_loaded(self):
        """Wait until the create category form is visible."""
        self.switch_to_frame_with_retry(self.CREATE_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_NEW_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until the edit category form is visible."""
        self.switch_to_frame_with_retry(self.EDIT_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_CHANGES_BUTTON))
        WebDriverWait(self.driver, 60).until(
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
        self.wait_for_grid_idle()
        rows = self.get_visible_category_rows()
        if not rows:
            return False
        for row in rows:
            if not row.find_elements(By.XPATH, ".//*[normalize-space()='Edit']"):
                return False
        return True

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

    def _quick_category_row(self, category_name, timeout=8):
        """Return the row element if found within *timeout* seconds, else None.

        Used as a fast first probe so callers avoid burning the full 45-second
        wait on categories that are inactive (hidden in the default view).
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    self.get_category_row_locator(category_name)
                )
            )
        except TimeoutException:
            return None

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

    def _find_first_matching_inactive(self, *category_names):
        """Apply inactive filter once and return the first matching row and name.

        Opens the inactive filter a SINGLE time (expensive UI op) then checks
        each name in sequence using an 8-second probe.  Returns
        (row_element, matched_name) for the first match, or (None, None).

        Caller must already be inside the service-categories iframe on the list
        page.  After returning the page is in the inactive-filtered view; callers
        responsible for subsequent navigation (typically open_service_categories).
        """
        self._show_inactive_categories()
        for name in category_names:
            self.search_category(name)
            try:
                row = WebDriverWait(self.driver, 8).until(
                    EC.visibility_of_element_located(
                        self.get_category_row_locator(name)
                    )
                )
                return row, name
            except TimeoutException:
                continue
        return None, None

    def _reset_to_default_view(self):
        """Remove any filter and return to the default list view."""
        try:
            self.wait_for_list_loaded()
            # Clear search before opening the filter panel — the Filter button
            # is disabled when the grid is in an empty-results state.
            self.clear_category_search()
            self.reset_filters()
            self.wait_for_list_loaded()
        except Exception:  # noqa: BLE001
            pass

    def category_exists(self, category_name):
        """Return True if the category exists (checks active then inactive view)."""
        self.wait_for_list_loaded()
        self.search_category(category_name)
        if self._quick_category_row(category_name) is not None:
            return True

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
        row = self._quick_category_row(category_name)
        if row is None:
            self._show_inactive_categories()
            self.search_category(category_name)
            row = self.wait_for_category_row(category_name)
        edit_button = row.find_element(
            By.XPATH,
            ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        self.driver.execute_script("arguments[0].click();", edit_button)
        self.wait_for_edit_loaded()

    # ------------------------------------------------------------------ search

    def search_category(self, category_name):
        """Search category by name."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        # _set_input_value uses React's native setter + dispatchEvent atomically.
        # select() + send_keys() is racy: a React re-render between the two
        # resets the native selection, causing send_keys to append rather than
        # replace, making the value-equality wait time out.
        self._set_input_value(search_input, category_name)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == category_name
        )
        self.wait_for_grid_idle()

    def clear_category_search(self):
        """Clear category search and wait until input is empty."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        self._set_input_value(search_input, "")
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == ""
        )
        self.wait_for_grid_idle()

    # ------------------------------------------------------------------ filter

    def open_filter_panel(self):
        """Open the filter panel and wait for it to render.

        Callers must be inside the service-categories iframe on the list page
        before calling this method (i.e. wait_for_list_loaded() already done).
        Using wait_for_grid_idle() instead of wait_for_list_loaded() avoids an
        unnecessary frame exit/re-entry (~15 s) on every filter operation.
        """
        self.wait_for_grid_idle()
        btn = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(self.FILTER_BUTTON))
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
        """Apply filters — clicks Apply button if present, else auto-applies.

        Uses wait_for_grid_idle() instead of wait_for_list_loaded() so we stay
        inside the iframe and avoid the ~15 s frame exit/re-entry overhead.
        Callers that need a fresh list-loaded guarantee should call
        wait_for_list_loaded() themselves after apply_filters().

        A brief sleep before wait_for_grid_idle() is needed because the React
        grid may not show its loading indicator immediately after the Apply
        click — without it wait_for_grid_idle() can return prematurely while
        the grid is still fetching filtered data.
        """
        apply_btns = self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)
        if apply_btns:
            self.driver.execute_script("arguments[0].click();", apply_btns[0])
            self.wait.until(
                EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON)
            )
        time.sleep(0.5)
        self.wait_for_grid_idle()
        # Wait for the filtered rows to be present (noop for empty result sets).
        try:
            self.wait.until(EC.presence_of_element_located(self.GRID_ROWS))
        except Exception:  # noqa: BLE001
            pass

    def _has_active_filter(self):
        """Return True if a filter count badge is visible (a filter is active)."""
        return bool(self.driver.find_elements(
            By.XPATH,
            "//button[contains(normalize-space(), 'Filter by (')]"
        ))

    def reset_filters(self):
        """Open filter panel and reset all filters."""
        self.open_filter_panel()
        reset_btns = self.driver.find_elements(*self.RESET_ALL_BUTTON)
        if reset_btns:
            self.driver.execute_script("arguments[0].click();", reset_btns[0])
        self.apply_filters()

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
            # Patch confirm BEFORE clicking: the app fires window.parent.confirm
            # asynchronously when switching Inactive → Active (unlike deactivation
            # whose confirm fires on Save).  In headless Chrome, a native confirm
            # auto-dismisses with false, reverting the switch back to Inactive
            # before we even call click_save_changes().  Patching here ensures the
            # async confirm returns true, so the form state commits to Active.
            self.driver.execute_script(
                "window.confirm = () => true;"
                " try { window.parent.confirm = () => true; } catch(e) {}"
            )
            try:
                switch.click()
            except ElementClickInterceptedException:
                self._dismiss_page_banner()
                self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(
                lambda driver: driver.find_element(
                    *self.ACTIVE_SWITCH
                ).get_attribute("aria-checked") == "true"
            )

    def ensure_active_switch_off(self):
        """Turn active switch off, using direct .click() to fire React events."""
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "false":
            try:
                switch.click()
            except ElementClickInterceptedException:
                self._dismiss_page_banner()
                self.driver.execute_script("arguments[0].click();", switch)
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
        """Save new category.

        Holds a reference to the Save button so we can wait for it to go stale
        after the click — a reliable DOM signal that the form has navigated
        away.  Guards against the headless race where wait_for_list_loaded()
        starts polling for the list iframe before the create frame has reloaded.
        For validation-failure cases the button re-appears quickly (or never
        leaves), so the 5-second staleness timeout is a low-cost guard.
        """
        btn = self.wait.until(EC.element_to_be_clickable(self.SAVE_NEW_BUTTON))
        try:
            btn.click()
        except ElementClickInterceptedException:
            self._dismiss_page_banner()
            self.driver.execute_script("arguments[0].click();", btn)
        try:
            WebDriverWait(self.driver, 5).until(EC.staleness_of(btn))
        except Exception:  # noqa: BLE001
            pass

    def click_save_changes(self):
        """Save category changes.

        Patches window.confirm to auto-accept — the app shows a native confirm
        dialog when deactivating, which headless Chrome auto-dismisses with
        false (cancel), preventing the save from completing.

        Same staleness guard as click_save_new — waits up to 10 s for the Save
        button to leave the DOM, which signals the edit form has navigated away
        and makes wait_for_list_loaded() safe to call immediately after.
        """
        self.driver.execute_script(
            "window.confirm = () => true;"
            " try { window.parent.confirm = () => true; } catch(e) {}"
        )
        time.sleep(0.5)
        btn = self.wait.until(EC.element_to_be_clickable(self.SAVE_CHANGES_BUTTON))
        try:
            btn.click()
        except ElementClickInterceptedException:
            self._dismiss_page_banner()
            self.driver.execute_script("arguments[0].click();", btn)
        try:
            WebDriverWait(self.driver, 10).until(EC.staleness_of(btn))
        except Exception:  # noqa: BLE001
            pass

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
        try:
            self.wait_for_list_loaded()
        except TimeoutException:
            error = self.get_visible_error()
            raise RuntimeError(
                "Service category save did not return to list. Page message: %s"
                % (error or "none visible")
            ) from None

    def create_inactive_category(self, category_name):
        """Create a category with Active switch OFF and return to list."""
        self.open_create_category()
        self.enter_category_name(category_name)
        self.ensure_active_switch_off()
        self.click_save_new()
        try:
            self.wait_for_list_loaded()
        except TimeoutException:
            error = self.get_visible_error()
            raise RuntimeError(
                "Inactive service category save did not return to list. Page message: %s"
                % (error or "none visible")
            ) from None

    def update_category_name(self, old_name, new_name):
        """Rename a category and return to list."""
        self.open_edit_category(old_name)
        self.enter_category_name(new_name)
        self.ensure_active_switch_on()
        self.click_save_changes()
        # A name-change save does not auto-navigate back to the list in headless
        # Chrome (the edit form stays displayed showing a success state, unlike
        # status-change saves which do trigger navigation).  Probe briefly; if
        # the list doesn't appear, drive the outer portal directly to the SC list.
        if not self._quick_list_check(timeout=6):
            self._navigate_outer_to_sc_list()
        self.wait_for_list_loaded()

    def _quick_list_check(self, timeout=6):
        """Return True if ADD_CATEGORY_BUTTON becomes clickable within timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.ADD_CATEGORY_BUTTON)
            )
            return True
        except TimeoutException:
            return False

    def _navigate_outer_to_sc_list(self):
        """Navigate the outer admin portal directly to the SC list page."""
        self.driver.switch_to.default_content()
        current = self.driver.current_url
        sc_path = "/services/serviceCategories"
        idx = current.find(sc_path)
        if idx != -1:
            self.driver.get(current[:idx + len(sc_path)])
