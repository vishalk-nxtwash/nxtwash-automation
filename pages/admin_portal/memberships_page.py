import time

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class MembershipsPage(BasePage):

    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/memberships') "
        "and not(contains(@src,'/services/memberships/'))]"
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
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Membership name']")
    FILTER_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(.), 'Filter by') "
        "or contains(@class, 'filterButton')]"
    )
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[starts-with(normalize-space(),'Filter by')]/following-sibling::button[1]"
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
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    SUPPORT_BUTTON = (
        By.XPATH,
        "//*[self::button or self::a][contains(normalize-space(.), 'Support')]"
    )
    PAGINATION_TEXT = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'Showing') "
        "or contains(normalize-space(.), 'Page')]"
    )
    RESULTS_PER_PAGE_SELECT = (
        By.XPATH,
        "//select | //*[@role='combobox' and contains(normalize-space(.), '100')]"
    )
    NO_RECORDS_TEXT = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'No records') "
        "or contains(normalize-space(.), 'No data') "
        "or contains(normalize-space(.), 'No results')]"
    )
    GRID_LOAD_MASK = (
        By.CSS_SELECTOR,
        ".inovua-react-toolkit-load-mask__background-layer"
    )
    FILTER_SITE_INPUT = (
        By.XPATH,
        "//*[normalize-space()='Select site']/following::input[1]"
    )
    MEMBERSHIP_TYPE_FILTER = (
        By.XPATH,
        "//*[normalize-space()='Membership type']"
        "/following::div[contains(@class,'form-select__control')][1]"
    )
    ACTIVE_MEMBERSHIP_FILTER_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active membership']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    FILTER_OPTION = (
        By.XPATH,
        "//*[contains(@class,'form-select__option')]"
    )
    GRID_TYPE_CELLS = (
        By.XPATH,
        "//*[@data-props-id='membershipType' or @data-props-id='type']"
    )
    GRID_STATUS_CELLS = (By.XPATH, "//*[@data-props-id='isActive']")

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
    BARCODE_INPUT = (By.NAME, "barcode")
    LIMIT_MEMBERSHIP_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Limit membership']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    LIMIT_PER_DAY_INPUT = (By.NAME, "redemptionLimitPerDay")
    LIMIT_PER_WEEK_INPUT = (By.NAME, "redemptionLimitPerWeek")
    LIMIT_PER_MONTH_INPUT = (By.NAME, "redemptionLimitPerMonth")
    DESCRIPTION_ACCORDION_HEADER = (
        By.XPATH,
        "//*[normalize-space()='Membership description']"
        "/parent::*[contains(@style,'cursor: pointer')]"
    )
    DESCRIPTION_TEXTAREA = (By.NAME, "description")
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
        self.switch_to_frame_with_retry(self.LIST_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(
            EC.element_to_be_clickable(self.ADD_MEMBERSHIP_BUTTON)
        )
        self.wait_for_grid_idle()

    def wait_for_grid_idle(self):
        """Wait until the React grid load mask is not blocking interactions."""
        self.wait.until(
            lambda driver: not any(
                mask.is_displayed()
                for mask in driver.find_elements(*self.GRID_LOAD_MASK)
            )
        )

    def wait_for_create_or_edit_form(self):
        """Wait until the create/edit membership form remains visible."""
        self.wait.until(
            EC.visibility_of_element_located(self.MEMBERSHIP_NAME_INPUT)
        )
        self.wait.until(EC.element_to_be_clickable(self.SAVE_MEMBERSHIP_BUTTON))

    def wait_for_form_save_blocked(self):
        """Wait until save leaves the user on a membership form."""
        self.wait.until(
            lambda driver: (
                "/services/memberships/new" in driver.current_url
                or "/services/memberships/edit/" in driver.current_url
            )
        )
        self.wait_for_create_or_edit_form()

    def wait_for_create_loaded(self):
        """Wait until the create membership form is visible."""
        self.switch_to_frame_with_retry(self.CREATE_FRAME)
        self.wait.until(
            EC.visibility_of_element_located(self.MEMBERSHIP_NAME_INPUT)
        )
        self.wait.until(EC.element_to_be_clickable(self.SAVE_MEMBERSHIP_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until the edit membership form is visible."""
        self.switch_to_frame_with_retry(self.EDIT_FRAME)
        self.wait.until(
            EC.visibility_of_element_located(self.MEMBERSHIP_NAME_INPUT)
        )
        self.wait.until(EC.element_to_be_clickable(self.SAVE_MEMBERSHIP_BUTTON))
        self.wait.until(lambda driver: self.get_membership_name_value() != "")

    def get_body_text(self):
        """Get visible text inside the current iframe."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def element_is_visible(self, locator):
        """Return whether an element is visible without failing the test."""
        return any(
            element.is_displayed()
            for element in self.driver.find_elements(*locator)
        )

    def get_membership_row_locator(self, membership_name):
        """Build a locator for a membership row by name."""
        return (
            By.XPATH,
            "//*[@data-props-id='membershipName']"
            "[.//span[normalize-space()='%s']]"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
            % membership_name
        )

    def wait_for_membership_row(self, membership_name, timeout=60):
        """Wait until a membership row is visible.

        Fails fast (with a clear error) when the grid shows the Inovua
        "No records available" empty-state text, rather than waiting out
        the full `timeout`.  A brief 3-second grace period is allowed so
        the grid can finish loading before the empty-state check fires.
        """
        import time
        _NO_RECORDS = (
            By.CSS_SELECTOR,
            "div.InovuaReactDataGrid__empty-text"
        )
        deadline = time.time() + timeout
        while time.time() < deadline:
            # Check whether the target row is already visible.
            els = self.driver.find_elements(
                *self.get_membership_row_locator(membership_name)
            )
            if els and els[0].is_displayed():
                return els[0]
            # Check for the explicit "No records available" sentinel.
            no_rec = self.driver.find_elements(*_NO_RECORDS)
            if no_rec and no_rec[0].is_displayed():
                # Give the grid 3 s in case it's still transitioning from
                # a loading state into displaying the actual records.
                try:
                    return WebDriverWait(self.driver, 3).until(
                        EC.visibility_of_element_located(
                            self.get_membership_row_locator(membership_name)
                        )
                    )
                except Exception:
                    raise TimeoutException(
                        "Grid shows 'No records available' — '%s' not found"
                        % membership_name
                    )
            time.sleep(0.5)
        raise TimeoutException(
            "Timed out after %ss waiting for membership row '%s'"
            % (timeout, membership_name)
        )

    def wait_for_no_membership_row(self, membership_name):
        """Wait until a membership row is not visible."""
        return self.wait.until(
            EC.invisibility_of_element_located(
                self.get_membership_row_locator(membership_name)
            )
        )

    def get_visible_membership_rows(self):
        """Return visible membership grid rows."""
        return [
            row
            for row in self.driver.find_elements(
                By.XPATH,
                "//*[contains(@class,'InovuaReactDataGrid__row') "
                "and .//*[@data-props-id='membershipName']]"
            )
            if row.is_displayed()
        ]

    def get_visible_membership_names(self):
        """Return visible membership names from the list grid."""
        names = []

        for row in self.get_visible_membership_rows():
            try:
                cell = row.find_element(
                    By.XPATH,
                    ".//*[@data-props-id='membershipName']"
                )
                text = cell.text.strip()
            except StaleElementReferenceException:
                continue

            if text:
                names.append(text)

        return names

    def get_visible_membership_count(self):
        """Return current visible membership row count."""
        return len(self.get_visible_membership_names())

    def no_records_message_is_visible(self):
        """Return whether the grid empty-state message is visible."""
        return self.element_is_visible(self.NO_RECORDS_TEXT)

    def pagination_controls_are_visible(self):
        """Return whether pagination or result count controls are visible."""
        return self.element_is_visible(self.PAGINATION_TEXT)

    def results_per_page_control_is_visible(self):
        """Return whether results-per-page control is visible."""
        body_text = self.get_body_text()
        return (
            "Results per page" in body_text
            or "Show 100" in body_text
            or self.element_is_visible(self.RESULTS_PER_PAGE_SELECT)
        )

    def support_button_is_visible(self):
        """Return whether the support button is visible."""
        self.driver.switch_to.default_content()
        try:
            return any(
                element.is_displayed()
                for element in self.driver.find_elements(*self.SUPPORT_BUTTON)
            )
        finally:
            self.wait_for_list_loaded()

    def every_visible_row_has_edit_action(self):
        """Return whether every visible membership row has an Edit action."""
        try:
            self.wait.until(
                lambda driver: len(self.get_visible_membership_rows()) > 0
            )
        except TimeoutException:
            return False

        rows = self.get_visible_membership_rows()
        if not rows:
            return False

        for row in rows:
            if not row.find_elements(By.XPATH, ".//*[normalize-space()='Edit']"):
                return False

        return True

    def membership_exists(self, membership_name):
        """Return whether the membership exists in the list."""
        self.wait_for_list_loaded()
        self.search_membership(membership_name)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    self.get_membership_row_locator(membership_name)
                )
            )
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
        self.wait_for_grid_idle()

    def clear_membership_search(self):
        """Clear membership search and wait for the grid to refresh."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        self._set_input_value(search_input, "")
        self.wait.until(
            lambda driver: self.driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == ""
        )
        self.wait_for_grid_idle()

    def search_input_value(self):
        """Return current membership search input value."""
        return self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        ).get_attribute("value")

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

    def _show_inactive_memberships(self):
        """Apply the inactive filter so hidden inactive rows become visible.

        Clears any active search first — the Filter button can be unavailable
        when the grid is in an empty-results state from a no-match search.
        """
        self.clear_membership_search()
        self.open_filter_panel()
        self.set_active_membership_filter(False)
        self.apply_filters()

    def open_filter_panel(self):
        """Open the Memberships filter panel."""
        self.wait_for_list_loaded()
        apply_buttons = self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)
        if not any(el.is_displayed() for el in apply_buttons):
            self.click(self.FILTER_BUTTON)
            self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))

    def get_visible_membership_types(self):
        """Return visible membership type values (e.g. 'Recurring') from the grid."""
        return [
            cell.text.strip()
            for cell in self.driver.find_elements(*self.GRID_TYPE_CELLS)
            if cell.is_displayed() and cell.text.strip()
        ]

    def get_visible_membership_statuses(self):
        """Return visible membership status values (e.g. 'Active') from the grid."""
        return [
            cell.text.strip()
            for cell in self.driver.find_elements(*self.GRID_STATUS_CELLS)
            if cell.is_displayed() and cell.text.strip()
        ]

    def select_membership_type_filter(self, type_text):
        """Open the 'Membership type' filter select and choose an option."""
        self.click(self.MEMBERSHIP_TYPE_FILTER)
        option = (
            By.XPATH,
            "//*[contains(@class,'form-select__option') "
            "and normalize-space()='%s']" % type_text,
        )
        self.wait.until(EC.element_to_be_clickable(option)).click()
        self.wait.until(
            lambda driver: type_text.lower()
            in self.driver.find_element(*self.MEMBERSHIP_TYPE_FILTER).text.lower()
        )

    def select_filter_site(self, site_query):
        """Type a query into the site filter and pick the matching option.

        Returns the chosen site label.
        """
        box = self.wait.until(EC.element_to_be_clickable(self.FILTER_SITE_INPUT))
        box.click()
        box.send_keys(site_query)
        option = (
            By.XPATH,
            "//*[contains(@class,'form-select__option') "
            "and contains(normalize-space(),'%s')]" % site_query,
        )
        chosen = self.wait.until(EC.element_to_be_clickable(option))
        label = chosen.text.strip()
        chosen.click()
        return label

    def set_active_membership_filter(self, on):
        """Set the filter panel 'Active membership' switch to the desired state."""
        if on:
            self.ensure_switch_on(self.ACTIVE_MEMBERSHIP_FILTER_SWITCH)
        else:
            self.ensure_switch_off(self.ACTIVE_MEMBERSHIP_FILTER_SWITCH)

    def has_active_filters(self):
        """Return whether any filters are currently active (instant, no wait)."""
        try:
            btn = self.driver.find_element(*self.FILTER_BUTTON)
            return "(" in btn.text
        except Exception:
            return False

    def clear_active_filters(self):
        """Unconditionally reset all filters and apply, then wait for grid to settle.

        The filter badge count is lazy — it only renders after an interactive
        event (e.g. typing in the search box), never at bare page load.  Checking
        the badge first would always return False and skip the reset, leaving a
        stale server-side filter in place.  Opening the panel and resetting
        unconditionally is the only reliable way to clear the state.

        wait_for_grid_idle() after apply ensures the grid has finished reloading
        before the caller issues a search, preventing a race where the search
        fires while the freshly-cleared grid is still loading.
        """
        import logging as _logging
        _log = _logging.getLogger("nxtwash")
        try:
            self.open_filter_panel()
            self.click(self.RESET_ALL_BUTTON)
            # Re-open panel if Reset All auto-closed it (mirrors user_roles fix)
            apply_btns = self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)
            if not any(el.is_displayed() for el in apply_btns):
                self.click(self.FILTER_BUTTON)
                self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
            self.apply_filters()
            self.wait_for_grid_idle()
            try:
                self.wait.until(
                    lambda driver: "Filter by (" not in driver.find_element(
                        By.TAG_NAME, "body"
                    ).text
                )
            except Exception:
                pass
        except Exception as exc:
            _log.warning("clear_active_filters: reset/apply failed: %s", exc)
        # Belt-and-suspenders: reset the Redux Persist filter state directly.
        # The app stores filter state in persist:root → tableFilterReducer →
        # tableFilters.memberships.  If the UI-based reset above failed to commit
        # the change (e.g. Apply Filters timed out), the stale isActive:false value
        # persists in localStorage and is rehydrated by Redux on the next navigation.
        # Resetting it here guarantees the next page load starts with the default filter.
        try:
            self.driver.execute_script("""
                try {
                    var root = JSON.parse(localStorage.getItem('persist:root') || '{}');
                    var tfr = JSON.parse(root.tableFilterReducer || '{}');
                    var tf = tfr.tableFilters || {};
                    tf.memberships = {
                        type: 0,
                        isActive: true,
                        membershipName: ''
                    };
                    tfr.tableFilters = tf;
                    root.tableFilterReducer = JSON.stringify(tfr);
                    localStorage.setItem('persist:root', JSON.stringify(root));
                } catch(e) {}
            """)
        except Exception as exc:
            _log.warning("clear_active_filters: redux persist reset failed: %s", exc)

    def apply_filters(self):
        """Apply the configured filters and wait for the grid to refresh."""
        sentinel_rows = self.driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'InovuaReactDataGrid__row') "
            "and .//*[@data-props-id='membershipName']]"
        )
        sentinel = sentinel_rows[0] if sentinel_rows else None
        self.click(self.APPLY_FILTERS_BUTTON)
        self.wait.until(
            EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON)
        )
        self.wait_for_list_loaded()
        if sentinel is not None:
            try:
                self.wait.until(EC.staleness_of(sentinel))
            except Exception:
                pass

    def reset_filters(self):
        """Open the filter panel and reset all filters back to defaults."""
        self.open_filter_panel()
        self.click(self.RESET_ALL_BUTTON)

    def download_button_is_clickable(self):
        """Return whether the download button can be clicked."""
        return self.wait.until(
            EC.element_to_be_clickable(self.DOWNLOAD_BUTTON)
        ).is_displayed()

    def click_download_memberships(self):
        """Click the memberships download button."""
        self.click(self.DOWNLOAD_BUTTON)

    def open_create_membership(self):
        """Open create membership form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_MEMBERSHIP_BUTTON)
        self.wait_for_create_loaded()

    def click_cancel(self):
        """Click cancel on create/edit form."""
        self.click(self.CANCEL_BUTTON)
        self.wait_for_list_loaded()

    def open_edit_membership_if_visible(self, membership_name):
        """Open edit for a membership that is already visible in the current list.

        Skips the wait_for_list_loaded() call that open_edit_membership() does.
        Use this when you are already in the list frame (e.g. after
        open_memberships_page()) to avoid an extra ~100 s reload on slow staging.
        Falls back to showing inactive rows if the membership is not found active.
        """
        self.search_membership(membership_name)
        self.wait_for_grid_idle()
        try:
            row = self.wait_for_membership_row(membership_name)
        except TimeoutException:
            self._show_inactive_memberships()
            self.search_membership(membership_name)
            self.wait_for_grid_idle()
            row = self.wait_for_membership_row(membership_name)
        edit_button = row.find_element(
            By.XPATH,
            ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        self.wait_for_grid_idle()
        self.driver.execute_script("arguments[0].click();", edit_button)
        self.wait_for_edit_loaded()

    def open_edit_membership(self, membership_name):
        """Open edit membership form, falling back to inactive filter if needed."""
        self.wait_for_list_loaded()
        self.search_membership(membership_name)
        self.wait_for_grid_idle()
        try:
            row = self.wait_for_membership_row(membership_name)
        except TimeoutException:
            self._show_inactive_memberships()
            self.search_membership(membership_name)
            self.wait_for_grid_idle()
            row = self.wait_for_membership_row(membership_name)
        edit_button = row.find_element(
            By.XPATH,
            ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        self.wait_for_grid_idle()
        self.driver.execute_script("arguments[0].click();", edit_button)
        self.wait_for_edit_loaded()

    def enter_membership_name(self, membership_name):
        """Enter membership name."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.MEMBERSHIP_NAME_INPUT)
        )
        self._set_input_value(element, membership_name)

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

    def select_recurring_membership_type(self):
        """Select Recurring membership type."""
        radio = self.wait.until(
            EC.presence_of_element_located(self.RECURRING_RADIO)
        )
        if not radio.is_selected():
            radio.click()
            self.wait.until(
                lambda driver: driver.find_element(
                    *self.RECURRING_RADIO
                ).is_selected()
            )

    def recurring_membership_type_is_selected(self):
        """Return whether Recurring membership type is selected."""
        radio = self.wait.until(
            EC.presence_of_element_located(self.RECURRING_RADIO)
        )
        return radio.is_selected()

    def prepaid_membership_type_is_selected(self):
        """Return whether Prepaid membership type is selected."""
        radio = self.wait.until(EC.presence_of_element_located(self.PREPAID_RADIO))
        return radio.is_selected()

    def set_prepaid_months(self, months):
        """Set prepaid membership duration months."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.PREPAID_MONTHS_INPUT)
        )
        self.set_grid_input_value(element, months)

    def set_barcode(self, barcode):
        """Set membership barcode."""
        element = self.wait.until(EC.visibility_of_element_located(self.BARCODE_INPUT))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({ block: 'center' }); arguments[0].focus();",
            element
        )
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(str(barcode))
        self.driver.execute_script(
            """
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            element
        )
        self.wait.until(
            lambda driver: driver.find_element(
                *self.BARCODE_INPUT
            ).get_attribute("value") == str(barcode)
        )

    def get_barcode_value(self):
        """Return membership barcode value."""
        element = self.wait.until(EC.visibility_of_element_located(self.BARCODE_INPUT))
        return element.get_attribute("value")

    def _expand_description_accordion(self):
        """Expand the Membership description accordion if it is collapsed."""
        textarea_els = self.driver.find_elements(*self.DESCRIPTION_TEXTAREA)
        if textarea_els and textarea_els[0].is_displayed():
            return
        header = self.wait.until(
            EC.element_to_be_clickable(self.DESCRIPTION_ACCORDION_HEADER)
        )
        header.click()
        self.wait.until(EC.visibility_of_element_located(self.DESCRIPTION_TEXTAREA))

    def set_membership_description(self, description):
        """Expand the description accordion and set the textarea value."""
        self._expand_description_accordion()
        element = self.wait.until(
            EC.visibility_of_element_located(self.DESCRIPTION_TEXTAREA)
        )
        element.clear()
        element.send_keys(description)

    def get_membership_description_value(self):
        """Expand the description accordion and return the textarea value."""
        self._expand_description_accordion()
        element = self.wait.until(
            EC.visibility_of_element_located(self.DESCRIPTION_TEXTAREA)
        )
        return element.get_attribute("value")

    def set_redemption_limits(self, per_day="1", per_week="7", per_month="30"):
        """Fill the per-period redemption limit inputs revealed by the Limit Membership toggle."""
        for locator, value in [
            (self.LIMIT_PER_DAY_INPUT, per_day),
            (self.LIMIT_PER_WEEK_INPUT, per_week),
            (self.LIMIT_PER_MONTH_INPUT, per_month),
        ]:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            self.set_grid_input_value(element, value)

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
        self.set_grid_input_value(element, points)

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
        self.set_grid_input_value(element, price)

    def get_global_price_value(self):
        """Return membership global price input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return element.get_attribute("value")

    def global_price_input_is_valid(self):
        """Return native validity state for global price input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def get_global_price_validation_message(self):
        """Return native validation message for global price input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def set_global_commission(self, commission):
        """Set membership global commission."""
        elements = self.wait.until(
            EC.visibility_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        element = elements[0]
        self.set_grid_input_value(element, commission)

    def get_global_commission_value(self):
        """Return membership global commission input value."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        return elements[0].get_attribute("value")

    def global_commission_input_is_valid(self):
        """Return native validity state for global commission input."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            elements[0]
        )

    def get_global_commission_validation_message(self):
        """Return native validation message for global commission input."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            elements[0]
        )

    def switch_is_on(self, locator):
        """Return whether a switch is on."""
        switch = self.wait.until(EC.presence_of_element_located(locator))
        return switch.get_attribute("aria-checked") == "true"

    def ensure_switch_on(self, locator):
        """Turn a switch on if needed."""
        switch = self.wait.until(EC.visibility_of_element_located(locator))
        if switch.get_attribute("aria-checked") != "true":
            ActionChains(self.driver).move_to_element(switch).click().perform()
            self.wait.until(
                lambda driver: driver.find_element(*locator)
                               .get_attribute("aria-checked") == "true"
            )

    def ensure_switch_off(self, locator):
        """Turn a switch off if needed."""
        switch = self.wait.until(EC.visibility_of_element_located(locator))
        if switch.get_attribute("aria-checked") != "false":
            ActionChains(self.driver).move_to_element(switch).click().perform()
            self.wait.until(
                lambda driver: driver.find_element(*locator)
                               .get_attribute("aria-checked") == "false"
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

    def ensure_customer_portal_switch_off(self):
        """Turn Show on customer portal off if needed."""
        self.ensure_switch_off(self.CUSTOMER_PORTAL_SWITCH)

    def limit_membership_switch_is_on(self):
        """Return whether Limit membership switch is on."""
        return self.switch_is_on(self.LIMIT_MEMBERSHIP_SWITCH)

    def ensure_limit_membership_switch_on(self):
        """Turn Limit membership on if needed."""
        self.ensure_switch_on(self.LIMIT_MEMBERSHIP_SWITCH)

    def ensure_active_switch_off(self):
        """Turn Active service off if needed."""
        self.ensure_switch_off(self.ACTIVE_SWITCH)

    def open_membership_settings(self):
        """Open Membership settings tab."""
        tab = self.wait.until(
            EC.presence_of_element_located(self.MEMBERSHIP_SETTINGS_TAB)
        )
        self.driver.execute_script("arguments[0].click();", tab)
        self.wait.until(
            EC.visibility_of_element_located(self.MEMBERSHIP_NAME_INPUT)
        )
        self.wait_for_grid_idle()

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
            EC.element_to_be_clickable(self.DISCOUNT_SETTINGS_TAB)
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
        rows = WebDriverWait(self.driver, 60).until(
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
        self.open_membership_settings()
        try:
            checkbox = self.get_location_checkbox_by_index(row_index)
            return self.row_checkbox_is_checked(checkbox)
        except AssertionError:
            return False

    def _click_location_checkbox(self, checkbox):
        """Toggle a location assignment checkbox via ActionChains on the checkbox element.

        Clicking the InovuaReactDataGrid__cell center misses the checkbox on
        expanded (already-assigned) rows because the cell is taller than the
        checkbox widget.  Targeting the checkbox element directly with a real
        (trusted) mouse event is reliable for both checked and unchecked rows
        and correctly propagates through Inovua → React Hook Form onChange.
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'nearest'});",
            checkbox,
        )
        ActionChains(self.driver).move_to_element(checkbox).click().perform()

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

        checkbox = rows[row_index].find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
        )

        if not self.row_checkbox_is_checked(checkbox):
            self._click_location_checkbox(checkbox)
            self.wait.until(
                lambda driver: self.row_checkbox_is_checked(
                    self.get_location_rows()[row_index].find_element(
                        By.XPATH,
                        ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
                    )
                )
            )

        # Set price/commission after assigning — the checkbox reveal may clear fields.
        self.set_location_price_and_commission_by_index(row_index, price, commission)

    def unassign_location_by_index(self, row_index):
        """Unassign one visible location row if it is checked."""
        rows = self.get_location_rows()

        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (row_index + 1, len(rows))
            )

        checkbox = rows[row_index].find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
        )

        if self.row_checkbox_is_checked(checkbox):
            self._click_location_checkbox(checkbox)
            self.wait.until(
                lambda driver: not self.row_checkbox_is_checked(
                    self.get_location_rows()[row_index].find_element(
                        By.XPATH,
                        ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
                    )
                )
            )

    def unassign_locations_after_first(self):
        """Keep only the first visible location assigned."""
        for row_index in range(1, len(self.get_location_rows())):
            self.unassign_location_by_index(row_index)

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
        """Set a React grid input value without appending to stale text."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({ block: 'center' });"
            "arguments[0].focus();",
            element
        )
        element.send_keys(Keys.CONTROL, "a")
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

    def fill_required_unassigned_location_values(self):
        """Fill required grid inputs for unassigned locations without assigning."""
        for row_index in range(1, len(self.get_location_rows())):
            self.set_location_price_and_commission_by_index(row_index, "0", "0")

    def get_redemption_rows(self):
        """Return unique visible redemption location rows."""
        rows = WebDriverWait(self.driver, 60).until(
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
            for checkbox in WebDriverWait(self.driver, 60).until(
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
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'nearest'});", checkbox
            )
            ActionChains(self.driver).move_to_element(checkbox).click().perform()
            self.wait.until(
                lambda driver: self.row_checkbox_is_checked(
                    [
                        cb
                        for cb in driver.find_elements(*self.REDEMPTION_CHECKBOXES)
                        if cb.rect["width"] > 0 and cb.rect["height"] > 0
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
        option = WebDriverWait(self.driver, 20).until(
            lambda d: self._find_react_option(service_name)
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
        self.wait_for_grid_idle()
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

        self.select_react_dropdown_option(
            self.APPLICABLE_DISCOUNTS_COMBOBOX, discount_name, clear_first=False
        )
        self.wait.until(lambda driver: self.discount_is_selected(discount_name))

    def deselect_applicable_discount(self, discount_name):
        """Remove a previously selected applicable discount."""
        self.open_discount_settings()
        remove_button = (
            By.XPATH,
            "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
            "//*[contains(@class,'form-select__multi-value')"
            " and .//*[normalize-space()='%s']]"
            "//*[contains(@class,'form-select__multi-value__remove')]"
            % discount_name
        )
        btn = self.wait.until(EC.element_to_be_clickable(remove_button))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(
            lambda driver: not self.discount_is_selected(discount_name)
        )

    def clear_applicable_discounts(self):
        """Remove all applicable discounts from the Discount settings tab."""
        self.open_discount_settings()
        remove_locator = (
            By.XPATH,
            "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
            "//*[contains(@class,'form-select__multi-value__remove')]"
        )
        while True:
            visible = [
                b for b in self.driver.find_elements(*remove_locator)
                if b.is_displayed()
            ]
            if not visible:
                break
            count_before = len(visible)
            self.driver.execute_script("arguments[0].click();", visible[0])
            self.wait.until(
                lambda driver, n=count_before: len([
                    b for b in driver.find_elements(*remove_locator)
                    if b.is_displayed()
                ]) < n
            )

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
        self.save_and_return_to_list()

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

    def save_and_return_to_list(self):
        """Save the current membership form and return to the list page.

        Patches window.confirm so deactivation dialogs are auto-accepted.
        The app no longer auto-redirects after save, so we force-navigate fresh.
        Waits for the save button to go disabled then re-enabled so we know the
        API call completed before we navigate away.
        """
        import time
        self.driver.execute_script("window.confirm = () => true;")
        self.click(self.SAVE_MEMBERSHIP_BUTTON)
        # Wait for button to go disabled (save in progress), then re-enabled
        # (save done).  Fall back to a fixed 8-second sleep if the button
        # never disables (i.e., the app doesn't reflect save state on it).
        try:
            self.wait.until(
                lambda driver: not driver.find_element(
                    *self.SAVE_MEMBERSHIP_BUTTON
                ).is_enabled()
            )
            self.wait.until(
                EC.element_to_be_clickable(self.SAVE_MEMBERSHIP_BUTTON)
            )
        except Exception:
            time.sleep(8)
        # Capture any visible error before navigating away — if save was rejected
        # (duplicate name, validation) the error shows in the iframe body here.
        save_error = self.get_visible_error()
        # Switch to the top-level document first so current_url is the main
        # page URL (the iframe URL can be null after a form submission).
        self.driver.switch_to.default_content()
        current = self.driver.current_url or ""
        if "/services/" in current:
            base_url = current.split("/services/")[0]
        else:
            base_url = current.rstrip("/")
        try:
            self.driver.get(base_url + "/services/memberships")
        except TimeoutException:
            pass  # page load timeout on slow staging; iframe content may still render
        self.wait_for_list_loaded()
        if save_error:
            import logging
            logging.getLogger("nxtwash").warning(
                "Membership save completed with page error: %s", save_error
            )

    def duplicate_membership_error_is_visible(self):
        """Return whether a duplicate membership error is visible."""
        body_text = self.get_body_text().lower()
        return "already exists" in body_text or "duplicate" in body_text

    def wait_for_duplicate_membership_error(self):
        """Wait until a duplicate membership validation/error is visible."""
        self.wait.until(lambda driver: self.duplicate_membership_error_is_visible())

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
        self.ensure_switch_off(self.LIMIT_MEMBERSHIP_SWITCH)
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
        self.unassign_locations_after_first()

    def fill_recurring_membership_form(
        self,
        membership_name,
        global_price,
        global_commission,
        first_location_price,
        first_location_commission
    ):
        """Fill membership settings for a recurring membership."""
        self.enter_membership_name(membership_name)
        self.select_recurring_membership_type()
        self.ensure_active_switch_on()
        self.ensure_customer_portal_switch_on()
        self.ensure_switch_off(self.LIMIT_MEMBERSHIP_SWITCH)
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
        self.unassign_locations_after_first()

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
        self.save_and_return_to_list()

    def create_recurring_membership(
        self,
        membership_name,
        global_price,
        global_commission,
        first_location_price,
        first_location_commission
    ):
        """Create an active recurring membership and return to list."""
        self.open_create_membership()
        self.fill_recurring_membership_form(
            membership_name,
            global_price,
            global_commission,
            first_location_price,
            first_location_commission
        )
        self.save_and_return_to_list()

    def update_membership_name(self, current_name, updated_name):
        """Update membership name and return to list."""
        self.open_edit_membership(current_name)
        self.enter_membership_name(updated_name)
        self.save_and_return_to_list()
