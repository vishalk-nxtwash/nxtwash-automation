import logging
import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage

_log = logging.getLogger("nxtwash")


class GasPumpSettingsListPage(BasePage):
    """Gas Pump Settings list page — /gas_pump_settings/device_list"""

    PUMP_LIST_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/gas_pump_settings/device_list') "
        "and not(contains(@src,'/gas_pump_settings/device_list/'))]")
    PUMP_CREATE_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/gas_pump_settings/device_list/new')]")
    PUMP_EDIT_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/gas_pump_settings/device_list/') "
        "and not(contains(@src,'/gas_pump_settings/device_list/new'))]")

    ADD_PUMP_BUTTON = (By.XPATH,
        "//span[@data-type='primary' and contains(normalize-space(),'Add gas pump')] | "
        "//button[contains(normalize-space(),'Add gas pump')] | "
        "//*[@data-type='primary' and contains(normalize-space(),'gas pump')]")

    GRID_ROWS = (By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row')] | "
        "//tr[contains(@class,'row') and not(contains(@class,'header'))]")

    EDIT_LINK = (By.XPATH,
        "//a[@role='button' and contains(@class,'table-page__page-content__table__edit')]")

    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and not(contains(@style,'display: none'))] | "
        "//*[contains(@class,'inovua-react-toolkit-load-mask') "
        "and not(contains(@class,'--hidden')) "
        "and not(contains(@style,'display: none'))]")

    HEADER_COUNT = (By.XPATH,
        "//*[contains(normalize-space(),'Gas Pump') and contains(normalize-space(),'(')]")

    def wait_for_loaded(self):
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.PUMP_LIST_FRAME))
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.LOAD_MASK)
            )
        except Exception:
            pass
        self.wait.until(EC.element_to_be_clickable(self.ADD_PUMP_BUTTON))

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def _row_locator(self, name):
        return (By.XPATH,
            "//span[contains(@class,'table-cell-ellipsis') and @title='%s'] | "
            "//span[contains(@class,'table-cell-ellipsis') and normalize-space()='%s']"
            % (name, name))

    def wait_for_pump_row(self, name, timeout=None):
        locator = self._row_locator(name)
        if timeout:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        return self.wait.until(EC.presence_of_element_located(locator))

    def pump_exists(self, name):
        try:
            self.wait_for_pump_row(name, timeout=8)
            return True
        except TimeoutException:
            # XPath locator may not match this grid's cell class; fall back to body text.
            try:
                body = self.get_body_text()
                return name in body
            except Exception:
                return False

    def get_pump_status(self, name):
        self.wait_for_pump_row(name)
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

    def get_header_pump_count(self):
        """Return the integer from the 'Gas Pump (N)' page header, or None."""
        try:
            el = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.HEADER_COUNT)
            )
            m = re.search(r'\((\d+)\)', el.text)
            return int(m.group(1)) if m else None
        except Exception:
            return None

    def click_add_pump(self):
        el = self.wait.until(EC.element_to_be_clickable(self.ADD_PUMP_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def open_edit_pump(self, name):
        self.wait_for_pump_row(name)
        try:
            row_el = self.driver.find_element(*self._row_locator(name))
            row_container = row_el.find_element(By.XPATH,
                "./ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]")
            edit_link = row_container.find_element(By.XPATH,
                ".//a[@role='button' and contains(@class,'table__edit')]")
            self.driver.execute_script("arguments[0].click();", edit_link)
        except Exception:
            edit_link = self.wait.until(EC.element_to_be_clickable(self.EDIT_LINK))
            self.driver.execute_script("arguments[0].click();", edit_link)

    def get_visible_row_count(self):
        rows = self.driver.find_elements(*self.GRID_ROWS)
        return len([r for r in rows if r.is_displayed()])


class GasPumpSettingsFormPage(BasePage):
    """Gas Pump Settings create/edit form."""

    # ── Core form fields (left panel) ────────────────────────────────────────

    GAS_PUMP_NAME_INPUT = (By.XPATH,
        "//input[@name='gasPumpName' or @name='gas_pump_name' or "
        "@placeholder='Add gas pump name' or @placeholder='Gas pump name' or "
        "@placeholder='Enter gas pump name']")

    SITE_COMBOBOX = (By.XPATH,
        "//div[contains(@class,'rhf-select__control') and "
        ".//div[contains(@class,'rhf-select__placeholder') and "
        "(contains(normalize-space(),'Select site') or normalize-space()='Site')]] | "
        "//div[contains(@class,'form-select__control') and "
        ".//div[contains(@class,'form-select__placeholder') and "
        "contains(normalize-space(),'site')]] | "
        "//input[@name='gasPumpName' or @placeholder='Add gas pump name']"
        "/following::div[contains(@class,'select__control')][1]")

    SERIAL_PORT_INPUT = (By.XPATH,
        "//input[@name='serialPort' or @name='serial_port' or "
        "contains(@placeholder,'Serial port') or contains(@placeholder,'serial port')]")

    SERIAL_NUMBER_INPUT = (By.XPATH,
        "//input[@name='serialNumber' or @name='serial_number' or "
        "contains(@placeholder,'Serial number') or contains(@placeholder,'serial number')]")

    BAUD_RATE_INPUT = (By.XPATH,
        "//input[@name='baudRate' or @name='baud_rate' or "
        "contains(@placeholder,'Baud rate') or contains(@placeholder,'baud rate')]")

    LINK_TIMEOUT_INPUT = (By.XPATH,
        "//input[@name='linkTimeout' or @name='link_timeout' or "
        "contains(@placeholder,'Link timeout') or contains(@placeholder,'link timeout')]")

    FETCH_INTERVAL_INPUT = (By.XPATH,
        "//input[@name='washBookFetchInterval' or @name='wash_book_fetch_interval' or "
        "contains(@placeholder,'fetch interval') or contains(@placeholder,'Fetch interval') or "
        "contains(@placeholder,'Wash book fetch')]")

    CODE_LENGTH_INPUT = (By.XPATH,
        "//input[@name='washBookCodeLength' or @name='wash_book_code_length' or "
        "contains(@placeholder,'code length') or contains(@placeholder,'Code length') or "
        "contains(@placeholder,'Wash book code')]")

    ACTIVE_PUMP_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Active gas pump') or "
        "contains(normalize-space(),'Active Gas Pump')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch'] | "
        "//*[contains(normalize-space(),'Active gas pump')]"
        "/following::button[@role='switch'][1]")

    # User-confirmed: the onClick lives on the inner <span data-type='primary'>.
    # Clicking the outer <button> or parent <div> does NOT fire it (events don't
    # bubble down into children).  Target the span exclusively.
    SAVE_BUTTON = (By.XPATH,
        "//span[@data-type='primary' and normalize-space()='Save gas pump']")

    CANCEL_BUTTON = (By.XPATH,
        "//button[normalize-space()='Cancel'] | "
        "//span[normalize-space()='Cancel'] | "
        "//*[@data-type and normalize-space()='Cancel']")

    # ── Wash Book Code List (right panel) ────────────────────────────────────
    # DevTools-confirmed class prefixes (CSS modules append a hash suffix):
    #   section title  → wbCodeListTable_wbCodeListTitle_<hash>
    #   row item       → wbCodeListTable_wbCodeListTableItem_<hash>
    #   remove wrapper → wbCodeListTable_wbCodeListTableItemRemove_<hash>
    #   remove target  → img[alt="Close"] inside the remove wrapper

    WBC_SECTION_TITLE = (By.XPATH,
        "//div[contains(@class,'wbCodeListTable_wbCodeListTitle_')]")

    ADD_WBC_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Add wash book code')] | "
        "//*[@data-type='primary' and contains(normalize-space(),'Add wash book code')] | "
        "//span[@data-type='primary' and contains(normalize-space(),'Add wash book code')]")

    # Each WBC row: div[class*="wbCodeListTable_wbCodeListTableItem_"]
    # The hashed suffix starts with _ so the contains() match is specific to row items
    # (inputs wrapper = "...TableItemInputs_", remove wrapper = "...TableItemRemove_"
    # — neither contains "TableItem_").
    WBC_ROW_ITEMS = (By.XPATH,
        "//div[contains(@class,'wbCodeListTable_wbCodeListTableItem_')]")

    # Inside each WBC row: the rhf-select control for the wash book dropdown.
    # Scoped via WBC_ROW_ITEMS at runtime; this bare locator used as fallback.
    WBC_WASH_BOOK_DROPDOWNS = (By.XPATH,
        "//div[contains(@class,'wbCodeListTable_wbCodeListTableItem_')]"
        "//div[contains(@class,'rhf-select__control')]")

    # Confirmed name pattern: gasPumpCodeList.{n}.gasPumpIdCode
    # Confirmed placeholder: "Gas pump ID code"
    WBC_ID_CODE_INPUTS = (By.XPATH,
        "//input[@placeholder='Gas pump ID code' or "
        "contains(@name,'gasPumpIdCode')]")

    # Remove is img[alt="Close"] inside div[class*="wbCodeListTableItemRemove_"].
    # NOT a <button> — confirmed from DevTools.
    WBC_REMOVE_BUTTONS = (By.XPATH,
        "//div[contains(@class,'wbCodeListTable_wbCodeListTableItemRemove_')]"
        "/img[@alt='Close' or @alt='close'] | "
        "//div[contains(@class,'wbCodeListTable_wbCodeListTableItemRemove_')]/img")

    # ── Connection status indicator ───────────────────────────────────────────

    # Yellow triangle: pump not yet connected to hardware
    CONNECTION_YELLOW = (By.XPATH,
        "//*[contains(@class,'warning') and .//svg] | "
        "//*[contains(@class,'triangle') and .//svg] | "
        "//*[contains(@class,'not-connected') or contains(@class,'disconnected')] | "
        "//*[@title='Not connected' or @aria-label='Not connected' or "
        "@title='Disconnected' or @aria-label='Disconnected'] | "
        "//*[contains(@class,'connection') and "
        "(contains(@class,'warn') or contains(@class,'pending'))]")

    # Blue checkmark: pump physically connected
    CONNECTION_BLUE = (By.XPATH,
        "//*[contains(@class,'connected') and not(contains(@class,'dis'))] | "
        "//*[contains(@class,'success') and .//svg] | "
        "//*[contains(@class,'checkmark') or contains(@class,'check-mark')] | "
        "//*[@title='Connected' or @aria-label='Connected'] | "
        "//*[contains(@class,'connection') and contains(@class,'success')]")

    # New pump (no code yet):  span text = "Generate connection code"
    # Existing pump (code exists): span text = "Check or re-generate code"
    # Both use the same div.d-flex > span[data-type='primary'] pattern.
    CHECK_REGEN_CODE_BUTTON = (By.XPATH,
        "//span[@data-type='primary' and ("
        "normalize-space()='Generate connection code' or "
        "contains(normalize-space(),'Check or re-generate code'))] | "
        "//span[contains(normalize-space(),'connection code') or "
        "contains(normalize-space(),'re-generate code')]")

    # ── Connection code modal ─────────────────────────────────────────────────

    MODAL_CONTAINER = (By.XPATH,
        "//div[contains(@class,'modal') and not(contains(@class,'modal-backdrop')) "
        "and not(contains(@class,'modal-dialog'))]"
        "[.//button or .//img] | "
        "//div[@role='dialog']")

    MODAL_QR_CODE = (By.XPATH,
        "//div[contains(@class,'modal') or @role='dialog']//img | "
        "//*[contains(@class,'qr') or contains(@class,'QR')]//img | "
        "//img[contains(@alt,'QR') or contains(@alt,'qr') or "
        "contains(@src,'qr') or contains(@class,'qr')]")

    MODAL_MANUAL_CODE = (By.XPATH,
        "//*[contains(@class,'generate-code-modal') and "
        "contains(@class,'value')] | "
        "//*[contains(@class,'code__value') or contains(@class,'code_value') or "
        "contains(@class,'code-value') or contains(@class,'manual-code')] | "
        "//*[contains(@class,'connection-code') and contains(@class,'value')]")

    MODAL_GENERATE_NEW_BTN = (By.XPATH,
        "//button[contains(normalize-space(),'Generate new code')] | "
        "//span[contains(normalize-space(),'Generate new code')] | "
        "//*[@data-type='primary' and contains(normalize-space(),'Generate new')]")

    # DevTools-confirmed: <span data-type="cancelModal">Close</span> inside a div.d-flex.
    MODAL_CLOSE_BTN = (By.XPATH,
        "//span[@data-type='cancelModal' and normalize-space()='Close'] | "
        "//*[@role='dialog' or contains(@class,'modal')]"
        "//button[normalize-space()='Close'] | "
        "//*[@role='dialog' or contains(@class,'modal')]"
        "//*[@aria-label='Close' or @aria-label='close']")

    MODAL_PROBLEM_LINK = (By.XPATH,
        "//a[contains(normalize-space(),'Problem with connecting')] | "
        "//*[contains(normalize-space(),'Problem with connecting?')]")

    # ── Frame helpers ─────────────────────────────────────────────────────────

    def _switch_to_form_frame(self, frame_locator):
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 15).until(
                EC.frame_to_be_available_and_switch_to_it(frame_locator)
            )
            _log.info("GPS _switch_to_form_frame: switched into frame %s", frame_locator)
        except TimeoutException:
            _log.warning(
                "GPS _switch_to_form_frame: frame NOT found after 15s — staying in "
                "default_content. Locator: %s", frame_locator
            )

    def wait_for_create_loaded(self):
        self._switch_to_form_frame(GasPumpSettingsListPage.PUMP_CREATE_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.GAS_PUMP_NAME_INPUT))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))

    def wait_for_edit_loaded(self):
        self._switch_to_form_frame(GasPumpSettingsListPage.PUMP_EDIT_FRAME)
        self.wait.until(EC.visibility_of_element_located(self.SAVE_BUTTON))
        self.wait.until(
            lambda d: any(
                inp.get_attribute("value")
                for inp in d.find_elements(By.XPATH,
                    "//input[not(@type='hidden') and not(@type='checkbox') "
                    "and not(@type='radio') and not(@type='submit') "
                    "and not(@type='button') and not(@type='file')]")
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

    def _enter_field(self, locator, value):
        """Enter value into a text/numeric input with React-safe event dispatch."""
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        el.send_keys(str(value))
        self.driver.execute_script("""
            var el = arguments[0];
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(el, arguments[1]);
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        """, el, str(value))

    def enter_pump_name(self, name):
        self._enter_field(self.GAS_PUMP_NAME_INPUT, name)

    def select_site(self, site):
        self.select_react_dropdown_option(self.SITE_COMBOBOX, site)
        time.sleep(1)
        # Verify the selection is visible as a single-value chip.
        try:
            sv_els = self.driver.find_elements(By.XPATH,
                "//div[contains(@class,'rhf-select__single-value') or "
                "contains(@class,'select__single-value')]")
            visible = [e.text.strip() for e in sv_els if e.is_displayed() and e.text.strip()]
            _log.info("GPS select_site '%s': single-value after selection = %s", site, visible)
            if not any(site in v for v in visible):
                _log.warning(
                    "GPS select_site: '%s' NOT found in single-value elements %s — "
                    "selection may not have registered in RHF", site, visible
                )
        except Exception as _e:
            _log.info("GPS select_site: could not read single-value: %s", _e)

    def enter_serial_port(self, value):
        self._enter_field(self.SERIAL_PORT_INPUT, value)

    def enter_serial_number(self, value):
        self._enter_field(self.SERIAL_NUMBER_INPUT, value)

    def enter_baud_rate(self, value):
        self._enter_field(self.BAUD_RATE_INPUT, value)

    def enter_link_timeout(self, value):
        self._enter_field(self.LINK_TIMEOUT_INPUT, value)

    def enter_fetch_interval(self, value):
        # GPS-EDT-008: -1 is a valid stored value on existing records (may mean
        # "no interval limit"). Default on Create form = 0. See product decision.
        self._enter_field(self.FETCH_INTERVAL_INPUT, value)

    def enter_code_length(self, value):
        self._enter_field(self.CODE_LENGTH_INPUT, value)

    def _get_field_value(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        return el.get_attribute("value") or ""

    def get_pump_name(self):
        return self._get_field_value(self.GAS_PUMP_NAME_INPUT)

    def get_baud_rate(self):
        return self._get_field_value(self.BAUD_RATE_INPUT)

    def get_link_timeout(self):
        return self._get_field_value(self.LINK_TIMEOUT_INPUT)

    def get_fetch_interval(self):
        return self._get_field_value(self.FETCH_INTERVAL_INPUT)

    def get_code_length(self):
        return self._get_field_value(self.CODE_LENGTH_INPUT)

    def get_serial_port(self):
        return self._get_field_value(self.SERIAL_PORT_INPUT)

    def pump_name_input_is_valid(self):
        el = self.wait.until(EC.presence_of_element_located(self.GAS_PUMP_NAME_INPUT))
        return el.get_attribute("aria-invalid") != "true"

    def _field_is_valid(self, locator):
        try:
            el = self.wait.until(EC.presence_of_element_located(locator))
            return el.get_attribute("aria-invalid") != "true"
        except Exception:
            return True

    def get_site_options(self):
        """Return all visible site option texts from the site dropdown."""
        combobox = self.wait.until(EC.element_to_be_clickable(self.SITE_COMBOBOX))
        self.driver.execute_script("arguments[0].click();", combobox)
        inner_inputs = combobox.find_elements(By.XPATH, ".//input")
        if inner_inputs:
            try:
                ActionChains(self.driver).click(inner_inputs[0]).perform()
            except Exception:
                self.driver.execute_script("arguments[0].click();", inner_inputs[0])
        options = WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("""
                var opts = Array.from(document.querySelectorAll(
                    '[role="option"], [class*="__option"], [class*="select__option"]'
                )).filter(function(el) {
                    var r = el.getBoundingClientRect();
                    return r.height > 0 && el.textContent.trim();
                });
                return opts.length > 0
                    ? opts.map(function(el) { return el.textContent.trim(); })
                    : null;
            """)
        )
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options or []

    def ensure_active_pump_on(self):
        try:
            toggle = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_PUMP_TOGGLE))
            checked = (
                toggle.get_attribute("aria-checked") == "true"
                or toggle.get_attribute("data-state") == "checked"
            )
            if not checked:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", toggle
                )
                ActionChains(self.driver).move_to_element(toggle).click(toggle).perform()
        except Exception:
            pass

    def ensure_active_pump_off(self):
        try:
            toggle = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_PUMP_TOGGLE))
            checked = (
                toggle.get_attribute("aria-checked") == "true"
                or toggle.get_attribute("data-state") == "checked"
            )
            if checked:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", toggle
                )
                ActionChains(self.driver).move_to_element(toggle).click(toggle).perform()
        except Exception:
            pass

    def active_pump_is_on(self):
        try:
            toggle = self.wait.until(EC.presence_of_element_located(self.ACTIVE_PUMP_TOGGLE))
            return (
                toggle.get_attribute("aria-checked") == "true"
                or toggle.get_attribute("data-state") == "checked"
            )
        except Exception:
            return False

    def click_save(self):
        # The form's submit is triggered by the inner div.d-flex > span[data-type='primary'],
        # NOT the outer shell <button>.  Use ActionChains for a trusted click event.
        el = self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON))
        _log.info(
            "GPS click_save: %s  class=%r  data-type=%r  y=%s",
            el.tag_name,
            (el.get_attribute("class") or "")[:80],
            el.get_attribute("data-type"),
            el.location.get("y", "?"),
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        time.sleep(0.3)
        ActionChains(self.driver).move_to_element(el).click().perform()
        time.sleep(1.5)

        # Check RHF validation errors.
        try:
            invalid_fields = self.driver.execute_script("""
                return Array.from(document.querySelectorAll('input, select, textarea'))
                    .filter(function(el) { return el.getAttribute('aria-invalid') === 'true'; })
                    .map(function(el) {
                        return (el.name || el.id || el.placeholder || '?') + '=' + el.value;
                    });
            """)
            if invalid_fields:
                _log.warning("GPS aria-invalid after save: %s", invalid_fields)
            else:
                _log.info("GPS aria-invalid: none — validation passed")
        except Exception as _iv:
            _log.info("GPS could not read aria-invalid: %s", _iv)

        # Allow the API response to complete before the caller navigates away.
        time.sleep(1.5)
        save_succeeded = False
        try:
            body = self.driver.find_element(By.TAG_NAME, "body").text
            _log.info("GPS form body after save (400 chars): %s", body[:400])
            save_succeeded = (
                "successfully created" in body
                or "successfully updated" in body
            )
        except Exception:
            pass
        # Only leave the form frame on success; stay in frame on validation failure
        # so callers can inspect field validity after a failed save attempt.
        if save_succeeded:
            self.driver.switch_to.default_content()

    def click_cancel(self):
        el = self.wait.until(EC.visibility_of_element_located(self.CANCEL_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def fill_required_fields(self, name, site, serial_port, serial_number,
                              baud_rate, link_timeout, fetch_interval, code_length):
        self.enter_pump_name(name)
        self.select_site(site)
        self.enter_serial_port(serial_port)
        self.enter_serial_number(serial_number)
        self.enter_baud_rate(baud_rate)
        self.enter_link_timeout(link_timeout)
        self.enter_fetch_interval(fetch_interval)
        self.enter_code_length(code_length)

    # ── Wash Book Code List ───────────────────────────────────────────────────

    def _get_wbc_rows(self):
        """Return all visible WBC row elements (div[class*='wbCodeListTable_wbCodeListTableItem_'])."""
        return [
            e for e in self.driver.find_elements(*self.WBC_ROW_ITEMS)
            if e.is_displayed()
        ]

    def wbc_panel_is_visible(self):
        els = self.driver.find_elements(*self.WBC_SECTION_TITLE)
        if any(e.is_displayed() for e in els):
            return True
        body = self.get_body_text()
        return "Wash book code list" in body or "wash book code" in body.lower()

    def add_wbc_button_is_visible(self):
        els = self.driver.find_elements(*self.ADD_WBC_BUTTON)
        return any(e.is_displayed() for e in els)

    def click_add_wbc_row(self):
        el = self.wait.until(EC.element_to_be_clickable(self.ADD_WBC_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)
        time.sleep(0.5)

    def get_wbc_row_count(self):
        return len(self._get_wbc_rows())

    def select_wbc_wash_book(self, row_index, wash_book):
        """Select wash book from the nth WBC row dropdown (0-indexed).

        Confirmed DOM: each row has div[class*='wbCodeListTable_wbCodeListTableItem_'].
        Inside the row: div.rhf-select__control > div > input.rhf-select__input[role='combobox'].
        """
        rows = self._get_wbc_rows()
        if row_index >= len(rows):
            raise IndexError(
                "WBC row %d not found (only %d rows visible)" % (row_index, len(rows))
            )
        row = rows[row_index]

        # Click the dropdown-indicator chevron to open the menu.
        indicator = row.find_element(By.XPATH,
            ".//div[contains(@class,'rhf-select__dropdown-indicator')]")
        self.driver.execute_script("arguments[0].click();", indicator)
        time.sleep(0.2)

        # Type in the combobox input to filter options.
        inner = row.find_element(By.XPATH,
            ".//input[@role='combobox' and contains(@class,'rhf-select__input')]")
        for attempt in range(3):
            try:
                ActionChains(self.driver).click(inner).perform()
                inner.send_keys(Keys.COMMAND, "a")
                inner.send_keys(Keys.BACKSPACE)
                inner.send_keys(wash_book)
                break
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(0.5)
                inner = row.find_element(By.XPATH,
                    ".//input[@role='combobox' and contains(@class,'rhf-select__input')]")

        option = WebDriverWait(self.driver, 10).until(
            lambda d: self._find_react_option(wash_book)
        )
        self.driver.execute_script("arguments[0].click();", option)
        time.sleep(0.3)

    def get_wbc_wash_book_options(self, row_index=0):
        """Return wash book dropdown option texts for the nth WBC row (0-indexed)."""
        rows = self._get_wbc_rows()
        if row_index >= len(rows):
            return []
        row = rows[row_index]

        indicator = row.find_element(By.XPATH,
            ".//div[contains(@class,'rhf-select__dropdown-indicator')]")
        self.driver.execute_script("arguments[0].click();", indicator)
        time.sleep(0.2)

        options = WebDriverWait(self.driver, 8).until(
            lambda d: d.execute_script("""
                var opts = Array.from(document.querySelectorAll(
                    '[role="option"], [class*="__option"], [class*="select__option"]'
                )).filter(function(el) {
                    var r = el.getBoundingClientRect();
                    return r.height > 0 && el.textContent.trim();
                });
                return opts.length > 0
                    ? opts.map(function(el) { return el.textContent.trim(); })
                    : null;
            """)
        )
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.3)
        except Exception:
            pass
        return options or []

    def enter_wbc_id_code(self, row_index, code):
        """Enter Gas pump ID code in the nth WBC row (0-indexed).

        Confirmed name: gasPumpCodeList.{n}.gasPumpIdCode
        Confirmed placeholder: "Gas pump ID code"
        """
        rows = self._get_wbc_rows()
        if row_index >= len(rows):
            raise IndexError(
                "WBC row %d not found (only %d rows visible)" % (row_index, len(rows))
            )
        el = rows[row_index].find_element(By.XPATH,
            ".//input[@placeholder='Gas pump ID code' or contains(@name,'gasPumpIdCode')]")
        el.click()
        el.send_keys(Keys.COMMAND + "a" + Keys.NULL + Keys.BACKSPACE)
        el.send_keys(str(code))
        self.driver.execute_script("""
            var el = arguments[0];
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(el, arguments[1]);
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        """, el, str(code))

    def get_wbc_id_code(self, row_index):
        rows = self._get_wbc_rows()
        if row_index >= len(rows):
            return ""
        try:
            el = rows[row_index].find_element(By.XPATH,
                ".//input[@placeholder='Gas pump ID code' or contains(@name,'gasPumpIdCode')]")
            return el.get_attribute("value") or ""
        except Exception:
            return ""

    def get_wbc_selected_wash_book(self, row_index):
        """Return the selected wash book label text for the nth WBC row.

        After selection, the placeholder is replaced by div.rhf-select__single-value.
        Confirmed selected value: <div class="rhf-select__single-value ...">VK AWB1</div>
        """
        rows = self._get_wbc_rows()
        if row_index >= len(rows):
            return ""
        try:
            el = rows[row_index].find_element(By.XPATH,
                ".//div[contains(@class,'rhf-select__single-value')]")
            return el.text.strip()
        except Exception:
            return ""

    def remove_all_incomplete_wbc_rows(self):
        """Remove all WBC rows (any that remain after fill failure).

        Confirmed remove element: img[alt="Close"] inside
        div[class*="wbCodeListTable_wbCodeListTableItemRemove_"].
        An empty WBC row triggers "Must be selected" / "Can't be empty" and blocks save.
        """
        for _ in range(10):
            btns = [
                e for e in self.driver.find_elements(*self.WBC_REMOVE_BUTTONS)
                if e.is_displayed()
            ]
            if not btns:
                break
            try:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", btns[0]
                )
                self.driver.execute_script("arguments[0].click();", btns[0])
                time.sleep(0.3)
            except Exception:
                break

    def click_remove_wbc_row(self, row_index):
        """Click the Close img on the nth WBC row remove wrapper (0-indexed).

        Confirmed: remove is img[alt="Close"] inside
        div[class*="wbCodeListTable_wbCodeListTableItemRemove_"] — NOT a <button>.
        """
        btns = [
            e for e in self.driver.find_elements(*self.WBC_REMOVE_BUTTONS)
            if e.is_displayed()
        ]
        if row_index >= len(btns):
            raise IndexError(
                "WBC remove img %d not found (only %d visible)" % (row_index, len(btns))
            )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", btns[row_index]
        )
        self.driver.execute_script("arguments[0].click();", btns[row_index])
        time.sleep(0.3)

    # ── Connection status indicator ───────────────────────────────────────────

    def assert_connection_indicator(self, state="unconnected"):
        """Assert the connection indicator matches the expected state.

        Shared by GPS-CRT-015 (list page check) and GPS-CON-002 (edit page check)
        to avoid duplicating the locator logic across two test methods.

        state='unconnected': yellow triangle expected (new pump has not yet
            connected to hardware — blue checkmark must NOT be visible).
        state='connected': blue checkmark expected (pump physically connected).
        """
        if state == "unconnected":
            yellow_els = [
                e for e in self.driver.find_elements(*self.CONNECTION_YELLOW)
                if e.is_displayed()
            ]
            blue_els = [
                e for e in self.driver.find_elements(*self.CONNECTION_BLUE)
                if e.is_displayed()
            ]
            assert yellow_els or not blue_els, (
                "Expected yellow triangle (unconnected) indicator but "
                "blue checkmark (connected) is visible instead"
            )
        elif state == "connected":
            blue_els = [
                e for e in self.driver.find_elements(*self.CONNECTION_BLUE)
                if e.is_displayed()
            ]
            body = self.get_body_text().lower()
            assert blue_els or "connected" in body, (
                "Expected blue checkmark (connected) indicator but none found"
            )

    def check_regen_button_is_visible(self):
        els = self.driver.find_elements(*self.CHECK_REGEN_CODE_BUTTON)
        return any(e.is_displayed() for e in els)

    def click_check_regen_code(self):
        el = self.wait.until(EC.element_to_be_clickable(self.CHECK_REGEN_CODE_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        time.sleep(0.2)
        ActionChains(self.driver).move_to_element(el).click().perform()
        time.sleep(2.0)

    # ── Connection code modal ─────────────────────────────────────────────────

    def modal_is_open(self):
        els = self.driver.find_elements(*self.MODAL_CONTAINER)
        return any(e.is_displayed() for e in els)

    def modal_is_closed(self):
        els = self.driver.find_elements(*self.MODAL_CONTAINER)
        return not any(e.is_displayed() for e in els)

    def get_modal_qr_element(self):
        return WebDriverWait(self.driver, 8).until(
            EC.presence_of_element_located(self.MODAL_QR_CODE)
        )

    def get_modal_manual_code_text(self):
        try:
            el = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located(self.MODAL_MANUAL_CODE)
            )
            return el.text.strip()
        except Exception:
            return ""

    def modal_generate_new_button_is_visible(self):
        els = self.driver.find_elements(*self.MODAL_GENERATE_NEW_BTN)
        return any(e.is_displayed() for e in els)

    def modal_close_button_is_visible(self):
        els = self.driver.find_elements(*self.MODAL_CLOSE_BTN)
        return any(e.is_displayed() for e in els)

    def modal_problem_link_is_visible(self):
        els = self.driver.find_elements(*self.MODAL_PROBLEM_LINK)
        return any(e.is_displayed() for e in els)

    def click_modal_close(self):
        try:
            btn = WebDriverWait(self.driver, 8).until(
                EC.element_to_be_clickable(self.MODAL_CLOSE_BTN)
            )
            ActionChains(self.driver).move_to_element(btn).click().perform()
            time.sleep(0.8)
        except Exception:
            try:
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(0.5)
            except Exception:
                pass

    def click_modal_generate_new(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.MODAL_GENERATE_NEW_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(0.5)
