import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class LaborShiftsPage(BasePage):
    """Page object for /reports/detailed/employee_labor (Labor & Shifts report).

    Phase 1: blocking filter modal auto-opens on load — site multiselect (no
    default, no 'All Sites' option), date preset (7 options incl. Custom),
    date range input, single-day checkbox, Apply filters button.

    Phase 2 widget stack (vertical, in order):
    1. Labor (%) KPI card
    2. Cost Per Car ($) KPI card
    3. Productivity (cars/hr) KPI card
    4. Employees summary card (Total / Active / Inactive + Total hours)
    5. Employee table     — searchable by name, Status filter, paginated
    6. Commission Details block:
       a. 4 commission cards (Membership Sales, Retail Sales, Washbook Sales,
          Total Commission)
       b. Commission Transactions table — searchable by employee, paginated

    No chart, no tabs, no export button.
    """

    # TODO: Confirm iframe src pattern via DevTools before first run.
    _FRAME_SRC_PATTERNS = [
        "employee_labor", "employee-labor", "labor_shifts", "labor-shifts",
    ]

    # ── Filter modal / bar controls ───────────────────────────────────────────
    # TODO: Confirm exact button text and element via DevTools.

    APPLY_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters'] | "
        "//button[contains(normalize-space(),'Apply filters')]")

    # Site multiselect — same portal as CDL; follows overview__site-select__ prefix.
    # TODO: Confirm CSS class prefix via DevTools. Generic fallback uses __control + writable input.
    SITE_MULTISELECT = (By.XPATH,
        "//div[contains(@class,'overview__site-select__control')] | "
        "//div[contains(@class,'nxt-multi-select__control')] | "
        "//div[contains(@class,'__control') and "
        ".//input[not(@aria-readonly='true') and not(@inputmode='none') and not(@type='hidden')]]")

    SITE_INPUT = (By.XPATH,
        "//input[contains(@class,'overview__site-select__input')] | "
        "//input[contains(@class,'nxt-multi-select__input')]")

    # Date preset: readonly combobox (inputmode='none' or aria-readonly='true').
    DATE_PRESET_COMBOBOX = (By.XPATH,
        "//input[@inputmode='none' and @role='combobox']"
        "/ancestor::div[contains(@class,'-control')][1] | "
        "//div[./div/input[@aria-readonly='true'][@role='combobox']]")

    # LAB exposes 7 date presets (Today … Last month + Custom).
    DATE_RANGE_INPUT = (By.XPATH,
        "//input[@placeholder='Select range of dates'] | "
        "//input[@placeholder='Select date range']")

    # TODO: Confirm class for single-day checkbox via DevTools.
    MODAL_SINGLE_DAY_CHECKBOX = (By.CSS_SELECTOR,
        "input.header-widget__title__descr_checkbox")

    # ── Site chips ────────────────────────────────────────────────────────────

    SITE_CHIPS = (By.XPATH,
        "//div[contains(@class,'overview__site-select__multi-value__label')] | "
        "//div[contains(@class,'nxt-multi-select__multi-value__label')]")

    SITE_CHIP_REMOVE = (By.XPATH,
        "//div[contains(@class,'overview__site-select__multi-value__remove')] | "
        "//div[contains(@class,'nxt-multi-select__multi-value__remove')]")

    SITE_CLEAR_BTN = (By.XPATH,
        "//div[contains(@class,'overview__site-select__clear-indicator')] | "
        "//div[contains(@class,'nxt-multi-select__clear-indicator')]")

    SITE_OVERFLOW_CHIP = (By.XPATH,
        "//div[contains(@class,'overview__site-select__multi-value__least-count')] | "
        "//div[contains(@class,'nxt-multi-select__multi-value__least-count')]")

    # ── Page-bar single-day checkbox (post-apply) ─────────────────────────────
    # TODO: Confirm class and ancestor distinction from modal checkbox via DevTools.
    PAGE_BAR_SINGLE_DAY_CHECKBOX = (By.XPATH,
        "//input[contains(@class,'header-widget__title__descr_checkbox')]"
        "[not(ancestor::*[@role='dialog'])]")

    # ── Load mask / spinner ───────────────────────────────────────────────────

    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and "
        "not(contains(@style,'display: none') or contains(@style,'display:none'))] | "
        "//*[contains(@class,'spinner') and "
        "not(contains(@style,'display: none') or contains(@style,'display:none'))]")

    # ── No-data indicators ────────────────────────────────────────────────────

    NO_DATA_MESSAGE = (By.XPATH,
        "//*[contains(normalize-space(),'No data') or "
        "contains(normalize-space(),'no data') or "
        "contains(normalize-space(),'No records') or "
        "contains(normalize-space(),'No information') or "
        "contains(normalize-space(),'out of 0 records') or "
        "contains(normalize-space(),'No results')]")

    # ── Employee table ─────────────────────────────────────────────────────────
    # TODO: Confirm table container class and column order via DevTools on first run.
    EMPLOYEE_TABLE = (By.XPATH,
        "//table[.//th[contains(normalize-space(),'Hours Worked') or "
        "contains(normalize-space(),'Total shifts')]] | "
        "//*[contains(@class,'employee-table') or contains(@class,'emp-table')]")

    # Employee search — ancestor-excluded to avoid matching the CTX search box.
    # TODO: Confirm placeholder text and ancestor exclusion xpath via DevTools.
    EMPLOYEE_SEARCH = (By.XPATH,
        "(//input[@type='search' or contains(@placeholder,'Search') or "
        "contains(@placeholder,'employee') or contains(@placeholder,'name')])"
        "[not(ancestor::*[contains(@class,'commission') or "
        "contains(normalize-space(),'Commission Transaction')])]"
        "[1]")

    # Employee status filter dropdown (All / Active / Inactive).
    # TODO: Confirm element type (HTML <select> vs React Select) via DevTools.
    EMPLOYEE_STATUS_FILTER = (By.XPATH,
        "//select[option[normalize-space()='Active'] and "
        "option[normalize-space()='Inactive']] | "
        "(//*[@role='combobox']"
        "[not(ancestor::*[contains(@class,'commission')])])[last()]")

    EMPLOYEE_TABLE_ROWS = (By.XPATH,
        "(//table[.//th[contains(normalize-space(),'Hours Worked') or "
        "contains(normalize-space(),'Total shifts')]]//tbody/tr)")

    # ── Employees summary card ─────────────────────────────────────────────────
    # TODO: Confirm container class and exact label text via DevTools.
    EMPLOYEES_SUMMARY_CARD = (By.XPATH,
        "//*[(contains(normalize-space(),'Total') and "
        "contains(normalize-space(),'Active') and "
        "contains(normalize-space(),'Inactive'))] | "
        "//*[contains(@class,'employee') and "
        "(contains(@class,'card') or contains(@class,'summary'))]")

    # ── Commission section ─────────────────────────────────────────────────────
    # TODO: Confirm section heading text via DevTools.
    COMMISSION_SECTION_HEADING = (By.XPATH,
        "//*[contains(normalize-space(),'Commission Details') or "
        "contains(normalize-space(),'Commission Summary')]"
        "[not(self::td or self::th)]")

    # ── Commission Transactions table ──────────────────────────────────────────
    # TODO: Confirm table container class via DevTools on first run.
    CTX_TABLE = (By.XPATH,
        "//table[.//th[contains(normalize-space(),'Commission Amount') or "
        "contains(normalize-space(),'License plate')]]")

    # Commission Transactions search — scoped to commission ancestor.
    # TODO: Confirm placeholder and ancestor scope via DevTools.
    CTX_SEARCH = (By.XPATH,
        "(//input[@type='search' or contains(@placeholder,'Search') or "
        "contains(@placeholder,'employee')])"
        "[ancestor::*[contains(@class,'commission') or "
        "contains(normalize-space(),'Commission Transaction')]]"
        "[1]")

    CTX_TABLE_ROWS = (By.XPATH,
        "//table[.//th[contains(normalize-space(),'Commission Amount') or "
        "contains(normalize-space(),'License plate')]]"
        "//tbody/tr")

    # ── Frame helpers ─────────────────────────────────────────────────────────

    def _switch_to_frame(self):
        self.driver.switch_to.default_content()
        time.sleep(0.3)
        apply_btns = self.driver.find_elements(By.XPATH,
            "//button[contains(normalize-space(),'Apply filters')]")
        if any(b.is_displayed() for b in apply_btns):
            return
        for pattern in self._FRAME_SRC_PATTERNS:
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.XPATH, "//iframe[contains(@src,'%s')]" % pattern)
                    )
                )
                apply_btns = self.driver.find_elements(By.XPATH,
                    "//button[contains(normalize-space(),'Apply filters')]")
                if any(b.is_displayed() for b in apply_btns):
                    return
                self.driver.switch_to.default_content()
            except TimeoutException:
                pass

    # ── Page lifecycle ────────────────────────────────────────────────────────

    def wait_for_modal(self):
        """Wait for the blocking filter modal (Apply button) to be clickable."""
        self._switch_to_frame()
        try:
            self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON))
        except TimeoutException:
            try:
                self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
            except TimeoutException:
                pass
        try:
            self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        except TimeoutException:
            pass

    def modal_is_open(self):
        """Return True if the blocking filter modal (Apply button) is visible.

        Retries briefly because React may re-render the button once after load.
        """
        for _ in range(4):
            try:
                els = self.driver.find_elements(*self.APPLY_BUTTON)
                if any(e.is_displayed() for e in els):
                    return True
            except Exception:
                pass
            time.sleep(0.4)
        return False

    def get_body_text(self):
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except Exception:
            self.driver.switch_to.default_content()
            return self.driver.find_element(By.TAG_NAME, "body").text

    def get_current_url(self):
        return self.driver.current_url

    # ── Site filter ───────────────────────────────────────────────────────────

    def get_site_options(self):
        """Open the site dropdown and return visible option texts via JS."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
        except TimeoutException:
            pass
        self.driver.execute_script("""
            var ctrl = document.querySelector('.overview__site-select__control')
                    || document.querySelector('.nxt-multi-select__control')
                    || (function() {
                           var ctrls = document.querySelectorAll('div[class*="__control"]');
                           for (var i = 0; i < ctrls.length; i++) {
                               var inp = ctrls[i].querySelector('input');
                               if (inp && inp.getAttribute('aria-readonly') !== 'true'
                                       && inp.getAttribute('inputmode') !== 'none'
                                       && ctrls[i].offsetParent !== null) return ctrls[i];
                           }
                           return null;
                       })();
            if (ctrl) {
                ctrl.dispatchEvent(new MouseEvent('mousedown', {
                    bubbles: true, cancelable: true, view: window
                }));
            }
        """)
        time.sleep(0.5)
        try:
            WebDriverWait(self.driver, 8).until(
                lambda d: d.execute_script(
                    "return document.querySelectorAll('[role=\"option\"]').length > 0;"
                )
            )
        except TimeoutException:
            pass
        options = self.driver.execute_script("""
            return Array.from(document.querySelectorAll('[role="option"]'))
                .filter(function(el) { return el.textContent.trim(); })
                .map(function(el) { return el.textContent.trim(); });
        """)
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options or []

    def _open_site_multiselect(self):
        """Open the site multiselect dropdown via JS (avoids holding stale element refs)."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
        except TimeoutException:
            pass  # element may still be in DOM; proceed with JS approach
        self.driver.execute_script("""
            var ctrl = document.querySelector('.overview__site-select__control')
                    || document.querySelector('.nxt-multi-select__control')
                    || (function() {
                           var ctrls = document.querySelectorAll('div[class*="__control"]');
                           for (var i = 0; i < ctrls.length; i++) {
                               var inp = ctrls[i].querySelector('input');
                               if (inp && inp.getAttribute('aria-readonly') !== 'true'
                                       && inp.getAttribute('inputmode') !== 'none'
                                       && ctrls[i].offsetParent !== null) return ctrls[i];
                           }
                           return null;
                       })();
            if (ctrl) {
                ctrl.dispatchEvent(new MouseEvent('mousedown', {
                    bubbles: true, cancelable: true, view: window
                }));
            }
        """)
        time.sleep(0.4)

    def _get_site_input(self):
        """Wait up to 5s for the visible site multiselect search input to appear."""
        js = """
            var selectors = ['.overview__site-select__input', '.nxt-multi-select__input'];
            for (var i = 0; i < selectors.length; i++) {
                var el = document.querySelector(selectors[i]);
                if (el && el.type !== 'hidden' && el.offsetParent !== null) return el;
            }
            // Generic fallback: writable input inside any React Select control div
            var ctrls = document.querySelectorAll('div[class*="__control"]');
            for (var j = 0; j < ctrls.length; j++) {
                var inp = ctrls[j].querySelector('input');
                if (inp && inp.type !== 'hidden' && inp.offsetParent !== null
                        && inp.getAttribute('aria-readonly') !== 'true'
                        && inp.getAttribute('inputmode') !== 'none') return inp;
            }
            return null;
        """
        try:
            return WebDriverWait(self.driver, 5).until(
                lambda d: d.execute_script(js)
            )
        except TimeoutException:
            return None

    def select_site(self, site_name, clear_first=True):
        """Select *site_name* from the site multiselect by typing to filter."""
        self._open_site_multiselect()
        # Get a fresh input reference AFTER re-render (avoids StaleElementReferenceException)
        inner = self._get_site_input()
        if inner is None:
            try:
                inner = self.driver.find_element(By.XPATH,
                    "//input[not(@type='hidden') and "
                    "(contains(@class,'site-select__input') or "
                    "contains(@class,'nxt-multi-select__input'))]")
            except Exception:
                inner = self.driver.find_element(*self.SITE_MULTISELECT)
        if clear_first:
            inner.send_keys(Keys.COMMAND + "a")
            inner.send_keys(Keys.BACKSPACE)
            time.sleep(0.1)
        inner.send_keys(site_name)
        time.sleep(0.3)
        # Find and click in a single atomic JS call to avoid stale reference between
        # the two separate operations (_find_react_option then execute_script click).
        _CLICK_JS = """
            var text = arguments[0].toLowerCase();
            var option = Array.from(document.querySelectorAll('[role="option"]'))
                .find(function(el) {
                    return el.offsetParent !== null
                        && el.textContent.trim().toLowerCase() === text;
                });
            if (option) { option.click(); return true; }
            return false;
        """
        WebDriverWait(self.driver, 20).until(
            lambda d: d.execute_script(_CLICK_JS, site_name)
        )
        time.sleep(0.3)

    def get_site_chips(self):
        chips = self.driver.find_elements(*self.SITE_CHIPS)
        seen, result = set(), []
        for c in chips:
            try:
                if not c.is_displayed():
                    continue
                text = c.text.strip()
                if text and text not in seen:
                    seen.add(text)
                    result.append(text)
            except Exception:
                pass
        return result

    def site_overflow_chip_visible(self):
        """Return True if the +N overflow chip is visible in the site multiselect."""
        els = self.driver.find_elements(*self.SITE_OVERFLOW_CHIP)
        return any(e.is_displayed() for e in els)

    def get_overflow_chip_text(self):
        """Return the overflow chip text (e.g. '+3') or '' if not present."""
        els = self.driver.find_elements(*self.SITE_OVERFLOW_CHIP)
        for el in els:
            if el.is_displayed():
                return el.text.strip()
        return ""

    def clear_sites(self):
        """Remove all selected site chips via the clear-all indicator."""
        try:
            controls = self.driver.find_elements(*self.SITE_MULTISELECT)
            if controls:
                ActionChains(self.driver).move_to_element(controls[0]).perform()
                time.sleep(0.3)
            btn = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(self.SITE_CLEAR_BTN)
            )
            ActionChains(self.driver).move_to_element(btn).click(btn).perform()
            time.sleep(0.5)
            return
        except TimeoutException:
            pass
        for _ in range(30):
            remove_btns = self.driver.find_elements(*self.SITE_CHIP_REMOVE)
            visible = [b for b in remove_btns if b.is_displayed()]
            if not visible:
                break
            try:
                self.driver.execute_script("arguments[0].click();", visible[0])
                time.sleep(0.2)
            except Exception:
                break

    # ── Date filter ───────────────────────────────────────────────────────────

    def _open_date_preset_dropdown(self):
        """Open the date preset combobox via JS events + Selenium click fallback."""
        js_opened = self.driver.execute_script("""
            // Try multiple selectors for the readonly date combobox input
            var input = document.querySelector('input[aria-readonly="true"][role="combobox"]')
                     || document.querySelector('input[inputmode="none"][role="combobox"]')
                     || document.querySelector('input[readonly][role="combobox"]')
                     || (function() {
                            var ctrls = document.querySelectorAll('div[class*="__control"]');
                            for (var i = 0; i < ctrls.length; i++) {
                                var inp = ctrls[i].querySelector('input');
                                if (inp && (inp.getAttribute('aria-readonly') === 'true'
                                         || inp.getAttribute('inputmode') === 'none'
                                         || inp.readOnly)
                                        && ctrls[i].offsetParent !== null) return inp;
                            }
                            return null;
                        })();
            if (!input) return false;
            var el = input.parentElement;
            while (el && !el.className.includes('-control')) {
                el = el.parentElement;
            }
            if (el) {
                el.dispatchEvent(new MouseEvent('mousedown', {
                    bubbles: true, cancelable: true, view: window
                }));
                el.dispatchEvent(new MouseEvent('click', {
                    bubbles: true, cancelable: true, view: window
                }));
                return true;
            }
            return false;
        """)
        if not js_opened:
            # Selenium click fallback when JS can't find the control
            try:
                el = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(self.DATE_PRESET_COMBOBOX)
                )
                el.click()
            except Exception:
                pass
        time.sleep(0.6)

    def select_date_preset(self, preset):
        """Select a named preset from the date preset combobox."""
        self._open_date_preset_dropdown()
        # Atomic find-and-click. Use startsWith to handle options that show a date
        # suffix (e.g. "Today 07/14/2026", "This month July 2026") when no site is selected.
        _CLICK_PRESET_JS = """
            var text = arguments[0].toLowerCase();
            var option = Array.from(document.querySelectorAll(
                '[role="option"], [class*="-option"], [class*="__option"]'
            )).find(function(el) {
                var t = el.textContent.trim().toLowerCase();
                return el.offsetParent !== null
                    && (t === text || t.startsWith(text));
            });
            if (option) { option.click(); return true; }
            return false;
        """
        WebDriverWait(self.driver, 20).until(
            lambda d: d.execute_script(_CLICK_PRESET_JS, preset)
        )
        time.sleep(0.3)

    def get_date_preset_options(self):
        """Open the date preset dropdown and return visible preset name texts.

        Some deployments append a date hint (e.g. 'Today 07/14/2026') to option
        labels when no site is pre-selected.  We return only the first line /
        word-group before any date suffix so callers can do simple string checks.
        """
        self._open_date_preset_dropdown()
        # Wait for at least one option to appear before reading
        try:
            WebDriverWait(self.driver, 8).until(
                lambda d: d.execute_script(
                    "return document.querySelectorAll("
                    "  '[role=\"option\"], [class*=\"-option\"], [class*=\"__option\"]'"
                    ").length > 0;"
                )
            )
        except TimeoutException:
            pass
        options = self.driver.execute_script("""
            return Array.from(document.querySelectorAll(
                '[role="option"], [class*="-option"], [class*="__option"]'
            )).filter(function(el) {
                return el.offsetParent !== null && el.textContent.trim();
            }).map(function(el) {
                // Strip trailing date hints (e.g. "Today 07/14/2026" → "Today")
                var raw = el.textContent.trim();
                // Take text up to the first date-like pattern or newline
                var cleaned = raw.split('\\n')[0].trim();
                var m = cleaned.match(/^([A-Za-z][A-Za-z ]*?)\s+\d{2}\/\d{2}\/\d{4}/);
                if (m) cleaned = m[1].trim();
                return cleaned;
            });
        """)
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options or []

    def get_date_range_value(self):
        try:
            el = self.driver.find_element(*self.DATE_RANGE_INPUT)
            return el.get_attribute("value") or ""
        except Exception:
            return ""

    def date_range_input_placeholder(self):
        try:
            el = self.driver.find_element(*self.DATE_RANGE_INPUT)
            return el.get_attribute("placeholder") or ""
        except Exception:
            return ""

    def click_date_range_input(self):
        """Click the date range input to open the calendar picker."""
        try:
            el = self.wait.until(EC.element_to_be_clickable(self.DATE_RANGE_INPUT))
            self.driver.execute_script("arguments[0].click();", el)
            time.sleep(0.5)
        except TimeoutException:
            pass

    def calendar_picker_visible(self):
        """Return True if a calendar widget is visible after clicking the date field."""
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'calendar') or contains(@class,'datepicker') or "
            "contains(@class,'DayPicker') or contains(@class,'react-calendar') or "
            "(@role='grid' and not(contains(@class,'data')))]"
            "[not(contains(@style,'display: none') or contains(@style,'display:none'))]")
        return any(el.is_displayed() for el in els)

    def enter_date_range(self, start, end):
        """Type a custom date range into the date range input.

        LAB uses a typeable date input (unlike CDL which is readonly).
        TODO: Confirm via DevTools whether direct typing is accepted.
        """
        try:
            el = self.wait.until(EC.element_to_be_clickable(self.DATE_RANGE_INPUT))
            el.send_keys(Keys.COMMAND + "a")
            el.send_keys(Keys.BACKSPACE)
            el.send_keys(start)
            time.sleep(0.3)
            el.send_keys(Keys.TAB)
            time.sleep(0.3)
            el.send_keys(end)
            time.sleep(0.5)
        except Exception:
            self.click_date_range_input()

    # ── Single day mode ───────────────────────────────────────────────────────

    def check_modal_single_day(self):
        els = self.driver.find_elements(*self.MODAL_SINGLE_DAY_CHECKBOX)
        for el in els:
            if el.is_displayed() and not el.is_selected():
                try:
                    self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(0.3)
                    return
                except Exception:
                    pass

    def uncheck_modal_single_day(self):
        els = self.driver.find_elements(*self.MODAL_SINGLE_DAY_CHECKBOX)
        for el in els:
            if el.is_displayed() and el.is_selected():
                try:
                    self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(0.3)
                    return
                except Exception:
                    pass

    def modal_single_day_is_checked(self):
        els = self.driver.find_elements(*self.MODAL_SINGLE_DAY_CHECKBOX)
        return any(el.is_displayed() and el.is_selected() for el in els)

    def modal_single_day_checkbox_visible(self):
        els = self.driver.find_elements(*self.MODAL_SINGLE_DAY_CHECKBOX)
        return any(el.is_displayed() for el in els)

    def check_page_bar_single_day(self):
        els = self.driver.find_elements(*self.PAGE_BAR_SINGLE_DAY_CHECKBOX)
        for el in els:
            if el.is_displayed() and not el.is_selected():
                try:
                    self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(0.5)
                    return
                except Exception:
                    pass

    def page_bar_single_day_is_checked(self):
        els = self.driver.find_elements(*self.PAGE_BAR_SINGLE_DAY_CHECKBOX)
        return any(el.is_displayed() and el.is_selected() for el in els)

    def page_bar_single_day_checkbox_visible(self):
        els = self.driver.find_elements(*self.PAGE_BAR_SINGLE_DAY_CHECKBOX)
        return any(el.is_displayed() for el in els)

    # ── Apply ─────────────────────────────────────────────────────────────────

    def apply_modal_filters(self):
        """Click Apply filters and wait for the blocking modal to close."""
        try:
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.APPLY_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", btn)
        except TimeoutException:
            pass
        time.sleep(1.5)
        # Wait for modal to close (Apply button disappears)
        def _apply_still_visible(d):
            for e in d.find_elements(*self.APPLY_BUTTON):
                try:
                    if e.is_displayed():
                        return True
                except Exception:
                    pass
            return False

        try:
            WebDriverWait(self.driver, 15).until(lambda d: not _apply_still_visible(d))
        except TimeoutException:
            pass
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.LOAD_MASK)
            )
        except TimeoutException:
            pass

    # ── Generic visibility ────────────────────────────────────────────────────

    def widget_section_visible(self, keyword):
        """Return True if any visible element contains *keyword*."""
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(normalize-space(),'%s')]" % keyword)
        for el in els:
            try:
                if el.is_displayed():
                    return True
            except Exception:
                pass
        return False

    def _text_visible(self, keyword):
        return self.widget_section_visible(keyword)

    # ── KPI cards ─────────────────────────────────────────────────────────────

    def kpi_card_visible(self, label):
        """Return True if a KPI card widget containing *label* is visible."""
        return self._text_visible(label)

    def kpi_values_non_zero(self):
        """Heuristic: at least one non-zero numeric value in the page body."""
        body = self.get_body_text()
        numbers = re.findall(r"\b([1-9]\d*(?:\.\d+)?)\b", body)
        return len(numbers) > 0

    def all_kpis_zero_or_empty(self):
        """Return True if KPI section shows all zeros / empty / no-data state."""
        body = self.get_body_text()
        if self.no_data_message_visible():
            return True
        # Accept any of: 0%, $0.00, 0.00, 0h 0m as zero signals
        zero_patterns = ["0%", "$0.00", "0.00", "0h 0m", "0 h"]
        return any(p in body for p in zero_patterns)

    def kpi_currency_format_ok(self):
        """Return True if at least one $X.XX value exists in the page body."""
        body = self.get_body_text()
        return bool(re.search(r"\$\d+\.\d{2}", body))

    def kpi_percentage_format_ok(self):
        """Return True if at least one X.XX% value exists in the page body."""
        body = self.get_body_text()
        return bool(re.search(r"\d+\.?\d*\s*%", body))

    # ── Employees summary card ────────────────────────────────────────────────

    def employee_summary_visible(self):
        """Return True if the Employees summary card is visible."""
        # Requires 'Total', 'Active' (or 'Inactive'), and hour info to all appear.
        body = self.get_body_text()
        return (
            "Total" in body
            and ("Active" in body or "Inactive" in body)
            and re.search(r"\d+h|\d+\s*hours?", body, re.I) is not None
        )

    def get_employee_summary_count(self, label):
        """Return the integer count next to *label* in the Employees summary card.

        *label* should be 'Total', 'Active', or 'Inactive'.
        Finds the section where all three labels appear together (the Employees summary
        card), avoiding false matches in pagination text ("out of 250 records") or
        column headers ("Total shifts", "Active" status values).
        """
        body = self.get_body_text()
        # Anchor on "Total hours" (unique to Employees summary card) or the
        # "Xh Ym" hours pattern — NOT present in pagination text or commission section.
        # Look backwards from the anchor to find Total / Active / Inactive counts.
        anchor = re.search(r"Total\s*[Hh]ours|\d+\s*h\s+\d+\s*m", body)
        if anchor:
            anchor_idx = anchor.start()
            card_start = max(0, anchor_idx - 400)
            card_text = body[card_start:anchor_idx + 20]
            idx = card_text.find(label)
            if idx != -1:
                snippet = card_text[idx:idx + 60]
                numbers = re.findall(r"\b\d+\b", snippet)
                if numbers:
                    return int(numbers[0])
        return None

    def hours_format_present(self):
        """Return True if a 'Xh Ym' or similar total hours pattern appears."""
        body = self.get_body_text()
        return bool(re.search(r"\d+h\s*\d+m|\d+\s*h\s*\d+\s*m", body))

    # ── Employee table ────────────────────────────────────────────────────────

    def employee_table_visible(self):
        """Return True if the Employee table is present on the page."""
        try:
            els = self.driver.find_elements(*self.EMPLOYEE_TABLE)
            if any(e.is_displayed() for e in els):
                return True
        except Exception:
            pass
        body = self.get_body_text()
        return "Hours Worked" in body or "Total shifts" in body

    def get_employee_table_row_count(self):
        """Return the count of visible data rows in the employee table."""
        try:
            rows = self.driver.find_elements(*self.EMPLOYEE_TABLE_ROWS)
            return sum(1 for r in rows if r.is_displayed())
        except Exception:
            return 0

    def employee_table_empty_state_visible(self):
        """Return True if the employee table shows a zero-records state."""
        body = self.get_body_text().lower()
        return (
            "out of 0 records" in body
            or (self.no_data_message_visible() and self.employee_table_visible())
            or self.get_employee_table_row_count() == 0
        )

    def search_employee_table(self, term):
        """Type *term* into the employee table search input."""
        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.EMPLOYEE_SEARCH)
            )
            el.send_keys(Keys.COMMAND + "a")
            el.send_keys(Keys.BACKSPACE)
            el.send_keys(term)
            time.sleep(1.0)
        except TimeoutException:
            pass

    def clear_employee_search(self):
        """Clear the employee table search box (Cmd+A → Backspace)."""
        try:
            el = self.driver.find_element(*self.EMPLOYEE_SEARCH)
            if el.is_displayed():
                el.send_keys(Keys.COMMAND + "a")
                el.send_keys(Keys.BACKSPACE)
                time.sleep(0.5)
        except Exception:
            pass

    def get_employee_row_status_values(self):
        """Return Status cell text from all visible employee table rows.

        TODO: Confirm Status column index via DevTools (expected last column).
        """
        rows = self.driver.find_elements(*self.EMPLOYEE_TABLE_ROWS)
        statuses = []
        for row in rows:
            if not row.is_displayed():
                continue
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells:
                statuses.append(cells[-1].text.strip())
        return statuses

    def select_employee_status_filter(self, status):
        """Select *status* ('All', 'Active', or 'Inactive') from the status dropdown.

        TODO: Confirm element type (HTML <select> vs React Select) via DevTools.
        """
        try:
            from selenium.webdriver.support.select import Select
            el = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.EMPLOYEE_STATUS_FILTER)
            )
            if el.tag_name.lower() == "select":
                Select(el).select_by_visible_text(status)
                time.sleep(1.0)
                return
        except Exception:
            pass
        try:
            self.select_react_dropdown_option(self.EMPLOYEE_STATUS_FILTER, status)
            time.sleep(1.0)
        except Exception:
            pass

    # ── Commission section ────────────────────────────────────────────────────

    def commission_section_visible(self):
        """Return True if the Commission Details section is visible."""
        return (
            self._text_visible("Commission Details")
            or self._text_visible("Commission Summary")
            or (
                self._text_visible("Total Commission")
                and self._text_visible("Membership Sales")
            )
        )

    def commission_subtitle_text(self):
        """Return the Commission Transactions subtitle line from the page body.

        LAB-NAV-008: defect renders 'Commision Transactions' (missing 'm').
        TODO: Confirm exact subtitle element via DevTools.
        """
        body = self.get_body_text()
        for line in body.splitlines():
            stripped = line.strip()
            if "ommis" in stripped.lower() and "transaction" in stripped.lower():
                return stripped
        return ""

    def commission_card_visible(self, label):
        """Return True if a commission card labelled *label* is visible."""
        return self._text_visible(label)

    def get_commission_card_value(self, label):
        """Return the dollar amount text for a commission card named *label*.

        TODO: Tighten to commission card container after DevTools inspection.
        """
        body = self.get_body_text()
        idx = body.find(label)
        if idx == -1:
            return "$0.00"
        snippet = body[idx:idx + 120]
        match = re.search(r"\$[\d,]+\.\d{2}", snippet)
        return match.group(0) if match else "$0.00"

    def commission_cards_all_zero(self):
        """Return True if all 4 commission cards show $0.00."""
        body = self.get_body_text()
        idx = body.find("Membership Sales")
        if idx == -1:
            # Fallback: check if any non-zero currency exists near commission text
            ci = body.lower().find("commission")
            if ci == -1:
                return False
            snippet = body[ci:ci + 500]
        else:
            snippet = body[idx:idx + 500]
        amounts = re.findall(r"\$[\d,]+\.\d{2}", snippet)
        if not amounts:
            return True
        return all(float(a.replace("$", "").replace(",", "")) == 0.0 for a in amounts)

    def commission_card_format_ok(self, label):
        """Return True if the commission card value matches $X.XX format."""
        val = self.get_commission_card_value(label)
        return bool(re.match(r"^\$[\d,]+\.\d{2}$", val))

    # ── Commission Transactions table ─────────────────────────────────────────

    def ctx_table_visible(self):
        """Return True if the Commission Transactions table is visible."""
        try:
            els = self.driver.find_elements(*self.CTX_TABLE)
            if any(e.is_displayed() for e in els):
                return True
        except Exception:
            pass
        return self._text_visible("Commission Amount") and self._text_visible("License plate")

    def get_ctx_table_row_count(self):
        """Return the count of visible data rows in the CTX table."""
        try:
            rows = self.driver.find_elements(*self.CTX_TABLE_ROWS)
            return sum(1 for r in rows if r.is_displayed())
        except Exception:
            return 0

    def ctx_table_empty_state_visible(self):
        """Return True if the CTX table shows a zero-records state."""
        body = self.get_body_text().lower()
        return (
            "out of 0 records" in body
            or (self.no_data_message_visible() and self.ctx_table_visible())
            or self.get_ctx_table_row_count() == 0
        )

    def search_ctx_table(self, term):
        """Type *term* into the Commission Transactions search input."""
        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.CTX_SEARCH)
            )
            el.send_keys(Keys.COMMAND + "a")
            el.send_keys(Keys.BACKSPACE)
            el.send_keys(term)
            time.sleep(1.0)
        except TimeoutException:
            pass

    def clear_ctx_search(self):
        """Clear the Commission Transactions search box (Cmd+A → Backspace)."""
        try:
            el = self.driver.find_element(*self.CTX_SEARCH)
            if el.is_displayed():
                el.send_keys(Keys.COMMAND + "a")
                el.send_keys(Keys.BACKSPACE)
                time.sleep(0.5)
        except Exception:
            pass

    def get_ctx_type_values(self):
        """Return the Type cell text from all visible CTX table rows.

        TODO: Confirm Type column index (0-based) via DevTools.
        """
        rows = self.driver.find_elements(*self.CTX_TABLE_ROWS)
        types = []
        for row in rows:
            if not row.is_displayed():
                continue
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 4:
                types.append(cells[3].text.strip())  # TODO: confirm index
        return types

    def _sum_column(self, rows, col_idx):
        """Sum numeric text in column *col_idx* across *rows*."""
        total = 0.0
        for row in rows:
            if not row.is_displayed():
                continue
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > col_idx:
                text = cells[col_idx].text.strip()
                nums = re.findall(r"\d+\.\d+|\d+", text.replace(",", ""))
                if nums:
                    total += float(nums[0])
        return total

    def _ctx_column_index(self, label):
        """Return the 0-based index of *label* column in the CTX table header."""
        headers = self.driver.find_elements(By.XPATH,
            "(//table[.//th[contains(normalize-space(),'Commission Amount') or "
            "contains(normalize-space(),'License plate')]]//th)")
        for i, h in enumerate(headers):
            if label.lower() in h.text.strip().lower():
                return i
        # Fallback indices for known columns (TODO: confirm via DevTools)
        fallbacks = {
            "commission amount": 7,
            "type": 3,
            "service price": 6,
        }
        return fallbacks.get(label.lower(), 7)

    def sum_transaction_column(self, column_label):
        """Sum all values in *column_label* of the CTX table (all visible rows).

        LAB-CTX-009: used to verify sum == Total Commission card.
        """
        col_idx = self._ctx_column_index(column_label)
        rows = self.driver.find_elements(*self.CTX_TABLE_ROWS)
        return self._sum_column(rows, col_idx)

    def sum_transaction_column_by_type(self, column_label, type_value):
        """Sum *column_label* values for rows where Type matches *type_value*.

        LAB-CSM-005: used to verify Retail Sales card == Retail Sale row sum.
        """
        col_idx  = self._ctx_column_index(column_label)
        type_idx = self._ctx_column_index("type")
        rows = self.driver.find_elements(*self.CTX_TABLE_ROWS)
        total = 0.0
        for row in rows:
            if not row.is_displayed():
                continue
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) <= max(col_idx, type_idx):
                continue
            if type_value.lower() in cells[type_idx].text.strip().lower():
                text = cells[col_idx].text.strip()
                nums = re.findall(r"\d+\.\d+|\d+", text.replace(",", ""))
                if nums:
                    total += float(nums[0])
        return total

    # ── Commission reconciliation chain ───────────────────────────────────────

    def assert_commission_reconciliation(self):
        """Assert the 3-step commission reconciliation chain.

        Step 1 (LAB-CTX-009): sum(Commission Amount column) == Total Commission card
        Step 2 (LAB-CSM-005): Retail Sales card == sum of Retail Sale type rows
        Step 3 (LAB-CSM-004): Membership + Retail + Washbook == Total Commission
            LAB-CSM-004 is Automation=No in the sheet but is trivially assertable
            from card text values; included as a structural check per test plan.

        Call from TestLaborShiftsCommissionCards.test_commission_reconciliation_chain
        after applying a filter with known data (lab_page fixture).
        """
        def _parse(text):
            nums = re.findall(r"\d+\.\d+|\d+", text.replace(",", ""))
            return float(nums[0]) if nums else 0.0

        total_card      = _parse(self.get_commission_card_value("Total Commission"))
        retail_card     = _parse(self.get_commission_card_value("Retail Sales"))
        membership_card = _parse(self.get_commission_card_value("Membership Sales"))
        washbook_card   = _parse(self.get_commission_card_value("Washbook Sales"))

        # Step 3 (LAB-CSM-004): card components sum to total
        card_sum = membership_card + retail_card + washbook_card
        assert abs(card_sum - total_card) < 0.01, (
            "LAB-CSM-004: Membership ($%.2f) + Retail ($%.2f) + Washbook ($%.2f) "
            "= $%.2f != Total Commission card ($%.2f)"
            % (membership_card, retail_card, washbook_card, card_sum, total_card)
        )

        # Step 2 (LAB-CSM-005): Retail card == sum of Retail Sale transaction rows
        retail_row_sum = self.sum_transaction_column_by_type(
            "Commission Amount", "Retail Sale"
        )
        assert abs(retail_row_sum - retail_card) < 0.01, (
            "LAB-CSM-005: Retail Sales card ($%.2f) != sum of Retail Sale "
            "transaction rows ($%.2f)" % (retail_card, retail_row_sum)
        )

        # Step 1 (LAB-CTX-009): transaction column sum == Total Commission card
        tx_sum = self.sum_transaction_column("Commission Amount")
        assert abs(tx_sum - total_card) < 0.01, (
            "LAB-CTX-009: Sum of Commission Amount column ($%.2f) != "
            "Total Commission card ($%.2f)" % (tx_sum, total_card)
        )

    # ── Pagination ────────────────────────────────────────────────────────────

    def assert_pagination_controls(self, table_locator=None):
        """Return True if pagination controls are visible, optionally table-scoped.

        Controls expected: <<, <, >, >>, Page X of Y, Show N, out of Z records.
        TODO: Confirm exact pagination widget class and ancestor structure via DevTools.
        """
        if table_locator is not None:
            try:
                table_el = self.driver.find_element(*table_locator)
                parent = table_el.find_element(By.XPATH, "..")
                if self.pagination_controls_present(context_el=parent):
                    return True
            except Exception:
                pass
        return self.pagination_controls_present()

    # ── No-data helpers ───────────────────────────────────────────────────────

    def no_data_message_visible(self):
        els = self.driver.find_elements(*self.NO_DATA_MESSAGE)
        for el in els:
            try:
                if el.is_displayed():
                    return True
            except Exception:
                pass
        return False

    # ── Sidebar ───────────────────────────────────────────────────────────────

    def sidebar_labor_shifts_active(self):
        """Return True if the sidebar 'Labor & Shifts' link appears active."""
        try:
            return bool(self.driver.execute_script("""
                function isActive(el, depth) {
                    if (!el || depth > 6) return false;
                    var cls = (el.className || '').toString().toLowerCase();
                    var attrs = [].slice.call(el.attributes || [])
                        .map(function(a) { return a.name + '=' + a.value; })
                        .join(' ').toLowerCase();
                    if (cls.match(/activ|select|current/) ||
                        attrs.match(/aria-current|aria-selected|data-active/)) {
                        return true;
                    }
                    return isActive(el.parentElement, depth + 1);
                }
                var links = document.querySelectorAll('a, [role="link"], [role="menuitem"]');
                for (var i = 0; i < links.length; i++) {
                    var t = links[i].textContent.trim().toLowerCase();
                    if (t.includes('labor') || t.includes('shifts')) {
                        if (isActive(links[i], 0)) return true;
                    }
                }
                return false;
            """))
        except Exception:
            return False
