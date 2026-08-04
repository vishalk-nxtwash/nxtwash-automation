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
    EXPORT_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Export') or contains(normalize-space(),'Download')] | "
        "//span[contains(normalize-space(),'Export') or contains(normalize-space(),'Download')]"
        "/ancestor::button[1]"
    )
    ROWS_PER_PAGE_SELECT = (
        By.XPATH,
        "//select[contains(@name,'pageSize') or contains(@name,'perPage') "
        "or contains(@name,'size')] | "
        "//*[@aria-label='Rows per page' or @aria-label='Per page' "
        "or contains(@class,'per-page')]//select"
    )

    def wait_for_loaded(self):
        self.driver.switch_to.default_content()
        WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME))
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
        element.click()
        element.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        element.send_keys(role_name)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value") == role_name
        )

    def clear_search(self):
        element = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        element.click()
        element.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
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

    def select_site_filter(self, site_name):
        self.open_filter_panel()
        self.click(self.SITE_FILTER_INPUT)
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "//*[@role='option' and normalize-space()='%s']" % site_name)
            )
        ).click()

    def apply_filters(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.element_to_be_clickable(self.ADD_ROLE_BUTTON))

    def reset_filters(self):
        self.open_filter_panel()
        btn = self.wait.until(EC.presence_of_element_located(self.RESET_ALL_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.element_to_be_clickable(self.ADD_ROLE_BUTTON))

    def click_export_button(self):
        el = self.wait.until(EC.element_to_be_clickable(self.EXPORT_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def get_rows_per_page_options(self):
        """Return a list of string values from the rows-per-page select control."""
        sel = self.wait.until(EC.presence_of_element_located(self.ROWS_PER_PAGE_SELECT))
        from selenium.webdriver.support.ui import Select
        return [o.text.strip() for o in Select(sel).options if o.text.strip()]

    def select_rows_per_page(self, value):
        """Select a specific rows-per-page value (e.g. '25', '50')."""
        sel = self.wait.until(EC.element_to_be_clickable(self.ROWS_PER_PAGE_SELECT))
        from selenium.webdriver.support.ui import Select
        Select(sel).select_by_visible_text(str(value))

    def get_site_filter_all_options(self):
        """Return all site names visible in the opened site filter dropdown."""
        self.open_filter_panel()
        self.click(self.SITE_FILTER_INPUT)
        options = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[@role='option']")
            )
        )
        return [o.text.strip() for o in options if o.text.strip()]

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
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(AdminUserRolesPage.CREATE_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.ROLE_NAME_INPUT))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))

    def wait_for_edit_loaded(self):
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(AdminUserRolesPage.EDIT_FRAME)
        )
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
        el = self.wait.until(EC.visibility_of_element_located(self.PRIORITY_INPUT))
        # React controlled numeric input: JS setter + input event required to update state
        self.driver.execute_script("""
            var input = arguments[0];
            var val = arguments[1];
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            ).set;
            setter.call(input, val);
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
        """, el, str(value))

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

    def _section_header(self, section_name):
        """Return the clickable accordion header element for a permission section."""
        els = self.driver.find_elements(
            By.XPATH,
            "//button[normalize-space()='%s'] | "
            "//*[@role='button' and normalize-space()='%s']" % (section_name, section_name)
        )
        if not els:
            from selenium.common.exceptions import TimeoutException
            raise TimeoutException("Permission section header not found: %s" % section_name)
        return els[0]

    def permission_section_is_expanded(self, section_name):
        """Return True if the section accordion is open (children are visible)."""
        header = self._section_header(section_name)
        expanded = header.get_attribute("aria-expanded")
        if expanded is not None:
            return expanded == "true"
        # Fallback: check if siblings contain visible switches
        children = self._get_section_child_switches(section_name)
        return any(sw.is_displayed() for sw in children)

    def expand_permission_section(self, section_name):
        if not self.permission_section_is_expanded(section_name):
            header = self._section_header(section_name)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", header
            )
            header.click()
            self.wait.until(lambda d: self.permission_section_is_expanded(section_name))

    def _get_section_child_switches(self, section_name):
        """Return all child switch buttons within a permission section."""
        return self.driver.execute_script("""
            var sectionName = arguments[0];
            var headers = Array.from(document.querySelectorAll('button, [role="button"]'));
            var header = headers.find(function(el) {
                return el.textContent.trim() === sectionName;
            });
            if (!header) return [];
            // Walk up to find the section container, then find all switches below it
            var container = header.parentElement;
            for (var i = 0; i < 5; i++) {
                if (!container) break;
                var switches = container.querySelectorAll('button[role="switch"]');
                // Return all switches except the header's own parent switch
                if (switches.length > 1) {
                    return Array.from(switches).filter(function(sw) {
                        return !header.contains(sw) && sw !== header;
                    });
                }
                container = container.parentElement;
            }
            return [];
        """, section_name)

    def _get_section_parent_switch(self, section_name):
        """Return the parent (master) switch for the given section, if present."""
        return self.driver.execute_script("""
            var sectionName = arguments[0];
            var headers = Array.from(document.querySelectorAll('button, [role="button"]'));
            var header = headers.find(function(el) {
                return el.textContent.trim() === sectionName;
            });
            if (!header) return null;
            var container = header.closest('li, .accordion-item, [class*="section"]');
            if (!container) container = header.parentElement;
            // The parent switch is the first visible switch in the header row
            var rowSwitches = header.parentElement
                ? header.parentElement.querySelectorAll('button[role="switch"]')
                : [];
            return rowSwitches.length > 0 ? rowSwitches[0] : null;
        """, section_name)

    def all_section_children_on(self, section_name):
        children = self._get_section_child_switches(section_name)
        if not children:
            return False
        return all(sw.get_attribute("aria-checked") == "true" for sw in children)

    def all_section_children_off(self, section_name):
        children = self._get_section_child_switches(section_name)
        if not children:
            return False
        return all(sw.get_attribute("aria-checked") == "false" for sw in children)

    def enable_permission_section(self, section_name):
        """Turn the parent switch ON for a permission section."""
        parent = self._get_section_parent_switch(section_name)
        if parent and parent.get_attribute("aria-checked") != "true":
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", parent
            )
            parent.click()
            self.wait.until(
                lambda d: (
                    self._get_section_parent_switch(section_name).get_attribute("aria-checked")
                    == "true"
                )
            )

    def disable_permission_section(self, section_name):
        """Turn the parent switch OFF for a permission section."""
        parent = self._get_section_parent_switch(section_name)
        if parent and parent.get_attribute("aria-checked") != "false":
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", parent
            )
            parent.click()
            self.wait.until(
                lambda d: (
                    self._get_section_parent_switch(section_name).get_attribute("aria-checked")
                    == "false"
                )
            )

    def toggle_first_child_permission(self, section_name):
        """Toggle the first child switch in a section and return the new state."""
        children = self._get_section_child_switches(section_name)
        if not children:
            return None
        child = children[0]
        before = child.get_attribute("aria-checked")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", child
        )
        child.click()
        expected = "false" if before == "true" else "true"
        self.wait.until(lambda d: child.get_attribute("aria-checked") == expected)
        return expected == "true"

    def get_first_child_permission_state(self, section_name):
        children = self._get_section_child_switches(section_name)
        if not children:
            return None
        return children[0].get_attribute("aria-checked") == "true"

    def any_section_header_visible(self):
        """Return True if at least one known permission section header is visible."""
        for name in self.KNOWN_PERMISSION_SECTIONS:
            els = self.driver.find_elements(
                By.XPATH,
                "//button[normalize-space()='%s'] | "
                "//*[@role='button' and normalize-space()='%s']" % (name, name)
            )
            if any(el.is_displayed() for el in els):
                return True
        return False

    def any_section_expanded(self):
        """Return True if any permission section is currently expanded."""
        for name in self.KNOWN_PERMISSION_SECTIONS:
            els = self.driver.find_elements(
                By.XPATH,
                "//button[normalize-space()='%s'][@aria-expanded='true'] | "
                "//*[@role='button' and normalize-space()='%s'][@aria-expanded='true']"
                % (name, name)
            )
            if els:
                return True
        return False
