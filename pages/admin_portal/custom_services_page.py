import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class CustomServicesPage(BasePage):

    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/customServices')"
        " and not(contains(@src,'/services/customServices/'))]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/customServices/new')]"
    )
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/customServices/')"
        " and not(contains(@src,'/services/customServices/new'))]"
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Custom services']")
    SEARCH_INPUT = (By.NAME, "serviceName")
    FILTER_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Filter by')]")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Filter by']/following-sibling::button[1]"
    )
    ADD_SERVICE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='+ Add new custom service']"
    )
    SAVE_SERVICE_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Save') "
        "and contains(normalize-space(),'custom service')]"
    )
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    GRID_ROWS = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row')"
        " and .//*[@data-props-id='serviceName']]"
    )
    GRID_LOAD_MASK = (
        By.CSS_SELECTOR,
        ".inovua-react-toolkit-load-mask__background-layer"
    )
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']"
    )
    RESET_ALL_BUTTON = (By.XPATH, "//button[normalize-space()='Reset all']")
    FILTER_SITE_INPUT = (
        By.XPATH,
        "//*[normalize-space()='Select site']/following::input[@role='combobox'][1]"
    )
    ACTIVE_SERVICE_FILTER_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active service']"
        "/following::*[@role='switch' or self::input][1]"
    )

    # Form fields
    SERVICE_NAME_INPUT = (By.NAME, "serviceName")
    GLOBAL_PRICE_INPUT = (By.NAME, "servicePrice")
    GLOBAL_COMMISSION_INPUTS = (By.NAME, "commission")
    BARCODE_INPUT = (By.NAME, "barcode")
    POINTS_AWARDED_INPUT = (By.NAME, "pointsAwarded")
    POINTS_REDEEMED_INPUT = (By.NAME, "pointsRedeemed")
    DESCRIPTION_TEXTAREA = (By.XPATH, "//textarea[@name='description']")
    DESCRIPTION_SECTION_TOGGLE = (
        By.XPATH,
        "//textarea[@name='description']"
        "/ancestor::div[contains(@class,'collapse')]"
        "/preceding-sibling::div[contains(@style,'cursor: pointer')]"
    )
    SERVICE_CATEGORY_INPUT = (
        By.XPATH,
        "//*[normalize-space()='Select service category']"
        "/following::input[@role='combobox'][1]"
    )
    ACTIVE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active service']"
        "/../following-sibling::button[@role='switch']"
    )
    FORCE_RECEIPT_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Force receipt printing']"
        "/../following-sibling::button[@role='switch']"
    )
    OPEN_PRICE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Open price']"
        "/../following-sibling::button[@role='switch']"
    )

    # Discount settings tab
    DISCOUNT_SETTINGS_TAB = (
        By.XPATH,
        "//button[@role='tab' and normalize-space()='Discount settings']"
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

    SITE_ASSIGNMENT_HEADER_CHECKBOX = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__column-header--first')]"
        "//*[contains(@class,'inovua-react-toolkit-checkbox')]"
    )

    # ---------------------------------------------------------------------- waits

    def wait_for_list_loaded(self):
        """Wait until the Custom Services list is visible."""
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 30).until(
                EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME)
            )
        except TimeoutException:
            self.driver.switch_to.default_content()
            current_url = self.driver.current_url
            list_url = re.sub(r'(/services/customServices)/[^?#]*', r'\1', current_url)
            self.driver.get(list_url)
            WebDriverWait(self.driver, 45).until(
                EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME)
            )
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_SERVICE_BUTTON))
        self.wait_for_grid_idle()

    def wait_for_grid_idle(self):
        """Wait until the React grid load mask is gone."""
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self.driver, 60).until(
            lambda driver: not any(
                mask.is_displayed()
                for mask in driver.find_elements(*self.GRID_LOAD_MASK)
            )
        )

    def wait_for_create_loaded(self):
        """Wait until the create custom service form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.SERVICE_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_SERVICE_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until the edit custom service form is visible and pre-populated."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.SERVICE_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_SERVICE_BUTTON))
        self.wait.until(lambda driver: self.get_service_name_value() != "")
        self.wait_for_grid_idle()

    # ---------------------------------------------------------------------- helpers

    def get_body_text(self):
        """Return visible text inside the current iframe."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def _set_input_value(self, element, value):
        """Set a React-controlled input or textarea value and fire change events."""
        self.driver.execute_script(
            """
            const el = arguments[0];
            const value = arguments[1];
            const proto = el.tagName === 'TEXTAREA'
                ? window.HTMLTextAreaElement.prototype
                : window.HTMLInputElement.prototype;
            const setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
            el.focus();
            setter.call(el, value);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            value,
        )

    # ---------------------------------------------------------------------- list

    def search_service(self, service_name):
        """Search for a custom service by name."""
        element = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        element.click()
        element.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        element.send_keys(service_name)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == service_name
        )
        self.wait_for_grid_idle()

    def clear_service_search(self):
        """Clear the search input and wait for the grid to refresh."""
        element = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        element.click()
        element.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == ""
        )
        self.wait_for_grid_idle()

    def get_service_row_locator(self, service_name):
        """Build a locator for a custom service grid row by name."""
        return (
            By.XPATH,
            "//*[@data-props-id='serviceName']"
            "[.//span[normalize-space()='%s']]"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row ')][1]"
            % service_name
        )

    def wait_for_service_row(self, service_name):
        """Wait until a service row is visible in the grid."""
        return self.wait.until(
            EC.visibility_of_element_located(self.get_service_row_locator(service_name))
        )

    def service_exists(self, service_name):
        """Return whether the service exists in the list."""
        self.wait_for_list_loaded()
        self.search_service(service_name)
        try:
            self.wait_for_service_row(service_name)
            return True
        except TimeoutException:
            return False

    def get_visible_service_names(self):
        """Return visible service names from the grid."""
        names = []
        for row in self.driver.find_elements(*self.GRID_ROWS):
            if not row.is_displayed():
                continue
            try:
                names.append(
                    row.find_element(
                        By.XPATH, ".//*[@data-props-id='serviceName']"
                    ).text.strip()
                )
            except Exception:  # noqa: BLE001
                continue
        return [n for n in names if n]

    def get_service_status(self, service_name):
        """Return visible status for a service row."""
        row = self.wait_for_service_row(service_name)
        return row.find_element(
            By.XPATH, ".//*[@data-props-id='isActive']"
        ).text.strip()

    def get_service_price(self, service_name):
        """Return visible price for a service row."""
        row = self.wait_for_service_row(service_name)
        return row.find_element(
            By.XPATH, ".//*[@data-props-id='servicePrice']"
        ).text.strip()

    def every_visible_row_has_edit_action(self):
        """Return whether each visible grid row contains an Edit link."""
        try:
            self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(@class,'InovuaReactDataGrid__row')"
                    " and .//*[normalize-space()='Edit']]"
                ))
            )
            return True
        except TimeoutException:
            return False

    def pagination_controls_are_visible(self):
        """Return whether pagination controls are present."""
        text = self.get_body_text()
        return "Page" in text and "Results per page" in text

    def search_input_is_visible(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        ).is_displayed()

    def filter_button_is_clickable(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.FILTER_BUTTON)
        ).is_displayed()

    def add_service_button_is_clickable(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.ADD_SERVICE_BUTTON)
        ).is_displayed()

    def download_button_is_clickable(self):
        button = self.wait.until(EC.presence_of_element_located(self.DOWNLOAD_BUTTON))
        return button.is_displayed()

    def save_service_button_is_clickable(self):
        return self.wait.until(
            EC.element_to_be_clickable(self.SAVE_SERVICE_BUTTON)
        ).is_displayed()

    def cancel_button_is_visible(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.CANCEL_BUTTON)
        ).is_displayed()

    # ---------------------------------------------------------------------- filter

    def open_filter_panel(self):
        """Open the filter panel if not already open."""
        # Use Apply-filters button as the open indicator — it is always visible
        # when the panel is open regardless of which site value is selected.
        if any(el.is_displayed() for el in self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)):
            return
        button = self.wait.until(EC.presence_of_element_located(self.FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)
        self.wait.until(EC.visibility_of_element_located(self.APPLY_FILTERS_BUTTON))

    def filter_panel_controls_are_visible(self):
        """Return whether expected filter controls are visible."""
        self.open_filter_panel()
        return (
            self.wait.until(
                EC.visibility_of_element_located(self.FILTER_SITE_INPUT)
            ).is_displayed()
            and self.wait.until(
                EC.presence_of_element_located(self.ACTIVE_SERVICE_FILTER_SWITCH)
            ) is not None
            and self.wait.until(
                EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON)
            ).is_displayed()
        )

    def select_site_filter(self, site_name):
        """Open the filter panel and select a site."""
        self.open_filter_panel()
        self.click(self.FILTER_SITE_INPUT)
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[normalize-space()='%s']" % site_name)
            )
        ).click()

    def toggle_active_service_filter(self):
        """Toggle the Active service switch in the open filter panel."""
        switch = self.wait.until(
            EC.presence_of_element_located(self.ACTIVE_SERVICE_FILTER_SWITCH)
        )
        self.driver.execute_script("arguments[0].click();", switch)

    def apply_filters(self):
        """Click Apply filters and wait for the grid to refresh."""
        button = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)
        self.wait.until(EC.element_to_be_clickable(self.ADD_SERVICE_BUTTON))

    def reset_filters(self):
        """Click Reset all in the filter panel and resync to the list."""
        self.open_filter_panel()
        buttons = self.driver.find_elements(*self.RESET_ALL_BUTTON)
        if buttons:
            self.driver.execute_script("arguments[0].click();", buttons[0])
        self.wait_for_list_loaded()

    # ---------------------------------------------------------------------- form navigation

    def open_create_service(self):
        """Open the Add new custom service form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_SERVICE_BUTTON)
        self.wait_for_create_loaded()

    def open_edit_service(self, service_name):
        """Open the edit form for an existing custom service."""
        self.wait_for_list_loaded()
        self.search_service(service_name)
        row = self.wait_for_service_row(service_name)
        edit_button = row.find_element(
            By.XPATH, ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        edit_button.click()
        self.wait_for_edit_loaded()

    # ---------------------------------------------------------------------- form inputs

    def enter_service_name(self, name):
        """Type a service name into the Service name input."""
        self.enter_text(self.SERVICE_NAME_INPUT, name)

    def get_service_name_value(self):
        """Return the current service name input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.SERVICE_NAME_INPUT)
        )
        return element.get_attribute("value")

    def select_service_category(self, category_name):
        """Select a service category from the dropdown."""
        self.select_react_dropdown_option(self.SERVICE_CATEGORY_INPUT, category_name)

    def get_service_category_value(self):
        """Return the currently selected service category text."""
        element = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH, "//*[contains(@class,'form-select__single-value')]"
            ))
        )
        return element.text.strip()

    def set_global_price(self, price):
        """Set the global price field."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        self._set_input_value(element, str(price))

    def get_global_price_value(self):
        """Return the global price input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return element.get_attribute("value")

    def set_global_commission(self, commission):
        """Set the global commission field."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        self._set_input_value(elements[0], str(commission))

    def get_global_commission_value(self):
        """Return the global commission input value."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        return elements[0].get_attribute("value")

    def set_loyalty_points(self, points_awarded, points_redeemed):
        """Set loyalty points awarded and redeemed."""
        awarded = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_AWARDED_INPUT)
        )
        redeemed = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_REDEEMED_INPUT)
        )
        self._set_input_value(awarded, str(points_awarded))
        self._set_input_value(redeemed, str(points_redeemed))

    def get_points_awarded_value(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_AWARDED_INPUT)
        )
        return element.get_attribute("value")

    def get_points_redeemed_value(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_REDEEMED_INPUT)
        )
        return element.get_attribute("value")

    def enter_barcode(self, barcode):
        self.enter_text(self.BARCODE_INPUT, barcode)
        self.wait.until(
            lambda d: d.find_element(*self.BARCODE_INPUT).get_attribute("value") == barcode
        )

    def get_barcode_value(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.BARCODE_INPUT)
        )
        return element.get_attribute("value")

    def enter_description(self, text):
        # Expand the collapsible "Service description" section if it's folded
        collapse_divs = self.driver.find_elements(
            By.XPATH,
            "//textarea[@name='description']"
            "/ancestor::div[contains(@class,'collapse')]"
        )
        if collapse_divs and 'show' not in (collapse_divs[0].get_attribute('class') or ''):
            toggles = self.driver.find_elements(*self.DESCRIPTION_SECTION_TOGGLE)
            if toggles:
                self.driver.execute_script("arguments[0].click();", toggles[0])
                time.sleep(0.4)
        element = self.wait.until(
            EC.presence_of_element_located(self.DESCRIPTION_TEXTAREA)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)
        element.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        element.send_keys(text)

    def get_description_value(self):
        element = self.wait.until(
            EC.presence_of_element_located(self.DESCRIPTION_TEXTAREA)
        )
        return element.get_attribute("value")

    # ---------------------------------------------------------------------- toggles

    def active_switch_is_on(self):
        switch = self.wait.until(EC.presence_of_element_located(self.ACTIVE_SWITCH))
        return switch.get_attribute("aria-checked") == "true"

    def ensure_active_switch_on(self):
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "true":
            switch.click()
            self.wait.until(lambda d: switch.get_attribute("aria-checked") == "true")

    def ensure_active_switch_off(self):
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "false":
            switch.click()
            self.wait.until(lambda d: switch.get_attribute("aria-checked") == "false")

    def force_receipt_is_on(self):
        switch = self.wait.until(EC.presence_of_element_located(self.FORCE_RECEIPT_SWITCH))
        return switch.get_attribute("aria-checked") == "true"

    def ensure_force_receipt_on(self):
        switch = self.wait.until(EC.element_to_be_clickable(self.FORCE_RECEIPT_SWITCH))
        if switch.get_attribute("aria-checked") != "true":
            switch.click()
            self.wait.until(lambda d: switch.get_attribute("aria-checked") == "true")

    def open_price_is_on(self):
        switch = self.wait.until(EC.presence_of_element_located(self.OPEN_PRICE_SWITCH))
        return switch.get_attribute("aria-checked") == "true"

    def ensure_open_price_on(self):
        switch = self.wait.until(EC.element_to_be_clickable(self.OPEN_PRICE_SWITCH))
        if switch.get_attribute("aria-checked") != "true":
            switch.click()
            self.wait.until(lambda d: switch.get_attribute("aria-checked") == "true")

    # ---------------------------------------------------------------------- site assignment

    def get_site_row(self, site_name):
        """Return the site assignment grid row for a given site."""
        # InovuaReactDataGrid--native-scroll uses a JS-managed virtual scroll
        # (inovua-react-scroll-container) that ignores CSS scroll APIs.
        # ASSIGNMENT_SITE must be in the grid's initially-rendered row batch
        # (first ~14 rows), otherwise it will never appear without the grid's
        # own scroll controls. Bring the grid body into view to ensure the
        # initial batch is rendered, then locate the target row directly.
        self.driver.execute_script(
            "var el = document.querySelector('.InovuaReactDataGrid__body');"
            "if (el) el.scrollIntoView({block: 'start', behavior: 'instant'});"
        )
        xpath = (
            "//*[@data-props-id='assignTo']"
            "[.//*[normalize-space()='%s']]"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row ')][1]"
            % site_name
        )
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def assign_site_with_price_and_commission(self, site_name, price, commission):
        """Assign a site and set site-level price and commission."""
        row = self.get_site_row(site_name)
        checkbox = row.find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
        )

        def _is_checked():
            classes = checkbox.get_attribute("class")
            return (
                "inovua-react-toolkit-checkbox--checked" in classes
                and "inovua-react-toolkit-checkbox--unchecked" not in classes
            )

        if not _is_checked():
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center',inline:'center'});", checkbox
            )
            self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(lambda d: _is_checked())

        # Use keyboard input so InovuaReactDataGrid fires onEditComplete on Tab,
        # committing the value to the grid's dataSource before the row unmounts.
        price_input = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//*[@data-props-id='assignTo']"
                 "[.//*[normalize-space()='%s']]"
                 "/ancestor::*[contains(@class,'InovuaReactDataGrid__row ')][1]"
                 "//input[@name='price']" % site_name)
            )
        )
        price_input.click()
        price_input.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        price_input.send_keys(str(price))
        price_input.send_keys(Keys.TAB)

        commission_input = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//*[@data-props-id='assignTo']"
                 "[.//*[normalize-space()='%s']]"
                 "/ancestor::*[contains(@class,'InovuaReactDataGrid__row ')][1]"
                 "//input[@name='commission']" % site_name)
            )
        )
        commission_input.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        commission_input.send_keys(str(commission))
        commission_input.send_keys(Keys.TAB)

    def toggle_site_tax_exemption(self, site_name):
        """Toggle the tax exemption switch for a site row."""
        row = self.get_site_row(site_name)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", row
        )
        switch = row.find_element(By.XPATH, ".//button[@role='switch']")
        self.driver.execute_script("arguments[0].click();", switch)

    def get_site_price_value(self, site_name):
        row = self.get_site_row(site_name)
        return row.find_element(By.NAME, "price").get_attribute("value")

    def get_site_commission_value(self, site_name):
        row = self.get_site_row(site_name)
        elements = row.find_elements(By.NAME, "commission")
        return elements[0].get_attribute("value") if elements else ""

    def select_all_sites(self):
        """Click the Select All header checkbox in the site assignment grid."""
        header_checkbox = self.wait.until(
            EC.element_to_be_clickable(self.SITE_ASSIGNMENT_HEADER_CHECKBOX)
        )
        self.driver.execute_script("arguments[0].click();", header_checkbox)

    # ---------------------------------------------------------------------- discount settings

    def open_discount_settings(self):
        """Open the Discount settings tab."""
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.click(self.DISCOUNT_SETTINGS_TAB)
        self.wait.until(EC.visibility_of_element_located(self.APPLICABLE_DISCOUNTS_TITLE))
        self.wait.until(EC.presence_of_element_located(self.DISCOUNTS_COMBOBOX))

    def get_selected_discount_locator(self, discount_name):
        return (
            By.XPATH,
            "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
            "//*[contains(@class,'form-select__multi-value__label')"
            " and normalize-space()='%s']" % discount_name
        )

    def discount_is_selected(self, discount_name):
        return len(self.driver.find_elements(*self.get_selected_discount_locator(discount_name))) > 0

    def select_applicable_discount(self, discount_name):
        """Select a discount from the Applicable discounts combobox."""
        if self.discount_is_selected(discount_name):
            return
        self.select_react_dropdown_option(self.DISCOUNTS_COMBOBOX, discount_name, clear_first=False)
        self.wait.until(
            EC.visibility_of_element_located(self.get_selected_discount_locator(discount_name))
        )

    def remove_applicable_discount(self, discount_name):
        """Click the × button on a selected discount chip."""
        remove_btn = self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
                "//*[contains(@class,'form-select__multi-value__label')"
                " and normalize-space()='%s']"
                "/ancestor::*[contains(@class,'form-select__multi-value')][1]"
                "//*[contains(@class,'form-select__multi-value__remove')]"
                % discount_name
            ))
        )
        self.driver.execute_script("arguments[0].click();", remove_btn)
        self.wait.until(lambda d: not self.discount_is_selected(discount_name))

    # ---------------------------------------------------------------------- validation

    def service_name_input_is_valid(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.SERVICE_NAME_INPUT)
        )
        return self.driver.execute_script("return arguments[0].checkValidity();", element)

    def global_price_input_is_valid(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return self.driver.execute_script("return arguments[0].checkValidity();", element)

    def global_commission_input_is_valid(self):
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        return self.driver.execute_script("return arguments[0].checkValidity();", elements[0])

    def get_service_name_validation_message(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.SERVICE_NAME_INPUT)
        )
        return self.driver.execute_script("return arguments[0].validationMessage;", element)

    def get_global_price_validation_message(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return self.driver.execute_script("return arguments[0].validationMessage;", element)

    # ---------------------------------------------------------------------- save / cancel

    def click_save_service(self):
        """Click the Save custom service button and wait for the save to settle."""
        self.driver.execute_script("window.scrollTo(0, 0);")
        btn = self.wait.until(EC.element_to_be_clickable(self.SAVE_SERVICE_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        # Wait for the button to go stale or the iframe to unload before the
        # caller navigates away — prevents races with in-flight POST requests.
        try:
            WebDriverWait(self.driver, 10).until(EC.staleness_of(btn))
        except Exception:
            pass
        self.driver.switch_to.default_content()

    def click_cancel(self):
        """Click Cancel to discard the form."""
        self.click(self.CANCEL_BUTTON)

    # ---------------------------------------------------------------------- high-level

    def fill_service_form(
        self,
        service_name,
        category_name,
        global_price,
        global_commission,
        site_name,
    ):
        """Fill the custom service form with required fields and site assignment."""
        self.enter_service_name(service_name)
        self.select_service_category(category_name)
        self.ensure_active_switch_on()
        self.set_global_price(global_price)
        self.set_global_commission(global_commission)
        self.assign_site_with_price_and_commission(site_name, global_price, global_commission)

    def create_service(
        self,
        service_name,
        category_name,
        global_price,
        global_commission,
        site_name,
    ):
        """Create an active custom service and return to the list."""
        self.open_create_service()
        self.fill_service_form(
            service_name, category_name, global_price, global_commission, site_name
        )
        self.click_save_service()
        try:
            self.wait_for_list_loaded()
        except TimeoutException:
            return
