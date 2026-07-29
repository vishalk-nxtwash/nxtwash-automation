import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class RedemptionsPage(BasePage):

    # TODO: Confirm iframe src pattern via DevTools before first run.
    _FRAME_SRC_PATTERNS = [
        "redemption_details", "redemption-details", "redemptions", "redemption"
    ]

    # ── Filter modal controls ─────────────────────────────────────────────────

    APPLY_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters']"
        "[ancestor::*[@role='dialog']]")

    # DevTools confirmed: RDM uses the same overview__site-select__ prefix as CDL.
    SITE_MULTISELECT = (By.XPATH,
        "//div[contains(@class,'overview__site-select__control')]")

    # Inner typeable search input inside the site multiselect.
    SITE_INPUT = (By.XPATH,
        "//input[contains(@class,'overview__site-select__input')]")

    # Date preset control: located via its dummy readonly inner input.
    # The outer control div has no stable named CSS class (Emotion hash).
    DATE_PRESET_COMBOBOX = (By.XPATH,
        "//div[./div/input[@aria-readonly='true'][@role='combobox']]")

    DATE_RANGE_INPUT = (By.XPATH,
        "//input[@placeholder='Select range of dates']")

    # DevTools confirmed class for the Single day checkbox.
    MODAL_SINGLE_DAY_CHECKBOX = (By.CSS_SELECTOR,
        "input.header-widget__title__descr_checkbox")

    # ── Site chips ────────────────────────────────────────────────────────────

    SITE_CHIPS = (By.XPATH,
        "//div[contains(@class,'overview__site-select__multi-value__label')]")

    SITE_CLEAR_BTN = (By.XPATH,
        "//div[contains(@class,'overview__site-select__clear-indicator')]")

    # ── Page-bar single day (persistent filter bar, post-apply) ──────────────
    PAGE_BAR_SINGLE_DAY_CHECKBOX = (By.XPATH,
        "//input[contains(@class,'header-widget__title__descr_checkbox')]"
        "[not(ancestor::*[@role='dialog'])]")

    # ── Expand / Collapse master toggle ──────────────────────────────────────
    # TODO: Confirm element type and class via DevTools.
    EXPAND_ALL_TOGGLE = (By.XPATH,
        "//*[self::button or @role='button']"
        "[contains(normalize-space(),'Expand All') or "
        "contains(normalize-space(),'Collapse All') or "
        "contains(normalize-space(),'Expand all') or "
        "contains(normalize-space(),'Collapse all')]")

    # ── Load mask ─────────────────────────────────────────────────────────────

    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and "
        "not(contains(@style,'display: none') or contains(@style,'display:none'))] | "
        "//*[contains(@class,'spinner') and "
        "not(contains(@style,'display: none') or contains(@style,'display:none'))]")

    NO_DATA_MESSAGE = (By.XPATH,
        "//*[contains(normalize-space(),'No data') or "
        "contains(normalize-space(),'no data') or "
        "contains(normalize-space(),'No records') or "
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
        try:
            frames = self.driver.find_elements(By.TAG_NAME, "iframe")
            if frames:
                self.driver.switch_to.frame(frames[0])
        except Exception:
            pass

    # ── Page lifecycle ────────────────────────────────────────────────────────

    def wait_for_modal(self):
        """Wait for the blocking filter modal (Apply filters button) to be ready."""
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
            try:
                return btn.is_displayed()
            except Exception:
                return False
        except TimeoutException:
            return False

    def apply_modal_filters(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON))
        btn.click()
        self.wait.until(EC.invisibility_of_element_located(self.APPLY_BUTTON))
        try:
            self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        except TimeoutException:
            pass

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
        """Open the site multiselect and return visible option texts.

        Only typing triggers React Select's onInputChange and opens the menu.
        Space is silently trimmed to '' before React sees it (no onInputChange
        fires); ARROW_DOWN's keydown event also does not reach the React handler
        in this iframe context.  'V' matches all known VK-prefixed test sites.
        offsetParent (not is_displayed) is used to detect true DOM visibility.
        """
        inner = self._get_site_inner_input()
        self.driver.execute_script("arguments[0].click();", inner)
        time.sleep(0.3)
        inner = self._get_site_inner_input()
        inner.send_keys("V")
        time.sleep(0.5)
        try:
            WebDriverWait(self.driver, 8).until(
                lambda d: len(d.find_elements(By.XPATH, "//*[@role='option']")) > 0
            )
        except TimeoutException:
            pass
        # Query live DOM inside JS — avoids stale-element errors from holding
        # WebElement references across React's re-render of the option list.
        options = self.driver.execute_script("""
            var els = document.querySelectorAll('[role="option"]');
            var seen = {};
            var result = [];
            Array.from(els).forEach(function(el) {
                if (el.offsetParent !== null) {
                    var text = (el.textContent || '').trim();
                    if (text && !seen[text]) {
                        seen[text] = true;
                        result.push(text);
                    }
                }
            });
            return result;
        """) or []
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options

    def _get_site_inner_input(self):
        """Return the typeable input inside the site multiselect control.

        Retries up to 3 times when EC.element_to_be_clickable internally
        encounters a stale reference (React re-renders between find and
        is_displayed/is_enabled checks inside the predicate).
        """
        from selenium.common.exceptions import StaleElementReferenceException
        for _ in range(3):
            try:
                return self.wait.until(EC.element_to_be_clickable(self.SITE_INPUT))
            except StaleElementReferenceException:
                time.sleep(0.3)
        return self.wait.until(EC.element_to_be_clickable(self.SITE_INPUT))

    def select_site(self, site_name, clear_first=True):
        # JS click is a single atomic round-trip — fires mousedown/mouseup/click
        # events that React Select's delegation picks up to open the menu.
        # Replaces ActionChains (multi-step) which was prone to stale reference
        # when React re-rendered the input between steps.
        inner = self._get_site_inner_input()
        self.driver.execute_script("arguments[0].click();", inner)
        time.sleep(0.3)
        inner = self._get_site_inner_input()
        if clear_first:
            inner.send_keys(Keys.CONTROL + "a")
            inner.send_keys(Keys.BACKSPACE)
        inner.send_keys(site_name)
        time.sleep(0.3)
        option = WebDriverWait(self.driver, 20).until(
            lambda d: self._find_react_option(site_name)
        )
        self.driver.execute_script("arguments[0].click();", option)
        time.sleep(0.3)

    def get_site_chips(self):
        # Scope to the first control div to avoid double-counting chips from
        # multiple React Select instances (modal + page-bar) sharing the same
        # CSS class prefix.  Dedup by text as a further safeguard.
        ctrls = self.driver.find_elements(*self.SITE_MULTISELECT)
        if not ctrls:
            return []
        chips = ctrls[0].find_elements(
            By.XPATH,
            ".//div[contains(@class,'overview__site-select__multi-value__label')]",
        )
        seen = set()
        result = []
        for c in chips:
            try:
                if c.is_displayed():
                    text = c.text.strip()
                    if text and text not in seen:
                        seen.add(text)
                        result.append(text)
            except Exception:
                continue
        return result

    def no_default_site_selected(self):
        return len(self.get_site_chips()) == 0

    def clear_sites(self):
        # React Select's clear indicator fires on onMouseDown, not onClick.
        # JS element.click() only dispatches the 'click' event — the handler
        # never sees it.  Dispatch mousedown explicitly instead.
        try:
            controls = self.driver.find_elements(*self.SITE_MULTISELECT)
            if controls:
                try:
                    ActionChains(self.driver).move_to_element(controls[0]).perform()
                    time.sleep(0.3)
                except Exception:
                    pass
            btn = self.wait.until(EC.element_to_be_clickable(self.SITE_CLEAR_BTN))
            self.driver.execute_script("""
                arguments[0].dispatchEvent(new MouseEvent('mousedown', {
                    bubbles: true, cancelable: true, view: window
                }));
            """, btn)
            time.sleep(0.5)
        except TimeoutException:
            pass

    # ── Date filter ───────────────────────────────────────────────────────────

    def _open_date_preset_dropdown(self):
        """Dispatch mousedown on the date-preset control (dummy readonly input)."""
        self.driver.execute_script("""
            var inp = document.querySelector('input[aria-readonly="true"][role="combobox"]');
            if (inp) {
                var ctrl = inp.parentElement && inp.parentElement.parentElement;
                if (ctrl) {
                    ctrl.dispatchEvent(new MouseEvent('mousedown', {
                        bubbles: true, cancelable: true, view: window
                    }));
                }
            }
        """)
        time.sleep(0.4)

    def select_date_preset(self, preset):
        self._open_date_preset_dropdown()
        try:
            WebDriverWait(self.driver, 8).until(
                lambda d: len(d.find_elements(By.XPATH, "//*[@role='option']")) > 0
            )
        except TimeoutException:
            pass
        for el in self.driver.find_elements(By.XPATH, "//*[@role='option']"):
            try:
                if el.text.strip() == preset:
                    self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(0.3)
                    return
            except Exception:
                continue
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass

    def get_date_preset_options(self):
        self._open_date_preset_dropdown()
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: len(d.find_elements(By.XPATH, "//*[@role='option']")) > 0
            )
        except TimeoutException:
            pass
        option_els = self.driver.find_elements(By.XPATH, "//*[@role='option']")
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
        """Enter a custom date range by typing 'start - end' into the range input.

        TODO: Verify on first live run whether the RDM date range input
        accepts direct keyboard entry (like CSH) or requires calendar
        interaction (like CDL).  Raise NotImplementedError and switch to
        calendar interaction if this method fails.
        """
        combined = "%s - %s" % (start, end)
        el = self.wait.until(EC.element_to_be_clickable(self.DATE_RANGE_INPUT))
        el.send_keys(Keys.CONTROL + "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(combined)
        el.send_keys(Keys.TAB)

    def open_date_range_calendar(self):
        """Click the date range input to open the calendar picker."""
        try:
            el = self.driver.find_element(*self.DATE_RANGE_INPUT)
            self.driver.execute_script("arguments[0].click();", el)
            time.sleep(0.5)
        except Exception:
            pass

    def future_dates_disabled_in_calendar(self):
        """Return True if dates after today are non-clickable in the calendar.

        # Correct: matches Revenue Overview. Differs from Performance Metrics
        # (known defect PFM-DTE-010 where future dates are incorrectly enabled).
        TODO: Tighten day-cell selector after DevTools inspection confirms
        the calendar component class names used in RDM.
        """
        self.open_date_range_calendar()
        time.sleep(0.5)
        result = self.driver.execute_script("""
            var today = new Date();
            today.setHours(0, 0, 0, 0);
            var dayCells = Array.from(document.querySelectorAll(
                '[class*="day"],[class*="date-cell"],[class*="calendar-day"],' +
                '[aria-label][role="button"],[aria-label][role="gridcell"]'
            ));
            var futureCells = dayCells.filter(function(el) {
                var raw = el.getAttribute('aria-label') ||
                          el.getAttribute('data-date') || '';
                var d = new Date(raw);
                return !isNaN(d.getTime()) && d > today;
            });
            if (futureCells.length === 0) return null;
            return futureCells.some(function(el) {
                return (
                    el.classList.contains('disabled') ||
                    el.getAttribute('aria-disabled') === 'true' ||
                    el.hasAttribute('disabled') ||
                    (el.className || '').toLowerCase().includes('disabled')
                );
            });
        """)
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return result

    # ── Single day ────────────────────────────────────────────────────────────

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

    # ── Page-level summary cards ──────────────────────────────────────────────

    def summary_card_visible(self, label):
        """Return True if a page-level summary card labelled *label* is visible."""
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(normalize-space(),'%s')]" % label
        )
        for el in els:
            try:
                if el.is_displayed():
                    return True
            except Exception:
                continue
        return False

    def get_summary_card_value(self, label):
        """Return the value text of the summary card for *label* (heuristic)."""
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(normalize-space(),'%s')]" % label
        )
        for el in els:
            if not el.is_displayed():
                continue
            parent_text = ""
            try:
                parent_text = el.find_element(By.XPATH, "parent::*").text.strip()
            except Exception:
                pass
            if parent_text and parent_text != label:
                return parent_text
        return ""

    def summary_card_value_is_currency(self, label):
        """Return True if the summary card value contains a $ or numeric pattern."""
        val = self.get_summary_card_value(label)
        return bool(re.search(r"[\$\d,\.]+", val))

    # ── Expand / Collapse ─────────────────────────────────────────────────────

    def expand_collapse_control_text(self):
        """Return the current text of the Expand All / Collapse All toggle."""
        try:
            el = self.driver.find_element(*self.EXPAND_ALL_TOGGLE)
            return el.text.strip()
        except Exception:
            return ""

    def expand_all(self):
        """Click Expand All; if already showing Collapse All, click it first then re-expand."""
        current = self.expand_collapse_control_text().lower()
        if "collapse" in current:
            try:
                self.driver.find_element(*self.EXPAND_ALL_TOGGLE).click()
                time.sleep(0.5)
            except Exception:
                pass
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.EXPAND_ALL_TOGGLE)
            )
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.8)
        except TimeoutException:
            pass

    def collapse_all(self):
        """Click Collapse All; if showing Expand All, expand first then collapse."""
        current = self.expand_collapse_control_text().lower()
        if "expand" in current:
            try:
                self.driver.find_element(*self.EXPAND_ALL_TOGGLE).click()
                time.sleep(0.5)
            except Exception:
                pass
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.EXPAND_ALL_TOGGLE)
            )
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.8)
        except TimeoutException:
            pass

    # ── Accordion section helpers ─────────────────────────────────────────────

    def _section_header_els(self, section_name):
        """Return clickable header elements associated with *section_name*."""
        return self.driver.find_elements(By.XPATH,
            "//*[contains(normalize-space(),'%s')]"
            "[@role='button' or @tabindex or "
            "contains(@class,'header') or contains(@class,'title') or "
            "contains(@class,'trigger') or contains(@class,'accordion')]"
            % section_name
        )

    def section_visible(self, section_name):
        """Return True if any element containing *section_name* text is displayed."""
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(normalize-space(),'%s')]" % section_name
        )
        for el in els:
            try:
                if el.is_displayed():
                    return True
            except Exception:
                continue
        return False

    def section_body_visible(self, section_name):
        """Return True if the accordion body for *section_name* appears expanded.

        Checks aria-expanded attribute and whether child content beyond the
        header title itself is visible.
        TODO: Tighten after DevTools inspection of the accordion DOM structure.
        """
        headers = self._section_header_els(section_name)
        for h in headers:
            if h.get_attribute("aria-expanded") == "true":
                return True
        # Heuristic: find a parent container and look for visible body content
        containers = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'accordion') or contains(@class,'collapse') or "
            "contains(@class,'panel') or contains(@class,'section')]"
            "[.//*[contains(normalize-space(),'%s')]]" % section_name
        )
        for c in containers:
            aria = c.get_attribute("aria-expanded")
            if aria == "true":
                return True
            # If the container has child tables or summary cards, body is open
            children = c.find_elements(By.XPATH,
                ".//table | .//*[contains(@class,'summary') or "
                "contains(@class,'card') or contains(@class,'breakdown')]"
            )
            if any(ch.is_displayed() for ch in children):
                return True
        return False

    def section_is_expanded(self, section_name):
        return self.section_body_visible(section_name)

    def toggle_section(self, section_name):
        """Click the section header/chevron to expand or collapse *section_name*."""
        headers = self._section_header_els(section_name)
        for h in headers:
            if h.is_displayed():
                try:
                    self.driver.execute_script("arguments[0].click();", h)
                    time.sleep(0.4)
                    return
                except Exception:
                    pass

    # ── Section summary cards ─────────────────────────────────────────────────

    def missing_section_summary_cards(self, section_name, expected_labels):
        """Return list of *expected_labels* not found in the page body text.

        Loyalty expects ["Redemptions", "Avg Per Redemption"].
        All other sections expect ["Redemptions", "Total Net Amount", "Avg Per Redemption"].
        Gift cards uses "Total amount" (not "Total Net Amount").
        """
        body = self.get_body_text()
        return [lbl for lbl in expected_labels if lbl not in body]

    # ── Section breakdown tables ──────────────────────────────────────────────

    def _find_table_by_heading(self, heading_text):
        """Return the <table> element under a heading containing *heading_text*.

        Walks up from the heading at most 5 DOM levels to find a card/section,
        then returns the first <table> in that subtree.  Inherited pattern from
        Cash Report page object.
        """
        headings = self.driver.find_elements(By.XPATH,
            "//h1 | //h2 | //h3 | //h4 | "
            "//*[contains(@class,'title') or contains(@class,'heading') or "
            "contains(@class,'card-header') or contains(@class,'section-header')]"
        )
        for h in headings:
            if heading_text.lower() not in h.text.strip().lower():
                continue
            ancestor = h
            for _ in range(6):
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

    def get_breakdown_columns(self, table_heading):
        """Return visible <th> texts from the breakdown table titled *table_heading*."""
        table = self._find_table_by_heading(table_heading)
        if table is None:
            return []
        headers = table.find_elements(By.XPATH, ".//th")
        return [h.text.strip() for h in headers if h.text.strip()]

    def missing_breakdown_columns(self, table_heading, expected_columns):
        """Return list of *expected_columns* absent from the breakdown table.

        Empty list means all columns are present.
        """
        actual = set(self.get_breakdown_columns(table_heading))
        return [col for col in expected_columns if col not in actual]

    def section_has_data_rows(self, section_name):
        """Return True if any visible tbody rows are present on the page."""
        rows = self.driver.find_elements(By.XPATH, "//tbody/tr")
        return any(r.is_displayed() for r in rows)

    def section_detail_has_pagination(self, section_name):
        """Return True if pagination controls are visible (page-level search).

        Inherits base class pagination_controls_present() — same pattern as
        table_pagination_present() in Cash Report.
        TODO: Scope to section container after DevTools confirms accordion DOM.
        """
        return self.pagination_controls_present()

    def section_detail_has_horizontal_scroll(self, section_name):
        """Return True if any table or its wrapper has a horizontal scrollbar."""
        return bool(self.driver.execute_script("""
            var candidates = Array.from(document.querySelectorAll(
                'table, [class*="table-wrap"], [class*="table-container"],' +
                '[class*="scroll-x"], [style*="overflow-x"]'
            ));
            return candidates.some(function(el) {
                if (el.scrollWidth > el.clientWidth) return true;
                var p = el.parentElement;
                for (var i = 0; i < 4 && p && p !== document.body; i++) {
                    if (p.scrollWidth > p.clientWidth &&
                        getComputedStyle(p).overflowX !== 'hidden') return true;
                    p = p.parentElement;
                }
                return false;
            });
        """))

    def section_has_no_data(self, section_name):
        """Return True if the section shows an empty / zero-data state."""
        if self.no_data_message_visible():
            return True
        body = self.get_body_text().lower()
        return "no data" in body or "no records" in body or "no results" in body

    def no_data_message_visible(self):
        els = self.driver.find_elements(*self.NO_DATA_MESSAGE)
        return any(el.is_displayed() for el in els)

    # ── Sidebar active state ──────────────────────────────────────────────────

    def sidebar_redemptions_active(self):
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'active') or @aria-current='page' or "
            "@aria-current='true' or @aria-selected='true']"
            "[contains(normalize-space(),'Redemption') or "
            "contains(normalize-space(),'redemption') or "
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
                        attrs.match(/aria-current|aria-selected|data-active/))
                        return true;
                    return isActive(el.parentElement, depth + 1);
                }
                var links = document.querySelectorAll('a,[role="link"],[role="menuitem"]');
                for (var i = 0; i < links.length; i++) {
                    var t = links[i].textContent.trim().toLowerCase();
                    if (t.includes('redemption') || t.includes('financial'))
                        if (isActive(links[i], 0)) return true;
                }
                return false;
            """))
        except Exception:
            return False
