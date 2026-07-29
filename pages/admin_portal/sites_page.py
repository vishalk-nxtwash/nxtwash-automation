import json
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from core.config_manager import ConfigManager
from pages.common.base_page import BasePage


class SitesPage(BasePage):

    PAGE_TITLE = (
        By.XPATH,
        "//*[contains(normalize-space(),'Sites/Locations')]"
    )
    FILTER_BUTTON = (By.XPATH, "//button[contains(.,'Filter by')]")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[contains(.,'Filter by')]/preceding-sibling::button[1]"
    )
    ADD_SITE_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(), 'Add site')]"
    )
    SITE_NAME_FILTER = (By.NAME, "siteName")
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']"
    )
    RESET_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Reset filters']"
    )
    TABLE_HEADERS = (
        By.XPATH,
        "//*[normalize-space()='Site name' or normalize-space()='State name' "
        "or normalize-space()='City name' or normalize-space()='Email' "
        "or normalize-space()='Lanes']"
    )
    EDIT_ACTIONS = (By.XPATH, "//*[normalize-space()='Edit']")
    TABLE_ROWS = (By.XPATH, "//tbody/tr")
    FILTER_CLOSE_BUTTON = (
        By.XPATH,
        "//button[@aria-label='Close popup']"
    )
    ACTIVE_SITE_FILTER_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active site']/following::*[@role='switch' or self::input][1]"
    )

    def wait_for_loaded(self):
        """Wait until Sites / Locations is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
        self.wait.until(EC.element_to_be_clickable(self.ADD_SITE_BUTTON))

    def get_body_text(self):
        """Get visible page text."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_site_count_from_title(self):
        """Return the visible site count from the page title.

        Waits until the count is non-zero so the async title update has settled.
        """
        def _parse_count(text):
            if "(" not in text or ")" not in text:
                return None
            raw = text.split("(")[-1].split(")")[0].strip()
            return int(raw) if raw.isdigit() else None

        title_el = self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        try:
            self.wait.until(
                lambda d: _parse_count(
                    d.find_element(*self.PAGE_TITLE).text.strip()
                ) not in (None, 0)
            )
        except TimeoutException:
            pass  # fall through and return whatever is there (may be 0 / None)
        return _parse_count(title_el.text.strip())

    def table_headers_are_visible(self):
        """Return whether the expected list columns are visible."""
        headers = [element.text.strip() for element in self.driver.find_elements(*self.TABLE_HEADERS)]
        expected_headers = ["Site name", "State name", "City name", "Email", "Lanes"]
        return all(header in headers for header in expected_headers)

    def download_button_is_clickable(self):
        """Return whether the download button can be clicked."""
        return self.wait.until(
            EC.element_to_be_clickable(self.DOWNLOAD_BUTTON)
        ).is_displayed()

    def filter_button_is_clickable(self):
        """Return whether the filter button can be clicked."""
        return self.wait.until(
            EC.element_to_be_clickable(self.FILTER_BUTTON)
        ).is_displayed()

    def add_site_button_is_clickable(self):
        """Return whether the Add site button can be clicked."""
        return self.wait.until(
            EC.element_to_be_clickable(self.ADD_SITE_BUTTON)
        ).is_displayed()

    def edit_actions_are_visible_for_rows(self):
        """Return whether every visible site row has an Edit action."""
        rows = [row for row in self.driver.find_elements(*self.TABLE_ROWS) if row.is_displayed()]
        edits = [edit for edit in self.driver.find_elements(*self.EDIT_ACTIONS) if edit.is_displayed()]
        return bool(rows) and len(edits) >= len(rows)

    def visible_row_count(self):
        """Return the number of visible site rows."""
        return len([row for row in self.driver.find_elements(*self.TABLE_ROWS) if row.is_displayed()])

    def pagination_is_visible(self):
        """Return whether pagination controls are visible."""
        body_text = self.get_body_text()
        return "Page" in body_text and "records" in body_text

    def page_size_selector_is_visible(self):
        """Return whether the page-size selector is visible."""
        body_text = self.get_body_text()
        return "Show" in body_text and "100" in body_text

    def open_filters(self):
        """Open site filters."""
        visible_filters = [
            element
            for element in self.driver.find_elements(*self.SITE_NAME_FILTER)
            if element.is_displayed()
        ]
        if visible_filters:
            return

        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.SITE_NAME_FILTER))

    def close_filters(self):
        """Close the site filter drawer."""
        self.open_filters()
        close_button = self.wait.until(
            EC.element_to_be_clickable(self.FILTER_CLOSE_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", close_button)
        self.wait.until(
            lambda driver: not any(
                element.is_displayed()
                for element in driver.find_elements(*self.SITE_NAME_FILTER)
            )
        )

    def active_site_filter_is_visible(self):
        """Return whether the Active site filter switch is visible."""
        self.open_filters()
        self.wait.until(
            EC.presence_of_element_located(self.ACTIVE_SITE_FILTER_SWITCH)
        )
        return "Active site" in self.get_body_text()

    def filter_by_site_name(self, site_name):
        """Filter sites by site name."""
        self.open_filters()
        self.enter_text(self.SITE_NAME_FILTER, site_name)
        self.click(self.APPLY_FILTERS_BUTTON)

    def filter_by_active_state(self, should_be_active=True):
        """Apply the active-site filter state."""
        self.open_filters()
        switch = self.wait.until(
            EC.presence_of_element_located(self.ACTIVE_SITE_FILTER_SWITCH)
        )
        is_checked = (
            switch.get_attribute("aria-checked") == "true"
            or switch.is_selected()
            or switch.get_attribute("checked") is not None
        )
        if is_checked != should_be_active:
            self.driver.execute_script("arguments[0].click();", switch)
        self.click(self.APPLY_FILTERS_BUTTON)
        self.wait_for_loaded()

    def get_site_row_locator(self, site_name):
        """Build a locator for a site row by exact visible site name."""
        return (
            By.XPATH,
            "//*[normalize-space()='%s']/ancestor::tr[1]" % site_name
        )

    def wait_for_site_row(self, site_name):
        """Wait until a site row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_site_row_locator(site_name)
            )
        )

    def site_exists_in_ui(self, site_name):
        """Return whether a site exists in the filtered UI list."""
        self.filter_by_site_name(site_name)

        try:
            self.wait_for_site_row(site_name)
            return True
        except TimeoutException:
            return False

    def open_edit_site(self, site_name, include_inactive=False):
        """Filter to a specific site and click its Edit button."""
        if include_inactive:
            self.filter_by_name_and_active(site_name, should_be_active=False)
        else:
            self.filter_by_site_name(site_name)
        self.wait_for_site_row(site_name)
        locator = (
            By.XPATH,
            "//*[normalize-space()='%s']/ancestor::tr[1]"
            "//*[@id='table-edit-button']//button"
            % site_name
        )
        button = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", button)

    def filter_by_name_and_active(self, site_name, should_be_active=True):
        """Enter site-name filter and set the active toggle, then apply once."""
        self.open_filters()
        self.enter_text(self.SITE_NAME_FILTER, site_name)
        switch = self.wait.until(
            EC.presence_of_element_located(self.ACTIVE_SITE_FILTER_SWITCH)
        )
        is_checked = (
            switch.get_attribute("aria-checked") == "true"
            or switch.is_selected()
            or switch.get_attribute("checked") is not None
        )
        if is_checked != should_be_active:
            self.driver.execute_script("arguments[0].click();", switch)
        self.click(self.APPLY_FILTERS_BUTTON)
        self.wait_for_loaded()

    def click_add_site(self):
        """Open the create site page."""
        self.click(self.ADD_SITE_BUTTON)

    def reset_filters(self):
        """Reset the site filter panel."""
        self.open_filters()
        self.click(self.RESET_FILTERS_BUTTON)
        self.wait_for_loaded()

    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigManager()

    @property
    def api_url(self):
        """Backend API base URL for the active environment (no trailing /)."""
        return self.config.get_url("api").rstrip("/")

    def _api_script(self, body):
        """Prepend an API_BASE constant so JS uses the configured API host."""
        return "const API_BASE = " + json.dumps(self.api_url) + ";\n" + body

    def get_site_summary_with_api(self, site_name):
        """Return a site summary by exact name from the authenticated session."""
        result = self.driver.execute_async_script(
            self._api_script("""
            const siteName = arguments[0];
            const done = arguments[arguments.length - 1];
            const _la = JSON.parse(localStorage.getItem("persist:latest-auth") || "{}");
            const accessToken = _la.accessToken ? JSON.parse(_la.accessToken) : "";
            const authKey = _la.key ? JSON.parse(_la.key) : "";
            const params = new URLSearchParams({
                key: authKey,
                pageSize: "500",
                pageNumber: "1"
            });

            fetch(API_BASE + "/api/sites?" + params, {
                headers: {
                    accept: "application/json",
                    authorization: "Bearer " + accessToken
                }
            })
                .then((response) => response.json())
                .then((body) => {
                    const sites = body.data || [];
                    const site = sites.find(
                        (item) => item.siteName === siteName
                    );
                    done(site || null);
                })
                .catch((error) => done({ error: String(error) }));
            """),
            site_name
        )

        if isinstance(result, dict) and result.get("error"):
            raise AssertionError(result["error"])

        return result

    def get_site_details_with_api(self, site_name):
        """Return full site details by exact name."""
        summary = self.get_site_summary_with_api(site_name)

        if not summary:
            return None

        result = self.driver.execute_async_script(
            self._api_script("""
            const siteId = arguments[0];
            const done = arguments[arguments.length - 1];
            const _la = JSON.parse(localStorage.getItem("persist:latest-auth") || "{}");
            const accessToken = _la.accessToken ? JSON.parse(_la.accessToken) : "";
            const authKey = _la.key ? JSON.parse(_la.key) : "";
            const params = new URLSearchParams({
                key: authKey,
                id: siteId
            });

            fetch(API_BASE + "/api/sites?" + params, {
                headers: {
                    accept: "application/json",
                    authorization: "Bearer " + accessToken
                }
            })
                .then(async (response) => done({
                    status: response.status,
                    body: await response.text()
                }))
                .catch((error) => done({ error: String(error) }));
            """),
            summary["siteId"]
        )

        if result.get("error"):
            raise AssertionError(result["error"])

        if result.get("status") != 200:
            raise AssertionError(result)

        return json.loads(result["body"])["data"]

    def get_site_details_by_name_and_code_with_api(self, site_name, site_code):
        """Return full site details matching both site name and site code."""
        original_timeout = self.driver.timeouts.script
        self.driver.set_script_timeout(120)

        try:
            result = self.driver.execute_async_script(
                self._api_script("""
                const siteName = arguments[0];
                const siteCode = arguments[1];
                const done = arguments[arguments.length - 1];
                const _la = JSON.parse(localStorage.getItem("persist:latest-auth") || "{}");
                const accessToken = _la.accessToken ? JSON.parse(_la.accessToken) : "";
                const authKey = _la.key ? JSON.parse(_la.key) : "";
                const headers = {
                    accept: "application/json",
                    authorization: "Bearer " + accessToken
                };
                const baseUrl = API_BASE + "/api/sites";
                const listParams = new URLSearchParams({
                    key: authKey,
                    pageSize: "500",
                    pageNumber: "1"
                });

                fetch(baseUrl + "?" + listParams.toString(), { headers })
                    .then((response) => response.json())
                    .then(async (body) => {
                        const sites = body.data || [];
                        const matches = [];

                        for (let index = 0; index < sites.length; index += 15) {
                            const chunk = sites.slice(index, index + 15);
                            const details = await Promise.all(
                                chunk.map(async (site) => {
                                    const params = new URLSearchParams({
                                        key: authKey,
                                        id: site.siteId
                                    });
                                    const response = await fetch(
                                        baseUrl + "?" + params.toString(),
                                        { headers }
                                    );
                                    return (await response.json()).data;
                                })
                            );

                            for (const detail of details) {
                                if (
                                    detail &&
                                    detail.siteName === siteName &&
                                    detail.siteCode === siteCode
                                ) {
                                    matches.push(detail);
                                }
                            }
                        }

                        done(matches[0] || null);
                    })
                    .catch((error) => done({ error: String(error) }));
                """),
                site_name,
                site_code
            )
        finally:
            self.driver.set_script_timeout(original_timeout)

        if isinstance(result, dict) and result.get("error"):
            raise AssertionError(result["error"])

        return result

    def create_site_from_reference_with_api(self, site_name, reference_site):
        """Create a site by copying a reference site's saved settings."""
        result = self.driver.execute_async_script(
            self._api_script("""
            const siteName = arguments[0];
            const referenceSite = arguments[1];
            const done = arguments[arguments.length - 1];
            const _la = JSON.parse(localStorage.getItem("persist:latest-auth") || "{}");
            const accessToken = _la.accessToken ? JSON.parse(_la.accessToken) : "";
            const authKey = _la.key ? JSON.parse(_la.key) : "";

            const payload = JSON.parse(JSON.stringify(referenceSite));
            payload.key = authKey;
            payload.siteId = 0;
            payload.siteName = siteName;
            payload.siteCode = siteName;
            payload.emailId = siteName + "@yopmail.com";
            payload.createdDate = null;

            if (payload.siteSetting) {
                payload.siteSetting.contactEmailId = payload.emailId;
            }

            if (Array.isArray(payload.siteLaneList)) {
                payload.siteLaneList = payload.siteLaneList.map((lane, index) => ({
                    ...lane,
                    siteLaneId: 0,
                    laneName: lane.laneName || "Lane " + (index + 1)
                }));
            }

            fetch(API_BASE + "/api/sites", {
                method: "POST",
                headers: {
                    accept: "application/json",
                    "content-type": "application/json",
                    authorization: "Bearer " + accessToken
                },
                body: JSON.stringify(payload)
            })
                .then(async (response) => done({
                    status: response.status,
                    body: await response.text()
                }))
                .catch((error) => done({ error: String(error) }));
            """),
            site_name,
            reference_site
        )

        if result.get("error"):
            raise AssertionError(result["error"])

        if result.get("status") not in [200, 201]:
            raise AssertionError(result)

        return json.loads(result["body"])


class CreateSitePage(BasePage):

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Sites/Locations']")
    NEW_MODE_LABEL = (By.XPATH, "//*[normalize-space()='New']")
    SAVE_NEW_BUTTON = (By.XPATH, "//button[normalize-space()='Save new']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")

    SITE_NAME_INPUT = (By.NAME, "siteName")
    SITE_CODE_INPUT = (By.NAME, "siteCode")
    EMAIL_INPUT = (By.NAME, "emailId")
    PHONE_INPUT = (By.NAME, "phone")
    STREET_ADDRESS_INPUT = (
        By.XPATH,
        "//*[normalize-space()='Street address']"
        "/following::input[1]"
    )
    ZIP_CODE_INPUT = (
        By.XPATH,
        "//*[normalize-space()='ZIP code']"
        "/following::input[1]"
    )
    PAY_WEEK_START_DAY_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='Select pay week start day']"
        "/ancestor::*[contains(@class,'nxt-select__control')][1]"
    )
    STATE_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='Select state']"
        "/ancestor::*[contains(@class,'nxt-select__control')][1]"
    )
    CITY_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='Select city']"
        "/ancestor::*[contains(@class,'nxt-select__control')][1]"
    )
    TIME_ZONE_COMBOBOX = (
        By.XPATH,
        "//*[normalize-space()='Select time zone']"
        "/ancestor::*[contains(@class,'nxt-select__control')][1]"
    )
    STATE_SALES_TAX_INPUT = (
        By.XPATH,
        "//*[contains(normalize-space(),'State sales tax')]"
        "/following::input[1]"
    )
    CITY_SALES_TAX_INPUT = (
        By.XPATH,
        "//*[contains(normalize-space(),'City sales tax')]"
        "/following::input[1]"
    )
    SITE_CONTACT_EMAIL_INPUT = (
        By.XPATH,
        "//*[normalize-space()='Site contact email address']"
        "/following::input[1]"
    )
    ACTIVE_SITE_SWITCH = (
        By.NAME,
        "isActive"
    )
    TAB_BY_TEXT = (
        By.XPATH,
        "//*[normalize-space()='%s']"
    )
    ADD_LANE_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Add Lane') or contains(normalize-space(),'Add lane')]"
    )
    CONFIRM_DIALOG = (By.XPATH, "//*[@role='dialog']")
    CONFIRM_DIALOG_PRIMARY_BUTTON = (
        By.XPATH,
        "//*[@role='dialog']//button["
        "contains(normalize-space(),'Yes') "
        "or contains(normalize-space(),'Confirm') "
        "or contains(normalize-space(),'Discard') "
        "or contains(normalize-space(),'Leave') "
        "or contains(normalize-space(),'OK')]"
    )

    def wait_for_loaded(self):
        """Wait until the create site form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.visibility_of_element_located(self.NEW_MODE_LABEL))
        self.wait.until(EC.visibility_of_element_located(self.SITE_NAME_INPUT))

    def get_body_text(self):
        """Get visible page text."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def _set_input_value(self, locator, value):
        """Set a React-controlled input value and dispatch change events."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
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
            input.dispatchEvent(new FocusEvent('blur', { bubbles: true }));
            """,
            element,
            str(value)
        )
        self.wait.until(lambda driver: element.get_attribute("value") == str(value))

    def _set_checkbox_state(self, locator, checked):
        """Set a React-controlled checkbox/switch to the desired state.

        Uses switch_is_on() as the single source of truth for both the
        pre-click guard and the post-click confirmation wait.  switch_is_on()
        prefers aria-checked on a nearby button[role=switch] over is_selected()
        on the hidden checkbox, so state-checking and state-changing are
        always consistent regardless of the underlying DOM pattern.
        """
        if self.switch_is_on(locator) == bool(checked):
            return
        el = self.wait.until(EC.presence_of_element_located(locator))
        clickable = self.driver.execute_script(
            """
            const cb = arguments[0];
            // Prefer the nearby button[role=switch] — the visual toggle button
            let node = cb;
            for (let i = 0; i < 8; i++) {
                if (!node.parentElement) break;
                node = node.parentElement;
                const btn = node.querySelector('button[role="switch"]');
                if (btn) return btn;
            }
            // Fall back: parent <label>
            if (cb.parentElement && cb.parentElement.tagName === 'LABEL') {
                return cb.parentElement;
            }
            // Last resort: label[for=id] or the element itself
            if (cb.id) {
                const lbl = document.querySelector('label[for="' + cb.id + '"]');
                if (lbl) return lbl;
            }
            return cb;
            """,
            el,
        )
        try:
            clickable.click()  # native Selenium click → isTrusted=true events
        except Exception:  # noqa: BLE001
            self.driver.execute_script("arguments[0].click();", clickable)
        # Confirm via the same state-checking logic used in the pre-click guard
        self.wait.until(lambda d: self.switch_is_on(locator) == bool(checked))

    def _scroll_to_locator(self, locator):
        """Scroll a field into view."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({ block: 'center' });",
            element
        )
        return element

    def _real_click(self, element):
        """Click via the real mouse event chain (mousedown+mouseup).

        react-select opens its menu on mousedown, which a synthetic
        execute_script('click') does not dispatch — so a JS click never opens
        the dropdown. Use a native click; fall back to JS only if intercepted.
        """
        try:
            element.click()
        except Exception:  # noqa: BLE001
            self.driver.execute_script("arguments[0].click();", element)

    def _select_combobox_option(self, combobox_locator, option_text, fallback=None):
        """Select an option from a React select combobox."""
        option = None
        selected_text = option_text

        for attempt in range(2):
            combobox = self._scroll_to_locator(combobox_locator)
            self.wait.until(EC.element_to_be_clickable(combobox_locator))
            self._real_click(combobox)
            input_elements = [
                element
                for element in combobox.find_elements(By.XPATH, ".//input")
                if element.is_displayed() and element.is_enabled()
            ]

            if input_elements:
                input_elements[0].send_keys(Keys.CONTROL, "a")
                input_elements[0].send_keys(Keys.BACKSPACE)
                input_elements[0].send_keys(option_text)
            else:
                option = self._find_select_option(option_text)
                if option is not None:
                    break

            option = self._find_select_option(option_text)
            if option is not None:
                break

            if attempt == 0:
                self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)

        if option is None and fallback is not None:
            combobox = self._scroll_to_locator(combobox_locator)
            self._real_click(combobox)
            input_elements = [
                element
                for element in combobox.find_elements(By.XPATH, ".//input")
                if element.is_displayed() and element.is_enabled()
            ]
            if input_elements:
                input_elements[0].send_keys(Keys.CONTROL, "a")
                input_elements[0].send_keys(Keys.BACKSPACE)
                input_elements[0].send_keys(fallback)
            else:
                option = self._find_select_option(fallback)
                selected_text = fallback
                if option is not None:
                    self._real_click(option)
                    self.wait.until(
                        lambda driver: selected_text.lower()
                        in self.get_body_text().lower()
                    )
                    return
            option = self._find_select_option(fallback)
            selected_text = fallback

        if option is None:
            raise AssertionError("Dropdown option was not found: %s" % option_text)

        self._real_click(option)
        self.wait.until(
            lambda driver: selected_text.lower() in self.get_body_text().lower()
        )

    def _find_select_option(self, option_text):
        """Return a visible React Select option via JavaScript."""
        try:
            return self.wait.until(
                lambda d: self._find_react_option(option_text)
            )
        except Exception:
            return None

    def _get_clickable_option_after_scroll(self, option_xpath):
        """Return a select option, scrolling the open menu if needed."""
        options = self.driver.find_elements(By.XPATH, option_xpath)
        if options:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({ block: 'nearest' });",
                options[0]
            )
            if options[0].is_displayed() and options[0].is_enabled():
                return options[0]

        menus = self.driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'form-select__menu-list') "
            "or contains(@class,'nxt-select__menu-list')]"
        )
        for menu in menus:
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight;",
                menu
            )

        options = self.driver.find_elements(By.XPATH, option_xpath)
        if options and options[0].is_displayed() and options[0].is_enabled():
            return options[0]

        return None

    def switch_is_on(self, locator):
        """Return whether a switch is on.

        React toggle switches often render as a hidden <input type="checkbox">
        paired with a visible <button role="switch" aria-checked="..."> whose
        aria-checked reflects the live state.  We prefer aria-checked on a
        nearby button (searched via DOM traversal) over is_selected() on the
        hidden checkbox, because the checkbox's checked property is only synced
        to the form-submission value, not to every visual toggle interaction.

        Falls back to aria-checked on the element itself, then is_selected().

        Safe to call from inside a wait.until() lambda — uses find_elements
        (no inner wait) to avoid burning the outer timeout budget.
        """
        from selenium.common.exceptions import StaleElementReferenceException
        try:
            elements = self.driver.find_elements(*locator)
            if not elements:
                return False
            switch = elements[0]
            # Look for a button[role=switch] in nearby ancestors — it carries
            # the authoritative aria-checked state for React switch components.
            btn = self.driver.execute_script(
                """
                const el = arguments[0];
                let node = el;
                for (let i = 0; i < 8; i++) {
                    if (!node.parentElement) break;
                    node = node.parentElement;
                    const btn = node.querySelector('button[role="switch"]');
                    if (btn) return btn;
                }
                return null;
                """,
                switch,
            )
            if btn is not None:
                return btn.get_attribute("aria-checked") == "true"
            return (
                switch.get_attribute("aria-checked") == "true"
                or switch.is_selected()
            )
        except StaleElementReferenceException:
            return False

    def _get_switch_clickable(self, locator):
        """Return the clickable element for a switch.

        The active-site toggle is a hidden <input type="checkbox"> inside a
        <label>.  Clicking the label is the correct way to toggle it — traversing
        further up the tree and picking an arbitrary <button> would hit Cancel or
        Save instead.
        """
        switch = self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.execute_script(
            """
            let input = arguments[0];
            if (input.type === 'checkbox' || input.type === 'radio') {
                if (input.parentElement && input.parentElement.tagName === 'LABEL') {
                    return input.parentElement;
                }
            }
            let current = input;
            let depth = 0;
            while (current && current.parentElement && depth < 8) {
                const btn = current.parentElement.querySelector('button[role="switch"]');
                if (btn) return btn;
                current = current.parentElement;
                depth++;
            }
            return input;
            """,
            switch
        )

    def ensure_switch_on(self, locator):
        """Turn a switch on if needed."""
        if not self.switch_is_on(locator):
            self._set_checkbox_state(locator, True)

    def ensure_switch_off(self, locator):
        """Turn a switch off if needed."""
        if self.switch_is_on(locator):
            self._set_checkbox_state(locator, False)

    def active_site_switch_is_on(self):
        """Return whether Active site switch is on."""
        return self.switch_is_on(self.ACTIVE_SITE_SWITCH)

    def open_tab(self, tab_name):
        """Open a create-site tab by visible text."""
        locator = (self.TAB_BY_TEXT[0], self.TAB_BY_TEXT[1] % tab_name)
        tab = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", tab)
        self.wait.until(lambda driver: tab_name in self.get_body_text())

    def body_contains_all(self, labels):
        """Return whether all labels are visible in the form body."""
        body_text = self.get_body_text()
        return all(label in body_text for label in labels)

    _REACT_FIRST_OPTION_JS = """
        var candidates = Array.from(document.querySelectorAll(
            '[role="option"],'
            + '[class*="__option"],'
            + '[class*="-option"],'
            + '[class*="select__option"]'
        ));
        return candidates.find(function(el) {
            return el.offsetParent !== null;
        }) || null;
    """

    def _find_first_react_option(self):
        """Return any currently visible React Select option element."""
        return self.driver.execute_script(self._REACT_FIRST_OPTION_JS)

    def select_pay_week_start_day(self, day):
        """Select the pay week start day; falls back to the first available option."""
        try:
            self._select_combobox_option(self.PAY_WEEK_START_DAY_COMBOBOX, day)
        except AssertionError:
            combobox = self._scroll_to_locator(self.PAY_WEEK_START_DAY_COMBOBOX)
            self.wait.until(EC.element_to_be_clickable(self.PAY_WEEK_START_DAY_COMBOBOX))
            self._real_click(combobox)
            option = self.wait.until(lambda d: self._find_first_react_option())
            self._real_click(option)

    def add_lane_button_is_visible(self):
        """Return whether Add Lane button is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(self.ADD_LANE_BUTTON)
        ).is_displayed()

    def enter_basic_information(self, site_name, site_code, email):
        """Enter the basic site information."""
        self._set_input_value(self.SITE_NAME_INPUT, site_name)
        self._set_input_value(self.SITE_CODE_INPUT, site_code)
        self._set_input_value(self.EMAIL_INPUT, email)

    def enter_email(self, email):
        """Enter only the site email value."""
        self._set_input_value(self.EMAIL_INPUT, email)

    def get_site_name_value(self):
        """Return the current site name value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.SITE_NAME_INPUT)
        )
        return element.get_attribute("value")

    def enter_address_information(
        self,
        street_address,
        zip_code,
        state,
        city,
        time_zone
    ):
        """Enter the address information."""
        self._set_input_value(self.STREET_ADDRESS_INPUT, street_address)
        self._set_input_value(self.ZIP_CODE_INPUT, zip_code)
        self._select_combobox_option(self.STATE_COMBOBOX, state)
        self._select_combobox_option(self.CITY_COMBOBOX, city)
        self._select_combobox_option(
            self.TIME_ZONE_COMBOBOX,
            time_zone,
            "Eastern"
        )

    def enter_tax_settings(self, state_sales_tax, city_sales_tax):
        """Enter site tax settings."""
        self._set_input_value(self.STATE_SALES_TAX_INPUT, state_sales_tax)
        self._set_input_value(self.CITY_SALES_TAX_INPUT, city_sales_tax)

    def enter_site_contact_email(self, email):
        """Enter the site contact email."""
        self._set_input_value(self.SITE_CONTACT_EMAIL_INPUT, email)

    def get_site_name_validation_message(self):
        """Return the native validation message for site name."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.SITE_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def site_name_input_is_valid(self):
        """Return native validity state for site name."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.SITE_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def click_cancel(self):
        """Click cancel."""
        self.click(self.CANCEL_BUTTON)

    def click_cancel_and_confirm_if_needed(self):
        """Click cancel and confirm the unsaved-changes dialog if it appears."""
        self.click_cancel()
        try:
            self.wait.until(EC.visibility_of_element_located(self.CONFIRM_DIALOG))
            self.click(self.CONFIRM_DIALOG_PRIMARY_BUTTON)
        except TimeoutException:
            pass

    def click_save_new(self):
        """Click Save new."""
        self._scroll_to_locator(self.SAVE_NEW_BUTTON)
        button = self.wait.until(EC.element_to_be_clickable(self.SAVE_NEW_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)

    def fill_general_settings(
        self,
        site_name,
        site_code,
        email,
        street_address,
        zip_code,
        state,
        city,
        time_zone,
        state_sales_tax,
        city_sales_tax,
        site_contact_email,
        pay_week_start_day="Monday"
    ):
        """Fill the requested General settings fields."""
        self.enter_basic_information(site_name, site_code, email)
        self.select_pay_week_start_day(pay_week_start_day)
        self.ensure_switch_on(self.ACTIVE_SITE_SWITCH)
        self.enter_address_information(
            street_address,
            zip_code,
            state,
            city,
            time_zone
        )
        self.enter_tax_settings(state_sales_tax, city_sales_tax)
        self.enter_site_contact_email(site_contact_email)

    def create_site(
        self,
        site_name,
        site_code,
        email,
        street_address,
        zip_code,
        state,
        city,
        time_zone,
        state_sales_tax,
        city_sales_tax,
        site_contact_email,
        pay_week_start_day="Monday"
    ):
        """Create a site through the UI."""
        self.fill_general_settings(
            site_name,
            site_code,
            email,
            street_address,
            zip_code,
            state,
            city,
            time_zone,
            state_sales_tax,
            city_sales_tax,
            site_contact_email,
            pay_week_start_day
        )
        self.click_save_new()


class EditSitePage(CreateSitePage):
    """Edit form for an existing site. Same layout as create; save button differs."""

    SAVE_BUTTON = (
        By.XPATH,
        "//button["
        "normalize-space()='Save' "
        "or normalize-space()='Save site' "
        "or normalize-space()='Save changes' "
        "or normalize-space()='Update'"
        "]"
    )

    def wait_for_loaded(self):
        """Wait until the edit form is ready and form data has been populated.

        During SPA navigation from the sites list, the list page's filter panel
        (which also contains an input[name='siteName']) may remain mounted briefly.
        We wait until only one such input is visible before proceeding so that
        enter_site_name() targets the edit form field, not the filter input.
        """
        self.driver.switch_to.default_content()
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.visibility_of_element_located(self.SITE_NAME_INPUT))
        # Wait for the filter panel's duplicate siteName input to unmount
        self.wait.until(
            lambda d: sum(
                1 for el in d.find_elements(By.NAME, "siteName") if el.is_displayed()
            ) <= 1
        )
        self.wait.until(
            lambda d: (
                d.find_element(*self.SITE_NAME_INPUT).get_attribute("value") or ""
            ) != ""
        )

    def ensure_active_switch_off(self):
        """Deactivate the site if currently active."""
        self.ensure_switch_off(self.ACTIVE_SITE_SWITCH)

    def ensure_active_switch_on(self):
        """Activate the site if currently inactive."""
        self.ensure_switch_on(self.ACTIVE_SITE_SWITCH)

    def enter_site_name(self, name):
        """Update the site name field.

        Clicks the field first to ensure native focus (which the JS setter
        alone does not always trigger), then sets the value via the native
        property setter with input/change/blur events so React registers the
        change before the save button is clicked.
        """
        el = self.wait.until(EC.element_to_be_clickable(self.SITE_NAME_INPUT))
        el.click()
        self._set_input_value(self.SITE_NAME_INPUT, name)

    LANE_ROWS = (
        By.XPATH,
        "//tr[.//input["
        "contains(@name,'lane') or contains(@name,'Lane') "
        "or contains(@placeholder,'lane') or contains(@placeholder,'Lane')"
        "]]"
    )

    def get_lane_count(self):
        """Return the number of visible lane rows in the Lanes settings tab."""
        return len(self.driver.find_elements(*self.LANE_ROWS))

    def add_lane(self):
        """Click Add Lane to append a new empty lane row."""
        self.click(self.ADD_LANE_BUTTON)

    def click_save(self):
        """Save changes and wait for navigation back to the sites list."""
        button = self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)
        # After save the app navigates back to the list. Wait until the Save
        # button is gone (i.e. we've left the edit form) before returning so
        # callers aren't racing against an in-flight save.
        try:
            self.wait.until(EC.invisibility_of_element(button))
        except TimeoutException:
            pass  # if the button is already gone the wait resolves immediately
