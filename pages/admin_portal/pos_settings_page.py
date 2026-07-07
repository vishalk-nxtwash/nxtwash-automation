import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class AdminPOSSettingsPage(BasePage):
    """POS Settings list page — /pos_settings/pos"""

    POS_LIST_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/pos_settings/pos') "
        "and not(contains(@src,'/pos_settings/pos/'))]")
    POS_CREATE_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/pos_settings/pos/new')]")
    POS_EDIT_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/pos_settings/pos/') "
        "and not(contains(@src,'/pos_settings/pos/new'))]")

    ADD_POS_BUTTON = (By.XPATH,
        "//span[@data-type='primary' and contains(normalize-space(),'Add new POS')] | "
        "//button[contains(normalize-space(),'Add new POS')] | "
        "//span[@data-type='primary' and contains(normalize-space(),'POS')]")

    SEARCH_INPUT = (By.XPATH,
        "//input[@name='posName' or @name='pos_name' or "
        "@placeholder='Search' or @placeholder='Search POS' or "
        "@placeholder='POS name' or @placeholder='Search by POS name']")

    FILTER_BUTTON = (By.XPATH,
        "//button[normalize-space()='Filter by'] | "
        "//button[contains(normalize-space(),'Filter')]")

    FILTER_SITE_COMBOBOX = (By.XPATH,
        "//div[contains(@class,'form-select__control') and "
        ".//div[contains(@class,'form-select__placeholder') and "
        "contains(normalize-space(),'site')]] | "
        "//div[contains(@class,'form-select__control')][1]")

    FILTER_ACTIVE_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Active POS') or "
        "contains(normalize-space(),'Active pos')]"
        "/following::button[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Active POS')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch']")

    APPLY_FILTERS_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters'] | "
        "//button[normalize-space()='Apply']")

    RESET_ALL_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Reset all')] | "
        "//button[contains(normalize-space(),'Reset All')]")

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
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.POS_LIST_FRAME))
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        self.wait.until(EC.element_to_be_clickable(self.ADD_POS_BUTTON))

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def search_pos(self, name):
        el = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        el.click()
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(name)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value") == name
        )
        time.sleep(1)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def clear_search(self):
        el = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        el.click()
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value") == ""
        )
        time.sleep(1)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def _row_locator(self, name):
        return (By.XPATH,
            "//span[contains(@class,'table-cell-ellipsis') and @title='%s'] | "
            "//span[contains(@class,'table-cell-ellipsis') and normalize-space()='%s']"
            % (name, name))

    def wait_for_pos_row(self, name, timeout=None):
        locator = self._row_locator(name)
        if timeout:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        return self.wait.until(EC.presence_of_element_located(locator))

    def pos_exists(self, name):
        self.search_pos(name)
        try:
            self.wait_for_pos_row(name, timeout=15)
            return True
        except TimeoutException:
            return False

    def get_pos_status(self, name):
        self.search_pos(name)
        row = self.wait_for_pos_row(name)
        try:
            badge = row.find_element(By.XPATH,
                ".//*[normalize-space()='Active' or normalize-space()='Inactive']")
            return badge.text.strip()
        except Exception:
            return ""

    def get_visible_row_count(self):
        rows = self.driver.find_elements(*self.GRID_ROWS)
        return len([r for r in rows if r.is_displayed()])

    def click_add_pos(self):
        el = self.wait.until(EC.element_to_be_clickable(self.ADD_POS_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def open_edit_pos(self, name):
        self.search_pos(name)
        self.wait_for_pos_row(name)
        edit_link = self.wait.until(EC.element_to_be_clickable(self.EDIT_LINK))
        self.driver.execute_script("arguments[0].click();", edit_link)

    def filter_panel_is_open(self):
        els = self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)
        return any(e.is_displayed() for e in els)

    def open_filter_panel(self):
        if self.filter_panel_is_open():
            return
        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.APPLY_FILTERS_BUTTON))

    def close_filter_panel(self):
        if not self.filter_panel_is_open():
            return
        btn = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)

    def filter_by_site(self, site):
        self.open_filter_panel()
        self.select_react_dropdown_option(self.FILTER_SITE_COMBOBOX, site)

    def filter_active_pos_on(self):
        self.open_filter_panel()
        toggle = self.wait.until(EC.element_to_be_clickable(self.FILTER_ACTIVE_TOGGLE))
        if toggle.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", toggle)

    def filter_active_pos_off(self):
        self.open_filter_panel()
        toggle = self.wait.until(EC.element_to_be_clickable(self.FILTER_ACTIVE_TOGGLE))
        if toggle.get_attribute("aria-checked") != "false":
            self.driver.execute_script("arguments[0].click();", toggle)

    def apply_filters(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def reset_filters(self):
        self.open_filter_panel()
        btn = self.wait.until(EC.element_to_be_clickable(self.RESET_ALL_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def filter_panel_has_expected_controls(self):
        self.open_filter_panel()
        body = self.get_body_text().lower()
        return "filter" in body or "site" in body or "active" in body

    def get_site_filter_options(self):
        self.open_filter_panel()
        self.driver.execute_script(
            "arguments[0].click();",
            self.wait.until(EC.element_to_be_clickable(self.FILTER_SITE_COMBOBOX))
        )
        options = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//*[@role='option']")
        ))
        return [o.text.strip() for o in options if o.text.strip()]


class AdminPOSFormPage(BasePage):
    """POS Settings create/edit form."""

    # ── Core form fields (Main Settings tab) ─────────────────────────────────

    POS_NAME_INPUT = (By.XPATH,
        "//input[@name='posName' or @name='name' or @name='pos_name' or "
        "@placeholder='POS name' or @placeholder='Name']")

    SITE_COMBOBOX = (By.XPATH,
        "//input[@name='posName' or @placeholder='POS name']"
        "/following::div[contains(@class,'form-select__control')][1]")

    LANE_COMBOBOX = (By.XPATH,
        "//input[@name='posName' or @placeholder='POS name']"
        "/following::div[contains(@class,'form-select__control')][2]")

    ALLOW_CHECKOUT_COMBOBOX = (By.XPATH,
        "//*[contains(normalize-space(),'Allow checkout') or "
        "contains(normalize-space(),'allow checkout')]"
        "/following::div[contains(@class,'form-select__control')][1]")

    CASH_CHECKBOX = (By.XPATH,
        "//*[contains(normalize-space(),'Cash')]"
        "/ancestor::*[.//input[@type='checkbox']][1]//input[@type='checkbox'] | "
        "//input[@name='cash' or @value='cash']")

    CARD_CHECKBOX = (By.XPATH,
        "//*[contains(normalize-space(),'Card') and "
        "not(contains(normalize-space(),'Cash'))]"
        "/ancestor::*[.//input[@type='checkbox']][1]//input[@type='checkbox'] | "
        "//input[@name='card' or @value='card']")

    ACTIVE_POS_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Active POS') or "
        "contains(normalize-space(),'Active pos')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch'] | "
        "//form//button[@role='switch'][1]")

    SAVE_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Save POS')] | "
        "//button[normalize-space()='Save'] | "
        "//*[@data-type='primary' and contains(normalize-space(),'Save')] | "
        "//span[@data-type='primary' and contains(normalize-space(),'Save')]")

    CANCEL_BUTTON = (By.XPATH,
        "//button[normalize-space()='Cancel'] | "
        "//*[@data-type and normalize-space()='Cancel']")

    # ── Tabs ─────────────────────────────────────────────────────────────────

    MAIN_SETTINGS_TAB = (By.XPATH,
        "//*[@role='tab' and contains(normalize-space(),'Main')] | "
        "//*[@role='tab' and contains(normalize-space(),'main settings')]")

    SERVICE_SETTINGS_TAB = (By.XPATH,
        "//*[@role='tab' and contains(normalize-space(),'Service')] | "
        "//*[@role='tab' and contains(normalize-space(),'service settings')]")

    # ── Tunnel Settings section ───────────────────────────────────────────────

    SEND_INVOICE_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Send invoice') or "
        "contains(normalize-space(),'send invoice')]"
        "/following::button[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Send invoice')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch']")

    TUNNEL_OPERATIONAL_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Tunnel operational') or "
        "contains(normalize-space(),'Tunnel Operational')]"
        "/following::button[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Tunnel operational')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch']")

    CONTROLLER_ID_COMBOBOX = (By.XPATH,
        "//*[contains(normalize-space(),'Controller') and "
        "(contains(normalize-space(),'ID') or contains(normalize-space(),'Id'))]"
        "/following::div[contains(@class,'form-select__control')][1]")

    TUNNEL_CONTROLLER_IP_INPUT = (By.XPATH,
        "//input[@name='tunnelControllerIp' or @name='tunnel_controller_ip' or "
        "@name='controllerIp' or @name='controller_ip' or "
        "contains(@placeholder,'192') or contains(@placeholder,'IP:port') or "
        "contains(@placeholder,'controller ip') or contains(@placeholder,'Controller')]")

    CAR_ROLLER_OUTPUT_COMBOBOX = (By.XPATH,
        "//*[contains(normalize-space(),'roller output') or "
        "contains(normalize-space(),'Roller output') or "
        "contains(normalize-space(),'Car/roller')]"
        "/following::div[contains(@class,'form-select__control')][1]")

    # ── Middleware Settings section ───────────────────────────────────────────

    MIDDLEWARE_IP_INPUT = (By.XPATH,
        "//input[@name='middlewareIp' or @name='middleware_ip' or "
        "@name='middlewareUrl' or @name='middleware_url' or "
        "contains(@placeholder,'middleware') or contains(@placeholder,'Middleware')]")

    # ── Device Settings section ───────────────────────────────────────────────

    PAYMENT_SERIAL_INPUT = (By.XPATH,
        "//input[@name='paymentSerial' or @name='payment_serial' or "
        "@name='serialNumber' or @name='serial_number' or "
        "@placeholder='Payment serial' or @placeholder='Serial number' or "
        "contains(@placeholder,'serial')]")

    # ── Sidebar navigation ────────────────────────────────────────────────────

    MAIN_SETTINGS_NAV = (By.XPATH,
        "//button[@aria-controls='mainPosSettings-tab-pane'] | "
        "//button[@role='tab' and normalize-space()='Main settings']")

    # ── Service Settings tab ──────────────────────────────────────────────────

    RESTORE_DEFAULT_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Restore default')] | "
        "//button[contains(normalize-space(),'Restore Default')]")

    HOT_SALE_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Hot Sale') or "
        "contains(normalize-space(),'Hot sale')]"
        "/following::button[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Hot Sale')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch']")

    HOME_CATEGORY_COMBOBOX = (By.XPATH,
        "//*[contains(normalize-space(),'POS home page') or "
        "contains(normalize-space(),'home page category') or "
        "contains(normalize-space(),'Home page')]"
        "/following::div[contains(@class,'form-select__control')][1]")

    # ── Load / frame ─────────────────────────────────────────────────────────

    def _click_main_settings_nav(self):
        """Click the 'Main settings' sidebar nav item to reveal the form fields."""
        nav = self.wait.until(EC.element_to_be_clickable(self.MAIN_SETTINGS_NAV))
        self.driver.execute_script("arguments[0].click();", nav)

    def _switch_to_form_frame(self, frame_locator):
        """Switch into the form iframe if one exists; stay on the main page if not."""
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it(frame_locator)
            )
        except TimeoutException:
            pass

    def wait_for_create_loaded(self):
        self._switch_to_form_frame(AdminPOSSettingsPage.POS_CREATE_FRAME)
        self._click_main_settings_nav()
        self.wait.until(EC.visibility_of_element_located(self.POS_NAME_INPUT))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))

    def wait_for_edit_loaded(self):
        self._switch_to_form_frame(AdminPOSSettingsPage.POS_EDIT_FRAME)
        self._click_main_settings_nav()
        self.wait.until(EC.visibility_of_element_located(self.POS_NAME_INPUT))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        self.wait.until(
            lambda d: d.find_element(*self.POS_NAME_INPUT).get_attribute("value") != ""
        )

    def get_body_text(self):
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except Exception:
            self.driver.switch_to.default_content()
            return self.driver.find_element(By.TAG_NAME, "body").text

    # ── Core form actions ─────────────────────────────────────────────────────

    def enter_pos_name(self, name):
        self.enter_text(self.POS_NAME_INPUT, name)

    def select_site(self, site):
        self.select_react_dropdown_option(self.SITE_COMBOBOX, site)
        # Lane dropdown is dynamically populated after site selection.
        time.sleep(1.5)

    def select_lane(self, lane):
        self.select_react_dropdown_option(self.LANE_COMBOBOX, lane)

    def select_allow_checkout(self, option):
        self.select_react_dropdown_option(self.ALLOW_CHECKOUT_COMBOBOX, option)

    def _get_dropdown_options(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", el)
        opts = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH,
             "//*[contains(@class,'form-select__option')] | //*[@role='option']")
        ))
        return [o.text.strip() for o in opts if o.text.strip()]

    def get_site_options(self):
        return self._get_dropdown_options(self.SITE_COMBOBOX)

    def get_lane_options(self):
        return self._get_dropdown_options(self.LANE_COMBOBOX)

    def ensure_cash_checked(self):
        el = self.wait.until(EC.presence_of_element_located(self.CASH_CHECKBOX))
        if not el.is_selected():
            self.driver.execute_script("arguments[0].click();", el)

    def ensure_cash_unchecked(self):
        el = self.wait.until(EC.presence_of_element_located(self.CASH_CHECKBOX))
        if el.is_selected():
            self.driver.execute_script("arguments[0].click();", el)

    def ensure_card_checked(self):
        el = self.wait.until(EC.presence_of_element_located(self.CARD_CHECKBOX))
        if not el.is_selected():
            self.driver.execute_script("arguments[0].click();", el)

    def ensure_card_unchecked(self):
        el = self.wait.until(EC.presence_of_element_located(self.CARD_CHECKBOX))
        if el.is_selected():
            self.driver.execute_script("arguments[0].click();", el)

    def cash_is_checked(self):
        el = self.wait.until(EC.presence_of_element_located(self.CASH_CHECKBOX))
        return el.is_selected()

    def card_is_checked(self):
        el = self.wait.until(EC.presence_of_element_located(self.CARD_CHECKBOX))
        return el.is_selected()

    def ensure_active_pos_on(self):
        try:
            toggle = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_POS_TOGGLE))
            checked = (
                toggle.get_attribute("aria-checked") == "true"
                or toggle.get_attribute("data-state") == "checked"
            )
            if not checked:
                self.driver.execute_script("arguments[0].click();", toggle)
        except Exception:
            pass

    def ensure_active_pos_off(self):
        try:
            toggle = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_POS_TOGGLE))
            checked = (
                toggle.get_attribute("aria-checked") == "true"
                or toggle.get_attribute("data-state") == "checked"
            )
            if checked:
                self.driver.execute_script("arguments[0].click();", toggle)
        except Exception:
            pass

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

    def pos_name_input_is_valid(self):
        el = self.wait.until(EC.presence_of_element_located(self.POS_NAME_INPUT))
        return el.get_attribute("aria-invalid") != "true"

    def click_main_settings_tab(self):
        self._click_main_settings_nav()

    def click_service_settings_tab(self):
        el = self.wait.until(EC.element_to_be_clickable(self.SERVICE_SETTINGS_TAB))
        self.driver.execute_script("arguments[0].click();", el)

    def get_visible_tabs(self):
        tabs = self.driver.find_elements(By.XPATH, "//*[@role='tab']")
        return [t.text.strip() for t in tabs if t.text.strip() and t.is_displayed()]

    # ── Section accordion helpers ─────────────────────────────────────────────

    def _section_header(self, section_name):
        els = self.driver.find_elements(By.XPATH,
            "//button[contains(normalize-space(),'%s')] | "
            "//*[@role='button' and contains(normalize-space(),'%s')] | "
            "//*[contains(@class,'accordion') and contains(normalize-space(),'%s')]"
            % (section_name, section_name, section_name))
        if not els:
            raise TimeoutException("Section header not found: %s" % section_name)
        return els[0]

    def section_is_expanded(self, section_name):
        els = self.driver.find_elements(By.XPATH,
            "//button[contains(normalize-space(),'%s')] | "
            "//*[@role='button' and contains(normalize-space(),'%s')] | "
            "//*[contains(@class,'accordion') and contains(normalize-space(),'%s')]"
            % (section_name, section_name, section_name))
        if not els:
            return False
        expanded = els[0].get_attribute("aria-expanded")
        return expanded == "true" if expanded is not None else False

    def expand_section(self, section_name):
        if not self.section_is_expanded(section_name):
            header = self._section_header(section_name)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", header
            )
            self.driver.execute_script("arguments[0].click();", header)
            self.wait.until(lambda d: self.section_is_expanded(section_name))

    def collapse_section(self, section_name):
        if self.section_is_expanded(section_name):
            header = self._section_header(section_name)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", header
            )
            self.driver.execute_script("arguments[0].click();", header)
            self.wait.until(lambda d: not self.section_is_expanded(section_name))

    # ── Tunnel Settings ───────────────────────────────────────────────────────

    def ensure_send_invoice_on(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.SEND_INVOICE_TOGGLE))
        if toggle.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.SEND_INVOICE_TOGGLE)
                .get_attribute("aria-checked") == "true"
            )

    def ensure_tunnel_operational_on(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.TUNNEL_OPERATIONAL_TOGGLE))
        if toggle.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.TUNNEL_OPERATIONAL_TOGGLE)
                .get_attribute("aria-checked") == "true"
            )

    def ensure_tunnel_operational_off(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.TUNNEL_OPERATIONAL_TOGGLE))
        if toggle.get_attribute("aria-checked") != "false":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.TUNNEL_OPERATIONAL_TOGGLE)
                .get_attribute("aria-checked") == "false"
            )

    def select_controller_id(self, controller):
        self.select_react_dropdown_option(self.CONTROLLER_ID_COMBOBOX, controller)

    def controller_id_is_valid(self):
        try:
            el = self.wait.until(EC.presence_of_element_located(self.CONTROLLER_ID_COMBOBOX))
            return el.get_attribute("aria-invalid") != "true"
        except Exception:
            body = self.get_body_text().lower()
            return "required" not in body and "controller" not in body

    def enter_tunnel_controller_ip(self, ip):
        self.enter_text(self.TUNNEL_CONTROLLER_IP_INPUT, ip)

    def get_tunnel_controller_ip(self):
        el = self.wait.until(EC.presence_of_element_located(self.TUNNEL_CONTROLLER_IP_INPUT))
        return el.get_attribute("value") or ""

    def tunnel_controller_ip_is_valid(self):
        el = self.wait.until(EC.presence_of_element_located(self.TUNNEL_CONTROLLER_IP_INPUT))
        return el.get_attribute("aria-invalid") != "true"

    def select_car_roller_output(self, option):
        self.select_react_dropdown_option(self.CAR_ROLLER_OUTPUT_COMBOBOX, option)

    def car_roller_output_is_valid(self):
        try:
            el = self.wait.until(EC.presence_of_element_located(self.CAR_ROLLER_OUTPUT_COMBOBOX))
            return el.get_attribute("aria-invalid") != "true"
        except Exception:
            body = self.get_body_text().lower()
            return "required" not in body

    # ── Middleware Settings ───────────────────────────────────────────────────

    def enter_middleware_ip(self, ip):
        self.enter_text(self.MIDDLEWARE_IP_INPUT, ip)

    def get_middleware_ip(self):
        el = self.wait.until(EC.presence_of_element_located(self.MIDDLEWARE_IP_INPUT))
        return el.get_attribute("value") or ""

    def middleware_ip_is_valid(self):
        el = self.wait.until(EC.presence_of_element_located(self.MIDDLEWARE_IP_INPUT))
        return el.get_attribute("aria-invalid") != "true"

    # ── Device Settings ───────────────────────────────────────────────────────

    def enter_payment_serial(self, serial):
        self.enter_text(self.PAYMENT_SERIAL_INPUT, serial)

    def get_payment_serial(self):
        el = self.wait.until(EC.presence_of_element_located(self.PAYMENT_SERIAL_INPUT))
        return el.get_attribute("value") or ""

    def payment_serial_is_valid(self):
        el = self.wait.until(EC.presence_of_element_located(self.PAYMENT_SERIAL_INPUT))
        return el.get_attribute("aria-invalid") != "true"

    # ── Service Settings tab ──────────────────────────────────────────────────

    def click_restore_default(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.RESTORE_DEFAULT_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)

    def ensure_hot_sale_on(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.HOT_SALE_TOGGLE))
        if toggle.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", toggle)

    def ensure_hot_sale_off(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.HOT_SALE_TOGGLE))
        if toggle.get_attribute("aria-checked") != "false":
            self.driver.execute_script("arguments[0].click();", toggle)

    def fill_create_form(self, pos_name, site, lane):
        self.enter_pos_name(pos_name)
        self.select_site(site)
        self.select_lane(lane)
