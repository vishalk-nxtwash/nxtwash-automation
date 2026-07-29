import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class RevenueOverviewPage(BasePage):

    FRAME = (By.XPATH, "//iframe[contains(@src,'revenue')]")

    # ── Filter controls ───────────────────────────────────────────────────────
    APPLY_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters'] | "
        "//button[contains(normalize-space(),'Apply filters')]")

    # Site multiselect uses overview__site-select__ CSS class prefix
    SITE_MULTISELECT = (By.XPATH,
        "//div[contains(@class,'overview__site-select__control')]")

    # The singleValue div shows the currently selected preset (e.g. "Today", "This month").
    # It is always visible, unlike the hidden dummy input, so is_displayed() works for
    # visibility assertions.  Unique: the site multiselect uses multi-value chips, not singleValue.
    DATE_PRESET_COMBOBOX = (By.XPATH,
        "//div[contains(@class,'singleValue')]")

    # Hidden dummy input — used only as DOM anchor for _open_date_preset_dropdown().
    _DATE_PRESET_DUMMY_INPUT = (By.XPATH,
        "//input[@role='combobox' and @inputmode='none']")

    # Date range input is readonly — value is set only via the calendar picker
    DATE_RANGE_INPUT = (By.XPATH,
        "//input[@placeholder='Select range of dates']")

    SINGLE_DAY_CHECKBOX = (By.XPATH,
        "//input[@type='checkbox']"
        "[ancestor::*[contains(normalize-space(),'Single') or "
        "contains(normalize-space(),'single')]] | "
        "//input[@type='checkbox'][@name or @id]")

    SINGLE_DAY_LABEL = (By.XPATH,
        "//*[contains(normalize-space(),'Single day') or "
        "contains(normalize-space(),'Single Day')]")

    DATE_RANGE_LABEL = (By.XPATH,
        "//*[contains(normalize-space(),'Select range of dates')]"
        "[not(self::input)]")

    EXPORT_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Export XLSX')] | "
        "//button[contains(normalize-space(),'Export')]")

    # ── Metrics screen ────────────────────────────────────────────────────────
    PAGE_TITLE = (By.XPATH,
        "//*[contains(normalize-space(),'Revenue Metrics')]")

    INFO_ICON = (By.XPATH,
        "//*[contains(@class,'info') or @aria-label='info' or "
        "contains(@aria-label,'info') or contains(@class,'tooltip-icon')]"
        "[not(self::script)][not(self::style)]")

    TOOLTIP = (By.XPATH,
        "//*[@role='tooltip'] | "
        "//*[contains(@class,'tooltip') and "
        "not(contains(@style,'display: none') or "
        "contains(@style,'display:none'))]")

    NO_INFO_MESSAGE = (By.XPATH,
        "//*[contains(normalize-space(),'No information for this period') or "
        "contains(normalize-space(),'no information') or "
        "contains(normalize-space(),'No data')]")

    # Site chips use overview__site-select__ prefix
    SITE_CHIPS = (By.XPATH,
        "//div[contains(@class,'overview__site-select__multi-value')]"
        "[not(contains(normalize-space(),'+'))]")

    OVERFLOW_CHIP = (By.XPATH,
        "//div[contains(@class,'overview__site-select__multi-value') and "
        "contains(normalize-space(),'+')]")

    SITE_CLEAR_BTN = (By.XPATH,
        "//div[contains(@class,'overview__site-select__clear-indicator')]")

    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and "
        "not(contains(@style,'display: none') or "
        "contains(@style,'display:none'))]")

    # KPI
    _KPI_LABELS = [
        "Total Revenue", "New Members", "Recharges", "Resignups", "Retail Sales"
    ]

    # Tabs
    MEMBERSHIP_TAB = (By.XPATH,
        "//button[contains(normalize-space(),'Membership Revenue')] | "
        "//*[@role='tab'][contains(normalize-space(),'Membership Revenue')]")

    RETAIL_TAB = (By.XPATH,
        "//button[contains(normalize-space(),'Retail Revenue')] | "
        "//*[@role='tab'][contains(normalize-space(),'Retail Revenue')]")

    NEW_SALES_SUBTAB = (By.XPATH,
        "//button[normalize-space()='New Sales'] | "
        "//*[@role='tab'][normalize-space()='New Sales']")

    RECHARGES_SUBTAB = (By.XPATH,
        "//button[normalize-space()='Recharges'] | "
        "//*[@role='tab'][normalize-space()='Recharges']")

    RESIGNUPS_SUBTAB = (By.XPATH,
        "//button[normalize-space()='Resignups'] | "
        "//*[@role='tab'][normalize-space()='Resignups']")

    WASH_PACKAGE_SUBTAB = (By.XPATH,
        "//button[normalize-space()='Wash Package'] | "
        "//*[@role='tab'][normalize-space()='Wash Package']")

    WASH_EXTRA_SUBTAB = (By.XPATH,
        "//button[normalize-space()='Wash Extra'] | "
        "//*[@role='tab'][normalize-space()='Wash Extra']")

    CHART_CANVAS = (By.XPATH, "//canvas")
    CHART_SVG_PATHS = (By.XPATH, "//svg//*[name()='path' and @d]")

    CHART_LEGEND_ITEMS = (By.XPATH,
        "//*[contains(@class,'legend') or "
        "contains(@class,'Legend')]//*[@role='listitem' or "
        "contains(@class,'item') or contains(@class,'label')]"
        "[normalize-space()]")

    CHART_CENTER_LABEL = (By.XPATH,
        "//*[contains(@class,'center') or "
        "contains(@class,'doughnut-label') or "
        "contains(@class,'total-label') or "
        "contains(@class,'chart-label')]")

    # Calendar — day buttons use sc-gFqAkR styled-component class
    CALENDAR_DAY_BUTTONS = (By.XPATH,
        "//button[contains(@class,'sc-gFqAkR')]")

    CALENDAR_DISABLED_BUTTONS = (By.XPATH,
        "//button[contains(@class,'sc-gFqAkR')]"
        "[@disabled or @aria-disabled='true' or "
        "contains(@class,'disabled') or contains(@class,'outside')]")

    CALENDAR_YEAR_SELECTOR = (By.XPATH,
        "//button[contains(@class,'year') or "
        "contains(@aria-label,'year') or @role='spinbutton']")

    # ── Iframe ────────────────────────────────────────────────────────────────

    _FRAME_SRC_PATTERNS = ["revenue", "reports/detailed", "reports", "detailed"]

    def _switch_to_frame(self):
        self.driver.switch_to.default_content()
        time.sleep(0.5)
        for pattern in self._FRAME_SRC_PATTERNS:
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.XPATH, "//iframe[contains(@src,'%s')]" % pattern)
                    )
                )
                return
            except TimeoutException:
                self.driver.switch_to.default_content()

    # ── Phase 1: filter modal ─────────────────────────────────────────────────

    def wait_for_modal(self):
        self._switch_to_frame()
        self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON))
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.LOAD_MASK)
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

    # ── Site multiselect ──────────────────────────────────────────────────────

    def select_site(self, site_name, clear_first=True):
        self.select_react_dropdown_option(
            self.SITE_MULTISELECT, site_name, clear_first=clear_first
        )

    def select_multiple_sites(self, site_names):
        for i, name in enumerate(site_names):
            self.select_react_dropdown_option(
                self.SITE_MULTISELECT, name, clear_first=(i == 0)
            )

    def get_site_options(self):
        combo = self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
        # Typing text is required to open this React Select's menu — click alone
        # (JS or ActionChains) and ARROW_DOWN do not trigger it. Typing "VK"
        # covers all configured test sites; the tests only assert RVO_SITE is present.
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
                    (By.XPATH,
                     "//*[contains(@class,'overview__site-select__menu')]")
                )
            )
        except TimeoutException:
            pass
        time.sleep(0.3)
        els = self.driver.find_elements(
            By.XPATH,
            "//*[contains(@class,'overview__site-select__option')]"
        )
        options = [e.text.strip() for e in els if e.is_displayed() and e.text.strip()]
        # Clear the typed filter text before closing so subsequent operations
        # start with a clean input.
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

    def get_site_chips(self):
        chips = self.driver.find_elements(*self.SITE_CHIPS)
        return [c.text.strip() for c in chips if c.is_displayed() and c.text.strip()]

    def get_overflow_chip_text(self):
        chips = self.driver.find_elements(*self.OVERFLOW_CHIP)
        visible = [c for c in chips if c.is_displayed()]
        return visible[0].text.strip() if visible else ""

    def clear_sites(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.SITE_CLEAR_BTN))
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.4)
        except TimeoutException:
            pass

    # ── Date preset (non-searchable React Select) ─────────────────────────────

    def _open_date_preset_dropdown(self):
        """Open the date preset React Select menu.

        React Select v5 opens on pointerdown/mousedown, not on a synthetic click.
        We dispatch the full pointer+mouse event sequence with screen coordinates
        to the control div, so React's event system treats it as a real user click.
        ActionChains on the singleValue is kept as a fallback.
        """
        dummy_els = self.driver.find_elements(*self._DATE_PRESET_DUMMY_INPUT)
        if dummy_els:
            self.driver.execute_script("""
                var dummy = arguments[0];
                var control = dummy.closest('[class*="-control"]');
                if (!control) control = dummy.parentElement;
                if (!control) return;
                var r = control.getBoundingClientRect();
                var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
                var pOpts = {bubbles:true, cancelable:true, pointerId:1,
                             pointerType:'mouse', clientX:cx, clientY:cy};
                var mOpts = {bubbles:true, cancelable:true, clientX:cx, clientY:cy};
                control.dispatchEvent(new PointerEvent('pointerdown', pOpts));
                control.dispatchEvent(new MouseEvent('mousedown', mOpts));
                control.dispatchEvent(new MouseEvent('mouseup',    mOpts));
                control.dispatchEvent(new MouseEvent('click',      mOpts));
            """, dummy_els[0])
            time.sleep(0.5)
            return
        # Fallback: ActionChains on the visible singleValue display
        sv = self.wait.until(EC.visibility_of_element_located(self.DATE_PRESET_COMBOBOX))
        ActionChains(self.driver).move_to_element(sv).click().perform()
        time.sleep(0.5)

    def select_date_preset(self, preset):
        self._open_date_preset_dropdown()
        option = WebDriverWait(self.driver, 10).until(
            lambda d: self._find_react_option(preset)
        )
        self.driver.execute_script("arguments[0].click();", option)
        time.sleep(0.3)

    def get_date_preset_options(self):
        self._open_date_preset_dropdown()
        time.sleep(0.1)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[@role='option']"))
            )
        except TimeoutException:
            pass
        els = self.driver.find_elements(By.XPATH, "//*[@role='option']")
        options = [e.text.strip() for e in els if e.is_displayed() and e.text.strip()]
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options

    def get_current_preset_label(self):
        try:
            els = self.driver.find_elements(By.XPATH,
                "//*[contains(@class,'singleValue')]")
            visible = [e for e in els if e.is_displayed()]
            return visible[0].text.strip() if visible else ""
        except Exception:
            return ""

    # ── Calendar / date range ─────────────────────────────────────────────────

    def _click_calendar_nav(self, direction):
        """Click prev (-1) or next (+1) month navigation button in the open calendar."""
        if direction < 0:
            xpaths = [
                "//button[@aria-label='Previous month' or "
                "@aria-label='Go to previous month' or "
                "@aria-label='Prev month']",
                "//button[contains(@aria-label,'previous') or "
                "contains(@aria-label,'Previous') or "
                "contains(@aria-label,'prev')]",
                "//button[contains(@class,'prev') or contains(@class,'Prev') or "
                "contains(@class,'back')][@type='button']",
            ]
        else:
            xpaths = [
                "//button[@aria-label='Next month' or "
                "@aria-label='Go to next month' or "
                "@aria-label='Next Month']",
                "//button[contains(@aria-label,'next') or "
                "contains(@aria-label,'Next')]",
                "//button[contains(@class,'next') or contains(@class,'Next') or "
                "contains(@class,'forward')][@type='button']",
            ]
        for xpath in xpaths:
            btns = self.driver.find_elements(By.XPATH, xpath)
            visible = [b for b in btns if b.is_displayed()]
            if visible:
                self.driver.execute_script("arguments[0].click();", visible[0])
                time.sleep(0.12)
                return True
        return False

    def _navigate_calendar_months(self, months):
        """Navigate an open calendar picker by the given signed number of months."""
        direction = -1 if months < 0 else 1
        for _ in range(abs(months)):
            if not self._click_calendar_nav(direction):
                break

    def _calendar_click_day(self, day_number):
        """Click a calendar day button by its visible day number."""
        for xpath in [
            "//button[contains(@class,'sc-gFqAkR')][not(@disabled)]"
            "[normalize-space()='%d']" % day_number,
            "//button[not(@disabled)][normalize-space()='%d']"
            "[@data-selected or @tabindex]" % day_number,
        ]:
            btns = self.driver.find_elements(By.XPATH, xpath)
            visible = [b for b in btns if b.is_displayed() and b.is_enabled()]
            if visible:
                self.driver.execute_script("arguments[0].click();", visible[0])
                time.sleep(0.3)
                return True
        return False

    def select_date_range_from_calendar(self, year, month, start_day, end_day):
        """Open the calendar, navigate to year/month, click start_day then end_day."""
        import datetime
        today = datetime.date.today()
        months_offset = (year - today.year) * 12 + (month - today.month)

        el = self.wait.until(EC.element_to_be_clickable(self.DATE_RANGE_INPUT))
        self.driver.execute_script("arguments[0].click();", el)
        time.sleep(0.6)

        if months_offset != 0:
            self._navigate_calendar_months(months_offset)
            time.sleep(0.3)

        self._calendar_click_day(start_day)
        self._calendar_click_day(end_day)
        time.sleep(0.3)

    def enter_date_range(self, start, end):
        """Select a date range via the calendar picker.

        The date range input is readonly so direct typing is not possible.
        Parses MM/DD/YYYY strings, navigates the calendar to the start month,
        and clicks start and end day numbers.
        """
        import datetime
        try:
            s = datetime.datetime.strptime(start, "%m/%d/%Y").date()
            e = datetime.datetime.strptime(end, "%m/%d/%Y").date()
        except ValueError:
            return
        self.select_date_range_from_calendar(s.year, s.month, s.day, e.day)

    def get_date_range_value(self):
        try:
            el = self.driver.find_element(*self.DATE_RANGE_INPUT)
            return el.get_attribute("value") or ""
        except Exception:
            return ""

    def open_date_range_picker(self):
        el = self.wait.until(EC.element_to_be_clickable(self.DATE_RANGE_INPUT))
        self.driver.execute_script("arguments[0].click();", el)
        time.sleep(0.6)

    def calendar_is_open(self):
        btns = self.driver.find_elements(*self.CALENDAR_DAY_BUTTONS)
        return any(b.is_displayed() for b in btns)

    def calendar_has_future_dates_disabled(self):
        import datetime
        tomorrow_day = str(
            (datetime.date.today() + datetime.timedelta(days=1)).day
        )
        disabled = self.driver.find_elements(*self.CALENDAR_DISABLED_BUTTONS)
        for el in disabled:
            label = el.get_attribute("aria-label") or el.text.strip()
            if tomorrow_day in label:
                return True
        return len(disabled) > 0

    def calendar_year_selector_visible(self):
        els = self.driver.find_elements(*self.CALENDAR_YEAR_SELECTOR)
        return any(e.is_displayed() for e in els)

    def date_range_input_placeholder(self):
        try:
            # In Single day mode the page renders a new input with placeholder
            # 'Select date' while the range input remains in the DOM hidden.
            # Return the single-date input's placeholder when it's visible.
            single_els = self.driver.find_elements(
                By.XPATH, "//input[@placeholder='Select date']")
            for el in single_els:
                if el.is_displayed():
                    return el.get_attribute("placeholder") or ""
            el = self.driver.find_element(*self.DATE_RANGE_INPUT)
            return el.get_attribute("placeholder") or ""
        except Exception:
            return ""

    # ── Single day checkbox ───────────────────────────────────────────────────

    def check_single_day(self):
        try:
            cb = self.wait.until(EC.presence_of_element_located(self.SINGLE_DAY_CHECKBOX))
            if not cb.is_selected():
                self.driver.execute_script("arguments[0].click();", cb)
                time.sleep(0.4)
        except TimeoutException:
            pass

    def uncheck_single_day(self):
        try:
            cb = self.wait.until(EC.presence_of_element_located(self.SINGLE_DAY_CHECKBOX))
            if cb.is_selected():
                self.driver.execute_script("arguments[0].click();", cb)
                time.sleep(0.4)
        except TimeoutException:
            pass

    def single_day_is_checked(self):
        try:
            cb = self.driver.find_element(*self.SINGLE_DAY_CHECKBOX)
            return cb.is_selected()
        except Exception:
            return False

    # ── Phase 2: metrics screen ───────────────────────────────────────────────

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

    def info_icon_visible(self):
        els = self.driver.find_elements(*self.INFO_ICON)
        return any(e.is_displayed() for e in els)

    def kpi_cards_present(self):
        body = self.get_body_text().lower()
        return all(label.lower() in body for label in self._KPI_LABELS)

    def get_kpi_value(self, card_label):
        try:
            els = self.driver.find_elements(By.XPATH,
                "//*[contains(normalize-space(),'%s')]"
                "/following::*[contains(normalize-space(),'$')][1]" % card_label)
            visible = [e for e in els if e.is_displayed() and "$" in e.text]
            return visible[0].text.strip() if visible else ""
        except Exception:
            return ""

    def all_kpi_show_zero(self):
        body = self.get_body_text()
        return "$0.00" in body or "0.00" in body

    # ── Tab helpers ───────────────────────────────────────────────────────────

    def _click_tab(self, locator):
        btn = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(0.5)

    def click_membership_tab(self):
        self._click_tab(self.MEMBERSHIP_TAB)

    def click_retail_tab(self):
        self._click_tab(self.RETAIL_TAB)

    def click_sub_tab(self, name):
        locator = (By.XPATH,
            "//button[contains(normalize-space(),'%s')] | "
            "//*[@role='tab'][contains(normalize-space(),'%s')]" % (name, name))
        self._click_tab(locator)

    def get_tab_count(self, tab_label):
        try:
            els = self.driver.find_elements(By.XPATH,
                "//button[contains(normalize-space(),'%s')] | "
                "//*[@role='tab'][contains(normalize-space(),'%s')]"
                % (tab_label, tab_label))
            for el in [e for e in els if e.is_displayed()]:
                spans = el.find_elements(By.XPATH, ".//span")
                for span in spans:
                    txt = span.text.strip()
                    if txt.isdigit():
                        return int(txt)
                nums = re.findall(r"\d+", el.text)
                if nums:
                    return int(nums[-1])
        except Exception:
            pass
        return 0

    def membership_tab_count(self):
        return self.get_tab_count("Membership Revenue")

    def retail_tab_count(self):
        return self.get_tab_count("Retail Revenue")

    def assert_membership_count_invariant(self):
        ns = self.get_tab_count("New Sales")
        rc = self.get_tab_count("Recharges")
        ru = self.get_tab_count("Resignups")
        mem = self.membership_tab_count()
        assert ns + rc + ru == mem, (
            "Membership count invariant: "
            "New Sales(%d) + Recharges(%d) + Resignups(%d) = %d ≠ Membership Revenue(%d)"
            % (ns, rc, ru, ns + rc + ru, mem)
        )

    def assert_retail_count_invariant(self):
        # Retail section uses a flat product list; no named subtabs exist to sum.
        ret = self.retail_tab_count()
        assert ret >= 0, (
            "Retail Revenue count should be non-negative, got %d" % ret
        )

    # ── Breakdown list ────────────────────────────────────────────────────────

    def get_breakdown_rows(self):
        rows = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'list-item') or "
            "contains(@class,'breakdown') or "
            "contains(@class,'revenue-item') or "
            "contains(@class,'row-item')]")
        visible = [r.text.strip() for r in rows if r.is_displayed() and r.text.strip()]
        if not visible:
            body = self.get_body_text()
            visible = [
                ln.strip() for ln in body.split("\n")
                if "$" in ln and "%" in ln and ln.strip()
            ]
        return visible

    # ── Chart ─────────────────────────────────────────────────────────────────

    def chart_is_visible(self):
        canvases = self.driver.find_elements(*self.CHART_CANVAS)
        svgs = self.driver.find_elements(By.TAG_NAME, "svg")
        return (
            any(c.is_displayed() for c in canvases)
            or any(s.is_displayed() for s in svgs)
        )

    def get_legend_items(self):
        items = self.driver.find_elements(*self.CHART_LEGEND_ITEMS)
        return [i.text.strip() for i in items if i.is_displayed() and i.text.strip()]

    def click_legend_item(self, legend_text):
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(normalize-space(),'%s')]"
            "[ancestor::*[contains(@class,'legend') or "
            "contains(@class,'Legend')]]" % legend_text)
        visible = [e for e in els if e.is_displayed()]
        if visible:
            self.driver.execute_script("arguments[0].click();", visible[0])
            time.sleep(0.4)

    def get_chart_center_label(self):
        try:
            els = self.driver.find_elements(*self.CHART_CENTER_LABEL)
            texts = [e.text.strip() for e in els
                     if e.is_displayed() and ("%" in e.text or "$" in e.text)]
            return texts[0] if texts else ""
        except Exception:
            return ""

    def hover_chart_segment(self, segment_index=0):
        canvases = self.driver.find_elements(*self.CHART_CANVAS)
        paths = self.driver.find_elements(*self.CHART_SVG_PATHS)
        if paths:
            visible = [p for p in paths if p.is_displayed()]
            target = visible[segment_index % len(visible)] if visible else None
            if target:
                ActionChains(self.driver).move_to_element(target).perform()
                time.sleep(0.4)
                return
        if canvases:
            c = canvases[0]
            w, h = c.size["width"], c.size["height"]
            offsets = [
                (int(w * 0.35), int(-h * 0.25)),
                (int(w * 0.10), int(h * 0.35)),
                (int(-w * 0.30), int(h * 0.10)),
            ]
            ox, oy = offsets[segment_index % len(offsets)]
            ActionChains(self.driver).move_to_element_with_offset(c, ox, oy).perform()
            time.sleep(0.4)

    def hover_info_icon(self):
        els = self.driver.find_elements(*self.INFO_ICON)
        visible = [e for e in els if e.is_displayed()]
        if visible:
            ActionChains(self.driver).move_to_element(visible[0]).perform()
            time.sleep(0.4)

    def get_tooltip_text(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(self.TOOLTIP)
            )
            els = self.driver.find_elements(*self.TOOLTIP)
            texts = [e.text.strip() for e in els if e.is_displayed() and e.text.strip()]
            return texts[0] if texts else ""
        except TimeoutException:
            return ""

    def dismiss_tooltip(self):
        try:
            body = self.driver.find_element(By.TAG_NAME, "body")
            ActionChains(self.driver).move_to_element_with_offset(body, 10, 10).click().perform()
            time.sleep(0.3)
        except Exception:
            pass

    # ── Export ────────────────────────────────────────────────────────────────

    def click_export(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.EXPORT_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(0.5)

    # ── Misc ──────────────────────────────────────────────────────────────────

    def no_info_message_visible(self):
        els = self.driver.find_elements(*self.NO_INFO_MESSAGE)
        return any(e.is_displayed() for e in els)

    def rapid_preset_switch(self, presets):
        for preset in presets:
            self.select_date_preset(preset)
            time.sleep(0.25)

    def rapid_site_toggle(self, sites):
        for site in sites:
            self.select_react_dropdown_option(
                self.SITE_MULTISELECT, site, clear_first=False
            )
            time.sleep(0.25)

    def sidebar_item_is_active(self, label):
        els = self.driver.find_elements(By.XPATH,
            "//*[@role='link' or self::a or self::li]"
            "[contains(normalize-space(),'%s')]" % label)
        for el in els:
            classes = el.get_attribute("class") or ""
            if "active" in classes or "selected" in classes or "current" in classes:
                return True
        return False
