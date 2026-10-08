import json
import time

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage
from pages.common.base_page import SELECT_ALL_KEY


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
    SEARCH_INPUT = (By.NAME, "membershipName")
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
        self.dismiss_dev_toast()
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

    def wait_for_membership_row(self, membership_name, attempts=6, per_try=10):
        """Wait until a membership row is present.

        The list search is served by an index that lags behind saves: right
        after a create, searching the new name can return no rows for a few
        seconds. If the search box already holds this name, re-run the search
        between short waits instead of one long wait on a stale result. Uses
        presence (not visibility) — InovuaReactDataGrid uses CSS transforms,
        which make the visibility check unreliable (same as wash_packages).
        """
        locator = self.get_membership_row_locator(membership_name)
        for attempt in range(attempts):
            try:
                return WebDriverWait(self.driver, per_try).until(
                    EC.presence_of_element_located(locator)
                )
            except TimeoutException:
                if attempt == attempts - 1:
                    raise
                boxes = self.driver.find_elements(*self.SEARCH_INPUT)
                if boxes and (boxes[0].get_attribute("value") or "") == membership_name:
                    self.search_membership(membership_name)

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
            self.wait_for_membership_row(membership_name)
            return True
        except TimeoutException:
            return False

    def search_membership(self, membership_name):
        """Search membership by name.

        Uses Cmd+A → Backspace to clear so React's onChange fires correctly.
        Ctrl+A on macOS Chrome moves the cursor to start of line rather than
        selecting all text, causing repeated searches to append instead of replace.
        """
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_input.click()
        search_input.send_keys(SELECT_ALL_KEY + "a" + Keys.NULL + Keys.BACKSPACE)
        search_input.send_keys(membership_name)
        self.wait.until(
            lambda driver: self.driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == membership_name
        )
        self.wait_for_grid_idle()
        # React may update the controlled input asynchronously after the grid
        # renders a zero-results state (deferred setState clears the value).
        # Poll until two consecutive reads agree so the caller sees the final
        # stable value rather than a transient intermediate state.
        prev = object()
        for _ in range(8):
            curr = self.driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value")
            if curr == prev:
                break
            prev = curr
            time.sleep(0.1)

    def clear_membership_search(self):
        """Clear membership search and wait for the grid to refresh."""
        search_input = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_input.click()
        search_input.send_keys(SELECT_ALL_KEY + "a" + Keys.NULL + Keys.BACKSPACE)
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
        """Open the Memberships filter panel (idempotent)."""
        self.wait_for_list_loaded()
        if any(el.is_displayed() for el in self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)):
            return
        btn = self.wait.until(EC.presence_of_element_located(self.FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.visibility_of_element_located(self.FILTER_SITE_INPUT))
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
        """Return whether any filters are currently active."""
        try:
            btn = self.driver.find_element(*self.FILTER_BUTTON)
            return "(" in btn.text
        except Exception:
            return False

    def clear_active_filters(self):
        """Reset all filters to guarantee clean state."""
        if not self.has_active_filters():
            return
        try:
            self.reset_filters()
        except Exception:
            pass

    def apply_filters(self):
        """Apply the configured filters and wait for the grid to refresh."""
        sentinel_rows = self.driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'InovuaReactDataGrid__row') "
            "and .//*[@data-props-id='membershipName']]"
        )
        sentinel = sentinel_rows[0] if sentinel_rows else None
        self.click(self.APPLY_FILTERS_BUTTON)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        self.wait.until(EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON))
        self.wait_for_list_loaded()
        if sentinel is not None:
            try:
                self.wait.until(EC.staleness_of(sentinel))
            except Exception:
                pass

    def reset_filters(self):
        """Open the filter panel and reset all filters back to defaults."""
        self.open_filter_panel()
        reset_btn = self.wait.until(EC.presence_of_element_located(self.RESET_ALL_BUTTON))
        self.driver.execute_script("arguments[0].click();", reset_btn)
        apply_btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
        self.driver.execute_script("arguments[0].click();", apply_btn)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        self.wait.until(EC.invisibility_of_element_located(self.APPLY_FILTERS_BUTTON))

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
        # SELECT_ALL_KEY stays its own call: Selenium sends one combined text
        # string per send_keys() call, and ChromeDriver holds a modifier key
        # down for the rest of whatever's in THAT string — merging backspace
        # and the barcode in with it meant they were sent as Ctrl/Cmd+<key>,
        # which does nothing in a plain input, so the value never changed
        # (confirmed in CI: test_edit_managed_membership_barcode_persists and
        # test_duplicate_barcode_is_rejected both hung forever waiting for a
        # value update that could never happen). Keys.BACKSPACE + the new
        # value don't involve a modifier, so merging those two is still safe.
        element.send_keys(SELECT_ALL_KEY, "a")
        element.send_keys(Keys.BACKSPACE, str(barcode))
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
        """Return unique location assignment rows currently mounted.

        The grid virtualizes (InovuaReactDataGrid) — this only reflects
        whatever is in the current scroll window. Use get_location_row(name)
        to reliably find a specific row, including one scrolled out of view.

        Reads every row's text in one JS round-trip instead of one
        row.text call per row — same fix, same reason, as the sibling
        get_redemption_rows(): with enough location rows mounted, a
        per-row .text loop is slow enough on a loaded host to meaningfully
        add to this method's cost every time it's called. Read-only — no
        write technique involved, so none of the stale-state risk that
        applies to set_grid_input_value here.
        """
        def _do():
            rows = WebDriverWait(self.driver, 60).until(
                EC.presence_of_all_elements_located(self.LOCATION_ROWS)
            )
            texts = self.driver.execute_script(
                "return arguments[0].map(function(el) { return el.innerText || ''; });",
                rows
            )
            unique_rows = []
            seen_locations = set()

            for row, text in zip(rows, texts):
                lines = [
                    line.strip()
                    for line in text.splitlines()
                    if line.strip()
                ]
                location_key = "\n".join(lines[:2])

                if not location_key or location_key in seen_locations:
                    continue

                seen_locations.add(location_key)
                unique_rows.append(row)

            return unique_rows

        return self._retry_transient(_do)

    def get_location_name_by_index(self, row_index):
        """Return the site name of whichever row is currently at ``row_index``.

        For picking a row to act on when the caller doesn't care which site.
        NOT stable across a save/reload — the grid virtualizes, so "row 0"
        can render as a different site after a fresh page load (this was the
        root cause of the index-based methods this file used to have; see
        docs/admin_test_coverage.md). Capture the name here once and address
        the row by name afterwards (get_location_row(), location_is_assigned(),
        ...) if it needs to survive a reload.
        """
        rows = self.get_location_rows()

        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s location rows, found %s"
                % (row_index + 1, len(rows))
            )

        lines = [
            line.strip() for line in rows[row_index].text.splitlines() if line.strip()
        ]
        return lines[0]

    def row_checkbox_is_checked(self, checkbox):
        """Return whether an Inovua checkbox is checked."""
        classes = checkbox.get_attribute("class")
        return (
            "inovua-react-toolkit-checkbox--checked" in classes
            and "inovua-react-toolkit-checkbox--unchecked" not in classes
        )

    def _scroll_grid_to_find_row(self, row_xpath, container_selector):
        """Scroll a virtualized Inovua grid until ``row_xpath`` is mounted.

        Both the location-assignment and redemption-location grids
        (InovuaReactDataGrid) recycle row DOM nodes: a row scrolled out of
        the actively-rendered window isn't removed, it's repositioned to a
        (0-width, 0-height) pooled state with stale content and left in the
        DOM — confirmed live, including with the row's OWN text still
        matching (so a presence-only check finds it and wrongly treats it as
        usable; its checkbox is then unclickable — "has no size and
        location"). A real, currently-rendered row always has non-zero
        width even when its own height is legitimately 0 (a positioning
        wrapper around visible child content) — that's the check below.
        Ported from WashPackagesPage.get_site_row(): find the grid's own
        scrollable container and step scrollTop through it, checking for a
        REAL row after each step (bypasses the WheelEvent -> React-state ->
        scroll-reset cycle that broke a simpler drag/scroll approach).
        """
        def _real(el):
            rect = el.rect
            return rect["width"] > 0

        els = [el for el in self.driver.find_elements(*row_xpath) if _real(el)]
        if els:
            return els[0]

        selector_json = json.dumps(container_selector)
        find_scroller_js = (
            "var vl = document.querySelector(%s);"
            "if (!vl) return null;"
            "var kids = Array.from(vl.querySelectorAll('div'));"
            "for (var i = 0; i < kids.length; i++) {"
            "  if (kids[i].scrollHeight > kids[i].clientHeight + 50)"
            "    return kids[i].scrollHeight - kids[i].clientHeight;"
            "}"
            "return null;"
        ) % selector_json
        max_scroll = self.driver.execute_script(find_scroller_js)
        if max_scroll is None:
            max_scroll = 4000

        set_scroll_js = (
            "var vl = document.querySelector(%s);"
            "if (!vl) return;"
            "var kids = Array.from(vl.querySelectorAll('div'));"
            "for (var i = 0; i < kids.length; i++) {"
            "  if (kids[i].scrollHeight > kids[i].clientHeight + 50) {"
            "    kids[i].scrollTop = arguments[0];"
            "    return;"
            "  }"
            "}"
        ) % selector_json

        step = 350
        for pos in range(0, int(max_scroll) + step, step):
            self.driver.execute_script(set_scroll_js, min(pos, int(max_scroll)))
            time.sleep(0.12)
            els = [el for el in self.driver.find_elements(*row_xpath) if _real(el)]
            if els:
                return els[0]

        return WebDriverWait(self.driver, 30).until(
            lambda d: next(
                (el for el in d.find_elements(*row_xpath) if _real(el)), False
            )
        )

    def get_location_row(self, site_name):
        """Return the location assignment grid row for a site, by name.

        Index-based lookup broke once the site count grew past one screen
        (now 20+) and after any reload that resets the grid's scroll window.
        This finds the row by its visible site name instead, which stays
        correct regardless of scroll position or row count.

        Checks get_location_rows()'s full, freshly-fetched list first — a
        single raw XPath lookup for the name is more likely to match a
        recycled/pooled (0-width) node (see _scroll_grid_to_find_row) than
        this Python-side scan is, confirmed live.
        """
        self.open_membership_settings()
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(self.LOCATION_ROWS)
        )
        for row in self.get_location_rows():
            if site_name in row.text and row.rect["width"] > 0:
                return row

        row_xpath = (
            By.XPATH,
            "//*[contains(@class,'InovuaReactDataGrid__row') "
            "and .//*[contains(@class,'inovua-react-toolkit-checkbox')]]"
            "[.//*[normalize-space()='%s']]" % site_name,
        )
        return self._scroll_grid_to_find_row(
            row_xpath, "[class*=\"InovuaReactDataGrid__virtual-list\"]"
        )

    def _location_checkbox(self, site_name):
        return self._retry_transient(
            lambda: self.get_location_row(site_name).find_element(
                By.XPATH, ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
            )
        )

    def location_is_assigned(self, site_name):
        """Return whether a location (by site name) is assigned."""
        try:
            return self.row_checkbox_is_checked(self._location_checkbox(site_name))
        except (TimeoutException, NoSuchElementException):
            return False

    _ASSIGNED_NAME_JS = """
        return arguments[0].map(function(row) {
            var rect = row.getBoundingClientRect();
            var checkbox = row.querySelector('[class*="inovua-react-toolkit-checkbox"]');
            var cls = checkbox ? checkbox.className : '';
            var checked = cls.indexOf('inovua-react-toolkit-checkbox--checked') !== -1
                && cls.indexOf('inovua-react-toolkit-checkbox--unchecked') === -1;
            return {width: rect.width, checked: checked, text: row.innerText || ''};
        });
    """

    def _assigned_names_from_rows(self, rows):
        """Site names of assigned (checked), currently-rendered rows, read in one JS call.

        Replaces a per-row loop that did 3-4 WebDriver round-trips each
        (rect, find the checkbox, read its class, read the row's text) —
        same batching rationale as get_location_rows()/get_redemption_rows().
        """
        if not rows:
            return []
        results = self.driver.execute_script(self._ASSIGNED_NAME_JS, rows)
        names = []
        for info in results:
            if info["width"] <= 0:
                continue  # recycled/pooled node — see _scroll_grid_to_find_row
            if not info["checked"]:
                continue
            lines = [line.strip() for line in info["text"].splitlines() if line.strip()]
            if lines:
                names.append(lines[0])
        return names

    def assigned_location_names(self):
        """Return the site names of every currently-mounted, assigned location row."""
        self.open_membership_settings()
        return self._assigned_names_from_rows(self.get_location_rows())

    def _click_location_checkbox(self, checkbox):
        """Toggle a location assignment checkbox via ActionChains on the checkbox element.

        Clicking the InovuaReactDataGrid__cell center misses the checkbox on
        expanded (already-assigned) rows because the cell is taller than the
        checkbox widget.  Targeting the checkbox element directly with a real
        (trusted) mouse event is reliable for both checked and unchecked rows
        and correctly propagates through Inovua → React Hook Form onChange.

        block: 'center', not 'nearest' — confirmed live: a row scrolled to
        just below the grid's sticky header reports a real, non-zero rect
        (so 'nearest' treats it as already in view and does nothing), but
        the header visually overlaps it, so the click silently lands on the
        header instead of the checkbox (no exception, checkbox never
        toggles). Centering it guarantees clear space above and below.
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            checkbox,
        )
        ActionChains(self.driver).move_to_element(checkbox).click().perform()

    def _toggle_checkbox_until(
        self, get_checkbox, click_checkbox, target_checked, attempts=5, per_attempt_timeout=3
    ):
        """Click a checkbox until it reaches ``target_checked``, retrying the click itself.

        A click here can complete with no exception yet not actually toggle
        the checkbox — confirmed live, apparently a genuine race in the app
        (not a geometry/overlap issue: reproduced and later failed to
        reproduce with identical element coordinates). So this retries the
        whole find-click-verify cycle with a short per-attempt wait, instead
        of one click followed by one long wait that has no recourse if that
        single click silently didn't register.

        ``attempts``/``per_attempt_timeout`` are overridable because retrying
        is only worth its cost when the checkbox has a real chance of
        catching up — unassign specifically almost never does (BUG 8,
        docs/bug_reports.md): the change is not reflected in what gets saved
        at all, not delayed, so retrying the default 5×3s budget against a
        known-broken record is pure wasted wall-clock time. Bulk cleanup
        (unassign_locations_after_first) passes a much smaller budget.
        """
        for attempt in range(attempts):
            checkbox = get_checkbox()
            if self.row_checkbox_is_checked(checkbox) == target_checked:
                return
            click_checkbox(checkbox)
            try:
                WebDriverWait(self.driver, per_attempt_timeout, poll_frequency=0.2).until(
                    lambda driver: self.row_checkbox_is_checked(get_checkbox())
                    == target_checked
                )
                return
            except TimeoutException:
                if attempt == attempts - 1:
                    raise

    def assign_location_with_price_and_commission(self, site_name, price, commission):
        """Assign a location (by site name) and set its price/commission."""
        self._retry_transient(
            lambda: self._toggle_checkbox_until(
                lambda: self._location_checkbox(site_name),
                self._click_location_checkbox,
                True,
            )
        )

        # Set price/commission after assigning — the checkbox reveal may clear fields.
        self.set_location_price_and_commission(site_name, price, commission)

    def unassign_location(self, site_name, attempts=5, per_attempt_timeout=3):
        """Unassign a location (by site name) if it is currently assigned.

        ``attempts``/``per_attempt_timeout`` default to a generous budget for
        callers that need a real unassign to actually land. Bulk cleanup
        (unassign_locations_after_first) overrides both to fail fast — see
        _toggle_checkbox_until for why.
        """
        self._retry_transient(
            lambda: self._toggle_checkbox_until(
                lambda: self._location_checkbox(site_name),
                self._click_location_checkbox,
                False,
                attempts=attempts,
                per_attempt_timeout=per_attempt_timeout,
            )
        )

    def unassign_locations_after_first(self, keep_site_name):
        """Unassign every currently-mounted, assigned location except ``keep_site_name``.

        Best-effort per location, with a deliberately small retry budget
        (1 attempt, ~1.5s): the location-assignment checkbox's visual state
        does not reliably persist through Save on staging (confirmed — see
        BUG 8, docs/bug_reports.md), so an unassign click essentially never
        catches up no matter how long we wait — this isn't transient, so the
        default 5×3s budget per location is pure wasted wall-clock time here.
        Measured impact: adopted leftover records can carry over a dozen
        stale locations (nothing has ever successfully unassigned them,
        since BUG 8 blocks that too), so at the default budget this step
        alone was costing several minutes of setup time per test. One
        unreachable checkbox must not crash setup for every other test that
        goes through fill_membership_form() either — log and move on, and
        let the test's own assertions (not this cleanup step) surface
        whether BUG 8 affected that specific test.
        """
        import logging
        for name in self.assigned_location_names():
            if name == keep_site_name:
                continue
            try:
                self.unassign_location(name, attempts=1, per_attempt_timeout=1.5)
            except Exception as error:  # noqa: BLE001
                logging.getLogger("nxtwash").warning(
                    "Could not unassign location '%s' (likely BUG 8): %s",
                    name, error,
                )

    def _retry_transient(self, fn, attempts=4, delay=0.5):
        """Retry ``fn`` on a handful of "the grid is mid-re-render" errors.

        The grid re-renders its row list on essentially every interaction
        (checkbox toggle, field blur) — confirmed live: a row/element found a
        moment ago can transiently fail a fresh lookup, or fail to click
        (ElementNotInteractableException: "has no size and location", seen
        live right after editing ~19 other rows' fields shifted layout),
        then succeed again a few hundred ms later. This is not the row
        actually being gone (see get_location_row()'s scroll-search for
        that case) — it is this app's grid settling after a change, so a
        short retry that re-fetches the element fresh is the fix, not a
        longer wait on any single lookup or reusing the stale handle.
        """
        last_error = None
        for _ in range(attempts):
            try:
                return fn()
            except (
                NoSuchElementException,
                StaleElementReferenceException,
                ElementNotInteractableException,
            ) as error:
                last_error = error
                time.sleep(delay)
        raise last_error

    def set_location_price_and_commission(self, site_name, price, commission):
        """Set price/commission for a location row (by site name) without (re)assigning it."""
        def _do():
            row = self.get_location_row(site_name)
            price_input = row.find_element(By.NAME, "price")
            commission_input = row.find_element(By.NAME, "commission")
            self.set_grid_input_value(price_input, price)
            self.set_grid_input_value(commission_input, commission)

        self._retry_transient(_do)

    def set_grid_input_value(self, element, value):
        """Set a React grid input value without appending to stale text.

        Keeps the keystroke sequence (not the native-setter write) as the
        primary technique deliberately: fill_all_empty_location_inputs()
        elsewhere in this file documents a confirmed prior incident where
        setting location-grid values via JS made React's handlers run on
        stale state and wipe OTHER rows (17 filled -> 33 empty) — this
        method is itself called in exactly that shape, in a loop over
        unassigned location rows, by fill_required_unassigned_location_values().
        _set_input_value is proven safe as a single-row write elsewhere
        (set_location_price_and_commission here, and the whole of
        wash_packages_page.py), but not proven safe in this multi-row-loop
        shape, and the cost of being wrong is silent data corruption, not
        just a slow test — so it stays the fallback, used only when the
        keystroke write doesn't verify. SELECT_ALL_KEY stays its own call,
        not merged with what follows: ChromeDriver holds a modifier key down
        for the rest of whatever text is in the SAME send_keys() string, so
        combining it with backspace/the new value sends them as Ctrl/Cmd+
        <key> — which does nothing in a plain input (confirmed in CI: this
        exact mistake in set_barcode() made two membership tests hang
        forever waiting for a value that could never change). Keys.BACKSPACE
        and the new value don't involve a modifier, so merging those two is
        still a safe one-round-trip cut.
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView({ block: 'center' });"
            "arguments[0].focus();",
            element
        )
        element.send_keys(SELECT_ALL_KEY, "a")
        element.send_keys(Keys.BACKSPACE, str(value))
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

    def fill_all_empty_location_inputs(self, value="0", max_passes=3):
        """Type ``value`` into every visible, empty per-location price/commission.

        Each staging site adds a required price + commission row, and sites
        accumulate over time. unassign_locations_after_first() empties the
        unassigned rows but the app still marks them required, so the browser's
        HTML5 validation silently blocked Save ("Please fill in this field").

        Uses real key presses: setting values via JS made React's handlers run
        on stale state and wipe other rows (17 filled -> 33 empty).
        """
        import time
        find_empty = (
            "return Array.from(document.querySelectorAll("
            "'input[name=\"price\"], input[name=\"commission\"]'))"
            ".filter(e => e.offsetParent && !e.disabled && e.value === '');"
        )
        for _ in range(max_passes):
            empties = self.driver.execute_script(find_empty)
            if not empties:
                return True
            for element in empties:
                try:
                    element.send_keys(value)
                except Exception:  # noqa: BLE001 — re-queried next pass
                    pass
            time.sleep(0.5)
        return not self.driver.execute_script(find_empty)

    def fill_required_unassigned_location_values(self, skip_site_name=None):
        """Fill required grid inputs for unassigned locations without assigning.

        Acts on each row's held element directly instead of re-finding rows
        by name afterwards — this only needs to touch every row currently in
        the DOM once, not preserve identity across time, so it sidesteps the
        re-render timing that makes name-based re-lookup mid-loop flaky (see
        _retry_transient). A row that's mid-re-render right when we reach it
        is skipped rather than failed — fill_all_empty_location_inputs()
        (called right after this, in fill_membership_form) is a second,
        catch-all pass over whatever's still empty.
        """
        for row in self.get_location_rows():
            if row.rect["width"] <= 0:
                continue  # recycled/pooled node — see _scroll_grid_to_find_row
            lines = [line.strip() for line in row.text.splitlines() if line.strip()]
            name = lines[0] if lines else None
            if not name or name == skip_site_name:
                continue
            try:
                price_input = row.find_element(By.NAME, "price")
                commission_input = row.find_element(By.NAME, "commission")
            except (NoSuchElementException, StaleElementReferenceException):
                continue
            self.set_grid_input_value(price_input, "0")
            self.set_grid_input_value(commission_input, "0")

    def get_redemption_rows(self):
        """Return unique redemption location rows currently mounted.

        Same virtualization caveat as get_location_rows(); use
        get_redemption_row(name) to reliably find a specific row.

        Reads every row's text in one JS round-trip instead of one
        row.text call per row — with enough redemption locations mounted,
        that per-row loop was slow enough on a loaded host to burn through
        a whole test's pytest-timeout budget on its own (confirmed in CI,
        runs 37531450569 / 37538816687: the timeout fired while this exact
        loop was still running, for two different tests). Retried as one
        unit via _retry_transient — a row going stale between the find and
        the script read re-fetches everything fresh rather than reusing a
        now-stale handle.
        """
        def _do():
            rows = WebDriverWait(self.driver, 60).until(
                EC.presence_of_all_elements_located(self.REDEMPTION_ROWS)
            )
            texts = self.driver.execute_script(
                "return arguments[0].map(function(el) { return el.innerText || ''; });",
                rows
            )
            unique_rows = []
            seen_locations = set()

            for row, text in zip(rows, texts):
                lines = [
                    line.strip()
                    for line in text.splitlines()
                    if line.strip()
                ]
                location_key = "\n".join(lines[:2])

                if not location_key or location_key in seen_locations:
                    continue

                seen_locations.add(location_key)
                unique_rows.append(row)

            return unique_rows

        return self._retry_transient(_do)

    def get_redemption_location_name_by_index(self, row_index):
        """Return the site name of whichever redemption row is at ``row_index``.

        Same "pick once, then address by name" caveat as
        get_location_name_by_index — not stable across a reload.
        """
        rows = self.get_redemption_rows()

        if row_index >= len(rows):
            raise AssertionError(
                "Expected at least %s redemption rows, found %s"
                % (row_index + 1, len(rows))
            )

        lines = [
            line.strip() for line in rows[row_index].text.splitlines() if line.strip()
        ]
        return lines[0]

    def get_redemption_row(self, site_name):
        """Return the redemption-location grid row for a site, by name.

        Same virtualized-grid handling and "check the full list first"
        rationale as get_location_row(); scoped to the active tab-pane since
        a hidden tab's grid stays mounted in the DOM. Replaces the old
        per-checkbox ``.rect`` scan (assign_redemption_location_by_index),
        which made one WebDriver round-trip per checkbox on the page and
        could hang for minutes once the location count grew.
        """
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(self.REDEMPTION_ROWS)
        )
        for row in self.get_redemption_rows():
            if site_name in row.text and row.rect["width"] > 0:
                return row

        row_xpath = (
            By.XPATH,
            "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
            "//*[contains(@class,'InovuaReactDataGrid__row') "
            "and .//*[contains(@class,'inovua-react-toolkit-checkbox')]]"
            "[.//*[normalize-space()='%s']]" % site_name,
        )
        return self._scroll_grid_to_find_row(
            row_xpath,
            ".tab-pane.active [class*=\"InovuaReactDataGrid__virtual-list\"]",
        )

    def _redemption_checkbox(self, site_name):
        return self._retry_transient(
            lambda: self.get_redemption_row(site_name).find_element(
                By.XPATH, ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
            )
        )

    def redemption_location_is_assigned(self, site_name):
        """Return whether a redemption location (by site name) is assigned."""
        try:
            return self.row_checkbox_is_checked(self._redemption_checkbox(site_name))
        except (TimeoutException, NoSuchElementException):
            return False

    def assigned_redemption_location_names(self):
        """Return the site names of every currently-mounted, assigned redemption row."""
        return self._assigned_names_from_rows(self.get_redemption_rows())

    def _click_redemption_checkbox(self, checkbox):
        # block: 'center' — see _click_location_checkbox for why not 'nearest'.
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", checkbox
        )
        ActionChains(self.driver).move_to_element(checkbox).click().perform()

    def assign_redemption_location(self, site_name):
        """Assign one redemption location row by site name."""
        self._retry_transient(
            lambda: self._toggle_checkbox_until(
                lambda: self._redemption_checkbox(site_name),
                self._click_redemption_checkbox,
                True,
            )
        )

    def select_redeem_as_option(self, site_name, service_name):
        """Select the Redeem-as service for one redemption row, by site name."""
        def _open_combobox():
            row = self.get_redemption_row(site_name)
            combobox = row.find_element(By.XPATH, ".//input[@role='combobox']")
            combobox.click()
            combobox.send_keys(service_name)
            return True

        self._retry_transient(_open_combobox)
        option = WebDriverWait(self.driver, 20).until(
            lambda d: self._find_react_option(service_name)
        )
        self.driver.execute_script("arguments[0].click();", option)
        self.wait.until(
            lambda driver: service_name.lower() in self.get_body_text().lower()
        )

    def configure_redemption_settings(self, redeem_as_service):
        """Assign a redemption location and set its redeem-as service.

        Picks whichever redemption row renders first — the two callers
        (fill_membership_form/fill_recurring_membership_form) just need any
        one valid redemption location, not a specific site.

        Returns the site name chosen, for callers that want to verify the
        same row persists after a reload.
        """
        self.open_redemption_settings()
        self.wait_for_grid_idle()
        site_name = self.get_redemption_location_name_by_index(0)
        self.assign_redemption_location(site_name)
        self.select_redeem_as_option(site_name, redeem_as_service)
        return site_name

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

    APPLICABLE_DISCOUNT_REMOVE_CHIP = (
        By.XPATH,
        "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
        "//*[contains(@class,'form-select__multi-value__remove')]"
    )

    def has_applicable_discounts(self):
        """Return whether any applicable discount chip is attached (Discount tab)."""
        self.open_discount_settings()
        return any(
            b.is_displayed()
            for b in self.driver.find_elements(*self.APPLICABLE_DISCOUNT_REMOVE_CHIP)
        )

    def clear_applicable_discounts(self):
        """Remove all applicable discounts from the Discount settings tab."""
        self.open_discount_settings()
        remove_locator = self.APPLICABLE_DISCOUNT_REMOVE_CHIP
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

    def get_location_price(self, site_name):
        """Return one location row's price (by site name)."""
        return self._retry_transient(
            lambda: self.get_location_row(site_name)
            .find_element(By.NAME, "price")
            .get_attribute("value")
        )

    def get_location_commission(self, site_name):
        """Return one location row's commission (by site name)."""
        return self._retry_transient(
            lambda: self.get_location_row(site_name)
            .find_element(By.NAME, "commission")
            .get_attribute("value")
        )

    def _scroll_to_save_button(self):
        """Scroll the Save button into view before clicking it.

        Confirmed live: after assigning two locations (heavy scrolling
        inside the location grid's own container), the Save button ended up
        at y=-243 — above the viewport — and a plain click() on it (native
        Selenium click, which is supposed to auto-scroll) silently did
        nothing: no exception, no network activity, no page state change,
        for a full 10 seconds. Explicitly scrolling first fixes it. This was
        the actual cause of "the second assigned location doesn't persist"
        — the save click itself was never landing, not a data/serialization
        bug.
        """
        element = self.wait.until(EC.element_to_be_clickable(self.SAVE_MEMBERSHIP_BUTTON))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def click_save_membership(self):
        """Click save membership, then wait for the save to land.

        Previously returned immediately after the click with no wait at
        all — same defect shape found and fixed in sites_page.py's
        click_save_new() (CI run 37612565958): the caller could check the
        list page while the browser was still on the create/edit form.
        Stays lenient (swallows a timeout) since test_memberships_validation.py
        calls this directly and expects to stay on the form after a rejected
        save. save_and_return_to_list() below is the strict version for
        callers expecting a guaranteed successful save.
        """
        self._scroll_to_save_button()
        self.click(self.SAVE_MEMBERSHIP_BUTTON)
        try:
            self.wait_for_legacy_save()
        except Exception:
            pass

    def save_and_return_to_list(self):
        """Save the membership, confirm the save landed, then show the list.

        Patches window.confirm so deactivation dialogs are auto-accepted.
        Waits for the app's own post-save redirect (BasePage.wait_for_legacy_save)
        before treating the save as landed — same pattern already fixed
        wash_packages/wash_books "silently dropped edits" failures, where
        navigating away on a disable/re-enable timer raced the actual save API
        call and the next read saw pre-save data. Falls back to the old
        disable/re-enable + fixed-sleep heuristic if this module turns out not
        to auto-redirect (kept only as a safety net, not the primary path).
        """
        self.driver.execute_script("window.confirm = () => true;")
        self._scroll_to_save_button()
        self.click(self.SAVE_MEMBERSHIP_BUTTON)
        try:
            outcome, error = self.wait_for_legacy_save()
            save_error = error if outcome == "error" else None
        except TimeoutError:
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
            # Capture any visible error before navigating away — if save was
            # rejected (duplicate name, validation) the error shows here.
            save_error = self.get_visible_error()
        # Switch to the top-level document first so current_url is the main
        # page URL (the iframe URL can be null after a form submission).
        self.driver.switch_to.default_content()
        current = self.driver.current_url or ""
        base_url = current.split("/services/")[0] if "/services/" in current else current.rstrip("/")
        try:
            self.driver.get(base_url + "/services/memberships")
        except TimeoutException:
            pass  # slow staging load; list wait below
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
        prepaid_months="1",
        redeem_as_service="VK detail wash"
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
        # Resolve "the first location" to a concrete site name once — index 0
        # isn't a stable identity across the reload save_and_return_to_list()
        # triggers, so everything past this point addresses the row by name.
        first_location_name = self.get_location_name_by_index(0)
        self.set_location_price_and_commission(
            first_location_name,
            first_location_price,
            first_location_commission
        )
        self.fill_required_unassigned_location_values(skip_site_name=first_location_name)
        self.assign_location_with_price_and_commission(
            first_location_name,
            first_location_price,
            first_location_commission
        )
        self.unassign_locations_after_first(first_location_name)
        # Any location row still empty would block Save via HTML5 validation.
        self.fill_all_empty_location_inputs()
        # Last: the app now blocks Save entirely without a redemption location
        # + redeem-as service ("Please select at least one redeem location").
        # Configuring it here covers every caller (create, managed-reset,
        # direct fill) instead of each call site remembering to do it.
        self.configure_redemption_settings(redeem_as_service)


    def fill_recurring_membership_form(
        self,
        membership_name,
        global_price,
        global_commission,
        first_location_price,
        first_location_commission,
        redeem_as_service="VK detail wash"
    ):
        """Fill membership settings for a recurring membership."""
        self.enter_membership_name(membership_name)
        self.select_recurring_membership_type()
        self.ensure_active_switch_on()
        self.ensure_customer_portal_switch_on()
        self.ensure_switch_off(self.LIMIT_MEMBERSHIP_SWITCH)
        self.set_global_price(global_price)
        self.set_global_commission(global_commission)
        # Resolve "the first location" to a concrete site name once — see
        # fill_membership_form() for why.
        first_location_name = self.get_location_name_by_index(0)
        self.set_location_price_and_commission(
            first_location_name,
            first_location_price,
            first_location_commission
        )
        self.fill_required_unassigned_location_values(skip_site_name=first_location_name)
        self.assign_location_with_price_and_commission(
            first_location_name,
            first_location_price,
            first_location_commission
        )
        self.unassign_locations_after_first(first_location_name)
        # Any location row still empty would block Save via HTML5 validation.
        self.fill_all_empty_location_inputs()
        # Last: the app now blocks Save entirely without a redemption location
        # + redeem-as service ("Please select at least one redeem location").
        self.configure_redemption_settings(redeem_as_service)


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
