import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class CardDeclinesPage(BasePage):

    # TODO: Confirm iframe src pattern via DevTools before first run.
    _FRAME_SRC_PATTERNS = ["cc-declines", "cc_declines", "card-declines", "card_declines", "declines"]

    # ── Filter / header controls ──────────────────────────────────────────────
    # DOM confirmed 2026-07-12 via DevTools inspection.

    APPLY_BUTTON = (By.XPATH,
        "//button[normalize-space()='Apply filters'] | "
        "//button[contains(normalize-space(),'Apply filters')]")

    # Site/location multiselect — prefix: overview__site-select__
    # (NOT nxt-multi-select__ used by other report pages)
    SITE_MULTISELECT = (By.XPATH,
        "//div[contains(@class,'overview__site-select__control')]")

    # The typeable search input inside the site multiselect.
    SITE_INPUT = (By.XPATH,
        "//input[contains(@class,'overview__site-select__input')]")

    # Date preset combobox — uses a non-typeable dummy input (inputmode='none',
    # aria-readonly='true').  Targeted by ARIA attributes rather than an
    # emotion-hash class (emotion hashes change between builds).
    DATE_PRESET_COMBOBOX = (By.XPATH,
        "//input[@inputmode='none' and @role='combobox']"
        "/ancestor::div[contains(@class,'-control')][1]")

    # Date range input — readonly; placeholder confirmed as 'Select range of dates'.
    # Cannot be typed into directly — clicking opens the calendar picker.
    # Value format: "Monday, MM/DD/YYYY - Tuesday, MM/DD/YYYY"
    DATE_RANGE_INPUT = (By.XPATH,
        "//input[@placeholder='Select range of dates']")

    # Single day checkbox — class confirmed as header-widget__title__descr_checkbox.
    MODAL_SINGLE_DAY_CHECKBOX = (By.XPATH,
        "//input[contains(@class,'header-widget__title__descr_checkbox')]")

    # ── Site chips ────────────────────────────────────────────────────────────

    SITE_CHIPS = (By.XPATH,
        "//div[contains(@class,'overview__site-select__multi-value__label')]")

    SITE_CLEAR_BTN = (By.XPATH,
        "//div[contains(@class,'overview__site-select__clear-indicator')]")

    # ── Page-bar single day checkbox ──────────────────────────────────────────
    # Same class as modal checkbox — CDL appears to use a single persistent
    # filter header rather than a blocking modal.
    # TODO: Confirm whether a separate page-bar instance exists via DevTools.
    PAGE_BAR_SINGLE_DAY_CHECKBOX = (By.XPATH,
        "//input[contains(@class,'header-widget__title__descr_checkbox')]")

    # ── Load mask / spinner ───────────────────────────────────────────────────

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
        # CDL filter header lives in the main document — confirm before trying any frame.
        if self.driver.find_elements(By.CSS_SELECTOR, ".overview__site-select__control"):
            return
        for pattern in self._FRAME_SRC_PATTERNS:
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.XPATH, "//iframe[contains(@src,'%s')]" % pattern)
                    )
                )
                # Verify CDL content is actually in this frame before committing.
                if self.driver.find_elements(By.CSS_SELECTOR, ".overview__site-select__control"):
                    return
                self.driver.switch_to.default_content()
            except TimeoutException:
                pass
        # No matching frame found — stay in default_content rather than
        # blindly switching to frames[0], which could be a tracking/chat iframe.

    # ── Page lifecycle ────────────────────────────────────────────────────────

    def wait_for_modal(self):
        """Wait for the Card Declines filter header to be ready.

        CDL uses a persistent filter header (not a blocking modal dialog).
        We wait for the site multiselect to be clickable as the readiness
        signal instead of an Apply-filters button.
        """
        self._switch_to_frame()
        try:
            self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
        except TimeoutException:
            # Fallback: wait for the date preset combobox
            try:
                self.wait.until(EC.element_to_be_clickable(self.DATE_PRESET_COMBOBOX))
            except TimeoutException:
                pass
        try:
            self.wait.until(EC.invisibility_of_element_located(self.LOAD_MASK))
        except TimeoutException:
            pass

    def modal_is_open(self):
        """CDL uses an inline filter header — always present after page load.

        Returns True if the site multiselect control is visible, which signals
        that the filter header has rendered.
        """
        try:
            els = self.driver.find_elements(*self.SITE_MULTISELECT)
            return any(e.is_displayed() for e in els)
        except Exception:
            return False

    def get_body_text(self):
        # JS innerText avoids StaleElementReferenceException — no Python-side
        # DOM reference is held across React re-renders.
        try:
            return self.driver.execute_script("return document.body.innerText;") or ""
        except Exception:
            self.driver.switch_to.default_content()
            return self.driver.execute_script("return document.body.innerText;") or ""

    def get_current_url(self):
        return self.driver.current_url

    # ── Site filter ───────────────────────────────────────────────────────────

    def get_site_options(self):
        """Open the site dropdown and return visible option texts via JS.

        React Select may render the menu in a portal (position:fixed) so
        offsetParent is null for portal options.  We use getBoundingClientRect
        instead to detect visible elements.  Click the dropdown-indicator arrow
        rather than the inner input for a more reliable React open event.
        """
        ctrl = self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
        try:
            indicator = ctrl.find_element(
                By.XPATH,
                ".//div[contains(@class,'overview__site-select__dropdown-indicator')]"
            )
            ActionChains(self.driver).move_to_element(indicator).click(indicator).perform()
        except Exception:
            inputs = ctrl.find_elements(By.XPATH, ".//input")
            target = inputs[0] if inputs else ctrl
            ActionChains(self.driver).move_to_element(target).click(target).perform()
        time.sleep(0.8)
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script(
                    "return document.querySelectorAll('[role=\"option\"]').length > 0;"
                )
            )
        except TimeoutException:
            pass
        options = self.driver.execute_script("""
            return Array.from(document.querySelectorAll(
                '[role="option"], [class*="__option"], [class*="-option"]'
            ))
            .filter(function(el) {
                var r = el.getBoundingClientRect();
                return (r.width > 0 || r.height > 0) && el.textContent.trim();
            })
            .map(function(el) { return el.textContent.trim(); });
        """)
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return options or []

    def _get_site_inner_input(self):
        """Re-find the site multiselect's typeable input (safe after React re-renders)."""
        ctrl = self.wait.until(EC.element_to_be_clickable(self.SITE_MULTISELECT))
        try:
            return ctrl.find_element(
                By.XPATH, ".//input[contains(@class,'overview__site-select__input')]"
            )
        except Exception:
            return ctrl.find_element(By.XPATH, ".//input")

    def select_site(self, site_name, clear_first=True):
        """Select *site_name* from the site/location multiselect.

        Clicks the typeable overview__site-select__input, types the site name
        to filter, then clicks the matching option.  Re-finds the inner input
        after click and after clear to survive React re-renders.
        """
        inner = self._get_site_inner_input()
        ActionChains(self.driver).move_to_element(inner).click(inner).perform()
        time.sleep(0.3)
        # Re-find after click — React may re-render the input container.
        inner = self._get_site_inner_input()
        if clear_first:
            try:
                inner.send_keys(Keys.COMMAND + "a")
                inner.send_keys(Keys.BACKSPACE)
            except StaleElementReferenceException:
                inner = self._get_site_inner_input()
                inner.send_keys(Keys.COMMAND + "a")
                inner.send_keys(Keys.BACKSPACE)
        try:
            inner.send_keys(site_name)
        except StaleElementReferenceException:
            inner = self._get_site_inner_input()
            inner.send_keys(site_name)
        time.sleep(0.3)
        # Atomic JS find-and-click avoids StaleElementReferenceException —
        # finding the element and clicking it in one script call leaves no gap
        # for React to re-render and invalidate the reference.
        WebDriverWait(self.driver, 20).until(
            lambda d: d.execute_script("""
                var text = arguments[0].toLowerCase().trim();
                var candidates = Array.from(document.querySelectorAll(
                    '[role="option"], [class*="__option"], [class*="-option"], [class*="select__option"]'
                ));
                var target = candidates.find(function(el) {
                    var r = el.getBoundingClientRect();
                    return r.height > 0 && el.textContent.trim().toLowerCase() === text;
                });
                if (target) { target.click(); return true; }
                return false;
            """, site_name)
        )
        time.sleep(0.3)

    def get_site_chips(self):
        chips = self.driver.find_elements(*self.SITE_CHIPS)
        result = []
        for c in chips:
            try:
                if c.is_displayed() and c.text.strip():
                    result.append(c.text.strip())
            except StaleElementReferenceException:
                pass
        return result

    def clear_sites(self):
        """Remove all selected site chips.

        CDL has no global clear-all button — all sites are pre-selected
        individually.  We click each chip's remove (×) button one at a time
        until no chip remove buttons remain.
        """
        # Try clear-all indicator first (may appear when hovering the control)
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
        # Fallback: click chip remove buttons one by one
        for _ in range(30):  # safety limit
            remove_btns = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'overview__site-select__multi-value__remove')]"
            )
            visible = [b for b in remove_btns if b.is_displayed()]
            if not visible:
                break
            try:
                self.driver.execute_script("arguments[0].click();", visible[0])
                time.sleep(0.2)
            except Exception:
                break

    def all_sites_selected_by_default(self):
        """CDL pre-selects all sites individually (no 'All Sites' aggregate chip).

        Returns True when multiple chips are present or the +N overflow count
        indicator is visible, indicating the default all-sites-selected state.
        """
        chips = self.get_site_chips()
        if len(chips) > 1:
            return True
        least_count = self.driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'overview__site-select__multi-value__least-count')]"
        )
        return any(el.is_displayed() for el in least_count)

    # ── Date filter ───────────────────────────────────────────────────────────

    def _open_date_preset_dropdown(self):
        """Open the date preset React Select dropdown.

        The DummyInput (inputmode=none) has transform:scale(0) — clicking it
        or its ancestor div via ActionChains does not trigger React's synthetic
        open handler.  Instead: focus the DummyInput via JS (it has tabindex=0)
        then dispatch an ARROW_DOWN key action, which is React Select's standard
        keyboard shortcut to open a non-searchable select.
        """
        date_input = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@inputmode='none' and @role='combobox']")
            )
        )
        self.driver.execute_script("arguments[0].focus();", date_input)
        time.sleep(0.2)
        ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).perform()
        time.sleep(0.5)

    def select_date_preset(self, preset):
        """Select a named preset from the date preset combobox.

        The combobox uses a dummy (aria-readonly) input — typing to filter is
        not supported.  Opens via JS mousedown then clicks the matching option.
        """
        self._open_date_preset_dropdown()
        option = WebDriverWait(self.driver, 10).until(
            lambda d: self._find_react_option(preset)
        )
        self.driver.execute_script("arguments[0].click();", option)
        time.sleep(0.3)

    def get_date_preset_options(self):
        """Open the date preset dropdown and return visible option texts."""
        self._open_date_preset_dropdown()
        options = self.driver.execute_script("""
            return Array.from(document.querySelectorAll(
                '[role="option"], [class*="-option"], [class*="__option"]'
            )).filter(function(el) {
                return el.offsetParent !== null && el.textContent.trim();
            }).map(function(el) { return el.textContent.trim(); });
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

    def enter_date_range(self, start, end):
        """Not available on Card Declines — the date range input is readonly.

        Clicking the input opens a calendar picker.  Direct keyboard entry is
        not supported by this control.  The cdl_zero_data fixture currently
        cannot set a custom date range via this method.
        TODO: Implement calendar-picker interaction after DevTools inspection.
        """
        raise NotImplementedError(
            "CDL date range input is readonly (placeholder='Select range of dates').  "
            "Calendar interaction is required to set a custom range."
        )

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

    # ── Apply ─────────────────────────────────────────────────────────────────

    def apply_modal_filters(self):
        """Apply the current filter header selections.

        CDL uses an inline filter header rather than a blocking modal.  If an
        Apply-filters button is present, click it; otherwise the filters apply
        automatically (e.g. on preset selection or site chip close) and we just
        wait briefly for any load mask to clear.
        TODO: Confirm whether an Apply button exists on CDL via DevTools.
        """
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.APPLY_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", btn)
        except TimeoutException:
            # No Apply button — filters are applied automatically.
            pass
        time.sleep(1.5)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.LOAD_MASK)
            )
        except TimeoutException:
            pass

    # ── Generic widget / section visibility ───────────────────────────────────

    def widget_section_visible(self, keyword):
        """Return True if any visible element contains *keyword* (case-sensitive)."""
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(normalize-space(),'%s')]" % keyword
        )
        for el in els:
            try:
                if el.is_displayed():
                    return True
            except StaleElementReferenceException:
                pass
        return False

    def _text_visible(self, keyword):
        return self.widget_section_visible(keyword)

    # ── Glossary widget ───────────────────────────────────────────────────────

    def glossary_section_visible(self):
        # TODO: Confirm heading text via DevTools — may be "Glossary" or "Terms".
        return self._text_visible("Glossary") or self._text_visible("Terms")

    def glossary_term_visible(self, term):
        """Return True if *term* appears anywhere in the visible page body."""
        return term in self.get_body_text()

    # ── KPI cards widget ──────────────────────────────────────────────────────

    def kpi_card_visible(self, label):
        """Return True if a KPI card labelled *label* is visible."""
        # TODO: Tighten to KPI card container after DevTools inspection.
        return self._text_visible(label)

    def kpi_values_non_zero(self):
        """Heuristic: at least one non-zero numeric value exists in page body."""
        body = self.get_body_text()
        # Look for digits other than 0 beyond the first character to avoid
        # matching dates or version strings.
        import re
        numbers = re.findall(r"\b([1-9]\d*)\b", body)
        return len(numbers) > 0

    # ── CC Declines Matrix widget ─────────────────────────────────────────────

    def matrix_section_visible(self):
        # TODO: Confirm exact heading via DevTools — may be "CC Declines" or similar.
        return (
            self._text_visible("Plan Name")
            or self._text_visible("CC Declines")
            or self._text_visible("Card Declines")
        )

    def get_matrix_columns(self):
        """Return visible column header texts from the CC Declines matrix table.

        TODO: Scope to matrix table container after DevTools inspection.
        """
        headers = self.driver.find_elements(By.XPATH,
            "//th | //*[@role='columnheader']"
        )
        return [h.text.strip() for h in headers if h.is_displayed() and h.text.strip()]

    def matrix_has_data_rows(self):
        rows = self.driver.find_elements(By.XPATH, "//tbody/tr")
        return any(r.is_displayed() for r in rows)

    def matrix_pagination_present(self):
        return self.pagination_controls_present()

    # ── Best & Worst Sites widget ─────────────────────────────────────────────

    def bws_section_visible(self):
        return self._text_visible("Best") and self._text_visible("Worst")

    def best_sites_visible(self):
        return self._text_visible("Best")

    def worst_sites_visible(self):
        return self._text_visible("Worst")

    def bws_shows_site(self, site_name):
        """Return True if *site_name* appears in the Best & Worst Sites section.

        TODO: Scope to BWS container after DevTools inspection — currently
        matches anywhere in the body which may produce false positives.
        """
        return site_name in self.get_body_text()

    # ── Daily Declines Summary widget ─────────────────────────────────────────

    def daily_summary_section_visible(self):
        # TODO: Confirm exact heading via DevTools.
        return (
            self._text_visible("Daily Declines")
            or self._text_visible("Daily Summary")
            or (self._text_visible("Daily") and self._text_visible("Decline"))
        )

    # ── Heatmap widget ────────────────────────────────────────────────────────

    def heatmap_section_visible(self):
        # TODO: Confirm exact heading via DevTools — may be "Heatmap" or "Heat Map".
        return self._text_visible("Heatmap") or self._text_visible("Heat Map")

    # ── Reason Distribution widget ────────────────────────────────────────────

    def reason_dist_section_visible(self):
        # TODO: Confirm exact heading via DevTools.
        return (
            self._text_visible("Reason Distribution")
            or self._text_visible("Decline Reason")
            or (self._text_visible("Reason") and self._text_visible("Distribution"))
        )

    # ── No-data helpers ───────────────────────────────────────────────────────

    def no_data_message_visible(self):
        els = self.driver.find_elements(*self.NO_DATA_MESSAGE)
        return any(el.is_displayed() for el in els)

    # ── Sidebar active state ──────────────────────────────────────────────────

    def sidebar_card_declines_active(self):
        els = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'active') or @aria-current='page' or "
            "@aria-current='true' or @aria-selected='true']"
            "[contains(normalize-space(),'Decline') or "
            "contains(normalize-space(),'decline') or "
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
                    if (t.includes('decline') || t.includes('financial')) {
                        if (isActive(links[i], 0)) return true;
                    }
                }
                return false;
            """))
        except Exception:
            return False
