import re
import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class WashActivityPage(BasePage):
    """Page object for /reports/detailed/cars_washed (Wash Activity report).

    Phase 1: blocking filter modal auto-opens on load — site multiselect
    (no default), date preset, date range, single-day checkbox, Apply button.
    Phase 2: 6 KPI cards → Hourly Distribution bar chart → Usage Breakdown
    (3-tab: Memberships / Paid Washes / Comp Washes).
    Export: direct "Export XLSX" button in the filter bar — no modal.
    """

    # TODO: Confirm iframe src pattern via DevTools before first run.
    _FRAME_SRC_PATTERNS = [
        "cars_washed", "car-washed", "wash-activity", "wash_activity",
    ]

    # ── Filter modal / bar controls ───────────────────────────────────────────
    # TODO: Confirm exact button text and element via DevTools.

    APPLY_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters']"
        "[ancestor::*[@role='dialog']]")

    # TODO: Confirm CSS class prefix (overview__site-select__ vs nxt-multi-select__).
    SITE_MULTISELECT = (By.XPATH,
        "//div[contains(@class,'overview__site-select__control')] | "
        "//div[contains(@class,'nxt-multi-select__control')]")

    SITE_INPUT = (By.XPATH,
        "//input[contains(@class,'overview__site-select__input')] | "
        "//input[contains(@class,'nxt-multi-select__input')]")

    # Date preset: readonly combobox (inputmode='none' or aria-readonly='true').
    DATE_PRESET_COMBOBOX = (By.XPATH,
        "//input[@inputmode='none' and @role='combobox']"
        "/ancestor::div[contains(@class,'-control')][1] | "
        "//div[./div/input[@aria-readonly='true'][@role='combobox']]")

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
    # TODO: Confirm class and ancestor distinction via DevTools.
    PAGE_BAR_SINGLE_DAY_CHECKBOX = (By.XPATH,
        "//input[contains(@class,'header-widget__title__descr_checkbox')]"
        "[not(ancestor::*[@role='dialog'])]")

    # ── Export ────────────────────────────────────────────────────────────────
    # WAC export is a direct button in the filter bar — no modal, no format selector.
    # TODO: Confirm exact button text via DevTools.
    EXPORT_XLSX_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Export XLSX') or "
        "contains(normalize-space(),'Export xlsx') or "
        "contains(normalize-space(),'EXPORT XLSX') or "
        "contains(normalize-space(),'Export')]"
        "[not(contains(normalize-space(),'filter'))]")

    # ── Load mask / spinner ───────────────────────────────────────────────────

    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and "
        "not(contains(@style,'display: none') or contains(@style,'display:none'))] | "
        "//*[contains(@class,'spinner') and "
        "not(contains(@style,'display: none') or contains(@style,'display:none'))]")

    # ── No-data indicators ────────────────────────────────────────────────────

    NO_DATA_MESSAGE = (By.XPATH,
        "//*[contains(normalize-space(),'No information for this period') or "
        "contains(normalize-space(),'No data') or "
        "contains(normalize-space(),'no data') or "
        "contains(normalize-space(),'No records') or "
        "contains(normalize-space(),'No results')]")

    # ── KPI cards ─────────────────────────────────────────────────────────────
    # TODO: Confirm KPI card container class via DevTools.
    KPI_CARD_CONTAINER = (By.XPATH,
        "//*[contains(@class,'kpi') or contains(@class,'KPI') or "
        "contains(@class,'metric') or contains(@class,'stat')]")

    # ── Hourly Distribution chart ─────────────────────────────────────────────
    # TODO: Confirm chart section heading and SVG bar/legend locators via DevTools.
    CHART_SECTION = (By.XPATH,
        "//*[contains(normalize-space(),'Hourly Distribution') or "
        "contains(normalize-space(),'hourly distribution') or "
        "contains(normalize-space(),'Hourly')] | "
        "//*[contains(@class,'chart') or contains(@class,'Chart')]"
        "[.//*[local-name()='svg']]")

    CHART_BARS = (By.XPATH,
        ".//*[local-name()='rect'][contains(@class,'bar') or @width]"
        "[not(contains(@class,'background') or contains(@class,'grid'))]")

    CHART_LEGEND_ITEMS = (By.XPATH,
        "//*[contains(@class,'legend') or contains(@class,'Legend')]"
        "//*[contains(@class,'item') or contains(@class,'label') or "
        "self::li or self::span or self::text]"
        "[string-length(normalize-space())>0] | "
        ".//*[local-name()='g'][contains(@class,'legend')]"
        "//*[local-name()='text' or local-name()='tspan']")

    # ── Usage Breakdown tabs ──────────────────────────────────────────────────
    # TODO: Confirm tab container and button classes via DevTools.
    USAGE_BREAKDOWN_SECTION = (By.XPATH,
        "//*[contains(normalize-space(),'Usage Breakdown') or "
        "contains(normalize-space(),'usage breakdown')]")

    TAB_BUTTONS = (By.XPATH,
        "//*[contains(@class,'tab') or @role='tab']"
        "[contains(normalize-space(),'Memberships') or "
        "contains(normalize-space(),'Paid Washes') or "
        "contains(normalize-space(),'Comp Washes')]")

    TAB_CONTENT = (By.XPATH,
        "//*[@role='tabpanel'] | "
        "//*[contains(@class,'tab-content') or contains(@class,'tabContent') or "
        "contains(@class,'tab-panel') or contains(@class,'tabPanel')]")

    TAB_BREAKDOWN_CARDS = (By.XPATH,
        "//*[@role='tabpanel']//*[contains(@class,'card') or "
        "contains(@class,'breakdown') or contains(@class,'item')] | "
        "//*[contains(@class,'tab') and contains(@class,'active')]"
        "//*[contains(@class,'card') or contains(@class,'breakdown')]")

    # ── Stale-element safe helpers ────────────────────────────────────────────

    def _safe_is_displayed(self, el):
        try:
            return el.is_displayed()
        except Exception:
            return False

    def _safe_text(self, el):
        try:
            return el.text.strip()
        except Exception:
            return ""

    def _safe_attr(self, el, attr):
        try:
            return el.get_attribute(attr) or ""
        except Exception:
            return ""

    # ── Frame helpers ─────────────────────────────────────────────────────────

    def _switch_to_frame(self):
        self.driver.switch_to.default_content()
        time.sleep(0.3)
        # If the filter controls are in the main document, no iframe switch needed.
        if self.driver.find_elements(By.CSS_SELECTOR,
                "[class*='overview__site-select__control'],[class*='nxt-multi-select__control']"):
            return
        # Try known WAC iframe src patterns only.
        # The "fallback to first iframe" is intentionally omitted — unrelated
        # tracking/analytics iframes (Intercom, HubSpot, etc.) would land
        # subsequent find_elements inside the wrong frame context.
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
        # No known iframe found — stay in default content.

    # ── Page lifecycle ────────────────────────────────────────────────────────

    def wait_for_modal(self):
        """Wait for the blocking filter modal to be interactive."""
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
        """Return True when the blocking filter modal is visible."""
        try:
            els = self.driver.find_elements(*self.APPLY_BUTTON)
            for el in els:
                try:
                    if el.is_displayed():
                        return True
                except Exception:
                    continue
            return False
        except Exception:
            return False

    def apply_modal_filters(self):
        """Click Apply filters and wait for the modal to dismiss and data to load."""
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON))
        btn.click()
        WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(self.APPLY_BUTTON))
        try:
            WebDriverWait(self.driver, 60).until(EC.invisibility_of_element_located(self.LOAD_MASK))
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

    def _wait_for_load(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.LOAD_MASK)
            )
        except TimeoutException:
            pass
        time.sleep(0.5)

    # ── Site filter ───────────────────────────────────────────────────────────

    def get_site_options(self):
        """Open the site multiselect and return visible option texts."""
        ctrl = self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
        self.driver.execute_script("""
            var ctrl = arguments[0];
            ctrl.dispatchEvent(new MouseEvent('mousedown',
                {bubbles:true, cancelable:true, view:window}));
        """, ctrl)
        time.sleep(0.5)
        try:
            WebDriverWait(self.driver, 15).until(
                lambda d: len(d.find_elements(By.XPATH,
                    "//*[@role='option'] | //*[contains(@class,'__option')]")) > 0
            )
        except TimeoutException:
            time.sleep(1.0)
        options = self.driver.execute_script("""
            var seen = {}; var result = [];
            Array.from(document.querySelectorAll('[role="option"]')).forEach(function(el) {
                if (el.offsetParent !== null) {
                    var t = (el.textContent || '').trim();
                    if (t && !seen[t]) { seen[t] = true; result.push(t); }
                }
            });
            return result;
        """) or []
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options

    def _get_site_input(self):
        """Re-fetch the site multiselect input element to avoid stale refs."""
        ctrl = self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
        try:
            return ctrl.find_element(By.XPATH, ".//input")
        except Exception:
            return ctrl

    def select_site(self, site_name, clear_first=True):
        """Select a site from the multiselect by typing to filter then clicking."""
        for _attempt in range(3):
            try:
                inner = self._get_site_input()
                ActionChains(self.driver).move_to_element(inner).click(inner).perform()
                break
            except StaleElementReferenceException:
                if _attempt == 2:
                    raise
                time.sleep(0.5)
        time.sleep(0.3)
        # Re-fetch after click — React may re-render the input on focus
        inner = self._get_site_input()
        if clear_first:
            inner.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
        inner.send_keys(site_name)
        time.sleep(0.4)
        option = WebDriverWait(self.driver, 20).until(
            lambda d: self._find_react_option(site_name)
        )
        self.driver.execute_script("arguments[0].click();", option)
        time.sleep(0.3)

    def get_site_chips(self):
        chips = self.driver.find_elements(*self.SITE_CHIPS)
        result = []
        for c in chips:
            if self._safe_is_displayed(c):
                t = self._safe_text(c)
                if t:
                    result.append(t)
        return result

    def clear_sites(self):
        """Remove all selected site chips."""
        try:
            ctrl = self.driver.find_elements(*self.SITE_MULTISELECT)
            if ctrl:
                ActionChains(self.driver).move_to_element(ctrl[0]).perform()
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
            removes = self.driver.find_elements(*self.SITE_CHIP_REMOVE)
            visible = [b for b in removes if b.is_displayed()]
            if not visible:
                break
            try:
                self.driver.execute_script("arguments[0].click();", visible[0])
                time.sleep(0.2)
            except Exception:
                break

    def site_overflow_chip_visible(self):
        """Return True when a +N overflow indicator is shown in the site control."""
        els = self.driver.find_elements(*self.SITE_OVERFLOW_CHIP)
        return any(self._safe_is_displayed(el) for el in els)

    # ── Date filter ───────────────────────────────────────────────────────────

    def _open_date_preset_dropdown(self):
        self.driver.execute_script("""
            var input = document.querySelector(
                'input[aria-readonly="true"][role="combobox"],'
                + 'input[inputmode="none"][role="combobox"]'
            );
            if (!input) return;
            var el = input.parentElement;
            while (el && !el.className.includes('-control')) el = el.parentElement;
            if (el) el.dispatchEvent(new MouseEvent('mousedown',
                {bubbles:true, cancelable:true, view:window}));
        """)
        time.sleep(0.5)

    def select_date_preset(self, preset):
        """Select a named preset from the date preset combobox."""
        self._open_date_preset_dropdown()
        option = WebDriverWait(self.driver, 10).until(
            lambda d: self._find_react_option(preset)
        )
        self.driver.execute_script("arguments[0].click();", option)
        time.sleep(0.3)

    def get_date_preset_options(self):
        """Open the date preset dropdown and return all visible option texts."""
        self._open_date_preset_dropdown()
        options = self.driver.execute_script("""
            return Array.from(document.querySelectorAll(
                '[role="option"],[class*="-option"],[class*="__option"]'
            )).filter(function(el) {
                return el.offsetParent !== null && el.textContent.trim();
            }).map(function(el) { return el.textContent.trim(); });
        """) or []
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options

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

    # ── Export ────────────────────────────────────────────────────────────────

    def export_xlsx_button_visible(self):
        els = self.driver.find_elements(*self.EXPORT_XLSX_BUTTON)
        return any(self._safe_is_displayed(el) for el in els)

    def click_export_xlsx(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.EXPORT_XLSX_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(2.0)

    # ── Generic helpers ───────────────────────────────────────────────────────

    def widget_section_visible(self, keyword):
        """Return True if any visible element's text contains *keyword*."""
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(normalize-space(),'%s')]" % keyword)
        return any(self._safe_is_displayed(el) for el in els)

    def _text_visible(self, keyword):
        return self.widget_section_visible(keyword)

    def no_data_message_visible(self):
        els = self.driver.find_elements(*self.NO_DATA_MESSAGE)
        return any(self._safe_is_displayed(el) for el in els)

    # ── KPI cards ─────────────────────────────────────────────────────────────

    def kpi_card_visible(self, label):
        """Return True if a KPI card with *label* text is visible on the page."""
        # TODO: Tighten to KPI card container class after DevTools inspection.
        return self._text_visible(label)

    def kpi_values_non_zero(self):
        """Heuristic: at least one non-zero numeric value present in body."""
        body = self.get_body_text()
        return bool(re.findall(r"\b([1-9]\d*)\b", body))

    def get_kpi_value(self, label):
        """Return the numeric value of a KPI card as an int (0 if not found).

        TODO: Tighten to KPI card DOM after DevTools inspection — currently uses
        body-text proximity heuristic.
        """
        body = self.get_body_text()
        lines = body.split("\n")
        for i, line in enumerate(lines):
            if label.lower() in line.lower():
                # Search on the label line and the next 3 lines only (not before)
                # to avoid picking up the numeric value from the previous KPI card.
                for j in range(i, min(len(lines), i + 4)):
                    m = re.search(r"\b(\d+)\b", lines[j])
                    if m:
                        try:
                            return int(m.group(1))
                        except ValueError:
                            pass
        return 0

    def kpi_sublabel_visible(self, card_label, sublabel):
        """Return True if *sublabel* appears near *card_label* in the body.

        TODO: Tighten to KPI card subtree after DevTools inspection.
        """
        body = self.get_body_text()
        lines = body.split("\n")
        for i, line in enumerate(lines):
            if card_label.lower() in line.lower():
                window = "\n".join(lines[max(0, i - 3):i + 5])
                if sublabel.lower() in window.lower():
                    return True
        return False

    # ── Hourly Distribution chart ─────────────────────────────────────────────

    def chart_section_visible(self):
        """Return True if the Hourly Distribution chart section is visible."""
        els = self.driver.find_elements(*self.CHART_SECTION)
        return any(self._safe_is_displayed(el) for el in els)

    def chart_has_bars(self):
        """Return True if the chart contains visible SVG bar elements with height > 1px."""
        bars = self.driver.find_elements(By.XPATH,
            "//*[local-name()='svg']//*[local-name()='rect']")
        for b in bars:
            try:
                if not b.is_displayed():
                    continue
                cls = (b.get_attribute("class") or "").lower()
                if any(x in cls for x in ("background", "grid", "overlay", "clip", "mask")):
                    continue
                h_attr = b.get_attribute("height") or "0"
                try:
                    h = float(re.sub(r"[^0-9.]", "", h_attr) or "0")
                except ValueError:
                    h = 0
                if h > 1:
                    return True
            except Exception:
                continue
        return False

    def get_chart_legend_items(self):
        """Return visible legend item elements from the Hourly Distribution chart."""
        items = self.driver.find_elements(*self.CHART_LEGEND_ITEMS)
        result = []
        for el in items:
            if self._safe_is_displayed(el) and self._safe_text(el):
                result.append(el)
        return result

    def toggle_chart_legend_item(self, label):
        """Click a legend item by label using ActionChains (required for SVG targets).

        WAC-CHT-006/007: move_to_element_with_offset() is used instead of a
        plain click() because SVG <text>/<tspan> nodes do not reliably receive
        synthetic click events in headless Chrome.
        """
        items = self.get_chart_legend_items()
        target = next(
            (el for el in items if label.lower() in el.text.lower()), None
        )
        if target is None:
            # Fallback: search all visible elements for the label text near the chart.
            all_els = self.driver.find_elements(By.XPATH,
                "//*[normalize-space()='%s' or contains(normalize-space(),'%s')]"
                % (label, label))
            target = next((el for el in all_els if el.is_displayed()), None)
        if target is None:
            raise ValueError("Chart legend item '%s' not found" % label)
        ActionChains(self.driver)\
            .move_to_element_with_offset(target, 5, 5)\
            .click()\
            .perform()
        time.sleep(0.5)

    def chart_legend_item_has_strikethrough(self, label):
        """Return True when the legend item for *label* has strikethrough styling.

        Covers both CSS text-decoration and common inactive/disabled class patterns.
        """
        items = self.get_chart_legend_items()
        target = next(
            (el for el in items if label.lower() in el.text.lower()), None
        )
        if target is None:
            return False
        style = target.get_attribute("style") or ""
        cls = target.get_attribute("class") or ""
        computed = self.driver.execute_script(
            "return window.getComputedStyle(arguments[0]).textDecoration;", target
        ) or ""
        return (
            "line-through" in style
            or "line-through" in computed
            or any(kw in cls for kw in ("strikethrough", "inactive", "disabled", "hidden"))
        )

    # ── Usage Breakdown tabs ──────────────────────────────────────────────────

    def usage_breakdown_visible(self):
        """Return True if the Usage Breakdown section is visible."""
        els = self.driver.find_elements(*self.USAGE_BREAKDOWN_SECTION)
        if any(self._safe_is_displayed(el) for el in els):
            return True
        return self._text_visible("Usage Breakdown")

    def get_tab_labels(self):
        """Return text labels of all visible Usage Breakdown tab buttons."""
        tabs = self.driver.find_elements(*self.TAB_BUTTONS)
        result = []
        for t in tabs:
            if self._safe_is_displayed(t):
                txt = self._safe_text(t)
                if txt:
                    result.append(txt)
        return result

    def get_active_tab_label(self):
        """Return the label of the currently active tab.

        TODO: Confirm active-tab CSS class or aria-selected via DevTools.
        """
        tabs = self.driver.find_elements(*self.TAB_BUTTONS)
        for tab in tabs:
            if not self._safe_is_displayed(tab):
                continue
            cls  = self._safe_attr(tab, "class")
            aria = self._safe_attr(tab, "aria-selected")
            data = self._safe_attr(tab, "data-active")
            if (
                any(kw in cls for kw in ("active", "selected", "current"))
                or aria.lower() == "true"
                or data.lower() == "true"
            ):
                return self._safe_text(tab)
        return ""

    def click_tab(self, tab_name):
        """Click the Usage Breakdown tab with the given label."""
        tabs = self.driver.find_elements(*self.TAB_BUTTONS)
        for tab in tabs:
            if self._safe_is_displayed(tab) and tab_name.lower() in self._safe_text(tab).lower():
                self.driver.execute_script("arguments[0].click();", tab)
                time.sleep(1.5)
                return
        raise ValueError("Tab '%s' not found in Usage Breakdown" % tab_name)

    def tab_has_active_class(self, tab_name):
        """Return True if the tab button for *tab_name* has an active indicator."""
        tabs = self.driver.find_elements(*self.TAB_BUTTONS)
        for tab in tabs:
            if self._safe_is_displayed(tab) and tab_name.lower() in self._safe_text(tab).lower():
                cls  = self._safe_attr(tab, "class")
                aria = self._safe_attr(tab, "aria-selected")
                data = self._safe_attr(tab, "data-active")
                return (
                    any(kw in cls for kw in ("active", "selected", "current"))
                    or aria.lower() == "true"
                    or data.lower() == "true"
                )
        return False

    def tab_content_visible(self, tab_name):
        """Return True if content related to *tab_name* is visible on the page."""
        return self._text_visible(tab_name)

    def get_tab_count(self, tab_name):
        """Return the numeric item count displayed in the *tab_name* tab button.

        Many tabs show a count badge like "Memberships (5)". Falls back to
        body-text proximity if no count is in the tab button text.
        TODO: Confirm count element class via DevTools.
        """
        tabs = self.driver.find_elements(*self.TAB_BUTTONS)
        for tab in tabs:
            if self._safe_is_displayed(tab) and tab_name.lower() in self._safe_text(tab).lower():
                txt = self._safe_text(tab)
                m = re.search(r"\b(\d+)\b", txt)
                if m:
                    return int(m.group(1))
        # Fallback: search body text on and after the tab-name line only.
        body = self.get_body_text()
        lines = body.split("\n")
        for i, line in enumerate(lines):
            if tab_name.lower() in line.lower():
                for j in range(i, min(len(lines), i + 4)):
                    m = re.search(r"\b(\d+)\b", lines[j])
                    if m:
                        return int(m.group(1))
        return 0

    def breakdown_cards_present(self, tab_name):
        """Return True if the active tab content shows breakdown cards/items.

        TODO: Tighten to breakdown card container after DevTools inspection.
        """
        self.click_tab(tab_name)
        content_els = self.driver.find_elements(*self.TAB_BREAKDOWN_CARDS)
        return any(el.is_displayed() for el in content_els)

    def breakdown_is_empty(self, tab_name):
        """Return True when a tab shows no breakdown cards (empty/zero-data state)."""
        self.click_tab(tab_name)
        content_els = self.driver.find_elements(*self.TAB_BREAKDOWN_CARDS)
        has_cards = any(el.is_displayed() for el in content_els)
        return not has_cards or self.no_data_message_visible()

    # ── Tab / KPI reconciliation utility ─────────────────────────────────────

    def assert_tab_kpi_reconciliation(self, tab_name, kpi_label):
        """Assert that the count in *tab_name* equals the *kpi_label* KPI card value.

        Used by WAC-MEM-004, WAC-PWS-002 (xfail), WAC-CMP-004.
        Returns (tab_count, kpi_value) for the caller to use in the assertion message.
        """
        self.click_tab(tab_name)
        tab_count = self.get_tab_count(tab_name)
        kpi_value = self.get_kpi_value(kpi_label)
        assert tab_count == kpi_value, (
            "Tab '%s' count (%d) does not match KPI '%s' value (%d)"
            % (tab_name, tab_count, kpi_label, kpi_value)
        )
        return tab_count, kpi_value
