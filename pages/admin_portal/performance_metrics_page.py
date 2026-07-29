"""Page Object for the Performance Metrics module.

Two-phase flow (identical pattern to Revenue Overview):
  Phase 1 — Filter modal (blocking, auto-opens on load):
    site multiselect, predefined date preset (6 options, no Custom),
    custom date range field, Apply filters button.
    No Single day checkbox.
  Phase 2 — Metrics screen:
    Conversion Rate line chart widget + Membership History table widget.
    Page-level filter bar auto-applies on change — no Apply button.

Calendar week start = Monday (differs from Revenue Overview which uses Sunday).
"""
import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class PerformanceMetricsPage(BasePage):

    # ── Phase 1: filter modal ─────────────────────────────────────────────────

    APPLY_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters' or normalize-space()='Apply']")

    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'loading') or contains(@class,'spinner') or "
        "contains(@class,'skeleton')]")

    # Site multiselect (React Select, searchable) — uses nxt-multi-select__ prefix.
    # Excludes --is-disabled so we match only the modal's interactive control, not the
    # compact page-bar control which is disabled while the modal is open.
    SITE_MULTISELECT = (By.XPATH,
        "//div[contains(@class,'nxt-multi-select__control') "
        "and not(contains(@class,'--is-disabled'))]")

    SITE_CHIPS = (By.XPATH,
        "//div[contains(@class,'nxt-multi-select__multi-value__label')]")

    OVERFLOW_CHIP = (By.XPATH,
        "//div[contains(@class,'nxt-multi-select__multi-value')]"
        "[contains(normalize-space(),'+')]")

    SITE_CLEAR_BTN = (By.XPATH,
        "//div[contains(@class,'nxt-multi-select__clear-indicator')]")

    # Date preset React Select (non-searchable) — uses nxt-select__ prefix, no inputmode='none'
    _DATE_PRESET_DUMMY_INPUT = (By.XPATH,
        "//input[contains(@class,'nxt-select__input') and @role='combobox']")

    DATE_PRESET_COMBOBOX = (By.XPATH,
        "//div[contains(@class,'nxt-select__single-value')]")

    DATE_RANGE_INPUT = (By.XPATH,
        "//input[@placeholder='Select date range']")

    DATE_RANGE_CLEAR_BTN = (By.XPATH,
        "//button[@aria-label='Clear date' or @aria-label='Clear' or "
        "contains(@aria-label,'lear')] | "
        "//*[contains(@class,'clear') and not(contains(@class,'nxt-multi-select'))] | "
        "//*[contains(@class,'reset') and not(contains(@class,'nxt-multi-select'))] | "
        "//input[@placeholder='Select date range']/parent::*/button | "
        "//input[@placeholder='Select date range']"
        "/parent::*//*[self::button or contains(@class,'clear')]")

    # Calendar uses react-day-picker (rdp) library
    CALENDAR_DAY_BUTTONS = (By.XPATH,
        "//button[contains(@class,'rdp-day_button')]")

    # ── Phase 2: metrics screen ───────────────────────────────────────────────

    PAGE_TITLE = (By.XPATH,
        "//*[contains(normalize-space(),'Performance Metrics')]"
        "[self::h1 or self::h2 or contains(@class,'title') or "
        "contains(@class,'heading') or contains(@class,'page-title')]")

    SIDEBAR_ACTIVE_ITEM = (By.XPATH,
        "//*["
        "contains(@class,'active') or contains(@class,'selected') or "
        "@aria-current='page' or @aria-current='true' or "
        "@aria-selected='true' or @data-active='true' or "
        "contains(@class,'is-active') or contains(@class,'current')]"
        "[contains(normalize-space(),'Performance') or "
        "contains(normalize-space(),'Reports')]")

    # ── Conversion Rate widget ────────────────────────────────────────────────

    CVR_WIDGET = (By.XPATH,
        "//*[contains(normalize-space(),'Conversion Rate')]"
        "[contains(@class,'widget') or contains(@class,'card') or "
        "contains(@class,'chart') or self::section]")

    CVR_CHART = (By.XPATH,
        "//canvas | "
        "//svg[descendant::*[contains(@class,'line') or contains(@class,'plot') or "
        "                    contains(@class,'series') or contains(@class,'path')]]")

    CVR_CONSTRAINT_MSG = (By.XPATH,
        "//*[contains(normalize-space(),'At least') and "
        "contains(normalize-space(),'week')]")

    CVR_LEGEND = (By.XPATH,
        "//*[contains(normalize-space(),'Retail transactions')]")

    CVR_Y_AXIS_LABELS = (By.XPATH,
        "//*[contains(@class,'y-axis') or contains(@class,'yAxis') or "
        "contains(@class,'tick')][contains(normalize-space(),'%') or "
        "contains(normalize-space(),'100')]")

    # ── Membership History widget ─────────────────────────────────────────────

    MHT_WIDGET = (By.XPATH,
        "//*[contains(normalize-space(),'Membership History')]"
        "[contains(@class,'widget') or contains(@class,'card') or "
        "contains(@class,'table') or self::section or self::div]")

    MHT_TABLE = (By.XPATH,
        "//table | //*[@role='table'] | //*[@role='grid']")

    MHT_HEADERS = (By.XPATH,
        "//th | //*[@role='columnheader']")

    MHT_ROWS = (By.XPATH,
        "//tbody/tr | //*[@role='row'][not(@role='columnheader')]"
        "[not(ancestor::thead)]")

    MHT_DATE_CELLS = (By.XPATH,
        "//tbody/tr/td[1] | //*[@role='row']//*[@role='cell'][1]")

    MHT_NO_DATA = (By.XPATH,
        "//*[contains(normalize-space(),'No data') or "
        "contains(normalize-space(),'no data') or "
        "contains(normalize-space(),'No information')]")

    MHT_SORT_CONTROLS = (By.XPATH,
        "//th[.//*[contains(@class,'sort')] or @aria-sort] | "
        "//*[@role='columnheader'][@aria-sort or .//*[contains(@class,'sort')]]")

    # ── Column Settings ───────────────────────────────────────────────────────

    # MHT column-settings button has a size-4 settings icon (the page-level
    # filter button also uses lucide-settings but with size-8 — exclude it).
    CST_ICON = (By.XPATH,
        "//button[.//*[contains(@class,'lucide-settings') and contains(@class,'size-4')]] | "
        "//button[@aria-label='Column settings' or @aria-label='Settings'] | "
        "//*[@title='Column settings' or @title='Settings']")

    CST_MODAL = (By.XPATH,
        "//*[@role='dialog'] | //*[contains(@class,'modal') and "
        ".//*[contains(normalize-space(),'column') or "
        "contains(normalize-space(),'Column')]]")

    # Each column row uses a <label> wrapping a hidden <input type="checkbox">.
    # The visible element to interact with is the <label>, not the hidden input.
    CST_TOGGLES = (By.XPATH,
        "//*[@role='dialog']//label[contains(@class,'min-w-9')] | "
        "(//*[@role='dialog'] | //*[contains(@class,'modal')])"
        "//*[@role='switch']")

    # 'Toggle all' is also a <label> adjacent to the 'Toggle all' text (not a button).
    CST_MASTER_BTN = (By.XPATH,
        "//*[@role='dialog']//*[normalize-space()='Toggle all']"
        "/ancestor::div[./label][1]/label | "
        "//button[contains(normalize-space(),'Toggle all') or "
        "contains(normalize-space(),'Select all') or "
        "contains(normalize-space(),'Deselect all')]")

    # ── Frame src patterns ────────────────────────────────────────────────────

    _FRAME_SRC_PATTERNS = ["performance-metrics", "performance", "metrics"]

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _switch_to_frame(self):
        self.driver.switch_to.default_content()
        time.sleep(0.5)
        for pattern in self._FRAME_SRC_PATTERNS:
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.XPATH, "//iframe[contains(@src,'%s')]" % pattern)
                    )
                )
                return
            except TimeoutException:
                self.driver.switch_to.default_content()

    # ── Phase 1 methods ───────────────────────────────────────────────────────

    def wait_for_modal(self):
        self._switch_to_frame()
        self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON))
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.LOAD_MASK)
            )
        except TimeoutException:
            pass
        # Also wait for the site multiselect to become interactive before returning,
        # since the Apply button can appear before the controls finish initialising.
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//div[contains(@class,'nxt-multi-select__control') "
                     "and not(contains(@class,'--is-disabled'))]")
                )
            )
        except TimeoutException:
            pass

    def modal_is_open(self):
        try:
            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located(self.APPLY_BUTTON)
            )
            return True
        except TimeoutException:
            return False

    def apply_modal_filters(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(1.5)
        self._switch_to_frame()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.LOAD_MASK)
            )
        except TimeoutException:
            pass
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.APPLY_BUTTON)
            )
        except TimeoutException:
            pass
        time.sleep(0.5)

    def modal_control_labels(self):
        """Return visible text labels of all four modal controls."""
        body = self.get_body_text()
        return body

    # ── Site multiselect ──────────────────────────────────────────────────────

    def select_site(self, site_name, clear_first=True):
        """Select a site in the filter modal.

        Overrides base select_react_dropdown_option to use ActionChains click on the
        inner <input> rather than a JS click on the outer control div.  JS synthetic
        clicks do not consistently trigger React Select's onMouseDown handler in a
        cold browser, so the dropdown never opens and _find_react_option times out.
        """
        ctrl_locator = (By.XPATH,
            "//div[contains(@class,'nxt-multi-select__control') "
            "and not(contains(@class,'--is-disabled'))]")
        ctrl = self.wait.until(EC.element_to_be_clickable(ctrl_locator))
        inputs = ctrl.find_elements(By.XPATH, ".//input")
        inner = next((i for i in inputs if i.is_displayed()), None)
        if inner is None and inputs:
            inner = inputs[0]
        if inner:
            ActionChains(self.driver).move_to_element(inner).click(inner).perform()
            time.sleep(0.4)
            if clear_first:
                inner.send_keys(Keys.CONTROL, "a")
                inner.send_keys(Keys.BACKSPACE)
            inner.send_keys(site_name)
        else:
            self.driver.execute_script("arguments[0].click();", ctrl)
            time.sleep(0.4)
        option = WebDriverWait(self.driver, 20).until(
            lambda d: self._find_react_option(site_name)
        )
        self.driver.execute_script("arguments[0].click();", option)
        time.sleep(0.3)

    def select_multiple_sites(self, site_names):
        for i, name in enumerate(site_names):
            self.select_react_dropdown_option(
                self.SITE_MULTISELECT, name, clear_first=(i == 0)
            )
            time.sleep(0.5)

    def get_site_options(self):
        """Return list of visible site option labels.

        Triggers the menu by typing "VK" — the only approach that reliably
        opens this React Select (click alone and ARROW_DOWN do not work).
        All configured test sites contain "VK" in their name.
        """
        combo = self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
        self.driver.execute_script("arguments[0].click();", combo)
        inner = None
        try:
            inputs = combo.find_elements(By.XPATH, ".//input")
            inner = next(
                (i for i in inputs if i.is_displayed()),
                inputs[0] if inputs else None
            )
            if inner:
                inner.send_keys("VK")
        except Exception:
            pass
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(@class,'nxt-multi-select__menu')]")
                )
            )
        except TimeoutException:
            pass
        time.sleep(0.3)
        els = self.driver.find_elements(
            By.XPATH, "//*[contains(@class,'nxt-multi-select__option')]"
        )
        options = [e.text.strip() for e in els if e.is_displayed() and e.text.strip()]
        try:
            if inner:
                inner.send_keys(Keys.CONTROL, "a")
                inner.send_keys(Keys.BACKSPACE)
        except Exception:
            pass
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options

    def site_dropdown_uses_checkboxes(self):
        """Return True if the site dropdown options contain checkbox elements."""
        self.get_site_options()
        checks = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'nxt-multi-select__option')]//input[@type='checkbox'] | "
            "//*[contains(@class,'nxt-multi-select__option')]//*[@role='checkbox']")
        return len(checks) > 0

    def get_site_chips(self):
        chips = self.driver.find_elements(*self.SITE_CHIPS)
        return [c.text.strip() for c in chips if c.is_displayed() and c.text.strip()]

    def get_overflow_chip_text(self):
        chips = self.driver.find_elements(*self.OVERFLOW_CHIP)
        visible = [c for c in chips if c.is_displayed()]
        return visible[0].text.strip() if visible else ""

    def clear_sites(self):
        try:
            # Hover over the multiselect first so the clear indicator becomes clickable
            control = self.driver.find_elements(*self.SITE_MULTISELECT)
            if control:
                ActionChains(self.driver).move_to_element(control[0]).perform()
                time.sleep(0.3)
            btn = self.wait.until(EC.element_to_be_clickable(self.SITE_CLEAR_BTN))
            ActionChains(self.driver).move_to_element(btn).click(btn).perform()
            time.sleep(1.0)
        except TimeoutException:
            pass

    def site_option_is_checked(self, site_name):
        """Return True if site_name option shows as selected/checked in the dropdown."""
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'nxt-multi-select__option--is-selected') or "
            "contains(@class,'nxt-multi-select__option--is-focused')]"
            "[contains(normalize-space(),'%s')]" % site_name)
        return any(e.is_displayed() for e in els)

    def site_dropdown_has_scroll(self):
        """Return True if the site dropdown menu container is scrollable."""
        menu = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'nxt-multi-select__menu-list')]")
        for m in menu:
            if m.is_displayed():
                overflow = self.driver.execute_script(
                    "return window.getComputedStyle(arguments[0]).overflowY;", m)
                if overflow in ("auto", "scroll"):
                    return True
        return False

    # ── Date preset (non-searchable React Select) ─────────────────────────────

    def _open_date_preset_dropdown(self):
        """Open the date preset React Select using a real browser click.

        ActionChains on the outer nxt-select__control reliably triggers React
        Select's onMouseDown handler.  The previous approach (JS pointer-event
        dispatch) was not consistently recognised by the React event system.
        """
        ctrl_locator = (By.XPATH,
            "//div[contains(@class,'nxt-select__control') "
            "and not(contains(@class,'nxt-multi-select'))]")
        ctrl = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ctrl_locator)
        )
        ActionChains(self.driver).move_to_element(ctrl).click(ctrl).perform()
        time.sleep(0.6)

    def select_date_preset(self, preset):
        self._open_date_preset_dropdown()
        option = WebDriverWait(self.driver, 10).until(
            lambda d: self._find_react_option(preset)
        )
        self.driver.execute_script("arguments[0].click();", option)
        time.sleep(0.3)

    def get_current_preset_label(self):
        try:
            els = self.driver.find_elements(By.XPATH,
                "//div[contains(@class,'singleValue')]")
            visible = [e for e in els if e.is_displayed()]
            return visible[0].text.strip() if visible else ""
        except Exception:
            return ""

    def get_date_preset_options(self):
        """Return all visible date preset option labels.

        Options render in a React Select portal (document.body) so Selenium's
        is_displayed() is unreliable for them.  Use offsetParent !== null as the
        visibility signal instead.
        """
        self._open_date_preset_dropdown()
        time.sleep(0.3)
        options = self.driver.execute_script("""
            return Array.from(document.querySelectorAll('[role="option"]'))
                .filter(function(el) {
                    var cls = el.className || '';
                    return el.offsetParent !== null
                        && el.textContent.trim()
                        && cls.indexOf('nxt-select__option') !== -1
                        && cls.indexOf('nxt-multi-select') === -1;
                }).map(function(el) { return el.textContent.trim(); });
        """)
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options or []

    # ── Date range / calendar ─────────────────────────────────────────────────

    def get_date_range_value(self):
        """Return the current value of the custom date range input."""
        try:
            els = self.driver.find_elements(By.XPATH,
                "//input[@placeholder='Select date range']")
            for el in els:
                if el.is_displayed():
                    v = el.get_attribute("value") or ""
                    if v:
                        return v
            return ""
        except Exception:
            return ""

    def click_date_range_input(self):
        """Open the calendar by clicking the custom date range field."""
        try:
            els = self.driver.find_elements(By.XPATH,
                "//input[@placeholder='Select date range']")
            for el in els:
                if el.is_displayed():
                    self.driver.execute_script("arguments[0].click();", el)
                    time.sleep(0.5)
                    return
        except Exception:
            pass

    def clear_date_range(self):
        """Click the circled-X button that clears the date range input."""
        # Hover first so CSS :hover-triggered buttons become visible
        try:
            els = self.driver.find_elements(By.XPATH,
                "//input[@placeholder='Select date range']")
            for el in els:
                if el.is_displayed():
                    ActionChains(self.driver).move_to_element(el).perform()
                    time.sleep(0.5)
                    break
        except Exception:
            pass
        # Try Selenium-visible button
        try:
            btns = self.driver.find_elements(*self.DATE_RANGE_CLEAR_BTN)
            for btn in btns:
                if btn.is_displayed():
                    ActionChains(self.driver).move_to_element(btn).click(btn).perform()
                    time.sleep(0.5)
                    return
        except Exception:
            pass
        # JS fallback: directly click any button in the input's ancestor tree that
        # does NOT wrap the input itself (works even if button is CSS :hover-hidden)
        try:
            clicked = self.driver.execute_script("""
                var input = document.querySelector('input[placeholder="Select date range"]');
                if (!input) return false;
                var el = input;
                for (var level = 0; level < 8; level++) {
                    el = el.parentElement;
                    if (!el) break;
                    var btns = el.querySelectorAll('button, [role="button"]');
                    var candidates = [];
                    for (var i = 0; i < btns.length; i++) {
                        if (!btns[i].contains(input)) candidates.push(btns[i]);
                    }
                    if (candidates.length >= 1) {
                        candidates[candidates.length - 1].click();
                        return true;
                    }
                }
                return false;
            """)
            if clicked:
                time.sleep(0.5)
        except Exception:
            pass

    def today_highlighted_in_calendar(self):
        """Return True if the today marker is visible in the open calendar."""
        markers = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'today') or contains(@class,'current-day') or "
            "@aria-current='date' or contains(@aria-label,'Today')]")
        return any(m.is_displayed() for m in markers)

    def future_day_is_disabled(self, days_ahead=1):
        """Return True if a future day's cell is marked disabled.

        react-day-picker places 'rdp-disabled' on the <td> wrapper, not the
        <button> itself.  Also checks aria-disabled on the button as fallback.
        """
        import datetime
        future = datetime.date.today() + datetime.timedelta(days=days_ahead)
        day_str = str(future.day)
        # Check <td> cells with rdp-disabled that contain the day number
        disabled_cells = self.driver.find_elements(By.XPATH,
            "//td[contains(@class,'rdp-disabled')]")
        for cell in disabled_cells:
            if cell.text.strip() == day_str or day_str in cell.text:
                return True
        # Fallback: check aria-disabled on the button itself
        btns = self.driver.find_elements(*self.CALENDAR_DAY_BUTTONS)
        for btn in btns:
            if btn.text.strip() == day_str:
                return btn.get_attribute("aria-disabled") == "true"
        return False

    def _click_calendar_nav(self, direction):
        """Click the prev (direction=-1) or next (direction=+1) month button."""
        if direction < 0:
            xpaths = [
                "//button[contains(@class,'rdp-button_previous')]",
                "//button[@aria-label='Previous month']",
                "//button[@aria-label='Go to previous month']",
                "//button[contains(@class,'prev')]",
                "//button[contains(@aria-label,'Prev') or contains(@aria-label,'prev')]",
            ]
        else:
            xpaths = [
                "//button[contains(@class,'rdp-button_next')]",
                "//button[@aria-label='Next month']",
                "//button[@aria-label='Go to next month']",
                "//button[contains(@class,'next')]",
                "//button[contains(@aria-label,'Next') or contains(@aria-label,'next')]",
            ]
        for xp in xpaths:
            btns = [b for b in self.driver.find_elements(By.XPATH, xp) if b.is_displayed()]
            if btns:
                self.driver.execute_script("arguments[0].click();", btns[0])
                time.sleep(0.3)
                return

    def _navigate_calendar_months(self, months):
        direction = -1 if months < 0 else 1
        for _ in range(abs(months)):
            self._click_calendar_nav(direction)

    def _calendar_click_day(self, day_number):
        from selenium.common.exceptions import StaleElementReferenceException
        for attempt in range(3):
            try:
                btns = self.driver.find_elements(*self.CALENDAR_DAY_BUTTONS)
                for btn in btns:
                    if btn.is_displayed() and btn.text.strip() == str(day_number):
                        self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(0.3)
                        return
                return
            except StaleElementReferenceException:
                time.sleep(0.4)

    def select_date_range_from_calendar(self, year, month, start_day, end_day):
        import datetime
        self.click_date_range_input()
        today = datetime.date.today()
        target = datetime.date(year, month, 1)
        months_diff = (target.year - today.year) * 12 + (target.month - today.month)
        self._navigate_calendar_months(months_diff)
        self._calendar_click_day(start_day)
        time.sleep(0.2)
        self._calendar_click_day(end_day)
        time.sleep(0.3)

    def enter_date_range(self, start_mmddyyyy, end_mmddyyyy):
        sm, sd, sy = (int(x) for x in start_mmddyyyy.split("/"))
        em, ed, ey = (int(x) for x in end_mmddyyyy.split("/"))
        self.select_date_range_from_calendar(sy, sm, sd, ed)

    # ── Phase 2: general ──────────────────────────────────────────────────────

    def wait_for_metrics(self):
        self.wait.until(EC.presence_of_element_located(self.PAGE_TITLE))
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.LOAD_MASK)
            )
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

    def page_title_visible(self):
        els = self.driver.find_elements(*self.PAGE_TITLE)
        return any(e.is_displayed() for e in els)

    def sidebar_active_item_visible(self):
        els = self.driver.find_elements(*self.SIDEBAR_ACTIVE_ITEM)
        if any(e.is_displayed() for e in els):
            return True
        # JS fallback: walk DOM ancestors of Reports/Performance links for any
        # active-state attribute (covers non-standard class names)
        try:
            return bool(self.driver.execute_script("""
                function isActive(el, depth) {
                    if (!el || depth > 6) return false;
                    var cls = (el.className || '').toString().toLowerCase();
                    var attrs = [].slice.call(el.attributes || [])
                        .map(function(a) { return a.name + '=' + a.value; })
                        .join(' ').toLowerCase();
                    if (cls.match(/activ|select|current|highlight/) ||
                        attrs.match(/aria-current|aria-selected|data-active|data-state=.active/)) {
                        return true;
                    }
                    return isActive(el.parentElement, depth + 1);
                }
                var links = document.querySelectorAll('a, [role="link"], [role="menuitem"]');
                for (var i = 0; i < links.length; i++) {
                    var lnk = links[i];
                    var text = lnk.textContent.trim();
                    if (text === 'Reports' || text.includes('Performance')) {
                        if (isActive(lnk, 0)) return true;
                    }
                }
                return false;
            """))
        except Exception:
            return False

    # ── Conversion Rate widget ─────────────────────────────────────────────────

    def cvr_widget_visible(self):
        body = self.get_body_text()
        return "conversion rate" in body.lower()

    def cvr_chart_visible(self):
        els = self.driver.find_elements(*self.CVR_CHART)
        return any(e.is_displayed() for e in els)

    def cvr_constraint_visible(self):
        els = self.driver.find_elements(*self.CVR_CONSTRAINT_MSG)
        return any(e.is_displayed() for e in els)

    def cvr_constraint_text(self):
        els = self.driver.find_elements(*self.CVR_CONSTRAINT_MSG)
        visible = [e for e in els if e.is_displayed()]
        return visible[0].text.strip() if visible else ""

    def cvr_legend_visible(self):
        els = self.driver.find_elements(*self.CVR_LEGEND)
        return any(e.is_displayed() for e in els)

    def cvr_y_axis_has_percentages(self):
        """Return True if y-axis labels contain percentage values."""
        body = self.get_body_text()
        return "%" in body

    # ── Membership History table ───────────────────────────────────────────────

    def mht_widget_visible(self):
        body = self.get_body_text()
        return "membership history" in body.lower() or "membership" in body.lower()

    def mht_table_visible(self):
        els = self.driver.find_elements(*self.MHT_TABLE)
        return any(e.is_displayed() for e in els)

    def mht_no_data_visible(self):
        els = self.driver.find_elements(*self.MHT_NO_DATA)
        return any(e.is_displayed() for e in els)

    def mht_get_column_headers(self):
        headers = self.driver.find_elements(*self.MHT_HEADERS)
        if not any(h.is_displayed() and h.text.strip() for h in headers):
            try:
                loc = self.MHT_HEADERS
                WebDriverWait(self.driver, 8).until(
                    lambda d: any(
                        h.is_displayed() and h.text.strip()
                        for h in d.find_elements(*loc)
                    )
                )
            except TimeoutException:
                pass
            headers = self.driver.find_elements(*self.MHT_HEADERS)
        return [h.text.strip() for h in headers if h.is_displayed() and h.text.strip()]

    def mht_column_visible(self, column_name):
        headers = self.mht_get_column_headers()
        return any(column_name.lower() in h.lower() for h in headers)

    def mht_get_row_count(self):
        rows = self.driver.find_elements(*self.MHT_ROWS)
        return len([r for r in rows if r.is_displayed()])

    def mht_get_date_values(self):
        cells = self.driver.find_elements(*self.MHT_DATE_CELLS)
        return [c.text.strip() for c in cells if c.is_displayed() and c.text.strip()]

    def mht_dates_are_descending(self):
        """Return True if the date column is sorted newest-first."""
        import datetime
        raw = self.mht_get_date_values()
        dates = []
        for r in raw:
            for fmt in ("%m/%d/%Y", "%b %d, %Y", "%Y-%m-%d"):
                try:
                    dates.append(datetime.datetime.strptime(r.split()[0], fmt).date())
                    break
                except ValueError:
                    continue
        return dates == sorted(dates, reverse=True) if len(dates) > 1 else True

    def mht_click_column_header(self, header_name):
        headers = self.driver.find_elements(*self.MHT_HEADERS)
        for h in headers:
            if h.is_displayed() and header_name.lower() in h.text.lower():
                self.driver.execute_script("arguments[0].click();", h)
                time.sleep(0.5)
                return

    def mht_has_sort_controls(self):
        els = self.driver.find_elements(*self.MHT_SORT_CONTROLS)
        return any(e.is_displayed() for e in els)

    def mht_horizontal_scroll_available(self):
        """Return True if the MHT container has horizontal scrollbar."""
        try:
            tables = self.driver.find_elements(*self.MHT_TABLE)
            for tbl in tables:
                if tbl.is_displayed():
                    parent = self.driver.execute_script(
                        "return arguments[0].parentElement;", tbl)
                    if parent:
                        overflow = self.driver.execute_script(
                            "return window.getComputedStyle(arguments[0]).overflowX;", parent)
                        if overflow in ("auto", "scroll"):
                            return True
        except Exception:
            pass
        body = self.get_body_text()
        return "membership history" in body.lower()

    def mht_cell_has_color_coding(self):
        """Return True if any MHT row cells use semantic colour classes."""
        colored = self.driver.find_elements(By.XPATH,
            "//tbody/tr/td[contains(@class,'green') or contains(@class,'red') or "
            "contains(@class,'positive') or contains(@class,'negative') or "
            "contains(@class,'success') or contains(@class,'danger') or "
            "contains(@style,'color')]")
        return len(colored) > 0

    def mht_has_zero_value_cells(self):
        """Return True if at least one table cell shows '0' (not blank)."""
        cells = self.driver.find_elements(By.XPATH, "//tbody/tr/td")
        return any(c.text.strip() == "0" for c in cells if c.is_displayed())

    def mht_body_contains(self, text):
        body = self.get_body_text()
        return text in body

    # ── Column Settings modal ─────────────────────────────────────────────────

    def cst_open_settings(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CST_ICON))
        self.driver.execute_script("arguments[0].click();", btn)
        # Wait for the settings modal to actually render before returning.
        # time.sleep(0.5) was insufficient late in long suite runs.
        try:
            WebDriverWait(self.driver, 8).until(lambda d: self.cst_settings_open())
        except TimeoutException:
            pass
        time.sleep(0.3)

    def cst_settings_open(self):
        els = self.driver.find_elements(*self.CST_MODAL)
        return any(e.is_displayed() for e in els)

    def cst_get_toggles(self):
        return [t for t in self.driver.find_elements(*self.CST_TOGGLES) if t.is_displayed()]

    def cst_toggle_count(self):
        return len(self.cst_get_toggles())

    def cst_all_toggles_on(self):
        toggles = self.cst_get_toggles()
        if not toggles:
            return False
        def _is_on(el):
            # Toggles are <label> wrappers; check their nested hidden <input>.
            # Use is_selected() (reads the .checked JS property) — avoid
            # get_attribute("checked") which returns "false" as a non-None string
            # in React-controlled checkboxes, causing a false-positive "checked" read.
            try:
                inp = el.find_element(By.XPATH, ".//input[@type='checkbox']")
                return inp.is_selected()
            except Exception:
                pass
            return el.get_attribute("aria-checked") == "true" or el.is_selected()
        return all(_is_on(t) for t in toggles)

    def cst_toggle_all(self):
        btns = self.driver.find_elements(*self.CST_MASTER_BTN)
        for btn in btns:
            if btn.is_displayed():
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.6)
                return

    def cst_toggle_column(self, column_name):
        """Toggle the <label> switch for the named column in the settings modal."""
        # Each row: <div>[column text]</div><label>...</label>
        # Walk from label's grandparent to find the text sibling
        labels = self.driver.find_elements(By.XPATH,
            "//*[@role='dialog']//label[contains(@class,'min-w-9')]")
        for label in labels:
            try:
                row = self.driver.execute_script(
                    "return arguments[0].parentElement;", label)
                row_text = (row.text if row else "")
                if column_name.lower() in row_text.lower():
                    self.driver.execute_script("arguments[0].click();", label)
                    time.sleep(0.3)
                    return
            except Exception:
                continue

    def cst_close_settings(self):
        """Close the Column Settings modal by pressing Escape."""
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.5)
        except Exception:
            pass

    def cst_date_column_always_visible(self):
        """Return True if Date header is visible in MHT even with other columns hidden."""
        return self.mht_column_visible("Date")
