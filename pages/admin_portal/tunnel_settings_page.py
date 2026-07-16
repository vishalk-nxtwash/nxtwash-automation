import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class TunnelSettingsListPage(BasePage):
    """Tunnel Settings list page — /tunnel_settings/tunnels"""

    TUNNEL_LIST_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/tunnel_settings/tunnels') "
        "and not(contains(@src,'/tunnel_settings/tunnels/'))]")
    TUNNEL_CREATE_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/tunnel_settings/tunnels/new')]")
    TUNNEL_EDIT_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/tunnel_settings/tunnels/') "
        "and not(contains(@src,'/tunnel_settings/tunnels/new'))]")

    ADD_TUNNEL_BUTTON = (By.XPATH,
        "//span[@data-type='primary' and contains(normalize-space(),'Add new tunnel')] | "
        "//button[contains(normalize-space(),'Add new tunnel')] | "
        "//span[@data-type='primary' and contains(normalize-space(),'tunnel')]")

    GRID_ROWS = (By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row')] | "
        "//tr[contains(@class,'row') and not(contains(@class,'header'))]")

    EDIT_LINK = (By.XPATH,
        "//a[@role='button' and contains(@class,'table-page__page-content__table__edit')]")

    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and not(contains(@style,'display: none'))] | "
        "//*[contains(@class,'inovua-react-toolkit-load-mask')]")

    def wait_for_loaded(self):
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.TUNNEL_LIST_FRAME))
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        self.wait.until(EC.element_to_be_clickable(self.ADD_TUNNEL_BUTTON))

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def _row_locator(self, name):
        return (By.XPATH,
            "//span[contains(@class,'table-cell-ellipsis') and @title='%s'] | "
            "//span[contains(@class,'table-cell-ellipsis') and normalize-space()='%s']"
            % (name, name))

    def wait_for_tunnel_row(self, name, timeout=None):
        locator = self._row_locator(name)
        if timeout:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        return self.wait.until(EC.presence_of_element_located(locator))

    def tunnel_exists(self, name):
        try:
            self.wait_for_tunnel_row(name, timeout=15)
            return True
        except TimeoutException:
            return False

    def get_tunnel_status(self, name):
        self.wait_for_tunnel_row(name)
        try:
            row_el = self.driver.find_element(*self._row_locator(name))
            row_container = row_el.find_element(By.XPATH,
                "./ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]")
            badge = row_container.find_element(By.XPATH,
                ".//*[normalize-space()='Active' or normalize-space()='Inactive']")
            return badge.text.strip()
        except Exception:
            body = self.get_body_text()
            for status in ("Active", "Inactive"):
                if status in body:
                    return status
            return ""

    def click_add_tunnel(self):
        el = self.wait.until(EC.element_to_be_clickable(self.ADD_TUNNEL_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def open_edit_tunnel(self, name):
        self.wait_for_tunnel_row(name)
        edit_link = self.wait.until(EC.element_to_be_clickable(self.EDIT_LINK))
        self.driver.execute_script("arguments[0].click();", edit_link)

    def get_visible_row_count(self):
        rows = self.driver.find_elements(*self.GRID_ROWS)
        return len([r for r in rows if r.is_displayed()])


class TunnelSettingsFormPage(BasePage):
    """Tunnel Settings create/edit form."""

    # ── Core form fields ──────────────────────────────────────────────────────

    TUNNEL_NAME_INPUT = (By.XPATH, "//input[@placeholder='Add tunnel name']")

    # Site dropdown uses rhf-select__ prefix (not form-select__) — confirmed via DevTools
    SITE_COMBOBOX = (By.XPATH,
        "//div[contains(@class,'rhf-select__control') and "
        ".//div[contains(@class,'rhf-select__placeholder') and normalize-space()='Select site']] | "
        "//div[contains(@class,'rhf-select__control') and "
        ".//div[contains(@class,'rhf-select__single-value')]]")

    CONTROLLER_IP_INPUT = (By.XPATH, "//input[@placeholder='Add controller IP']")

    MIDDLEWARE_IP_INPUT = (By.XPATH,
        "//input[@placeholder='Add middleware IP' or @placeholder='Middleware IP' or "
        "@name='middlewareIp' or @name='middleware_ip' or @name='middlewareUrl' or "
        "contains(@placeholder,'middleware') or contains(@placeholder,'Middleware')]")

    # ── Behavior radio buttons (main form, above sections) ────────────────────

    ALL_BEHAVIOR_RADIOS = (By.XPATH,
        "//*[contains(normalize-space(),'Behavior') or "
        "normalize-space()='Behavior']"
        "/following::input[@type='radio'] | "
        "//*[contains(normalize-space(),'Behavior')]"
        "/following::*[@role='radio']")

    # ── Form actions ──────────────────────────────────────────────────────────

    # Confirmed via DevTools: <span data-type="primary">Save changes</span>
    SAVE_BUTTON = (By.XPATH,
        "//span[@data-type='primary' and normalize-space()='Save changes'] | "
        "//span[@data-type='primary' and contains(normalize-space(),'Save')] | "
        "//*[@data-type='primary' and contains(normalize-space(),'Save')] | "
        "//button[contains(normalize-space(),'Save')]")

    # Confirmed via DevTools: <span>Cancel</span> (no data-type attribute)
    CANCEL_BUTTON = (By.XPATH,
        "//span[normalize-space()='Cancel'] | "
        "//button[normalize-space()='Cancel'] | "
        "//*[@data-type and normalize-space()='Cancel']")

    # ── Tunnel settings section internals ─────────────────────────────────────

    TUNNEL_OPERATIONAL_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Tunnel operational') or "
        "contains(normalize-space(),'Tunnel Operational')]"
        "/following::button[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Tunnel operational')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch']")

    CONTROLLER_ID_COMBOBOX = (By.XPATH,
        "//*[contains(normalize-space(),'Controller') and "
        "(contains(normalize-space(),'ID') or contains(normalize-space(),'Id') or "
        "contains(normalize-space(),'id'))]"
        "/following::div[contains(@class,'form-select__control')][1]")

    # ── Retract settings section internals ────────────────────────────────────

    # Confirmed via DevTools: <span data-type="primary">Add new</span>
    ADD_RETRACT_ROW_BUTTON = (By.XPATH,
        "//*[contains(normalize-space(),'Retract settings')]"
        "/following::span[@data-type='primary' and normalize-space()='Add new'][1] | "
        "//*[contains(normalize-space(),'Retract settings')]"
        "/following::*[@data-type='primary' and normalize-space()='Add new'][1]")

    RETRACT_SERVICE_DROPDOWNS = (By.XPATH,
        "//*[contains(normalize-space(),'Retract settings')]"
        "/following::div[contains(@class,'form-select__control')]")

    # Confirmed via DevTools: icon-only <button> containing SVG with data-name="Group 2405"
    RETRACT_REMOVE_BUTTONS = (By.XPATH,
        "//*[contains(normalize-space(),'Retract settings')]"
        "/following::button[.//*[@data-name='Group 2405']] | "
        "//*[contains(normalize-space(),'Retract settings')]"
        "/following::button[.//svg and not(normalize-space())]")

    # ── Frame switching ───────────────────────────────────────────────────────

    def _switch_to_form_frame(self, frame_locator):
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it(frame_locator)
            )
        except TimeoutException:
            pass

    def _switch_to_any_form_frame(self):
        """Try each known iframe pattern in order; stay on main page if none found."""
        self.driver.switch_to.default_content()
        for locator in (
            TunnelSettingsListPage.TUNNEL_CREATE_FRAME,
            TunnelSettingsListPage.TUNNEL_EDIT_FRAME,
            (By.XPATH, "//iframe[contains(@src,'tunnel')]"),
            (By.XPATH, "//iframe"),
        ):
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.frame_to_be_available_and_switch_to_it(locator)
                )
                return
            except TimeoutException:
                self.driver.switch_to.default_content()

    def wait_for_create_loaded(self):
        # click_add_tunnel() causes a full top-level navigation to /tunnels/new.
        # The form content is inside TUNNEL_CREATE_FRAME — must switch frames first.
        self._switch_to_form_frame(TunnelSettingsListPage.TUNNEL_CREATE_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))

    def wait_for_edit_loaded(self):
        # Same pattern: full navigation to /tunnels/{id}, form inside TUNNEL_EDIT_FRAME.
        self._switch_to_form_frame(TunnelSettingsListPage.TUNNEL_EDIT_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        # Confirm form data has loaded: at least one visible text input has a value.
        self.wait.until(
            lambda d: any(
                inp.get_attribute("value")
                for inp in d.find_elements(By.XPATH, "//input[@type='text']")
                if inp.is_displayed()
            )
        )

    def get_body_text(self):
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except Exception:
            self.driver.switch_to.default_content()
            return self.driver.find_element(By.TAG_NAME, "body").text

    # ── Core field actions ────────────────────────────────────────────────────

    def enter_tunnel_name(self, name):
        self.enter_text(self.TUNNEL_NAME_INPUT, name)

    def select_site(self, site):
        self.select_react_dropdown_option(self.SITE_COMBOBOX, site)
        time.sleep(1)

    def enter_controller_ip(self, ip):
        self.enter_text(self.CONTROLLER_IP_INPUT, ip)

    def enter_middleware_ip(self, ip):
        self.enter_text(self.MIDDLEWARE_IP_INPUT, ip)

    def get_controller_ip(self):
        el = self.wait.until(EC.presence_of_element_located(self.CONTROLLER_IP_INPUT))
        return el.get_attribute("value") or ""

    def get_middleware_ip(self):
        el = self.wait.until(EC.presence_of_element_located(self.MIDDLEWARE_IP_INPUT))
        return el.get_attribute("value") or ""

    def fill_required_fields(self, name, site, controller_ip):
        self.enter_tunnel_name(name)
        self.select_site(site)
        self.enter_controller_ip(controller_ip)

    def name_input_is_valid(self):
        el = self.wait.until(EC.presence_of_element_located(self.TUNNEL_NAME_INPUT))
        return el.get_attribute("aria-invalid") != "true"

    def controller_ip_is_valid(self):
        try:
            el = self.wait.until(EC.presence_of_element_located(self.CONTROLLER_IP_INPUT))
            return el.get_attribute("aria-invalid") != "true"
        except Exception:
            body = self.get_body_text().lower()
            return "required" not in body or "ip" not in body

    # ── Behavior radio helpers ────────────────────────────────────────────────

    def get_behavior_radio_elements(self):
        return [
            r for r in self.driver.find_elements(*self.ALL_BEHAVIOR_RADIOS)
            if r.is_displayed()
        ]

    def get_behavior_radio_state(self, label):
        locator = (By.XPATH,
            "//label[contains(normalize-space(),'%s')]//input[@type='radio'] | "
            "//*[normalize-space()='%s']/preceding-sibling::input[@type='radio'] | "
            "//*[normalize-space()='%s']/ancestor::label//input[@type='radio']"
            % (label, label, label))
        try:
            radio = self.wait.until(EC.presence_of_element_located(locator))
            return radio.is_selected()
        except Exception:
            return False

    def select_behavior(self, label):
        locator = (By.XPATH,
            "//label[contains(normalize-space(),'%s')]//input[@type='radio'] | "
            "//*[normalize-space()='%s']/preceding-sibling::input[@type='radio'] | "
            "//*[normalize-space()='%s']/ancestor::label//input[@type='radio']"
            % (label, label, label))
        try:
            radio = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].click();", radio)
        except Exception:
            pass

    # ── Generic toggle helpers (for the 8 main-form toggles) ─────────────────

    def _toggle_locator_by_label(self, label):
        return (By.XPATH,
            "//*[normalize-space()='%s']/following::button[@role='switch'][1]" % label)

    def get_toggle_state(self, label):
        locator = self._toggle_locator_by_label(label)
        toggle = self.wait.until(EC.presence_of_element_located(locator))
        return (
            toggle.get_attribute("aria-checked") == "true"
            or toggle.get_attribute("data-state") == "checked"
        )

    def set_toggle(self, label, on):
        locator = self._toggle_locator_by_label(label)
        toggle = self.wait.until(EC.element_to_be_clickable(locator))
        current = (
            toggle.get_attribute("aria-checked") == "true"
            or toggle.get_attribute("data-state") == "checked"
        )
        if current != on:
            self.driver.execute_script("arguments[0].click();", toggle)
            expected = "true" if on else "false"
            self.wait.until(
                lambda d: d.find_element(*locator).get_attribute("aria-checked") == expected
            )

    def toggle_is_present(self, label):
        els = self.driver.find_elements(*self._toggle_locator_by_label(label))
        return any(e.is_displayed() for e in els)

    # ── Tunnel operational toggle (inside Tunnel settings section) ────────────

    def get_tunnel_operational_state(self):
        toggle = self.wait.until(EC.presence_of_element_located(self.TUNNEL_OPERATIONAL_TOGGLE))
        return (
            toggle.get_attribute("aria-checked") == "true"
            or toggle.get_attribute("data-state") == "checked"
        )

    def set_tunnel_operational(self, on):
        toggle = self.wait.until(EC.element_to_be_clickable(self.TUNNEL_OPERATIONAL_TOGGLE))
        current = (
            toggle.get_attribute("aria-checked") == "true"
            or toggle.get_attribute("data-state") == "checked"
        )
        if current != on:
            self.driver.execute_script("arguments[0].click();", toggle)
            expected = "true" if on else "false"
            self.wait.until(
                lambda d: d.find_element(*self.TUNNEL_OPERATIONAL_TOGGLE)
                .get_attribute("aria-checked") == expected
            )

    # ── Controller ID (inside Tunnel settings section) ────────────────────────

    def select_controller_id(self, controller_id):
        self.select_react_dropdown_option(self.CONTROLLER_ID_COMBOBOX, controller_id)

    def get_controller_id_options(self):
        el = self.wait.until(EC.element_to_be_clickable(self.CONTROLLER_ID_COMBOBOX))
        self.driver.execute_script("arguments[0].click();", el)
        opts = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH,
             "//*[contains(@class,'form-select__option')] | //*[@role='option']")
        ))
        return [o.text.strip() for o in opts if o.text.strip()]

    # ── Retract settings ──────────────────────────────────────────────────────

    def click_add_retract_row(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.ADD_RETRACT_ROW_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)

    def get_retract_row_count(self):
        els = self.driver.find_elements(*self.RETRACT_SERVICE_DROPDOWNS)
        return len([e for e in els if e.is_displayed()])

    def select_retract_service(self, row_index, service):
        dropdowns = [
            e for e in self.driver.find_elements(*self.RETRACT_SERVICE_DROPDOWNS)
            if e.is_displayed()
        ]
        if row_index >= len(dropdowns):
            raise IndexError(
                "Retract row %d not found (%d visible)" % (row_index, len(dropdowns))
            )
        self.driver.execute_script("arguments[0].click();", dropdowns[row_index])
        opt = self.wait.until(lambda d: self._find_react_option(service))
        self.driver.execute_script("arguments[0].click();", opt)

    def get_retract_save_toggle_state(self, row_index):
        retract_toggles = [
            t for t in self.driver.find_elements(By.XPATH,
                "//*[contains(normalize-space(),'Retract settings')]"
                "/following::button[@role='switch']")
            if t.is_displayed()
        ]
        if row_index >= len(retract_toggles):
            return False
        toggle = retract_toggles[row_index]
        return (
            toggle.get_attribute("aria-checked") == "true"
            or toggle.get_attribute("data-state") == "checked"
        )

    def toggle_retract_save_for_car(self, row_index, on):
        retract_toggles = [
            t for t in self.driver.find_elements(By.XPATH,
                "//*[contains(normalize-space(),'Retract settings')]"
                "/following::button[@role='switch']")
            if t.is_displayed()
        ]
        if row_index >= len(retract_toggles):
            raise IndexError("Retract toggle %d not found" % row_index)
        toggle = retract_toggles[row_index]
        current = (
            toggle.get_attribute("aria-checked") == "true"
            or toggle.get_attribute("data-state") == "checked"
        )
        if current != on:
            self.driver.execute_script("arguments[0].click();", toggle)

    def remove_retract_row(self, row_index):
        remove_btns = [
            e for e in self.driver.find_elements(*self.RETRACT_REMOVE_BUTTONS)
            if e.is_displayed()
        ]
        if row_index >= len(remove_btns):
            raise IndexError("Remove button %d not found" % row_index)
        self.driver.execute_script("arguments[0].click();", remove_btns[row_index])

    # ── Section accordion helpers ─────────────────────────────────────────────

    # ── Section accordion helpers ─────────────────────────────────────────────
    # DevTools confirmed: heading text lives in *-heading__header-title div.
    # The parent div is the clickable toggle; no aria-expanded is set.

    _SECTION_XPATHS = [
        "//button[contains(normalize-space(),'%s')]",
        "//*[@role='button' and contains(normalize-space(),'%s')]",
        "//*[contains(@class,'accordion') and contains(normalize-space(),'%s')]",
        # confirmed pattern: e.g. <div class="retract-settings-heading__header-title">
        "//*[contains(@class,'heading__header-title') and normalize-space()='%s']/..",
        "//*[contains(@class,'heading__header-title') and normalize-space()='%s']",
    ]

    def _section_header(self, section_name):
        for xpath in self._SECTION_XPATHS:
            els = [e for e in self.driver.find_elements(By.XPATH, xpath % section_name)
                   if e.is_displayed()]
            if els:
                return els[0]
        raise TimeoutException("Section header not found: %s" % section_name)

    def section_is_expanded(self, section_name):
        for xpath in self._SECTION_XPATHS:
            els = [e for e in self.driver.find_elements(By.XPATH, xpath % section_name)
                   if e.is_displayed()]
            if not els:
                continue
            el = els[0]
            expanded = el.get_attribute("aria-expanded")
            if expanded is not None:
                return expanded == "true"
            # Class-based fallback (some frameworks toggle open/expanded/active)
            cls = (el.get_attribute("class") or "").lower()
            if any(k in cls for k in ("open", "expanded", "active")):
                return True
            if any(k in cls for k in ("collapsed", "closed")):
                return False
        return False

    def expand_section(self, section_name):
        if not self.section_is_expanded(section_name):
            header = self._section_header(section_name)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", header)
            self.driver.execute_script("arguments[0].click();", header)
            try:
                self.wait.until(lambda d: self.section_is_expanded(section_name))
            except TimeoutException:
                # No aria-expanded or class indicator — give the animation time to settle
                time.sleep(0.5)

    def collapse_section(self, section_name):
        if self.section_is_expanded(section_name):
            header = self._section_header(section_name)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", header)
            self.driver.execute_script("arguments[0].click();", header)
            try:
                self.wait.until(lambda d: not self.section_is_expanded(section_name))
            except TimeoutException:
                time.sleep(0.5)

    # ── Form save / cancel ────────────────────────────────────────────────────

    def click_save(self):
        url_before = self.driver.current_url
        el = self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)
        try:
            WebDriverWait(self.driver, 5).until(lambda d: d.current_url != url_before)
            self.driver.switch_to.default_content()
        except Exception:
            pass

    def click_cancel(self):
        el = self.wait.until(EC.visibility_of_element_located(self.CANCEL_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)
