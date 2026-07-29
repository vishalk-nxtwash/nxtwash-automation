import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class AdminGeneralSalesReportPage(BasePage):

    FRAME = (By.XPATH, "//iframe[contains(@src,'general-sales-report')]")

    # ── Filter bar ────────────────────────────────────────────────────────────
    # Confirmed class names from DevTools (July 2026):
    #   Sites:       nxt-multi-select__control
    #   Date preset: nxt-select__control
    SITE_MULTISELECT = (By.XPATH,
        "//div[contains(@class,'nxt-multi-select__control')]")

    DATE_PRESET_COMBOBOX = (By.XPATH,
        "//div[contains(@class,'nxt-select__control')]"
        "[not(contains(@class,'nxt-multi-select__control'))]")

    # Confirmed from DevTools: single combined text input, value format MM/DD/YYYY - MM/DD/YYYY
    DATE_RANGE_INPUT = (By.XPATH, "//input[@placeholder='Select date range']")

    # react-day-picker calendar buttons (class confirmed from DevTools)
    CALENDAR_DAY_BUTTON = (By.XPATH, "//*[contains(@class,'rdp-day_button')]")

    APPLY_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters'] | "
        "//button[normalize-space()='Apply'] | "
        "//button[contains(normalize-space(),'Apply filters')]")

    EXPORT_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Choose option')] | "
        "//button[contains(normalize-space(),'Export') and "
        "not(contains(normalize-space(),'format'))]")

    EXPORT_MODAL = (By.XPATH,
        "//*[@role='dialog'] | "
        "//*[contains(@class,'modal') and "
        "(contains(@class,'show') or contains(@class,'open') or "
        "contains(@class,'visible'))]")

    EXPORT_MODAL_OPTIONS = (By.XPATH,
        "(//*[@role='dialog'] | //*[contains(@class,'modal') and "
        "contains(@class,'show')])//*[@role='button' or @type='button' or "
        "contains(@class,'option') or contains(@class,'export-type') or "
        "contains(@class,'format')] | "
        "(//*[@role='dialog'] | //*[contains(@class,'modal') and "
        "contains(@class,'show')])//*[self::li or self::label]")

    REDEMPTIONS_FULL_REPORT_LINK = (By.XPATH,
        "//a[contains(normalize-space(),'Full report')] | "
        "//a[contains(normalize-space(),'full report')] | "
        "//button[contains(normalize-space(),'Full report')]")

    SITE_CHIP_CLEAR = (By.XPATH,
        "//div[contains(@class,'nxt-multi-select__multi-value__remove')] | "
        "//div[contains(@class,'nxt-multi-select__clear-indicator')]")

    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and "
        "not(contains(@style,'display: none') or "
        "contains(@style,'display:none'))] | "
        "//*[contains(@class,'spinner') and "
        "not(contains(@style,'display: none') or "
        "contains(@style,'display:none'))]")

    def _switch_to_frame(self):
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it(self.FRAME)
            )
        except TimeoutException:
            pass

    def wait_for_loaded(self):
        self._switch_to_frame()
        self.wait.until(EC.presence_of_element_located(self.APPLY_BUTTON))
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

    # ── Site filter helpers ───────────────────────────────────────────────────

    def select_site(self, site_name):
        # Dependency: Sites & Locations module
        self.open_filter_popup()
        self.select_react_dropdown_option(self.SITE_MULTISELECT, site_name)

    def select_multiple_sites(self, site_names):
        # Dependency: Sites & Locations module
        self.open_filter_popup()
        for name in site_names:
            self.select_react_dropdown_option(
                self.SITE_MULTISELECT, name, clear_first=False
            )

    def clear_site_selection(self):
        self.open_filter_popup()
        chips = self.driver.find_elements(*self.SITE_CHIP_CLEAR)
        for chip in chips:
            try:
                self.driver.execute_script("arguments[0].click();", chip)
                time.sleep(0.2)
            except Exception:
                pass

    # getBoundingClientRect works for any CSS position (fixed, absolute, relative)
    # and correctly reports zero dimensions for hidden elements.
    _COLLECT_OPTIONS_JS = """
        return Array.from(document.querySelectorAll(
            '[role="option"],[class*="__option"],[class*="-option"]'
        )).filter(function(el){
            var r = el.getBoundingClientRect();
            return r.width > 0 && r.height > 0 && el.textContent.trim();
        }).map(function(el){ return el.textContent.trim(); });
    """

    # ── Filter popup helpers ──────────────────────────────────────────────────

    def _is_filter_popup_open(self):
        """Return True if the filter popup is currently visible."""
        try:
            WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(self.APPLY_BUTTON)
            )
            return True
        except TimeoutException:
            return False

    def close_filter_popup(self):
        """Dismiss the filter popup if it is open (press Escape)."""
        if not self._is_filter_popup_open():
            return
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.3)
        except Exception:
            pass

    def open_filter_popup(self):
        """Ensure the filter popup is open before any filter interaction.

        The popup auto-opens on page load and closes after Apply is clicked.
        Re-opening it requires clicking the compact filter bar. If both compact
        bar clicks fail to surface the Apply button, a page refresh is used as
        a guaranteed fallback — the popup always auto-opens on fresh page load.
        """
        if self._is_filter_popup_open():
            return
        # First attempt: click the site multiselect in the compact bar.
        try:
            trigger = self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
            self.driver.execute_script("arguments[0].click();", trigger)
            WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable(self.APPLY_BUTTON)
            )
            return
        except TimeoutException:
            pass
        # Close any dropdown that may have opened instead of the popup.
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        time.sleep(0.3)
        # Second attempt: click the date preset control.
        try:
            trigger2 = self.wait.until(
                EC.element_to_be_clickable(self.DATE_PRESET_COMBOBOX)
            )
            self.driver.execute_script("arguments[0].click();", trigger2)
            WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable(self.APPLY_BUTTON)
            )
            return
        except TimeoutException:
            pass
        # Final fallback: refresh the page — popup always auto-opens on load.
        self.driver.refresh()
        self._switch_to_frame()
        self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON))

    # ── Site filter helpers ───────────────────────────────────────────────────

    def get_site_options(self):
        # Dependency: Sites & Locations module
        self.open_filter_popup()
        combo = self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
        # The outer control div click is intercepted by the inner input-container.
        # JS-click the inner search input directly, then send space+backspace to
        # trigger React Select's onInputChange which opens the dropdown while
        # leaving the filter text empty.
        try:
            inner = combo.find_element(By.XPATH, ".//input")
            self.driver.execute_script("arguments[0].click();", inner)
            inner.send_keys(" ")
            inner.send_keys(Keys.BACKSPACE)
        except Exception:
            self.driver.execute_script("arguments[0].click();", combo)
        # Wait for the menu container, then collect options via Selenium
        # find_elements (avoids JS timing races with zero-dimension elements).
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

    # ── Date filter helpers ───────────────────────────────────────────────────

    def select_date_preset(self, preset):
        self.open_filter_popup()
        self.select_react_dropdown_option(self.DATE_PRESET_COMBOBOX, preset)

    def get_date_preset_options(self):
        self.open_filter_popup()
        combo = self.wait.until(EC.element_to_be_clickable(self.DATE_PRESET_COMBOBOX))
        # Same pattern as get_site_options: JS-click inner input, space+backspace
        # to trigger React Select open without filtering the list.
        try:
            inner = combo.find_element(By.XPATH, ".//input")
            self.driver.execute_script("arguments[0].click();", inner)
            inner.send_keys(" ")
            inner.send_keys(Keys.BACKSPACE)
        except Exception:
            self.driver.execute_script("arguments[0].click();", combo)
        # Wait for the date preset menu, then collect via Selenium find_elements.
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

    def enter_custom_date_range(self, start, end):
        self.open_filter_popup()
        combined = "%s - %s" % (start, end)
        el = self.wait.until(EC.element_to_be_clickable(self.DATE_RANGE_INPUT))
        el.send_keys(Keys.CONTROL + "a" + Keys.BACKSPACE)
        el.send_keys(combined)
        el.send_keys(Keys.TAB)

    def get_date_range_values(self):
        """Return (start, end) by splitting the single date range field value."""
        try:
            el = self.driver.find_element(*self.DATE_RANGE_INPUT)
            value = el.get_attribute("value") or ""
            if " - " in value:
                start, end = value.split(" - ", 1)
                return start.strip(), end.strip()
            return value, value
        except Exception:
            return ("", "")

    def apply_filters(self):
        self.open_filter_popup()
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(1.5)
        try:
            self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        except TimeoutException:
            pass

    # ── Section / card helpers ────────────────────────────────────────────────

    def section_heading_visible(self, heading):
        return heading.lower() in self.get_body_text().lower()

    def expand_collapsible_section(self, section_name):
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(normalize-space(),'%s')]"
            "[@aria-expanded or @data-bs-toggle or @role='button']" % section_name)
        if not els:
            return
        hdr = els[0]
        if hdr.get_attribute("aria-expanded") != "true":
            self.driver.execute_script("arguments[0].click();", hdr)
            time.sleep(0.5)

    def section_is_expanded(self, section_name):
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(normalize-space(),'%s')][@aria-expanded]" % section_name)
        return bool(els) and els[0].get_attribute("aria-expanded") == "true"

    def get_table_column_headers(self, table_keyword):
        """Return visible column header texts from the table nearest to table_keyword."""
        try:
            ths = self.driver.find_elements(By.XPATH,
                "//*[contains(normalize-space(),'%s')]"
                "/following::table[1]//th" % table_keyword)
            visible = [th.text.strip() for th in ths
                       if th.is_displayed() and th.text.strip()]
            if visible:
                return visible
            roles = self.driver.find_elements(By.XPATH,
                "//*[contains(normalize-space(),'%s')]"
                "/following::*[@role='columnheader'][position()<=20]" % table_keyword)
            return [r.text.strip() for r in roles
                    if r.is_displayed() and r.text.strip()]
        except Exception:
            return []

    def count_card_line_items(self, card_title):
        """Count dollar-value lines inside the revenue card for card_title."""
        try:
            items = self.driver.find_elements(By.XPATH,
                "//*[contains(normalize-space(),'%s')]"
                "/following::*[contains(normalize-space(),'$')][position()<=30]"
                % card_title)
            return len([i for i in items if i.is_displayed()])
        except Exception:
            return 0

    def sub_card_count_after_expand(self, section_name):
        """Expand section_name and count visible child card-like containers."""
        self.expand_collapsible_section(section_name)
        time.sleep(0.5)
        try:
            cards = self.driver.find_elements(By.XPATH,
                "//*[contains(normalize-space(),'%s')]"
                "/following::*[contains(@class,'card') or "
                "contains(@class,'tile') or contains(@class,'widget') or "
                "contains(@class,'summary')][position()<=10]" % section_name)
            return len([c for c in cards if c.is_displayed()])
        except Exception:
            return 0

    # ── Export helpers ────────────────────────────────────────────────────────

    def click_export_button(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.EXPORT_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)

    def export_modal_is_open(self):
        els = self.driver.find_elements(*self.EXPORT_MODAL)
        return any(e.is_displayed() for e in els)

    def get_export_modal_option_count(self):
        self.wait.until(lambda d: self.export_modal_is_open())
        time.sleep(0.5)
        options = self.driver.find_elements(*self.EXPORT_MODAL_OPTIONS)
        return len([o for o in options if o.is_displayed() and o.text.strip()])

    # ── Redemption / navigation helpers ──────────────────────────────────────

    def click_redemptions_full_report(self):
        # Dependency: Redemption Details page
        # Close the filter popup first — if open, it overlays the report content
        # and intercepts the click before it reaches the Full report link.
        self.close_filter_popup()
        link = self.wait.until(
            EC.element_to_be_clickable(self.REDEMPTIONS_FULL_REPORT_LINK)
        )
        self.driver.execute_script("arguments[0].click();", link)

    def rapid_preset_switch(self, presets):
        for preset in presets:
            self.select_date_preset(preset)
            time.sleep(0.2)


class AdminRedemptionDetailsPage(BasePage):

    FRAME = (By.XPATH,
        "//iframe[contains(@src,'redemption') or contains(@src,'Redemption')]")

    # The RDT page may use a different React Select class prefix than 'nxt-'.
    # Anchor by placeholder text / label so the locator works regardless of prefix.
    SITE_COMBOBOX = (By.XPATH,
        "//div[contains(@class,'__control') and "
        ".//div[contains(normalize-space(),'Select site to filter')]]")

    DATE_PRESET_COMBOBOX = (By.XPATH,
        "//*[normalize-space()='Date range presets']/following::div"
        "[contains(@class,'__control')][1]")

    DATE_RANGE_INPUT = (By.XPATH, "//input[@placeholder='Select date range']")

    SINGLE_DAY_CHECKBOX = (By.XPATH,
        "//input[@type='checkbox' and ("
        "contains(@name,'singleDay') or contains(@name,'single_day') or "
        "contains(@id,'single') or contains(@id,'singleDay'))] | "
        "//*[contains(normalize-space(),'Single day')]"
        "/ancestor::*[.//input[@type='checkbox']][1]//input[@type='checkbox']")

    APPLY_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters'] | "
        "//button[normalize-space()='Apply'] | "
        "//button[contains(normalize-space(),'Apply filters')]")

    EXPAND_ALL_BUTTON = (By.XPATH,
        "//button[contains(normalize-space(),'Expand all') or "
        "contains(normalize-space(),'Expand All') or "
        "contains(normalize-space(),'expand all')]")

    COLLAPSIBLE_SECTIONS = (By.XPATH,
        "//*[@aria-expanded][self::button or @role='button' or "
        "@data-bs-toggle]")

    LOAD_MASK = (By.XPATH,
        "//*[contains(@class,'load-mask') and "
        "not(contains(@style,'display: none') or "
        "contains(@style,'display:none'))] | "
        "//*[contains(@class,'spinner') and "
        "not(contains(@style,'display: none') or "
        "contains(@style,'display:none'))]")

    def _switch_to_frame(self):
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 5).until(
                EC.frame_to_be_available_and_switch_to_it(self.FRAME)
            )
        except TimeoutException:
            pass

    def wait_for_loaded(self):
        self._switch_to_frame()
        self.wait.until(EC.presence_of_element_located(self.APPLY_BUTTON))
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

    def filter_panel_is_visible(self):
        body = self.get_body_text().lower()
        return "apply" in body and "filter" in body

    def select_site(self, site_name):
        # Dependency: Sites & Locations module
        self.select_react_dropdown_option(self.SITE_COMBOBOX, site_name)

    def select_date_preset(self, preset):
        self.select_react_dropdown_option(self.DATE_PRESET_COMBOBOX, preset)

    def get_date_preset_options(self):
        combo = self.wait.until(EC.element_to_be_clickable(self.DATE_PRESET_COMBOBOX))
        self.driver.execute_script("arguments[0].click();", combo)
        time.sleep(0.5)
        options = self.driver.execute_script(AdminGeneralSalesReportPage._COLLECT_OPTIONS_JS)
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options or []

    def get_date_range_values(self):
        try:
            el = self.driver.find_element(*self.DATE_RANGE_INPUT)
            value = el.get_attribute("value") or ""
            if " - " in value:
                start, end = value.split(" - ", 1)
                return start.strip(), end.strip()
            return value, value
        except Exception:
            return ("", "")

    def enable_custom_date_entry(self):
        """Select the Custom option to reveal manual date inputs."""
        self.select_react_dropdown_option(self.DATE_PRESET_COMBOBOX, "Custom")

    def toggle_single_day(self):
        el = self.wait.until(EC.element_to_be_clickable(self.SINGLE_DAY_CHECKBOX))
        self.driver.execute_script("arguments[0].click();", el)

    def apply_filters(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(1.5)
        try:
            self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        except TimeoutException:
            pass

    def click_expand_all(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.EXPAND_ALL_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(0.5)

    def get_visible_section_count(self):
        sections = self.driver.find_elements(*self.COLLAPSIBLE_SECTIONS)
        return len([s for s in sections if s.is_displayed()])
