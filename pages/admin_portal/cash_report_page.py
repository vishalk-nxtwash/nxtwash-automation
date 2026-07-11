import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class CashReportPage(BasePage):

    # TODO: Confirm iframe src pattern via DevTools before first run.
    # The report shell likely embeds the React app in an iframe whose src
    # contains one of these substrings (longest first).
    _FRAME_SRC_PATTERNS = ["cash-report", "cash_report", "cash"]

    # ── Filter modal controls ─────────────────────────────────────────────────

    APPLY_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters'] | "
        "//button[contains(normalize-space(),'Apply filters')]")

    # nxt-multi-select prefix confirmed on GSR / PFM (July 2026)
    SITE_MULTISELECT = (By.XPATH,
        "//div[contains(@class,'nxt-multi-select__control')]")

    DATE_PRESET_COMBOBOX = (By.XPATH,
        "//div[contains(@class,'nxt-select__control')]"
        "[not(contains(@class,'nxt-multi-select__control'))]")

    DATE_RANGE_INPUT = (By.XPATH, "//input[@placeholder='Select date range']")

    # Single day checkbox inside the filter modal (modal dialog scope).
    # TODO: Tighten ancestor selector to modal after DevTools inspection.
    MODAL_SINGLE_DAY_CHECKBOX = (By.XPATH,
        "//input[@type='checkbox']"
        "[ancestor::*[contains(normalize-space(),'Single') or "
        "contains(normalize-space(),'single')]]")

    # ── Site chips (compact filter bar, shown after apply) ────────────────────

    SITE_CHIPS = (By.XPATH,
        "//div[contains(@class,'nxt-multi-select__multi-value__label')]")

    SITE_CLEAR_BTN = (By.XPATH,
        "//div[contains(@class,'nxt-multi-select__clear-indicator')]")

    # ── Page-bar single day checkbox (persistent filter bar, outside modal) ───
    # TODO: Confirm exact locator via DevTools — the page bar checkbox is
    # a separate DOM element from the modal checkbox.  Currently disambiguated
    # by excluding @role='dialog' ancestors; verify after first live run.
    PAGE_BAR_SINGLE_DAY_CHECKBOX = (By.XPATH,
        "//input[@type='checkbox']"
        "[ancestor::*[contains(normalize-space(),'Single') or "
        "contains(normalize-space(),'single')]]"
        "[not(ancestor::*[@role='dialog'])]")

    # ── Export ────────────────────────────────────────────────────────────────
    # Cash Report uses a direct XLSX button (no export-format modal).
    EXPORT_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Export XLSX')] | "
        "//button[normalize-space()='Export XLSX']")

    # ── Tabs ──────────────────────────────────────────────────────────────────
    # TODO: Confirm element type (button / a / div) via DevTools
    TABS = (By.XPATH,
        "//*[@role='tab'] | "
        "//button[contains(@class,'tab')] | "
        "//a[contains(@class,'tab')]")

    # ── Load mask ─────────────────────────────────────────────────────────────
    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and "
        "not(contains(@style,'display: none') or "
        "contains(@style,'display:none'))] | "
        "//*[contains(@class,'spinner') and "
        "not(contains(@style,'display: none') or "
        "contains(@style,'display:none'))]")

    # ── No-data indicators ────────────────────────────────────────────────────
    NO_DATA_MESSAGE = (By.XPATH,
        "//*[contains(normalize-space(),'No data') or "
        "contains(normalize-space(),'no data') or "
        "contains(normalize-space(),'No records') or "
        "contains(normalize-space(),'No information') or "
        "contains(normalize-space(),'No results')]")

    # ── Frame helpers ─────────────────────────────────────────────────────────

    def _switch_to_frame(self):
        self.driver.switch_to.default_content()
        time.sleep(0.3)
        for pattern in self._FRAME_SRC_PATTERNS:
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.XPATH, "//iframe[contains(@src,'%s')]" % pattern)
                    )
                )
                return
            except TimeoutException:
                pass
        # Fallback: switch to first available iframe
        try:
            frames = self.driver.find_elements(By.TAG_NAME, "iframe")
            if frames:
                self.driver.switch_to.frame(frames[0])
        except Exception:
            pass

    # ── Page lifecycle ────────────────────────────────────────────────────────

    def wait_for_modal(self):
        """Wait for the filter modal (Apply filters button) to be ready."""
        self._switch_to_frame()
        self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON))
        try:
            self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        except TimeoutException:
            pass

    def modal_is_open(self):
        try:
            btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.APPLY_BUTTON)
            )
            return btn.is_displayed()
        except TimeoutException:
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
        """Open the site dropdown and return visible option texts."""
        combo = self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
        try:
            inner = combo.find_element(By.XPATH, ".//input")
            self.driver.execute_script("arguments[0].click();", inner)
            inner.send_keys(" ")
            inner.send_keys(Keys.BACKSPACE)
        except Exception:
            self.driver.execute_script("arguments[0].click();", combo)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(@class,'nxt-multi-select__menu')]")
                )
            )
        except TimeoutException:
            pass
        option_els = self.driver.find_elements(
            By.XPATH, "//*[contains(@class,'nxt-multi-select__option')]"
        )
        options = [
            el.text.strip() for el in option_els
            if el.is_displayed() and el.text.strip()
        ]
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options or []

    def select_site(self, site_name, clear_first=True):
        self.select_react_dropdown_option(
            self.SITE_MULTISELECT, site_name, clear_first=clear_first
        )
        time.sleep(0.3)

    def get_site_chips(self):
        chips = self.driver.find_elements(*self.SITE_CHIPS)
        return [c.text.strip() for c in chips if c.is_displayed() and c.text.strip()]

    def clear_sites(self):
        try:
            controls = self.driver.find_elements(*self.SITE_MULTISELECT)
            if controls:
                ActionChains(self.driver).move_to_element(controls[0]).perform()
                time.sleep(0.3)
            btn = self.wait.until(EC.element_to_be_clickable(self.SITE_CLEAR_BTN))
            ActionChains(self.driver).move_to_element(btn).click(btn).perform()
            time.sleep(0.5)
        except TimeoutException:
            pass

    # ── Date filter ───────────────────────────────────────────────────────────

    def select_date_preset(self, preset):
        self.select_react_dropdown_option(self.DATE_PRESET_COMBOBOX, preset)

    def get_date_preset_options(self):
        """Open the date preset dropdown and return visible option texts."""
        combo = self.wait.until(EC.element_to_be_clickable(self.DATE_PRESET_COMBOBOX))
        try:
            inner = combo.find_element(By.XPATH, ".//input")
            self.driver.execute_script("arguments[0].click();", inner)
            inner.send_keys(" ")
            inner.send_keys(Keys.BACKSPACE)
        except Exception:
            self.driver.execute_script("arguments[0].click();", combo)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(@class,'nxt-select__menu') and "
                     "not(contains(@class,'nxt-multi-select__menu'))]")
                )
            )
        except TimeoutException:
            pass
        option_els = self.driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'nxt-select__option') and "
            "not(contains(@class,'nxt-multi-select__option'))]"
        )
        options = [
            el.text.strip() for el in option_els
            if el.is_displayed() and el.text.strip()
        ]
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

    def enter_date_range(self, start, end):
        combined = "%s - %s" % (start, end)
        el = self.wait.until(EC.element_to_be_clickable(self.DATE_RANGE_INPUT))
        el.send_keys(Keys.COMMAND + "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(combined)
        el.send_keys(Keys.TAB)

    # ── Single day mode ───────────────────────────────────────────────────────

    def check_modal_single_day(self):
        """Check the single day checkbox inside the filter modal."""
        els = self.driver.find_elements(*self.MODAL_SINGLE_DAY_CHECKBOX)
        for el in els:
            if el.is_displayed() and not el.is_selected():
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
        """Check the single day checkbox in the persistent page-level filter bar.

        TODO: Confirm PAGE_BAR_SINGLE_DAY_CHECKBOX locator via DevTools after
        first live run — the current locator excludes dialog ancestors as a
        heuristic but may need a class-based anchor.
        """
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
        """Return True if the page-bar single day checkbox is checked.

        TODO: Same locator caveat as check_page_bar_single_day().
        """
        els = self.driver.find_elements(*self.PAGE_BAR_SINGLE_DAY_CHECKBOX)
        return any(el.is_displayed() and el.is_selected() for el in els)

    def page_bar_single_day_checkbox_visible(self):
        els = self.driver.find_elements(*self.PAGE_BAR_SINGLE_DAY_CHECKBOX)
        return any(el.is_displayed() for el in els)

    # ── Apply ─────────────────────────────────────────────────────────────────

    def apply_modal_filters(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(1.5)
        try:
            self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        except TimeoutException:
            pass

    # ── Tab navigation ────────────────────────────────────────────────────────

    def get_visible_tabs(self):
        """Return text of all currently visible tab elements."""
        tab_els = self.driver.find_elements(*self.TABS)
        return [el.text.strip() for el in tab_els if el.is_displayed() and el.text.strip()]

    def click_tab(self, tab_name):
        """Click a named tab.  Matches case-insensitively."""
        tab_el = WebDriverWait(self.driver, 10).until(
            lambda d: next(
                (el for el in d.find_elements(*self.TABS)
                 if el.is_displayed() and el.text.strip().lower() == tab_name.lower()),
                None
            )
        )
        if tab_el:
            self.driver.execute_script("arguments[0].click();", tab_el)
            time.sleep(0.6)

    def get_active_tab(self):
        """Return the name of the currently active tab, or empty string."""
        for el in self.driver.find_elements(*self.TABS):
            if not el.is_displayed():
                continue
            aria_selected = el.get_attribute("aria-selected") or ""
            cls = (el.get_attribute("class") or "").lower()
            if aria_selected == "true" or "active" in cls or "selected" in cls:
                return el.text.strip()
        return ""

    def tab_content_visible(self, keyword):
        """Return True if *keyword* (case-insensitive) appears in the page body."""
        try:
            return keyword.lower() in self.get_body_text().lower()
        except Exception:
            return False

    # ── Table helpers ─────────────────────────────────────────────────────────

    def _find_table_by_heading(self, section_title):
        """Return the <table> element that follows a heading containing *section_title*.

        Walks up from the heading element at most 5 DOM levels to find a
        containing card/section, then searches that subtree for the first
        <table>.  Returns None if not found.
        """
        headings = self.driver.find_elements(By.XPATH,
            "//h1 | //h2 | //h3 | //h4 | "
            "//*[contains(@class,'title') or contains(@class,'heading') or "
            "contains(@class,'card-header') or contains(@class,'section-header')]"
        )
        for h in headings:
            if section_title.lower() not in h.text.strip().lower():
                continue
            ancestor = h
            for _ in range(5):
                try:
                    ancestor = self.driver.execute_script(
                        "return arguments[0].parentElement;", ancestor
                    )
                    if not ancestor:
                        break
                    tables = ancestor.find_elements(By.XPATH, ".//table")
                    if tables:
                        return tables[0]
                except Exception:
                    break
        return None

    def table_section_visible(self, section_title):
        """Return True if a heading/label matching *section_title* is visible."""
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(normalize-space(),'%s')]" % section_title
        )
        return any(el.is_displayed() for el in els)

    def get_table_headers(self, section_title):
        """Return column header texts for the table under *section_title*."""
        table = self._find_table_by_heading(section_title)
        if table is None:
            return []
        headers = table.find_elements(By.XPATH, ".//th")
        return [h.text.strip() for h in headers if h.text.strip()]

    def get_table_row_count(self, section_title):
        """Return the number of visible data rows under *section_title*."""
        table = self._find_table_by_heading(section_title)
        if table is None:
            return 0
        rows = table.find_elements(By.XPATH, ".//tbody/tr")
        return sum(1 for r in rows if r.is_displayed())

    def table_has_data(self, section_title):
        return self.get_table_row_count(section_title) > 0

    def table_pagination_present(self, section_title):
        """Return True if pagination controls are visible for the given table.

        Uses the base class helper on the full page (table-level scoping is not
        always possible since pagination may be rendered outside the <table> tag).
        TODO: Scope to card container once DOM structure is confirmed via DevTools.
        """
        return self.pagination_controls_present()

    # ── Export ────────────────────────────────────────────────────────────────

    def export_button_visible(self):
        els = self.driver.find_elements(*self.EXPORT_BUTTON)
        return any(el.is_displayed() for el in els)

    def click_export_xlsx(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.EXPORT_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(1.0)

    # ── No-data ───────────────────────────────────────────────────────────────

    def no_data_message_visible(self):
        els = self.driver.find_elements(*self.NO_DATA_MESSAGE)
        return any(el.is_displayed() for el in els)

    # ── Sidebar active state ──────────────────────────────────────────────────

    def sidebar_cash_report_active(self):
        """Return True if the FINANCIAL / Cash Report sidebar link appears active.

        Uses the same JS DOM-walk fallback pattern as PFM.  Known limitation:
        the sidebar uses Tailwind visual styling with no detectable aria-current
        or active-class attribute (see PFM-NAV-007 for precedent).
        """
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'active') or @aria-current='page' or "
            "@aria-current='true' or @aria-selected='true']"
            "[contains(normalize-space(),'Cash') or "
            "contains(normalize-space(),'cash') or "
            "contains(normalize-space(),'Financial')]"
        )
        if any(el.is_displayed() for el in els):
            return True
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
                    if (t.includes('cash') || t.includes('financial')) {
                        if (isActive(links[i], 0)) return true;
                    }
                }
                return false;
            """))
        except Exception:
            return False
