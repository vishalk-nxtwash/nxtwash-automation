import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class AdminKioskSettingsPage(BasePage):
    """Kiosk Settings list page — /kiosk"""

    KSK_LIST_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/kiosk_settings/kiosks') "
        "and not(contains(@src,'/kiosk_settings/kiosks/'))]")
    KSK_CREATE_FRAME = (By.XPATH,
        "//iframe[contains(@src,'/kiosk_settings/kiosks/new')]")
    KSK_EDIT_FRAME = (By.XPATH,
        "//iframe["
        "(contains(@src,'/kiosk_settings/kiosks/') or "
        " (contains(@src,'/kiosk_settings/kiosks') and contains(@src,'?'))) "
        "and not(contains(@src,'/new'))"
        "]")

    ADD_KIOSK_BUTTON = (By.XPATH,
        "//span[@data-type='primary' and contains(normalize-space(),'Add new kiosk')] | "
        "//span[@data-type='primary' and contains(normalize-space(),'kiosk')] | "
        "//button[contains(normalize-space(),'Add new kiosk')]")

    SEARCH_INPUT = (By.XPATH,
        "//input[@name='kioskName' or @name='kiosk_name' or "
        "@placeholder='Search' or @placeholder='Search kiosk' or "
        "@placeholder='Kiosk name' or @placeholder='Search by kiosk name']")

    FILTER_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Filter by')] | "
        "//span[contains(normalize-space(),'Filter by') and not(ancestor::*[@role='dialog'])] | "
        "//*[@role='button' and contains(normalize-space(),'Filter by')]")
    FILTER_STATUS_COMBOBOX = (By.XPATH,
        "//*[normalize-space()='Status' or normalize-space()='Active']"
        "/following::*[@role='combobox'][1]")
    FILTER_SITE_COMBOBOX = (By.XPATH,
        "//div[contains(@class,'form-select__control') and "
        ".//div[contains(@class,'form-select__placeholder') and "
        "contains(normalize-space(),'site')]] | "
        "//div[contains(@class,'form-select__control')][1]")
    APPLY_FILTERS_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters'] | "
        "//button[normalize-space()='Apply'] | "
        "//span[normalize-space()='Apply filters'] | "
        "//span[normalize-space()='Apply'] | "
        "//*[@role='button' and (normalize-space()='Apply filters' or normalize-space()='Apply')]")
    RESET_ALL_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Reset all')] | "
        "//button[contains(normalize-space(),'Reset All')] | "
        "//button[contains(normalize-space(),'Clear all')] | "
        "//button[contains(normalize-space(),'Clear All')] | "
        "//span[contains(normalize-space(),'Reset all')] | "
        "//span[contains(normalize-space(),'Reset All')] | "
        "//*[@role='button' and (contains(normalize-space(),'Reset') or contains(normalize-space(),'Clear all'))]")

    GRID_ROWS = (By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row')] | "
        "//tr[contains(@class,'row') and not(contains(@class,'header'))]")

    EDIT_LINK = (By.XPATH,
        "//a[@role='button' and contains(@class,'table-page__page-content__table__edit')] | "
        "//a[contains(@href,'/kiosk_settings/kiosks/') and not(contains(@href,'/new'))] | "
        "//a[contains(@class,'edit') and contains(@href,'/kiosk')]")

    # Configurator chooser dialog that appears when clicking Edit on some kiosks.
    CONFIGURATOR_DIALOG = (By.XPATH,
        "//*[contains(normalize-space(),'Choose which kiosk configurator') or "
        "contains(normalize-space(),'kiosk configurator to use')]")
    CONFIGURATOR_LEGACY_BTN = (By.XPATH,
        "//button[normalize-space()='Legacy'] | "
        "//span[@role='button' and normalize-space()='Legacy'] | "
        "//*[@role='button' and normalize-space()='Legacy']")
    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and not(contains(@style,'display: none'))] | "
        "//*[contains(@class,'inovua-react-toolkit-load-mask')]")

    def wait_for_loaded(self):
        self.switch_to_frame_with_retry(self.KSK_LIST_FRAME, timeout=60)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        self.wait.until(EC.element_to_be_clickable(self.ADD_KIOSK_BUTTON))
        # The filter badge count is fetched asynchronously after the page renders.
        # Wait for the button text to stabilize so reset_filters_if_active() sees the final state.
        self._wait_for_filter_stable()
        # Dismiss any staging/environment toasts that overlay the iframe and intercept clicks.
        self._dismiss_toasts()

    def _wait_for_filter_stable(self, stable_for=1.0, timeout=15):
        """Poll the filter button until its text hasn't changed for stable_for seconds."""
        FILTER_BTN = (By.XPATH, "//button[contains(@class,'filterButton')]")
        prev_text = None
        last_change = time.monotonic()
        end_time = time.monotonic() + timeout
        while time.monotonic() < end_time:
            try:
                els = self.driver.find_elements(*FILTER_BTN)
                text = els[0].text.strip() if els else ""
            except Exception:
                text = ""
            if text != prev_text:
                last_change = time.monotonic()
                prev_text = text
            elif text and (time.monotonic() - last_change) >= stable_for:
                return
            time.sleep(0.2)

    def _dismiss_toasts(self):
        """Click away any Toastify banners in the outer document.

        Staging emits a persistent 'dev-environment-unstable' warning toast that
        overlaps the iframe and intercepts native clicks on iframe elements.
        We switch to the outer document, dismiss all visible toasts, then re-enter
        the list iframe so subsequent actions work cleanly.
        """
        TOAST = (By.XPATH, "//*[contains(@class,'Toastify__toast') and @role='alert']")
        try:
            self.driver.switch_to.default_content()
            toasts = self.driver.find_elements(*TOAST)
            for toast in toasts:
                try:
                    if toast.is_displayed():
                        self.driver.execute_script("arguments[0].click();", toast)
                except Exception:
                    pass
            WebDriverWait(self.driver, 5).until(
                lambda d: not any(t.is_displayed() for t in d.find_elements(*TOAST))
            )
        except Exception:
            pass
        finally:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it(self.KSK_LIST_FRAME)
                )
            except Exception:
                pass

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def search_kiosk(self, name):
        el = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        el.send_keys(name)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value") == name
        )
        time.sleep(1)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def clear_search(self):
        el = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
        el.click()
        el.send_keys(Keys.CONTROL + "a" + Keys.NULL + Keys.BACKSPACE)
        self.wait.until(
            lambda d: d.find_element(*self.SEARCH_INPUT).get_attribute("value") == ""
        )
        time.sleep(1)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def _row_locator(self, name):
        return (By.XPATH,
            "//span[contains(@class,'table-cell-ellipsis') and @title='{n}'] | "
            "//span[contains(@class,'table-cell-ellipsis') and normalize-space()='{n}'] | "
            "//*[contains(@class,'InovuaReactDataGrid__row')]//*[normalize-space()='{n}' or @title='{n}'] | "
            "//*[@role='row']//*[normalize-space()='{n}' or @title='{n}'] | "
            "//*[@role='gridcell' and (normalize-space()='{n}' or @title='{n}')]"
            .format(n=name))

    def wait_for_kiosk_row(self, name, timeout=None):
        locator = self._row_locator(name)
        if timeout:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        return self.wait.until(EC.presence_of_element_located(locator))

    def kiosk_exists(self, name):
        # Reset filters so inactive kiosks are visible before searching.
        self.reset_filters_if_active()
        self.search_kiosk(name)
        try:
            self.wait_for_kiosk_row(name, timeout=15)
            return True
        except TimeoutException:
            return False

    def get_kiosk_status(self, name):
        self.search_kiosk(name)
        row = self.wait_for_kiosk_row(name)
        try:
            badge = row.find_element(By.XPATH,
                ".//*[normalize-space()='Active' or normalize-space()='Inactive']")
            return badge.text.strip()
        except Exception:
            return ""

    def get_visible_row_count(self):
        rows = self.driver.find_elements(*self.GRID_ROWS)
        return len([r for r in rows if r.is_displayed()])

    def click_add_kiosk(self):
        el = self.wait.until(EC.element_to_be_clickable(self.ADD_KIOSK_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)

    def open_edit_kiosk(self, name):
        self.search_kiosk(name)
        self.wait_for_kiosk_row(name)
        edit_link = self.wait.until(EC.element_to_be_clickable(self.EDIT_LINK))
        # Prefer navigating the outer page to the edit URL so the shell renders a
        # real KSK_EDIT_FRAME iframe that wait_for_edit_loaded() can switch into.
        # If the href is just the list root URL or empty, fall back to a JS click
        # (React Router in-frame navigation — wait_for_edit_loaded handles this too).
        href = edit_link.get_attribute("href") or ""
        _kiosk_base = "/kiosk_settings/kiosks"
        _is_list_root = (
            not href
            or href.rstrip("/").endswith(_kiosk_base)
            and "?" not in href
        )
        if href and _kiosk_base in href and "/new" not in href and not _is_list_root:
            self.driver.switch_to.default_content()
            self.driver.get(href)
        else:
            self.driver.execute_script("arguments[0].click();", edit_link)
        # Some kiosks show a "Choose which kiosk configurator to use" dialog
        # before opening the edit form.  Click "Legacy" to proceed.
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.CONFIGURATOR_DIALOG)
            )
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CONFIGURATOR_LEGACY_BTN)
            )
            self.driver.execute_script("arguments[0].click();", btn)
        except Exception:
            pass  # No configurator dialog — edit form opens directly.

    def filter_panel_is_open(self):
        els = self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)
        return any(e.is_displayed() for e in els)

    def open_filter_panel(self):
        if self.filter_panel_is_open():
            return
        # Use native Selenium click — Radix Dialog triggers need browser event dispatch.
        btn = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
        btn.click()
        # Dialog renders in the iframe's DOM via Radix portal.  Short outer-doc fallback.
        try:
            WebDriverWait(self.driver, 8).until(
                EC.visibility_of_element_located(self.APPLY_FILTERS_BUTTON)
            )
            return
        except TimeoutException:
            pass
        # Panel not visible in iframe — check outer document.
        self.driver.switch_to.default_content()
        self.wait.until(EC.visibility_of_element_located(self.APPLY_FILTERS_BUTTON))

    def close_filter_panel(self):
        if not self.filter_panel_is_open():
            return
        # Press ESC — closes most drawer components regardless of context.
        try:
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
            WebDriverWait(self.driver, 5).until(lambda d: not self.filter_panel_is_open())
            return
        except Exception:
            pass
        # Fallback: toggle via the filter button (which is inside the iframe).
        btn = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        WebDriverWait(self.driver, 10).until(lambda d: not self.filter_panel_is_open())

    def filter_by_status(self, status):
        self.open_filter_panel()
        self.select_react_dropdown_option(self.FILTER_STATUS_COMBOBOX, status)

    def filter_by_site(self, site):
        self.open_filter_panel()
        self.select_react_dropdown_option(self.FILTER_SITE_COMBOBOX, site)

    def apply_filters(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def reset_filters(self):
        self.open_filter_panel()
        btn = self.wait.until(EC.element_to_be_clickable(self.RESET_ALL_BUTTON))
        btn.click()
        # Clicking Apply filters commits the cleared state (Reset all alone only clears the UI).
        try:
            apply = self.wait.until(EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON))
            apply.click()
        except Exception:
            pass
        self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))

    def reset_filters_if_active(self):
        """Reset the active kiosk list filter.

        Called after wait_for_loaded() which ensures the filter badge text is stable.
        The filter button is a Radix UI Dialog trigger — clicking it opens a dialog
        inside the iframe.  Reset all clears the UI; Apply filters commits to server.
        Both clicks are required.
        """
        if "Filter by (" not in self.get_body_text():
            return

        # Native click preferred for Radix Dialog trigger; JS-click fallback handles
        # any residual overlay that survives toast dismissal.
        btn = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

        # Dialog renders in the iframe's DOM.  Try current context first.
        reset_btn = None
        try:
            reset_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.RESET_ALL_BUTTON)
            )
        except TimeoutException:
            pass

        if reset_btn is None:
            # Fall back to outer document (React portal pattern).
            self.driver.switch_to.default_content()
            try:
                reset_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.RESET_ALL_BUTTON)
                )
            except TimeoutException:
                self.wait.until(
                    EC.frame_to_be_available_and_switch_to_it(self.KSK_LIST_FRAME)
                )
                return

        # Click Reset all, then Apply filters to commit the cleared state.
        reset_btn.click()
        try:
            apply_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON)
            )
            apply_btn.click()
        except Exception:
            pass

        # Return to the list iframe and wait for grid to settle.
        try:
            self.driver.switch_to.default_content()
        except Exception:
            pass
        WebDriverWait(self.driver, 60).until(EC.frame_to_be_available_and_switch_to_it(self.KSK_LIST_FRAME))
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.LOAD_MASK)
            )
        except Exception:
            pass

    def filter_panel_has_expected_controls(self):
        self.open_filter_panel()
        body = self.get_body_text().lower()
        return "filter" in body or "status" in body

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

    def wait_for_create_frame(self, timeout=60):
        """Switch to default content and wait for the create-form iframe to appear."""
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(self.KSK_CREATE_FRAME)
            )
            return True
        except Exception:
            return False


class AdminKioskFormPage(BasePage):
    """Kiosk create/edit form — /kiosk/new or /kiosk?kioskId=..."""

    # ── Core form fields ─────────────────────────────────────────────────────

    KIOSK_NAME_INPUT = (By.XPATH,
        "//input[@name='kioskName' or @name='name' or @name='kiosk_name' or "
        "@placeholder='Kiosk name' or @placeholder='Name']")

    SITE_COMBOBOX = (By.XPATH,
        "//input[@name='kioskName' or @placeholder='Kiosk name']"
        "/following::div[contains(@class,'form-select__control')][1]")

    LANE_COMBOBOX = (By.XPATH,
        "//div[contains(@class,'form-select__control') and "
        ".//div[contains(@class,'form-select__placeholder') and "
        "contains(translate(normalize-space(),'LANE','lane'),'lane')]] | "
        "//input[@name='kioskName' or @placeholder='Kiosk name']"
        "/following::div[contains(@class,'form-select__control')][3]")

    ACTIVE_KIOSK_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Active kiosk') or "
        "contains(normalize-space(),'Active Kiosk')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch'] | "
        "//form//button[@role='switch'][1]")

    SAVE_BUTTON = (By.XPATH,
        "//span[@data-type='primary' and normalize-space()='Save kiosk'] | "
        "//span[@data-type='primary' and contains(normalize-space(),'Save kiosk')] | "
        "//button[contains(normalize-space(),'Save kiosk')] | "
        "//*[@data-type='primary' and normalize-space()='Save kiosk']")

    CANCEL_BUTTON = (By.XPATH,
        "//span[normalize-space()='Cancel'] | "
        "//button[normalize-space()='Cancel']")

    # ── Service Settings ─────────────────────────────────────────────────────

    MEMBERSHIPS_CHECKBOX = (By.XPATH,
        "//*[contains(normalize-space(),'Memberships')]"
        "/ancestor::*[.//input[@type='checkbox']][1]//input[@type='checkbox'] | "
        "//input[@name='memberships' or @name='membership']")

    WASH_PACKAGES_CHECKBOX = (By.XPATH,
        "//*[contains(normalize-space(),'Wash packages') or "
        "contains(normalize-space(),'Wash Packages')]"
        "/ancestor::*[.//input[@type='checkbox']][1]//input[@type='checkbox'] | "
        "//input[@name='washPackages' or @name='wash_packages']")

    WASH_EXTRAS_CHECKBOX = (By.XPATH,
        "//*[contains(normalize-space(),'Wash extras') and "
        "not(contains(normalize-space(),'Second'))]"
        "/ancestor::*[.//input[@type='checkbox']][1]//input[@type='checkbox'] | "
        "//input[@name='washExtras' or @name='wash_extras']")

    SECOND_WASH_EXTRAS_CHECKBOX = (By.XPATH,
        "//*[contains(normalize-space(),'Second wash extras') or "
        "contains(normalize-space(),'Second Wash Extras')]"
        "/ancestor::*[.//input[@type='checkbox']][1]//input[@type='checkbox'] | "
        "//input[@name='secondWashExtras' or @name='second_wash_extras']")

    UPSALE_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Upsale') or contains(normalize-space(),'upsale')]"
        "/following::button[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Upsale') or contains(normalize-space(),'upsale')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch']")

    # ── Gate Settings ────────────────────────────────────────────────────────

    GATE_OPERATIONAL_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Gate operational') or "
        "contains(normalize-space(),'Gate Operational')]"
        "/following::button[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Gate operational') or "
        "contains(normalize-space(),'Gate Operational')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch']")

    # ── Tunnel Settings ──────────────────────────────────────────────────────

    TUNNEL_OPERATIONAL_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Tunnel operational') or "
        "contains(normalize-space(),'Tunnel Operational')]"
        "/following::button[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Tunnel operational') or "
        "contains(normalize-space(),'Tunnel Operational')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch']")

    # ── Middleware Settings ──────────────────────────────────────────────────

    # Section header is a cursor:pointer <div>, not a <button>.
    MIDDLEWARE_SECTION_HEADER = (By.XPATH,
        "//div[contains(@class,'color-dark') and normalize-space()='Middleware settings']"
        "/ancestor::div[contains(@style,'cursor')][1] | "
        "//div[normalize-space()='Middleware settings' and "
        "contains(@style,'cursor')]")

    MIDDLEWARE_IP_INPUT = (By.XPATH,
        "//input[@name='middlewareIp' or "
        "@placeholder='Add middleware IP' or "
        "contains(@placeholder,'middleware') or contains(@placeholder,'Middleware')]")

    # ── Device Settings ──────────────────────────────────────────────────────

    PAYMENT_SERIAL_INPUT = (By.XPATH,
        "//input[@name='paymentSerial' or @name='payment_serial' or "
        "@name='serialNumber' or @name='serial_number' or "
        "@placeholder='Payment serial' or @placeholder='Serial number' or "
        "contains(@placeholder,'serial')]")

    CAR_RECOGNITION_BY_PLATE_RADIO = (By.XPATH,
        "//*[contains(normalize-space(),'License Plate') or "
        "contains(normalize-space(),'license plate')]"
        "/ancestor::*[.//input[@type='radio']][1]//input[@type='radio'] | "
        "//input[@type='radio' and @value='plate']")

    CAR_RECOGNITION_BY_RFID_RADIO = (By.XPATH,
        "//*[contains(normalize-space(),'RFID tag') or "
        "contains(normalize-space(),'RFID Tag') or "
        "contains(normalize-space(),'rfid')]"
        "/ancestor::*[.//input[@type='radio']][1]//input[@type='radio'] | "
        "//input[@type='radio' and @value='rfid']")

    CC_ENTRY_METHODS_INPUT = (By.XPATH,
        "//input[@name='ccEntryMethods' or @name='cc_entry_methods' or "
        "contains(@placeholder,'CC') or contains(@placeholder,'entry method')]")

    # ── Timer Settings ───────────────────────────────────────────────────────

    RECEIPT_MODAL_DELAY_INPUT = (By.XPATH,
        "//input[@name='receiptModalDelay' or @name='receipt_modal_delay' or "
        "contains(@placeholder,'receipt') or contains(@placeholder,'Receipt')]")

    RFID_TAG_DELAY_INPUT = (By.XPATH,
        "//input[@name='rfidTagDelay' or @name='rfid_tag_delay' or "
        "contains(@placeholder,'RFID') or contains(@placeholder,'rfid')]")

    EXTRAS_DISMISS_DELAY_INPUT = (By.XPATH,
        "//input[@name='extrasDismissDelay' or @name='extras_dismiss_delay' or "
        "contains(@placeholder,'extras') or contains(@placeholder,'Extras')]")

    # ── Flow/Appearance Settings ─────────────────────────────────────────────

    # Second batch of "remaining" toggles covered by KSK-FLW-009
    ENABLE_LOG_WRITE_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Enable log write') or "
        "contains(normalize-space(),'log write')]"
        "/following::button[@role='switch'][1]")

    USE_SOFTWARE_KEYBOARD_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'software keyboard') or "
        "contains(normalize-space(),'Software keyboard')]"
        "/following::button[@role='switch'][1]")

    HIDE_HELP_BUTTON_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Hide help') or "
        "contains(normalize-space(),'hide help')]"
        "/following::button[@role='switch'][1]")

    ENABLE_DC_DIRECT_TIP_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'DC direct tip') or "
        "contains(normalize-space(),'direct tip')]"
        "/following::button[@role='switch'][1]")

    ENABLE_AUTO_NAVIGATE_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'auto navigate') or "
        "contains(normalize-space(),'Auto navigate')]"
        "/following::button[@role='switch'][1]")

    ACCEPT_CASH_WITHOUT_ACCEPTOR_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'cash without acceptor') or "
        "contains(normalize-space(),'Cash without acceptor')]"
        "/following::button[@role='switch'][1]")

    WEX_WASH_CARDS_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Wex') or "
        "contains(normalize-space(),'Wash card') or "
        "contains(normalize-space(),'wash card')]"
        "/following::button[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Wex') or "
        "contains(normalize-space(),'Wash card')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch']")

    THEME_DROPDOWN = (By.XPATH,
        "//*[normalize-space()='Theme' or contains(normalize-space(),'Theme')]"
        "/following::*[@role='combobox'][1]")

    OPTSPOT_TEXT_INPUT = (By.XPATH,
        "//input[contains(@name,'optspot') or contains(@name,'Optspot') or "
        "contains(@placeholder,'optspot') or contains(@placeholder,'Optspot')]")

    DEDUP_TIMER_INPUT = (By.XPATH,
        "//input[@name='dedupTimer' or @name='dedup_timer' or "
        "contains(@placeholder,'dedup') or contains(@placeholder,'Dedup')]")

    SIGN_MEMBERSHIP_HEADING_INPUT = (By.XPATH,
        "//input[@name='signMembershipHeading' or @name='sign_membership_heading' or "
        "contains(@placeholder,'membership heading') or "
        "contains(@placeholder,'Membership heading')]")

    # ── Localization Settings ────────────────────────────────────────────────

    USE_EXTERNAL_TRANSLATIONS_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'external translation') or "
        "contains(normalize-space(),'External translation') or "
        "contains(normalize-space(),'Use external')]"
        "/following::button[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Use external translation')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch']")

    TRANSLATION_URL_INPUT = (By.XPATH,
        "//input[@name='translationUrl' or @name='translation_url' or "
        "contains(@placeholder,'translation') or "
        "contains(@placeholder,'Translation URL')]")

    ADD_TRANSLATION_URL_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Add') and "
        "contains(normalize-space(),'URL')] | "
        "//button[contains(normalize-space(),'Add translation')]")

    # ── Fleet Settings ───────────────────────────────────────────────────────

    FLEET_CAPABILITIES_DROPDOWN = (By.XPATH,
        "//*[contains(normalize-space(),'Fleet capabilities') or "
        "contains(normalize-space(),'Capabilities')]"
        "/following::*[@role='combobox'][1]")

    FLEET_MANAGER_URL_INPUT = (By.XPATH,
        "//input[@name='fleetManagerUrl' or @name='fleet_manager_url' or "
        "contains(@placeholder,'fleet manager') or "
        "contains(@placeholder,'Fleet manager')]")

    CALL_ATTENDANT_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Call attendant') or "
        "contains(normalize-space(),'call attendant')]"
        "/following::button[@role='switch'][1] | "
        "//*[contains(normalize-space(),'Call attendant')]"
        "/ancestor::*[.//button[@role='switch']][1]//button[@role='switch']")

    FLEET_TOGGLE = (By.XPATH,
        "//*[contains(normalize-space(),'Fleet') and "
        "not(contains(normalize-space(),'capabilities')) and "
        "not(contains(normalize-space(),'manager')) and "
        "not(contains(normalize-space(),'attendant'))]"
        "/following::button[@role='switch'][1]")

    # ── Active/Connection ────────────────────────────────────────────────────

    KIOSK_CONNECTED_TEXT = (By.XPATH,
        "//*[contains(normalize-space(),'Kiosk connected') or "
        "contains(normalize-space(),'kiosk connected')]")

    CHECK_REGEN_CODE_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Check') or "
        "contains(normalize-space(),'re-generate') or "
        "contains(normalize-space(),'regenerate') or "
        "contains(normalize-space(),'Generate code')]")

    # ── Connection Code Modal ────────────────────────────────────────────────

    GENERATE_CONNECTION_CODE_BTN = (By.XPATH,
        "//span[@data-type='primary' and "
        "contains(normalize-space(),'Generate connection code')] | "
        "//div[contains(@class,'d-flex')]"
        "//span[contains(normalize-space(),'Generate connection code')] | "
        "//button[contains(normalize-space(),'Generate connection code')]")

    CODE_MODAL_CONTAINER = (By.XPATH,
        "//*[contains(@class,'generate-code-modal')]")

    CODE_MODAL_MANUAL_VALUE = (By.XPATH,
        "//*[contains(@class,'generate-code-modal__code_qr-descr__value')]")

    CODE_MODAL_CLOSE_BTN = (By.XPATH,
        "//span[@data-type='cancelModal' and normalize-space()='Close'] | "
        "//button[normalize-space()='Close']")

    # ── Load / frame ─────────────────────────────────────────────────────────

    def wait_for_create_loaded(self):
        self.switch_to_frame_with_retry(AdminKioskSettingsPage.KSK_CREATE_FRAME, timeout=60)
        self.wait.until(EC.visibility_of_element_located(self.KIOSK_NAME_INPUT))

    def wait_for_edit_loaded(self):
        """Wait for the kiosk name input in the edit form.

        Handles multiple iframe architectures:
        1. Dedicated edit iframe (KSK_EDIT_FRAME) — outer-page navigation
        2. Current iframe context (React Router in-frame navigation from list)
        3. List iframe re-entered explicitly (fallback for React Router case)
        """
        # Try each context briefly so we do not spend 60 s in the wrong one.
        for ctx_fn, visible_timeout in (
            (lambda: self.switch_to_frame_with_retry(
                AdminKioskSettingsPage.KSK_EDIT_FRAME, timeout=20), 15),
            (lambda: None, 5),   # current context after JS click (list iframe)
            (lambda: self.switch_to_frame_with_retry(
                AdminKioskSettingsPage.KSK_LIST_FRAME, timeout=8), 10),
        ):
            try:
                ctx_fn()
                WebDriverWait(self.driver, visible_timeout).until(
                    EC.visibility_of_element_located(self.KIOSK_NAME_INPUT)
                )
                # Found — wait for the pre-populated value.
                self.wait.until(
                    lambda d: d.find_element(
                        *self.KIOSK_NAME_INPUT
                    ).get_attribute("value") != ""
                )
                return
            except Exception:
                continue
        # Final long-wait in edit frame (slow cold-start page load)
        self.switch_to_frame_with_retry(AdminKioskSettingsPage.KSK_EDIT_FRAME, timeout=45)
        self.wait.until(EC.visibility_of_element_located(self.KIOSK_NAME_INPUT))
        self.wait.until(
            lambda d: d.find_element(*self.KIOSK_NAME_INPUT).get_attribute("value") != ""
        )

    def get_body_text(self):
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except Exception:
            self.driver.switch_to.default_content()
            return self.driver.find_element(By.TAG_NAME, "body").text

    # ── Core form actions ─────────────────────────────────────────────────────

    def get_kiosk_name_value(self):
        el = self.wait.until(EC.presence_of_element_located(self.KIOSK_NAME_INPUT))
        return el.get_attribute("value") or ""

    def enter_kiosk_name(self, name):
        self.enter_text(self.KIOSK_NAME_INPUT, name)

    def _select_dropdown(self, locator, value):
        self.select_react_dropdown_option(locator, value)

    def select_site(self, site):
        self._select_dropdown(self.SITE_COMBOBOX, site)

    def select_lane(self, lane):
        self._select_dropdown(self.LANE_COMBOBOX, lane)

    def _get_dropdown_options(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", el)
        opts = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH,
             "//*[contains(@class,'form-select__option')] | //*[@role='option']")
        ))
        return [o.text.strip() for o in opts if o.text.strip()]

    def get_lane_options(self):
        return self._get_dropdown_options(self.LANE_COMBOBOX)

    def get_site_options(self):
        return self._get_dropdown_options(self.SITE_COMBOBOX)

    def ensure_active_kiosk_on(self):
        try:
            toggle = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_KIOSK_TOGGLE))
            checked = (
                toggle.get_attribute("aria-checked") == "true"
                or toggle.get_attribute("data-state") == "checked"
            )
            if not checked:
                self.driver.execute_script("arguments[0].click();", toggle)
        except Exception:
            pass

    def ensure_active_kiosk_off(self):
        try:
            toggle = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_KIOSK_TOGGLE))
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
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 10).until(lambda d: d.current_url != url_before)
            # URL changed — outer-page navigation: save succeeded.
        except Exception:
            # URL unchanged: either validation blocked save (form stays) or
            # React Router navigated within the same iframe.
            # Re-enter the best available iframe for post-save assertions.
            for frame_loc in (
                AdminKioskSettingsPage.KSK_CREATE_FRAME,
                AdminKioskSettingsPage.KSK_EDIT_FRAME,
                AdminKioskSettingsPage.KSK_LIST_FRAME,
            ):
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.frame_to_be_available_and_switch_to_it(frame_loc)
                    )
                    break
                except Exception:
                    continue

    def click_cancel(self):
        # Cancel button is inside the form iframe — stay in current context, then exit.
        el = self.wait.until(EC.visibility_of_element_located(self.CANCEL_BUTTON))
        self.driver.execute_script("arguments[0].click();", el)
        self.driver.switch_to.default_content()

    def kiosk_name_input_is_valid(self):
        el = self.wait.until(EC.presence_of_element_located(self.KIOSK_NAME_INPUT))
        aria_invalid = el.get_attribute("aria-invalid")
        if aria_invalid == "true":
            return False
        return True

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
        if expanded is not None:
            return expanded == "true"
        return False

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

    def configure_panel_is_visible(self):
        body = self.get_body_text()
        return (
            "Configure your kiosk service screens" in body
            or "configure" in body.lower()
        )

    def get_configure_panel_tabs(self):
        tabs = self.driver.find_elements(By.XPATH, "//*[@role='tab']")
        return [t.text.strip() for t in tabs if t.text.strip() and t.is_displayed()]

    # ── Service Settings ──────────────────────────────────────────────────────

    def ensure_checkbox_checked(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        if not el.is_selected():
            self.driver.execute_script("arguments[0].click();", el)
            self.wait.until(lambda d: d.find_element(*locator).is_selected())

    def ensure_checkbox_unchecked(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        if el.is_selected():
            self.driver.execute_script("arguments[0].click();", el)
            self.wait.until(lambda d: not d.find_element(*locator).is_selected())

    def get_checkbox_state(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        return el.is_selected()

    def ensure_upsale_on(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.UPSALE_TOGGLE))
        if toggle.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.UPSALE_TOGGLE)
                .get_attribute("aria-checked") == "true"
            )

    def ensure_upsale_off(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.UPSALE_TOGGLE))
        if toggle.get_attribute("aria-checked") != "false":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.UPSALE_TOGGLE)
                .get_attribute("aria-checked") == "false"
            )

    # ── Gate Settings ─────────────────────────────────────────────────────────

    def ensure_gate_operational_on(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.GATE_OPERATIONAL_TOGGLE))
        if toggle.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.GATE_OPERATIONAL_TOGGLE)
                .get_attribute("aria-checked") == "true"
            )

    def ensure_gate_operational_off(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.GATE_OPERATIONAL_TOGGLE))
        if toggle.get_attribute("aria-checked") != "false":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.GATE_OPERATIONAL_TOGGLE)
                .get_attribute("aria-checked") == "false"
            )

    def get_gate_operational_state(self):
        toggle = self.wait.until(
            EC.presence_of_element_located(self.GATE_OPERATIONAL_TOGGLE)
        )
        return "on" if toggle.get_attribute("aria-checked") == "true" else "off"

    # ── Tunnel Settings ───────────────────────────────────────────────────────

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

    # ── Middleware Settings ───────────────────────────────────────────────────

    def enter_middleware_ip(self, ip):
        # Expand the Middleware settings section if the input is not yet visible.
        inputs = self.driver.find_elements(*self.MIDDLEWARE_IP_INPUT)
        if not inputs or not any(e.is_displayed() for e in inputs):
            try:
                header = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.MIDDLEWARE_SECTION_HEADER)
                )
                self.driver.execute_script("arguments[0].click();", header)
            except Exception:
                pass
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.MIDDLEWARE_IP_INPUT)
        )
        element.clear()
        element.send_keys(ip)

    def get_middleware_ip(self):
        el = self.wait.until(EC.presence_of_element_located(self.MIDDLEWARE_IP_INPUT))
        return el.get_attribute("value") or ""

    # ── Device Settings ───────────────────────────────────────────────────────

    def enter_payment_serial(self, serial):
        self.enter_text(self.PAYMENT_SERIAL_INPUT, serial)

    def select_car_recognition_type(self, type_text):
        if "license plate" in type_text.lower() or "plate" in type_text.lower():
            el = self.wait.until(
                EC.element_to_be_clickable(self.CAR_RECOGNITION_BY_PLATE_RADIO)
            )
        else:
            el = self.wait.until(
                EC.element_to_be_clickable(self.CAR_RECOGNITION_BY_RFID_RADIO)
            )
        self.driver.execute_script("arguments[0].click();", el)

    def get_car_recognition_type(self):
        try:
            plate = self.driver.find_element(*self.CAR_RECOGNITION_BY_PLATE_RADIO)
            if plate.is_selected():
                return "By License Plate"
        except Exception:
            pass
        try:
            rfid = self.driver.find_element(*self.CAR_RECOGNITION_BY_RFID_RADIO)
            if rfid.is_selected():
                return "By RFID tag"
        except Exception:
            pass
        return ""

    def enter_cc_entry_methods(self, text):
        self.enter_text(self.CC_ENTRY_METHODS_INPUT, text)

    # ── Timer Settings ────────────────────────────────────────────────────────

    def enter_receipt_modal_delay(self, value):
        self.enter_text(self.RECEIPT_MODAL_DELAY_INPUT, str(value))

    def enter_rfid_tag_delay(self, value):
        self.enter_text(self.RFID_TAG_DELAY_INPUT, str(value))

    def enter_extras_dismiss_delay(self, value):
        self.enter_text(self.EXTRAS_DISMISS_DELAY_INPUT, str(value))

    def get_receipt_modal_delay(self):
        el = self.wait.until(EC.presence_of_element_located(self.RECEIPT_MODAL_DELAY_INPUT))
        return el.get_attribute("value") or ""

    def get_rfid_tag_delay(self):
        el = self.wait.until(EC.presence_of_element_located(self.RFID_TAG_DELAY_INPUT))
        return el.get_attribute("value") or ""

    def get_extras_dismiss_delay(self):
        el = self.wait.until(EC.presence_of_element_located(self.EXTRAS_DISMISS_DELAY_INPUT))
        return el.get_attribute("value") or ""

    def timer_input_is_valid(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        aria_invalid = el.get_attribute("aria-invalid")
        if aria_invalid == "true":
            return False
        class_attr = el.get_attribute("class") or ""
        if "error" in class_attr.lower() or "invalid" in class_attr.lower():
            return False
        return True

    # ── Flow/Appearance Settings ──────────────────────────────────────────────

    def ensure_flow_toggle_on(self, toggle_locator):
        toggle = self.wait.until(EC.element_to_be_clickable(toggle_locator))
        if toggle.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*toggle_locator)
                .get_attribute("aria-checked") == "true"
            )

    def ensure_flow_toggle_off(self, toggle_locator):
        toggle = self.wait.until(EC.element_to_be_clickable(toggle_locator))
        if toggle.get_attribute("aria-checked") != "false":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*toggle_locator)
                .get_attribute("aria-checked") == "false"
            )

    def select_theme(self, theme_name):
        self.select_react_dropdown_option(self.THEME_DROPDOWN, theme_name)

    def enter_optspot_text(self, text):
        self.enter_text(self.OPTSPOT_TEXT_INPUT, text)

    def enter_sign_membership_heading(self, text):
        self.enter_text(self.SIGN_MEMBERSHIP_HEADING_INPUT, text)

    def enter_dedup_timer(self, value):
        self.enter_text(self.DEDUP_TIMER_INPUT, str(value))

    def ensure_secondary_flow_toggles_on(self):
        """Toggle ON the second batch of Flow/Appearance switches (KSK-FLW-009)."""
        for locator in (
            self.ENABLE_LOG_WRITE_TOGGLE,
            self.USE_SOFTWARE_KEYBOARD_TOGGLE,
            self.HIDE_HELP_BUTTON_TOGGLE,
            self.ENABLE_DC_DIRECT_TIP_TOGGLE,
            self.ENABLE_AUTO_NAVIGATE_TOGGLE,
            self.ACCEPT_CASH_WITHOUT_ACCEPTOR_TOGGLE,
        ):
            try:
                toggle = self.wait.until(EC.element_to_be_clickable(locator))
                if toggle.get_attribute("aria-checked") != "true":
                    self.driver.execute_script("arguments[0].click();", toggle)
            except Exception:
                pass

    def get_all_flow_toggle_states(self):
        toggles = self.driver.find_elements(By.XPATH, "//button[@role='switch']")
        result = {}
        for t in toggles:
            label = (
                t.get_attribute("aria-label")
                or t.get_attribute("name")
                or t.get_attribute("id")
                or ""
            )
            if label:
                result[label] = t.get_attribute("aria-checked") == "true"
        return result

    # ── Localization Settings ─────────────────────────────────────────────────

    def ensure_use_external_translations_on(self):
        toggle = self.wait.until(
            EC.element_to_be_clickable(self.USE_EXTERNAL_TRANSLATIONS_TOGGLE)
        )
        if toggle.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.USE_EXTERNAL_TRANSLATIONS_TOGGLE)
                .get_attribute("aria-checked") == "true"
            )

    def ensure_use_external_translations_off(self):
        toggle = self.wait.until(
            EC.element_to_be_clickable(self.USE_EXTERNAL_TRANSLATIONS_TOGGLE)
        )
        if toggle.get_attribute("aria-checked") != "false":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.USE_EXTERNAL_TRANSLATIONS_TOGGLE)
                .get_attribute("aria-checked") == "false"
            )

    def enter_translation_url(self, url):
        self.enter_text(self.TRANSLATION_URL_INPUT, url)

    # ── Fleet Settings ────────────────────────────────────────────────────────

    def select_fleet_capabilities(self, option):
        self.select_react_dropdown_option(self.FLEET_CAPABILITIES_DROPDOWN, option)

    def enter_fleet_manager_url(self, url):
        self.enter_text(self.FLEET_MANAGER_URL_INPUT, url)

    def ensure_call_attendant_on(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.CALL_ATTENDANT_TOGGLE))
        if toggle.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.CALL_ATTENDANT_TOGGLE)
                .get_attribute("aria-checked") == "true"
            )

    def ensure_call_attendant_off(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.CALL_ATTENDANT_TOGGLE))
        if toggle.get_attribute("aria-checked") != "false":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.CALL_ATTENDANT_TOGGLE)
                .get_attribute("aria-checked") == "false"
            )

    def ensure_fleet_toggle_on(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.FLEET_TOGGLE))
        if toggle.get_attribute("aria-checked") != "true":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.FLEET_TOGGLE)
                .get_attribute("aria-checked") == "true"
            )

    def ensure_fleet_toggle_off(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.FLEET_TOGGLE))
        if toggle.get_attribute("aria-checked") != "false":
            self.driver.execute_script("arguments[0].click();", toggle)
            self.wait.until(
                lambda d: d.find_element(*self.FLEET_TOGGLE)
                .get_attribute("aria-checked") == "false"
            )

    # ── Active/Connection ─────────────────────────────────────────────────────

    def kiosk_is_connected(self):
        body = self.get_body_text().lower()
        return "connected" in body

    def check_regen_code_button_visible(self):
        els = self.driver.find_elements(*self.CHECK_REGEN_CODE_BUTTON)
        return any(e.is_displayed() for e in els)

    # ── Connection Code Modal ─────────────────────────────────────────────────

    def click_generate_connection_code(self):
        # Button is inside KSK_CREATE_FRAME alongside the form fields (same as Save/Cancel).
        el = self.wait.until(EC.element_to_be_clickable(self.GENERATE_CONNECTION_CODE_BTN))
        self.driver.execute_script("arguments[0].click();", el)
        try:
            self.wait.until(EC.visibility_of_element_located(self.CODE_MODAL_CONTAINER))
        except TimeoutException:
            pass

    def click_close_code_modal(self):
        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.CODE_MODAL_CLOSE_BTN)
            )
            self.driver.execute_script("arguments[0].click();", el)
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.CODE_MODAL_CLOSE_BTN)
            )
        except Exception:
            pass

    def get_connection_code(self):
        el = self.wait.until(EC.visibility_of_element_located(self.CODE_MODAL_MANUAL_VALUE))
        return el.text.strip()

    def click_connection_code_value(self):
        el = self.wait.until(EC.element_to_be_clickable(self.CODE_MODAL_MANUAL_VALUE))
        self.driver.execute_script("arguments[0].click();", el)
