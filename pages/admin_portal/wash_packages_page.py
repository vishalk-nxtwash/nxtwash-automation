from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class WashPackagesPage(BasePage):

    FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/washPackages')]"
    )
    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/washPackages') "
        "and not(contains(@src,'/services/washPackages/'))]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/washPackages/new')]"
    )
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/washPackages/') "
        "and not(contains(@src,'/services/washPackages/new'))]"
    )

    PAGE_TITLE = (By.XPATH,
        "//*[normalize-space()='Wash packages' or normalize-space()='Wash Packages']")
    SEARCH_INPUT = (By.NAME, "serviceName")
    FILTER_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Filter by')]")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Filter by')]/following-sibling::button[1]"
    )
    ADD_PACKAGE_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Add new wash package')]"
    )
    EDIT_ACTIONS = (By.XPATH, "//*[normalize-space()='Edit']")
    GRID_ROWS = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row') "
        "and .//*[@data-props-id='serviceName']]"
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
    ACTIVE_SERVICE_FILTER_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active service']"
        "/following::*[@role='switch' or self::input][1]"
    )

    SAVE_PACKAGE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save wash package']"
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
    APPLICABLE_DISCOUNTS_TITLE = (
        By.XPATH,
        "//*[normalize-space()='Applicable discounts']"
    )
    DISCOUNTS_COMBOBOX = (
        By.XPATH,
        "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
        "//input[@role='combobox']"
    )
    DESCRIPTION_ACCORDION_HEADER = (
        By.XPATH,
        "//*[normalize-space()='Service description']"
        "/parent::*[contains(@style,'cursor: pointer')]"
    )
    DESCRIPTION_TEXTAREA = (By.NAME, "description")
    SITE_ASSIGNMENT_HEADER_CHECKBOX = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__column-header--first')]"
        "//*[contains(@class,'inovua-react-toolkit-checkbox')]"
    )
    GRID_LOAD_MASK = (
        By.CSS_SELECTOR,
        ".inovua-react-toolkit-load-mask__background-layer"
    )

    def wait_for_list_loaded(self):
        """Wait until the Wash Packages list is visible."""
        self.switch_to_frame_with_retry(self.LIST_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_PACKAGE_BUTTON))
        self.wait_for_grid_idle()

    def wait_for_grid_idle(self):
        """Wait until the React grid load mask is not blocking interactions."""
        self.wait.until(
            lambda driver: not any(
                mask.is_displayed()
                for mask in driver.find_elements(*self.GRID_LOAD_MASK)
            )
        )

    def wait_for_create_loaded(self):
        """Wait until the create package form is visible."""
        self.switch_to_frame_with_retry(self.CREATE_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.SERVICE_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_PACKAGE_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until the edit package form is visible."""
        self.switch_to_frame_with_retry(self.EDIT_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.SERVICE_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_PACKAGE_BUTTON))
        self.wait.until(lambda driver: self.get_service_name_value() != "")

    def get_body_text(self):
        """Get visible text inside the current iframe."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def search_input_is_visible(self):
        """Return whether the package search input is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        ).is_displayed()

    def filter_button_is_clickable(self):
        """Return whether the Filter by button is clickable."""
        return self.wait.until(
            EC.element_to_be_clickable(self.FILTER_BUTTON)
        ).is_displayed()

    def add_package_button_is_clickable(self):
        """Return whether Add new wash package is clickable."""
        return self.wait.until(
            EC.element_to_be_clickable(self.ADD_PACKAGE_BUTTON)
        ).is_displayed()

    def save_package_button_is_clickable(self):
        """Return whether Save wash package is clickable."""
        return self.wait.until(
            EC.element_to_be_clickable(self.SAVE_PACKAGE_BUTTON)
        ).is_displayed()

    def cancel_button_is_visible(self):
        """Return whether Cancel is visible on the form."""
        return self.wait.until(
            EC.visibility_of_element_located(self.CANCEL_BUTTON)
        ).is_displayed()

    def get_visible_package_rows(self):
        """Return visible package grid rows."""
        return [
            row for row in self.driver.find_elements(*self.GRID_ROWS)
            if row.is_displayed()
        ]

    def get_visible_package_names(self):
        """Return visible package names from the grid."""
        names = []
        for row in self.get_visible_package_rows():
            try:
                names.append(
                    row.find_element(
                        By.XPATH,
                        ".//*[@data-props-id='serviceName']"
                    ).text.strip()
                )
            except Exception:  # noqa: BLE001
                continue
        return [name for name in names if name]

    def every_visible_row_has_edit_action(self):
        """Return whether the grid has loaded rows with an Edit action.

        Uses a direct wait for a row+Edit combination to avoid the race where
        the InovuaReactDataGrid load mask disappears briefly before row data
        has rendered — checking rows immediately after would find an empty grid.
        """
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
        """Return whether pagination controls are visible."""
        text = self.get_body_text()
        return "Page" in text and "Results per page" in text

    def results_per_page_control_is_visible(self):
        """Return whether results-per-page control is visible."""
        text = self.get_body_text()
        return "Results per page" in text

    def get_package_row_locator(self, package_name):
        """Build a locator for a package row by package name."""
        # Inovua renders the name cell with both a visible truncated text node
        # and a full-text node (div, not span, in recent grid versions).
        # normalize-space() on the cell concatenates both, so exact equality
        # fails. contains() is safe because package names are unique.
        return (
            By.XPATH,
            "//*[contains(@class,'InovuaReactDataGrid__row')]"
            "[.//*[@data-props-id='serviceName' and contains(normalize-space(),'%s')]]"
            % package_name
        )

    def wait_for_package_row(self, package_name):
        """Wait until a package row is present (InovuaReactDataGrid uses CSS transforms; visibility check is unreliable)."""
        return self.wait.until(
            EC.presence_of_element_located(
                self.get_package_row_locator(package_name)
            )
        )

    def package_exists(self, package_name):
        """Return whether the package exists in the list."""
        self.wait_for_list_loaded()
        self.search_package(package_name)

        try:
            self.wait_for_package_row(package_name)
            return True
        except TimeoutException:
            return False

    def search_package(self, package_name):
        """Search package by service name.

        JS input.select() selects all text cross-platform (Ctrl+A only selects
        on Linux; on macOS it moves the cursor).  send_keys then replaces the
        selection so React's onChange fires cleanly on all platforms.
        """
        element = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        element.click()
        self.driver.execute_script("arguments[0].select();", element)
        element.send_keys(package_name)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == package_name
        )
        self.wait_for_grid_idle()

    def clear_package_search(self):
        """Clear package search input and wait until the grid refreshes."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        element.click()
        self.driver.execute_script("arguments[0].select();", element)
        element.send_keys(Keys.BACKSPACE)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == ""
        )
        self.wait_for_grid_idle()

    def get_package_price(self, package_name):
        """Return visible price for a package row."""
        row = self.wait_for_package_row(package_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='servicePrice']"
        ).text.strip()

    def get_package_status(self, package_name):
        """Return visible status for a package row."""
        row = self.wait_for_package_row(package_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='isActive']"
        ).text.strip()

    def open_filter_panel(self):
        """Open the Wash Packages filter panel."""
        self.wait_for_list_loaded()
        visible_site_inputs = [
            element for element in self.driver.find_elements(*self.FILTER_SITE_INPUT)
            if element.is_displayed()
        ]
        if visible_site_inputs:
            return

        button = self.wait.until(EC.presence_of_element_located(self.FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)
        self.wait.until(EC.visibility_of_element_located(self.FILTER_SITE_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))

    def filter_panel_controls_are_visible(self):
        """Return whether expected filter controls are visible."""
        self.open_filter_panel()
        try:
            self.wait.until(EC.visibility_of_element_located(self.FILTER_SITE_INPUT))
            self.wait.until(EC.presence_of_element_located(self.ACTIVE_SERVICE_FILTER_SWITCH))
            self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
            self.wait.until(EC.element_to_be_clickable(self.RESET_ALL_BUTTON))
            return True
        except TimeoutException:
            return False

    def filter_site_option_is_visible(self, site_name):
        """Return whether a site option is visible in the opened filter panel."""
        self.open_filter_panel()
        self.click(self.FILTER_SITE_INPUT)
        try:
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[normalize-space()='%s']" % site_name)
                )
            )
            return True
        except TimeoutException:
            return False

    def reset_filters(self):
        """Reset filters from the opened filter panel."""
        self.open_filter_panel()
        button = self.wait.until(EC.presence_of_element_located(self.RESET_ALL_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)
        self.wait.until(EC.visibility_of_element_located(self.FILTER_SITE_INPUT))

    def clear_active_filters(self):
        """Reset all filters and wait until the active-filter badge is gone."""
        try:
            self.reset_filters()
            self.apply_filters()
            self.wait.until(
                lambda driver: "Filter by (" not in driver.find_element(
                    By.TAG_NAME, "body"
                ).text
            )
            self.wait_for_grid_idle()
        except Exception as exc:
            import logging
            logging.getLogger("nxtwash").warning("clear_active_filters (wash_packages): %s", exc)

    def reset_filters_if_active(self):
        """Reset filter panel state if any filter is currently active.

        The app persists site filter state after edit-form site assignment,
        causing 'Filter by (1)' on the next list load. Call this before any
        operation that needs to find a specific row in an unfiltered grid.
        """
        try:
            body = self.driver.find_element(By.TAG_NAME, "body").text
            if "Filter by (" in body:
                self.reset_filters()
                try:
                    self.apply_filters()
                except Exception:  # noqa: BLE001
                    pass
                try:
                    self.wait.until(
                        lambda driver: "Filter by (" not in driver.find_element(
                            By.TAG_NAME, "body"
                        ).text
                    )
                    self.wait_for_grid_idle()
                except Exception:  # noqa: BLE001
                    pass
        except Exception:  # noqa: BLE001
            pass

    def download_button_is_clickable(self):
        """Return whether the download button can be clicked."""
        button = self.wait.until(EC.presence_of_element_located(self.DOWNLOAD_BUTTON))
        return button.is_displayed()

    def open_create_package(self):
        """Open create package form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_PACKAGE_BUTTON)
        self.wait_for_create_loaded()

    def open_edit_package(self, package_name):
        """Open edit package form."""
        self.wait_for_list_loaded()
        self.clear_active_filters()
        self.search_package(package_name)
        self.wait_for_package_row(package_name)
        # Atomic JS click — InovuaReactDataGrid uses <div> rows, not <tr>.
        _CLICK_EDIT_JS = (
            "var name=arguments[0];"
            "var rows=Array.from(document.querySelectorAll('[class*=\"InovuaReactDataGrid__row\"]'));"
            "for(var i=0;i<rows.length;i++){"
            " if(rows[i].textContent.indexOf(name)!==-1){"
            "  var a=Array.from(rows[i].querySelectorAll('a,button'))"
            "   .find(function(x){return x.textContent.trim()==='Edit';});"
            "  if(a){a.click();return true;}"
            " }}"
            "return false;"
        )
        WebDriverWait(self.driver, 45).until(
            lambda d: d.execute_script(_CLICK_EDIT_JS, package_name)
        )
        self.wait_for_edit_loaded()

    def enter_service_name(self, service_name):
        """Enter package service name."""
        self.enter_text(self.SERVICE_NAME_INPUT, service_name)

    def get_service_name_value(self):
        """Return the current package service name input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.SERVICE_NAME_INPUT)
        )
        return element.get_attribute("value")

    def get_global_price_value(self):
        """Return package global price input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        return element.get_attribute("value")

    def get_global_commission_value(self):
        """Return package global commission input value."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        return elements[0].get_attribute("value")

    def open_discount_settings(self):
        """Open Discount settings tab."""
        self.click(self.DISCOUNT_SETTINGS_TAB)
        self.wait.until(
            EC.visibility_of_element_located(self.APPLICABLE_DISCOUNTS_TITLE)
        )
        self.wait.until(EC.presence_of_element_located(self.DISCOUNTS_COMBOBOX))

    def get_selected_discount_locator(self, discount_name):
        """Build a locator for a selected discount chip label."""
        return (
            By.XPATH,
            "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
            "//*[contains(@class,'form-select__multi-value__label') "
            "and normalize-space()='%s']" % discount_name
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

        self.click(self.DISCOUNTS_COMBOBOX)
        option = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[@role='option' and normalize-space()='%s']"
                    % discount_name
                )
            )
        )
        option.click()
        self.wait.until(
            EC.visibility_of_element_located(
                self.get_selected_discount_locator(discount_name)
            )
        )

    def get_service_name_validation_message(self):
        """Return native validation message for service name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.SERVICE_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
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

    def service_name_input_is_valid(self):
        """Return native validity state for service name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.SERVICE_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def global_price_input_is_valid(self):
        """Return native validity state for global price input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
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
        """Set package global price."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GLOBAL_PRICE_INPUT)
        )
        self._set_input_value(element, str(price))

    def set_global_commission(self, commission):
        """Set package global commission."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        self._set_input_value(elements[0], str(commission))

    def set_loyalty_points(self, points_awarded, points_redeemed):
        """Set loyalty points fields."""
        awarded = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_AWARDED_INPUT)
        )
        redeemed = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_REDEEMED_INPUT)
        )

        self._set_input_value(awarded, str(points_awarded))
        self._set_input_value(redeemed, str(points_redeemed))

    def get_site_row(self, site_name):
        """Return the site assignment grid row for a site.

        InovuaReactDataGrid rows have is_displayed()=False even when rendered
        (the grid uses CSS transforms/clipping for its virtual scroller).
        Uses EC.presence_of_element_located (DOM presence) instead of visibility.

        Scroll strategy: direct scrollTop on the inner scrollable container
        (the unnamed div with scrollH > clientH inside the virtual-list wrapper).
        This bypasses the WheelEvent→Inovua→React-state→re-render→scroll-reset
        cycle that caused the previous approach to fail after form field changes.
        """
        import time as _time
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        any_row_locator = (By.XPATH, "//*[contains(@class,'InovuaReactDataGrid__row')]")
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(any_row_locator))
        _time.sleep(0.5)

        row_xpath = (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
            % site_name,
        )

        els = self.driver.find_elements(*row_xpath)
        if els:
            return els[0]

        # Find the real scroller and get its max scrollTop.
        _find_scroller_js = """
var vl = document.querySelector('[class*="InovuaReactDataGrid__virtual-list"]');
if (!vl) return null;
var kids = Array.from(vl.querySelectorAll('div'));
for (var i = 0; i < kids.length; i++) {
    if (kids[i].scrollHeight > kids[i].clientHeight + 50) return kids[i].scrollHeight - kids[i].clientHeight;
}
return null;
"""
        max_scroll = self.driver.execute_script(_find_scroller_js)
        if max_scroll is None:
            max_scroll = 4000  # fallback

        _set_scroll_js = """
var vl = document.querySelector('[class*="InovuaReactDataGrid__virtual-list"]');
if (!vl) return;
var kids = Array.from(vl.querySelectorAll('div'));
for (var i = 0; i < kids.length; i++) {
    if (kids[i].scrollHeight > kids[i].clientHeight + 50) {
        kids[i].scrollTop = arguments[0];
        return;
    }
}
"""
        # Scan in ~350 px steps (slightly less than viewport height so rows
        # near viewport edges are always included in at least one window).
        step = 350
        for pos in range(0, int(max_scroll) + step, step):
            self.driver.execute_script(_set_scroll_js, min(pos, int(max_scroll)))
            _time.sleep(0.12)
            els = self.driver.find_elements(*row_xpath)
            if els:
                return els[0]

        return WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(row_xpath))

    def _set_site_input(self, element, value):
        """Set a React-controlled site-grid input via native setter + events."""
        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            ).set;
            input.scrollIntoView({block: 'center', inline: 'center'});
            input.focus();
            setter.call(input, value);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            input.dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            element,
            str(value),
        )

    def assign_site_with_price_and_commission(
        self, site_name, price, commission, controller_code=None
    ):
        """Assign a package to a site and set site-level price/commission."""
        import time as _t
        # Let preceding form-field React re-renders settle before touching the grid.
        _t.sleep(2)
        row = self.get_site_row(site_name)
        checkbox = row.find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox')"
            " and not(contains(@class,'__icon'))]"
        )

        _CB_XPATH = (
            By.XPATH,
            "//*[contains(@class,'InovuaReactDataGrid__row')]"
            "[.//*[normalize-space()='%s']]"
            "//*[contains(@class,'inovua-react-toolkit-checkbox')"
            " and not(contains(@class,'__icon'))]" % site_name,
        )

        def _checkbox_checked(d):
            try:
                return any(
                    "inovua-react-toolkit-checkbox--checked" in el.get_attribute("class")
                    and "inovua-react-toolkit-checkbox--unchecked"
                        not in el.get_attribute("class")
                    for el in d.find_elements(*_CB_XPATH)
                )
            except Exception:
                return False

        if not _checkbox_checked(self.driver):
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'nearest'});", checkbox
            )
            _t.sleep(0.3)
            # JS click is required — ActionChains coordinates are unreliable for
            # Inovua checkboxes inside iframes (ActionChains offset is relative
            # to the outer document, but the checkbox lives inside the iframe).
            self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(_checkbox_checked)

        # Re-find row after React re-render triggered by checkbox state change.
        row = self.get_site_row(site_name)
        price_inputs = row.find_elements(By.NAME, "price")
        if price_inputs:
            self._set_site_input(price_inputs[0], price)

        row = self.get_site_row(site_name)
        commission_inputs = row.find_elements(By.NAME, "commission")
        if commission_inputs:
            self._set_site_input(commission_inputs[0], commission)

        if controller_code is not None:
            row = self.get_site_row(site_name)
            cc_inputs = row.find_elements(By.NAME, "controllerCode")
            if cc_inputs:
                self._set_site_input(cc_inputs[0], controller_code)

    def fill_package_form(
        self,
        service_name,
        points_awarded,
        points_redeemed,
        global_price,
        global_commission,
        site_name,
        barcode=None,
        controller_code=None,
        location_price=None,
    ):
        """Fill package form with package and site assignment details."""
        self.enter_service_name(service_name)
        if barcode is not None:
            self.enter_barcode(barcode)
        self.set_loyalty_points(points_awarded, points_redeemed)
        self.ensure_active_switch_on()
        self.set_global_price(global_price)
        self.set_global_commission(global_commission)
        self.assign_site_with_price_and_commission(
            site_name,
            location_price if location_price is not None else global_price,
            global_commission,
            controller_code=controller_code,
        )

    def click_save_package(self):
        """Click save package."""
        self.click(self.SAVE_PACKAGE_BUTTON)

    def save_and_return_to_list(self):
        """Save wash package and navigate explicitly to the list.

        Staging does not always auto-redirect after save; this method forces
        navigation so callers don't have to depend on the SPA redirect.
        """
        import time as _t
        self.click(self.SAVE_PACKAGE_BUTTON)
        try:
            self.wait.until(
                lambda driver: not driver.find_element(
                    *self.SAVE_PACKAGE_BUTTON
                ).is_enabled()
            )
            self.wait.until(EC.element_to_be_clickable(self.SAVE_PACKAGE_BUTTON))
        except Exception:
            _t.sleep(5)
        save_error = self.get_visible_error()
        self.driver.switch_to.default_content()
        origin = self.driver.execute_script("return window.location.origin")
        try:
            self.driver.get(origin + "/services/washPackages")
        except TimeoutException:
            pass
        self.wait_for_list_loaded()
        if save_error:
            raise RuntimeError("Wash package save error: %s" % save_error)

    def ensure_active_switch_off(self):
        """Turn active switch off if needed."""
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "false":
            switch.click()
            self.wait.until(
                lambda driver: switch.get_attribute("aria-checked") == "false"
            )

    def global_commission_input_is_valid(self):
        """Return native validity state for the first global commission input."""
        elements = self.wait.until(
            EC.presence_of_all_elements_located(self.GLOBAL_COMMISSION_INPUTS)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            elements[0]
        )

    def toggle_active_service_filter(self):
        """Toggle the Active service filter switch inside the open filter panel."""
        switch = self.wait.until(
            EC.presence_of_element_located(self.ACTIVE_SERVICE_FILTER_SWITCH)
        )
        self.driver.execute_script("arguments[0].click();", switch)

    def select_site_filter(self, site_name):
        """Open the site dropdown in the filter panel and click the named option."""
        self.open_filter_panel()
        self.click(self.FILTER_SITE_INPUT)
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[normalize-space()='%s']" % site_name)
            )
        ).click()

    def apply_filters(self):
        """Click Apply filters and wait for the grid to refresh within the current frame."""
        button = self.wait.until(
            EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)
        # Wait for the list to update without switching frames — we are already inside
        # the list iframe; calling wait_for_list_loaded() would re-enter the frame and
        # break subsequent calls to filter/download methods.
        self.wait.until(EC.element_to_be_clickable(self.ADD_PACKAGE_BUTTON))

    def enter_barcode(self, barcode):
        """Set the barcode input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.BARCODE_INPUT)
        )
        self.driver.execute_script("arguments[0].select();", element)
        element.send_keys(barcode)

    def get_barcode_value(self):
        """Return the current barcode input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.BARCODE_INPUT)
        )
        return element.get_attribute("value")

    def get_points_awarded_value(self):
        """Return the current points awarded input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_AWARDED_INPUT)
        )
        return element.get_attribute("value")

    def get_points_redeemed_value(self):
        """Return the current points redeemed input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.POINTS_REDEEMED_INPUT)
        )
        return element.get_attribute("value")

    def _expand_description_accordion(self):
        """Expand the Service description accordion if it is collapsed."""
        els = self.driver.find_elements(*self.DESCRIPTION_TEXTAREA)
        if els and els[0].is_displayed():
            return
        header = self.wait.until(
            EC.element_to_be_clickable(self.DESCRIPTION_ACCORDION_HEADER)
        )
        header.click()
        self.wait.until(EC.visibility_of_element_located(self.DESCRIPTION_TEXTAREA))

    def enter_description(self, text):
        """Expand the description accordion and set the textarea value."""
        self._expand_description_accordion()
        element = self.wait.until(
            EC.visibility_of_element_located(self.DESCRIPTION_TEXTAREA)
        )
        element.clear()
        element.send_keys(text)

    def get_description_value(self):
        """Expand the description accordion and return the textarea value."""
        self._expand_description_accordion()
        element = self.wait.until(
            EC.visibility_of_element_located(self.DESCRIPTION_TEXTAREA)
        )
        return element.get_attribute("value")

    def remove_applicable_discount(self, discount_name):
        """Click the remove (×) button on a selected discount chip."""
        remove_btn = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class,'tab-pane') and contains(@class,'active')]"
                "//*[contains(@class,'form-select__multi-value__label')"
                " and normalize-space()='%s']"
                "/ancestor::*[contains(@class,'form-select__multi-value')][1]"
                "/*[contains(@class,'form-select__multi-value__remove')]"
                % discount_name
            ))
        )
        remove_btn.click()
        self.wait.until(lambda driver: not self.discount_is_selected(discount_name))

    def unassign_site(self, site_name):
        """Uncheck the site row checkbox in the site assignment grid."""
        row = self.get_site_row(site_name)
        checkbox = row.find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
        )

        def checkbox_is_unchecked():
            return "inovua-react-toolkit-checkbox--unchecked" in checkbox.get_attribute("class")

        if not checkbox_is_unchecked():
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", checkbox
            )
            self.driver.execute_script("arguments[0].click();", checkbox)
            self.wait.until(lambda driver: checkbox_is_unchecked())

    def get_site_price_value(self, site_name):
        """Return the site-level price input value for the given site row."""
        row = self.get_site_row(site_name)
        return row.find_element(By.NAME, "price").get_attribute("value")

    def get_site_commission_value(self, site_name):
        """Return the site-level commission input value for the given site row."""
        row = self.get_site_row(site_name)
        elements = row.find_elements(By.NAME, "commission")
        return elements[0].get_attribute("value") if elements else ""

    def site_is_assigned(self, site_name):
        """Return True if the site's checkbox is checked in the assignment grid.

        Uses get_site_row to scroll the Inovua virtual grid to the correct row
        before inspecting the checkbox class, so the row need not be in the
        currently visible viewport.
        """
        try:
            row = self.get_site_row(site_name)
            checkboxes = row.find_elements(
                By.XPATH,
                ".//*[contains(@class,'inovua-react-toolkit-checkbox')"
                " and not(contains(@class,'__icon'))]"
            )
            return any(
                "inovua-react-toolkit-checkbox--checked" in (el.get_attribute("class") or "")
                and "inovua-react-toolkit-checkbox--unchecked"
                    not in (el.get_attribute("class") or "")
                for el in checkboxes
            )
        except Exception:
            return False

    def select_all_sites(self):
        """Click the Select All header checkbox to select all sites.

        Inovua's tristate header checkbox deselects all when in indeterminate
        state (some-but-not-all rows checked). Normalise to unchecked first so
        the click always transitions to the all-checked state.
        """
        import time as _ts
        header_checkbox = self.wait.until(
            EC.element_to_be_clickable(self.SITE_ASSIGNMENT_HEADER_CHECKBOX)
        )
        classes = header_checkbox.get_attribute("class") or ""
        if "inovua-react-toolkit-checkbox--unchecked" not in classes:
            # Indeterminate or checked: one click reaches the unchecked state.
            self.driver.execute_script("arguments[0].click();", header_checkbox)
            _ts.sleep(0.5)
            header_checkbox = self.wait.until(
                EC.element_to_be_clickable(self.SITE_ASSIGNMENT_HEADER_CHECKBOX)
            )
        # From unchecked state: click selects all rows.
        self.driver.execute_script("arguments[0].click();", header_checkbox)

    def click_download_button(self):
        """Click the export/download button."""
        button = self.wait.until(EC.element_to_be_clickable(self.DOWNLOAD_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)

    def click_cancel(self):
        """Cancel create/edit package."""
        self.click(self.CANCEL_BUTTON)

    def update_package_name(self, old_name, new_name):
        """Update package service name and return to the list."""
        self.open_edit_package(old_name)
        self.enter_service_name(new_name)
        self.ensure_active_switch_on()
        self.click_save_package()
        try:
            self.wait_for_list_loaded()
        except TimeoutException:
            return

    def create_package(
        self,
        service_name,
        points_awarded,
        points_redeemed,
        global_price,
        global_commission,
        site_name,
        barcode=None,
        controller_code=None,
        location_price=None,
    ):
        """Create an active wash package and force navigation back to the list.

        Staging does not auto-redirect after create; we force navigation so
        callers don't depend on the SPA redirect behavior.
        """
        self.open_create_package()
        self.fill_package_form(
            service_name,
            points_awarded,
            points_redeemed,
            global_price,
            global_commission,
            site_name,
            barcode=barcode,
            controller_code=controller_code,
            location_price=location_price,
        )
        self.save_and_return_to_list()
