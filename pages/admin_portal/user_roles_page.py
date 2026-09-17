from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class AdminUserRolesPage(BasePage):
    """List page — /users/userRoles."""

    # ── Iframe locators ──────────────────────────────────────────────────────
    # The admin portal embeds module content in iframes (same pattern as
    # WashPackagesPage).  All three variants are listed so wait_for_loaded()
    # can switch into whichever frame is present for the current route.
    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/users/userRoles?') "
        "or (contains(@src,'/users/userRoles') "
        "and not(contains(@src,'/users/userRoles/')))]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/users/userRoles/new')]"
    )
    # Edit URLs contain a numeric ID: /users/userRoles/123 or /users/userRoles/edit/123
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/users/userRoles/') "
        "and not(contains(@src,'/users/userRoles/new'))]"
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='User roles']")
    ADD_ROLE_BUTTON = (
        By.XPATH,
        "//span[@data-type='primary' and normalize-space()='+ Add user role'] | "
        "//*[normalize-space()='+ Add user role']"
    )
    SEARCH_INPUT = (By.NAME, "roleName")
    FILTER_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Filter by')] | "
        "//*[@role='button' and contains(normalize-space(),'Filter by')]"
    )
    SITE_FILTER_INPUT = (
        By.XPATH,
        "//*[normalize-space()='Select site']/following::input[1]"
    )
    # Anchor from "Select site" label/placeholder — works whether "Select site" is
    # a placeholder inside the control (ancestor path) or an external label (following path).
    SITE_FILTER_CONTROL = (By.XPATH,
        "//*[contains(@class,'nxt-select__placeholder') and contains(normalize-space(),'Select site')]"
        "/ancestor::*[contains(@class,'nxt-select__control')][1]"
    )
    ACTIVE_FILTER_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active' or normalize-space()='Show active only']"
        "/following::*[@role='switch' or self::input[@type='checkbox']][1]"
    )
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']"
    )
    RESET_ALL_BUTTON = (By.XPATH, "//button[normalize-space()='Reset all']")
    # Export: first click the download icon to open the panel, then submit the form
    EXPORT_ICON_BUTTON = (
        By.XPATH,
        "//button[.//svg[contains(@class,'lucide-download')]]"
    )
    EXPORT_SUBMIT_BUTTON = (
        By.XPATH,
        "//button[@type='submit' and @form='user-roles-export-form']"
    )
    # Rows-per-page is an nxt-select whose current value reads "Show N"
    ROWS_PER_PAGE_SELECT = (
        By.XPATH,
        "//div[contains(@class,'nxt-select__control') and "
        ".//*[contains(@class,'nxt-select__single-value') "
        "and contains(normalize-space(),'Show')]]"
    )

    def wait_for_loaded(self, frame_timeout=45):
        self.switch_to_frame_with_retry(self.LIST_FRAME, timeout=frame_timeout)
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.visibility_of_element_located(self.ADD_ROLE_BUTTON))
        # Wait for the data-loading spinner to clear so body text reflects real rows
        self.wait.until(
            lambda d: "Please wait" not in d.find_element(By.TAG_NAME, "body").text
        )

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def search_role(self, role_name):
        element = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        # JS click + select(): select() is cross-platform and reliable in headless Chrome;
        # CTRL+A can mis-fire in headless when modifier key release timing is off.
        self.driver.execute_script("arguments[0].click(); arguments[0].select();", element)
        element.send_keys(role_name)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value") == role_name
        )

    def clear_search(self):
        element = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        self.driver.execute_script("arguments[0].click(); arguments[0].select();", element)
        element.send_keys(Keys.BACKSPACE)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value") == ""
        )

    def _role_row_locator(self, role_name):
        return (
            By.XPATH,
            "//*[contains(@class,'InovuaReactDataGrid__row') and "
            ".//*[contains(normalize-space(),'%s')]]" % role_name
        )

    def wait_for_role_row(self, role_name):
        return self.wait.until(
            EC.presence_of_element_located(self._role_row_locator(role_name))
        )

    def role_exists(self, role_name):
        self.search_role(role_name)
        try:
            self.wait_for_role_row(role_name)
            return True
        except TimeoutException:
            return False

    def get_role_status(self, role_name):
        row = self.wait_for_role_row(role_name)
        try:
            return row.find_element(
                By.XPATH,
                ".//*[normalize-space()='Active' or normalize-space()='Inactive']"
            ).text.strip()
        except Exception:  # noqa: BLE001
            return ""

    def open_edit_role(self, role_name):
        self.search_role(role_name)
        rows = self.driver.find_elements(*self._role_row_locator(role_name))
        if not any(r.is_displayed() for r in rows):
            # Role is hidden by the active filter (e.g. it is inactive).
            # Toggle the filter off so inactive roles are visible too.
            self.toggle_active_filter()
            self.apply_filters()
            # The search term is still set from above. Wait up to 5 s for the
            # re-filtered list to surface the row before re-entering the search.
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda d: any(
                        el.is_displayed()
                        for el in d.find_elements(*self._role_row_locator(role_name))
                    )
                )
            except Exception:
                # Row not yet visible — re-enter the search to trigger a fresh render.
                self.search_role(role_name)
        row = self.wait_for_role_row(role_name)
        # Edit is <a role="button"> with a class containing "edit", not a <button>
        edit_link = row.find_element(
            By.XPATH,
            ".//a[@role='button' and contains(@class,'edit')]"
        )
        self.driver.execute_script("arguments[0].click();", edit_link)

    def click_add_role(self):
        el = self.wait.until(EC.visibility_of_element_located(self.ADD_ROLE_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def open_filter_panel(self):
        # Use APPLY_FILTERS_BUTTON as the "is-open" indicator: it is always visible
        # when the panel is open, regardless of whether a site has been selected
        # (selecting a site changes the "Select site" label, breaking SITE_FILTER_INPUT).
        if any(el.is_displayed() for el in self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)):
            return
        # JS click bypasses toast/overlay interception that blocks native click.
        btn = self.wait.until(EC.presence_of_element_located(self.FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.visibility_of_element_located(self.APPLY_FILTERS_BUTTON))

    def filter_panel_is_open(self):
        return any(
            el.is_displayed()
            for el in self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)
        )

    def filter_panel_has_site_and_active_controls(self):
        self.open_filter_panel()
        site_visible = any(
            el.is_displayed()
            for el in self.driver.find_elements(*self.SITE_FILTER_INPUT)
        )
        switch_present = bool(self.driver.find_elements(*self.ACTIVE_FILTER_SWITCH))
        return site_visible and switch_present

    def toggle_active_filter(self):
        self.open_filter_panel()
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_FILTER_SWITCH))
        try:
            switch.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", switch)

    def _active_filter_switch_is_on(self):
        switch = self.wait.until(EC.presence_of_element_located(self.ACTIVE_FILTER_SWITCH))
        aria = switch.get_attribute("aria-checked")
        if aria is not None:
            return aria.lower() == "true"
        return switch.is_selected()

    def ensure_active_filter_on(self):
        """Set the active-only switch to ON regardless of its current state."""
        self.open_filter_panel()
        if not self._active_filter_switch_is_on():
            switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_FILTER_SWITCH))
            try:
                switch.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", switch)

    def select_site_filter(self, site_name):
        self.open_filter_panel()
        control = self._find_site_filter_control()   # may switch to default_content
        self.driver.execute_script("arguments[0].click();", control)
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//*[contains(@class,'nxt-select__option') and normalize-space()='%s']" % site_name)
            )
        ).click()
        # Wait for the dropdown menu to close before the caller applies the filter
        try:
            WebDriverWait(self.driver, 8).until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "[class*='select__menu']")
                )
            )
        except Exception:
            pass
        # Re-enter the iframe — _find_site_filter_control may have switched to default_content
        self.switch_to_frame_with_retry(self.LIST_FRAME, timeout=30)

    def apply_filters(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.element_to_be_clickable(self.ADD_ROLE_BUTTON))

    def reset_filters(self):
        self.open_filter_panel()
        btn = self.wait.until(EC.presence_of_element_located(self.RESET_ALL_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.element_to_be_clickable(self.ADD_ROLE_BUTTON))

    def close_filter_panel_if_open(self):
        """Dismiss the filter panel by clicking Apply — no-op if already closed."""
        if not self.filter_panel_is_open():
            return
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
            self.driver.execute_script("arguments[0].click();", btn)
            # Wait for the panel itself to close rather than for the grid to finish
            # re-loading — with 279+ records on staging the grid re-load can exceed
            # the 45 s timeout, silently leaving the panel open.
            WebDriverWait(self.driver, 15).until(lambda d: not self.filter_panel_is_open())
        except Exception:
            pass

    def clear_active_filters(self):
        """Reset active filters and ensure the panel is closed.

        Skips reset_filters() when no filters are active to avoid the 45-second
        wait for the "Reset all" button that never appears on a clean page load.
        """
        try:
            body = self.get_body_text()
            if "Filter by (" in body:
                self.reset_filters()
        except Exception as exc:
            import logging
            logging.getLogger("nxtwash").warning("clear_active_filters (user_roles): %s", exc)
        self.close_filter_panel_if_open()

    def reset_filters_if_active(self):
        try:
            body = self.get_body_text()
            if "Filter by (" in body:
                self.reset_filters()
                try:
                    self.apply_filters()
                except Exception:
                    pass
        except Exception:
            pass

    # JavaScript that finds the export button by walking SVG class via getAttribute()
    # (XPath @class evaluation on SVG is unreliable in headless Chrome)
    _JS_FIND_EXPORT_BTN = """
        var svgs = document.querySelectorAll('svg');
        for (var i = 0; i < svgs.length; i++) {
            var cls = svgs[i].getAttribute('class') || '';
            if (cls.indexOf('lucide-download') >= 0) {
                var btn = svgs[i].closest('button');
                if (btn) return btn;
            }
        }
        return null;
    """

    def click_export_button(self):
        # XPath @class on SVG elements is unreliable in headless Chrome; use JS.
        # Try the current iframe context first, then fall back to the parent document.
        for _switch in (None, "default"):
            if _switch == "default":
                self.driver.switch_to.default_content()
            el = self.driver.execute_script(self._JS_FIND_EXPORT_BTN)
            if el:
                self.driver.execute_script("arguments[0].click();", el)
                return
        raise TimeoutException("Export icon button (lucide-download) not found in any frame")

    def submit_export(self):
        """Click the Export submit button inside the export panel."""
        # Submit button uses @type and @form — regular attributes work fine with XPath.
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.EXPORT_SUBMIT_BUTTON)
            )
        except Exception:
            self.driver.switch_to.default_content()
            btn = self.wait.until(EC.element_to_be_clickable(self.EXPORT_SUBMIT_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)

    def _find_rows_per_page_control(self):
        """Return the rows-per-page nxt-select control, trying iframe then parent doc."""
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.ROWS_PER_PAGE_SELECT)
            )
        except Exception:
            pass
        self.driver.switch_to.default_content()
        return self.wait.until(EC.element_to_be_clickable(self.ROWS_PER_PAGE_SELECT))

    def get_rows_per_page_options(self):
        """Return all option labels from the rows-per-page nxt-select (e.g. 'Show 25')."""
        control = self._find_rows_per_page_control()
        self.driver.execute_script("arguments[0].click();", control)
        options = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".nxt-select__option")
            )
        )
        return [o.text.strip() for o in options if o.text.strip()]

    def select_rows_per_page(self, value):
        """Select a rows-per-page option. Accepts 'Show 25' or bare '25'."""
        control = self._find_rows_per_page_control()
        self.driver.execute_script("arguments[0].click();", control)
        label = str(value) if "Show" in str(value) else "Show %s" % value
        self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//*[contains(@class,'nxt-select__option') and normalize-space()='%s']" % label
            ))
        ).click()

    def _find_site_filter_control(self):
        # Try within the current iframe context first
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.SITE_FILTER_CONTROL)
            )
        except Exception:
            pass
        # Filter panel is portalled to the main document — switch out and search there
        self.driver.switch_to.default_content()
        return self.wait.until(EC.element_to_be_clickable(self.SITE_FILTER_CONTROL))

    def get_site_filter_all_options(self):
        """Return all site names visible in the opened site filter dropdown."""
        self.open_filter_panel()
        control = self._find_site_filter_control()   # may switch to default_content
        self.driver.execute_script("arguments[0].click();", control)
        options = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".nxt-select__option")
            )
        )
        result = [o.text.strip() for o in options if o.text.strip()]
        # Re-enter the iframe — _find_site_filter_control may have switched to default_content
        self.switch_to_frame_with_retry(self.LIST_FRAME, timeout=30)
        return result

    def get_visible_row_count(self):
        rows = self.driver.find_elements(
            By.XPATH,
            "//tr[.//button[normalize-space()='Edit']] | "
            "//*[contains(@class,'row') and .//button[normalize-space()='Edit']]"
        )
        return len([r for r in rows if r.is_displayed()])


class AdminUserRoleFormPage(BasePage):
    """Create / Edit form — /users/userRoles/new and /users/userRoles/edit/{id}."""

    ROLE_NAME_INPUT = (
        By.XPATH,
        "//input[@name='roleName' or @name='name' or @name='role']"
    )
    PRIORITY_INPUT = (By.NAME, "priorityOrder")
    # Active user role toggle — lives in <div class="flex-toggler"> next to the label
    ACTIVE_SWITCH = (
        By.XPATH,
        "//div[contains(@class,'flex-toggler')]"
        "[.//*[normalize-space()='Active user role']]"
        "//button[@role='switch']"
    )
    # Save is <span data-type="primary">Save</span> — same pattern as Add button
    SAVE_BUTTON = (
        By.XPATH,
        "//span[@data-type='primary' and normalize-space()='Save'] | "
        "//*[normalize-space()='Save' and @data-type='primary']"
    )
    CANCEL_BUTTON = (
        By.XPATH,
        "//span[@data-type and normalize-space()='Cancel'] | "
        "//button[normalize-space()='Cancel']"
    )

    # ── Permission accordion ─────────────────────────────────────────────────
    KNOWN_PERMISSION_SECTIONS = [
        "Dashboard Overview",
        "Sites",
        "Services",
        "Gift Cards",
        "Customers",
        "Users",
        "Employees",
        "User Roles",
        "Kiosk Settings",
        "Kiosk App",
        "POS Settings",
        "POS App",
        "Tunnel Settings",
        "Gas Pump Settings",
        "Reports",
    ]

    def wait_for_create_loaded(self):
        self.switch_to_frame_with_retry(AdminUserRolesPage.CREATE_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.ROLE_NAME_INPUT))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))

    def wait_for_edit_loaded(self):
        self.switch_to_frame_with_retry(AdminUserRolesPage.EDIT_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.ROLE_NAME_INPUT))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        # Best-effort: wait up to 5s for React to populate the name field.
        # Don't block on this — the role may legitimately have an empty name.
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_element(*self.ROLE_NAME_INPUT).get_attribute("value") != ""
            )
        except Exception:
            pass

    def get_body_text(self):
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except Exception:
            # The create/edit iframe was removed by a post-save SPA navigation.
            # Fall back to the main document so callers like page_has_no_broken_state
            # still get a string rather than an exception.
            self.driver.switch_to.default_content()
            return self.driver.find_element(By.TAG_NAME, "body").text

    def enter_role_name(self, name):
        self.enter_text(self.ROLE_NAME_INPUT, name)

    def clear_role_name(self):
        el = self.wait.until(EC.element_to_be_clickable(self.ROLE_NAME_INPUT))
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)

    def get_role_name_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.ROLE_NAME_INPUT)
        ).get_attribute("value")

    def enter_priority(self, value):
        # type="text" inputmode="numeric" — send_keys triggers React's synthetic events correctly
        el = self.wait.until(EC.element_to_be_clickable(self.PRIORITY_INPUT))
        el.click()
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(str(value))

    def type_priority_raw(self, value):
        """Type into the priority field via real keystrokes — use for invalid-input tests."""
        self.enter_text(self.PRIORITY_INPUT, str(value))

    def get_priority_value(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.PRIORITY_INPUT)
        ).get_attribute("value")

    def active_switch_is_on(self):
        switch = self.wait.until(EC.presence_of_element_located(self.ACTIVE_SWITCH))
        return switch.get_attribute("aria-checked") == "true"

    def ensure_active_switch_on(self):
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(
                lambda d: d.find_element(*self.ACTIVE_SWITCH).get_attribute("aria-checked") == "true"
            )

    def ensure_active_switch_off(self):
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "false":
            self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(
                lambda d: d.find_element(*self.ACTIVE_SWITCH).get_attribute("aria-checked") == "false"
            )

    def click_save(self):
        url_before = self.driver.current_url
        el = self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)
        # Wait for the SPA to navigate away from the form (indicates save completed).
        # If validation fails the URL won't change — silently timeout so tests can
        # inspect the form state themselves.
        try:
            # 15 s gives CI enough headroom; fails fast locally when validation blocks.
            WebDriverWait(self.driver, 15).until(lambda d: d.current_url != url_before)
            # URL changed: SPA navigated away from the form. Release the stale iframe so
            # subsequent find_element calls don't search inside a detached frame.
            self.driver.switch_to.default_content()
        except Exception:
            error = self.get_visible_error()
            if error:
                import logging
                logging.getLogger("nxtwash").warning(
                    "Role save did not navigate away. Page message: %s", error
                )

    def click_cancel(self):
        el = self.wait.until(EC.visibility_of_element_located(self.CANCEL_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def role_name_validation_message(self):
        els = self.driver.find_elements(*self.ROLE_NAME_INPUT)
        if not els:
            return ""
        return self.driver.execute_script("return arguments[0].validationMessage;", els[0])

    def role_name_input_is_valid(self):
        # Use find_elements (no wait) so this is safe when the form navigated away after save.
        els = self.driver.find_elements(*self.ROLE_NAME_INPUT)
        if not els:
            return True  # form no longer active; cannot determine invalid state
        return self.driver.execute_script("return arguments[0].checkValidity();", els[0])

    def priority_input_is_valid(self):
        els = self.driver.find_elements(*self.PRIORITY_INPUT)
        if not els:
            return True
        return self.driver.execute_script("return arguments[0].checkValidity();", els[0])

    # ── Location checkboxes ─────────────────────────────────────────────────

    def _location_checkbox(self, site_name):
        return self.wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//*[normalize-space()='%s']"
                "/ancestor::*[.//input[@type='checkbox']][1]"
                "//input[@type='checkbox']" % site_name
            ))
        )

    def location_is_checked(self, site_name):
        try:
            return self._location_checkbox(site_name).is_selected()
        except StaleElementReferenceException:
            return self._location_checkbox(site_name).is_selected()

    def assign_location(self, site_name):
        cb = self._location_checkbox(site_name)
        if not cb.is_selected():
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", cb
            )
            self.driver.execute_script("arguments[0].click();", cb)
            self.wait.until(lambda d: self._location_checkbox(site_name).is_selected())

    def get_location_names(self):
        """Return all site-name labels shown beside location checkboxes."""
        els = self.driver.find_elements(
            By.XPATH,
            "//*[.//input[@type='checkbox']]"
            "//*[not(self::input) and normalize-space() != '']"
            "[ancestor::*[.//input[@type='checkbox']]]"
        )
        seen = set()
        names = []
        for el in els:
            text = el.text.strip()
            if text and text not in seen:
                seen.add(text)
                names.append(text)
        return names

    def remove_location(self, site_name):
        cb = self._location_checkbox(site_name)
        if cb.is_selected():
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", cb
            )
            self.driver.execute_script("arguments[0].click();", cb)
            self.wait.until(lambda d: not self._location_checkbox(site_name).is_selected())

    # ── Permission accordion ─────────────────────────────────────────────────
    # Toggles are <input type="checkbox" name="SectionName"> inside a <label>.
    # The section header contains a <svg class="lucide-chevron-down"> that gets
    # the class "rotate-180" when the section is expanded.

    def _section_header(self, section_name):
        """Return the clickable accordion header element for a permission section."""
        els = self.driver.find_elements(
            By.XPATH,
            "//*[.//svg[contains(@class,'lucide-chevron-down')] "
            "and .//*[normalize-space()='%s']]" % section_name
        )
        if not els:
            raise TimeoutException("Permission section header not found: %s" % section_name)
        return els[0]

    def permission_section_is_expanded(self, section_name):
        """Return True if the section accordion is open (chevron is rotate-180)."""
        try:
            header = self._section_header(section_name)
            svg = header.find_element(
                By.XPATH, ".//svg[contains(@class,'lucide-chevron-down')]"
            )
            return "rotate-180" in (svg.get_attribute("class") or "")
        except Exception:
            return False

    def expand_permission_section(self, section_name):
        if not self.permission_section_is_expanded(section_name):
            header = self._section_header(section_name)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", header
            )
            self.driver.execute_script("arguments[0].click();", header)
            self.wait.until(lambda d: self.permission_section_is_expanded(section_name))

    def _get_section_child_switches(self, section_name):
        """Return all child checkbox inputs within a permission section."""
        return self.driver.execute_script("""
            var sectionName = arguments[0];
            var input = document.querySelector(
                'input[type="checkbox"][name="' + sectionName + '"]'
            );
            if (!input) return [];
            var container = input.parentElement;
            for (var i = 0; i < 8; i++) {
                if (!container) break;
                var checkboxes = Array.from(
                    container.querySelectorAll('input[type="checkbox"]')
                );
                if (checkboxes.length >= 2) {
                    return checkboxes.filter(function(cb) {
                        return cb.name !== sectionName && cb.name !== '';
                    });
                }
                container = container.parentElement;
            }
            return [];
        """, section_name)

    def _get_section_parent_switch(self, section_name):
        """Return the parent checkbox input for the given section."""
        els = self.driver.find_elements(
            By.XPATH,
            "//input[@type='checkbox' and @name='%s']" % section_name
        )
        return els[0] if els else None

    def all_section_children_on(self, section_name):
        children = self._get_section_child_switches(section_name)
        if not children:
            return False
        return all(cb.is_selected() for cb in children)

    def all_section_children_off(self, section_name):
        children = self._get_section_child_switches(section_name)
        if not children:
            return False
        return all(not cb.is_selected() for cb in children)

    def enable_permission_section(self, section_name):
        """Turn the parent checkbox ON for a permission section."""
        cb = self._get_section_parent_switch(section_name)
        if cb and not cb.is_selected():
            label = self.driver.find_element(
                By.XPATH,
                "//input[@type='checkbox' and @name='%s']/parent::label" % section_name
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", label
            )
            self.driver.execute_script("arguments[0].click();", label)
            self.wait.until(
                lambda d: d.find_element(
                    By.XPATH,
                    "//input[@type='checkbox' and @name='%s']" % section_name
                ).is_selected()
            )

    def disable_permission_section(self, section_name):
        """Turn the parent checkbox OFF for a permission section."""
        cb = self._get_section_parent_switch(section_name)
        if cb and cb.is_selected():
            label = self.driver.find_element(
                By.XPATH,
                "//input[@type='checkbox' and @name='%s']/parent::label" % section_name
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", label
            )
            self.driver.execute_script("arguments[0].click();", label)
            self.wait.until(
                lambda d: not d.find_element(
                    By.XPATH,
                    "//input[@type='checkbox' and @name='%s']" % section_name
                ).is_selected()
            )

    def toggle_first_child_permission(self, section_name):
        """Toggle the first child checkbox in a section and return the new state."""
        children = self._get_section_child_switches(section_name)
        if not children:
            return None
        child = children[0]
        before = child.is_selected()
        label = self.driver.execute_script(
            "return arguments[0].closest('label');", child
        )
        target = label if label else child
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", target
        )
        self.driver.execute_script("arguments[0].click();", target)
        expected = not before
        self.wait.until(
            lambda d: self._get_section_child_switches(section_name)[0].is_selected() == expected
        )
        return expected

    def get_first_child_permission_state(self, section_name):
        children = self._get_section_child_switches(section_name)
        if not children:
            return None
        return children[0].is_selected()

    def any_section_header_visible(self):
        """Return True if at least one known permission section header is visible."""
        for name in self.KNOWN_PERMISSION_SECTIONS:
            els = self.driver.find_elements(
                By.XPATH,
                "//*[.//svg[contains(@class,'lucide-chevron-down')] "
                "and .//*[normalize-space()='%s']]" % name
            )
            if any(el.is_displayed() for el in els):
                return True
        return False

    def any_section_expanded(self):
        """Return True if any permission section accordion is currently open."""
        expanded = self.driver.find_elements(
            By.XPATH,
            "//svg[contains(@class,'lucide-chevron-down') and contains(@class,'rotate-180')]"
        )
        return any(e.is_displayed() for e in expanded)
