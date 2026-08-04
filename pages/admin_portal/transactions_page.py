import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class TransactionsPage(BasePage):
    """Page object for /transactions/report.

    The report page itself is a top-level SPA route with no load-time modal.
    EXCEPTION: the transaction detail page (/reports/transactions_log/{id})
    renders its content inside a legacy iframe (legacy-staging.nxtwash.com).
    Call _switch_to_detail_frame() before querying detail-page elements.

    Locators confirmed via page-source inspection on 2026-07-13 are marked
    "# confirmed".  Remaining TODOs need live DevTools verification.
    """

    # ── Detail page — legacy iframe ───────────────────────────────────────────
    # Confirmed via DevTools 2026-07-13: detail page embeds content in this iframe.
    # src="https://legacy-admin.nxtwash.com/reports/transactions_log/{id}?key=...&authToken=..."
    _DETAIL_FRAME_PATTERNS = ["legacy-admin.nxtwash.com", "transactions_log"]

    # ── Main data table ───────────────────────────────────────────────────────
    # TODO: Confirm table tag (HTML <table> vs. role="grid") via DevTools.
    TABLE = (By.XPATH,
        "//table | //*[@role='grid'] | //*[contains(@class,'transactions-table')]")

    TABLE_HEADERS = (By.XPATH,
        "//table//th | //*[@role='columnheader'] | "
        "//*[contains(@class,'table__header') or contains(@class,'col-header')]")

    TABLE_ROWS = (By.XPATH,
        "//table//tbody/tr | //*[@role='row'][not(@role='columnheader')]"
        "[not(ancestor::*[@role='rowgroup' and position()=1])]")

    # TODO: Confirm invoice link href pattern via DevTools.
    # Primary: first-column anchor tags (invoice numbers); broad fallback for
    # confirmed: invoice number is a <div class="...cursor-pointer text-blue-500...underline">
    # NOT an <a> tag — clicks open the detail page in a new tab.
    INVOICE_LINK = (By.XPATH,
        "//tbody//td//div[contains(@class,'cursor-pointer') and "
        "contains(@class,'text-blue-500') and contains(@class,'underline')]")

    # confirmed: "Full info" is a <button> inside <div id="table-action-button">,
    # NOT an <a> tag.  Contains a text div "Full info" + lucide-move-right SVG.
    FULL_INFO_LINK = (By.XPATH,
        "//*[@id='table-action-button']//button | "
        "//button[./div[normalize-space()='Full info']]")

    # ── Header / toolbar controls ─────────────────────────────────────────────
    # TODO: Confirm exact heading text and element tag via DevTools.
    PAGE_TITLE = (By.XPATH,
        "//*[normalize-space()='Transactions Report'] | "
        "//h1[contains(normalize-space(),'Transactions')] | "
        "//*[contains(@class,'page-title') and "
        "contains(normalize-space(),'Transactions')]")

    # confirmed: plain <button> wrapping a lucide-download SVG; no aria-label or export class.
    EXPORT_ICON = (By.XPATH,
        "//button[.//*[contains(@class,'lucide-download')]]")

    # confirmed: nxt-select (React Select) — selected value lives in .nxt-select__single-value
    EXPORT_FORMAT_SELECTED = (By.CSS_SELECTOR, ".nxt-select__single-value")

    # TODO: Confirm "Filter by" button text/class via DevTools.
    FILTER_BY_BTN = (By.XPATH,
        "//button[contains(normalize-space(),'Filter by') or "
        "contains(normalize-space(),'Filter By') or "
        "contains(normalize-space(),'Filters')]")

    # ── Filter panel ──────────────────────────────────────────────────────────
    # confirmed: panel uses role="dialog" + aria-modal="true"; identified by the
    # embedded form id so it is not confused with the export modal.
    FILTER_PANEL = (By.XPATH,
        "//*[@role='dialog'][@aria-modal='true']"
        "[.//form[@id='transactions-report-filter-form']]")

    # confirmed: chips are plain <button> elements inside the QUICK FILTERS div;
    # no semantic class — located via the section heading text.
    QUICK_FILTER_CHIPS = (By.XPATH,
        "//form[@id='transactions-report-filter-form']"
        "//*[normalize-space()='QUICK FILTERS']"
        "/following-sibling::div//button")

    # confirmed: filter tabs are <button data-active="true|false"> elements;
    # data-active is the only stable attribute on the tab strip buttons.
    FILTER_TABS = (By.XPATH,
        "//form[@id='transactions-report-filter-form']//button[@data-active]")

    # TODO: Confirm Apply / Reset / Close button texts via DevTools.
    # confirmed: type="submit" form="transactions-report-filter-form"
    APPLY_FILTERS_BTN = (By.XPATH,
        "//button[@type='submit'][@form='transactions-report-filter-form'] | "
        "//button[normalize-space()='Apply filters' or normalize-space()='Apply Filters']")

    RESET_FILTERS_BTN = (By.XPATH,
        "//button[contains(normalize-space(),'Reset') and "
        "(contains(normalize-space(),'filter') or contains(normalize-space(),'Filter') or "
        "normalize-space()='Reset')]")

    # Close button is in the dialog header, outside the form — distinguished from
    # the per-chip X buttons that are inside the form.
    CLOSE_PANEL_BTN = (By.XPATH,
        "//*[@role='dialog'][@aria-modal='true']"
        "//*[not(ancestor::form)]//button[.//*[contains(@class,'lucide-x')]] | "
        "//*[@role='dialog'][@aria-modal='true']"
        "//*[@aria-label='Close' or @aria-label='close']")

    # TODO: Confirm live results count element class/text pattern via DevTools.
    RESULTS_COUNT = (By.XPATH,
        "//*[contains(normalize-space(),'Results') or contains(normalize-space(),'results')] | "
        "//*[contains(@class,'results-count') or contains(@class,'resultsCount') or "
        "contains(@class,'live-count') or contains(@class,'liveCount')]")

    # ── Pagination / record count ─────────────────────────────────────────────
    # Broad: class-based + "Page X of Y" text pattern (covers NxtWash table footer).
    PAGINATION = (By.XPATH,
        "//*[contains(@class,'pagination') or contains(@class,'pager')] | "
        "//*[@aria-label='pagination' or @role='navigation'] | "
        "//*[contains(normalize-space(),'Page') and contains(normalize-space(),' of ')]")

    # TODO: Confirm record count display format ("18 records" / "Showing 18") via DevTools.
    RECORD_COUNT_DISPLAY = (By.XPATH,
        "//*[contains(normalize-space(),'record') or contains(normalize-space(),'Record')] | "
        "//*[contains(normalize-space(),'Showing') or contains(normalize-space(),'showing')]")

    # confirmed: active filter chips live in a separate "ACTIVE FILTERS" section
    # inside the form — distinguished from QUICK FILTERS chips by section heading.
    # Active state is visual-only (Tailwind bg-blue-200 vs bg-gray-200); no
    # aria-selected / aria-pressed attribute exists on these elements.
    ACTIVE_FILTER_CHIPS = (By.XPATH,
        "//form[@id='transactions-report-filter-form']"
        "//*[normalize-space()='ACTIVE FILTERS']"
        "/following-sibling::*//button")

    # ── Export modal ──────────────────────────────────────────────────────────
    # TODO: Confirm export modal container selector via DevTools.
    EXPORT_MODAL = (By.XPATH,
        "//*[contains(@class,'export-modal') or contains(@class,'exportModal')] | "
        "//*[@role='dialog' and .//*[contains(normalize-space(),'Export')]] | "
        "//*[contains(@class,'modal') and .//*[contains(normalize-space(),'Export')]]")

    # TODO: Confirm format selector (radio buttons or tab-style) via DevTools.
    # Broad locator: @role='button' checks the attribute, not the inferred ARIA role, so
    # plain <button> elements are excluded by that predicate — removed to catch them.
    EXPORT_FORMAT_OPTIONS = (By.XPATH,
        "//input[@type='radio'] | //*[@role='radio'] | "
        "//*[normalize-space()='XLSX' or normalize-space()='CSV']")

    # TODO: Confirm export column toggle structure (checkbox + label) via DevTools.
    EXPORT_COLUMN_LABELS = (By.XPATH,
        "//label[./input[@type='checkbox']] | "
        "//*[@role='checkbox']/parent::label | "
        "//*[contains(@class,'export-column') or contains(@class,'exportColumn')]//label")

    EXPORT_BTN = (By.XPATH,
        "//*[@role='dialog']//button[normalize-space()='Export'] | "
        "//*[contains(@class,'modal')]//button[normalize-space()='Export'] | "
        "//button[normalize-space()='Export' and not(contains(@class,'export-icon'))]")

    CANCEL_BTN = (By.XPATH,
        "//button[normalize-space()='Cancel'] | //button[@aria-label='Cancel']")

    # ── Detail page panels ────────────────────────────────────────────────────
    # confirmed via DevTools 2026-07-13: panel headings inside the legacy iframe are
    # <button class="settings-page__page-header__title">Transaction details</button>
    DETAIL_PANEL_HEADINGS = (By.XPATH,
        "//button[contains(@class,'page-header__title')]")

    # Service section confirmed visible in screenshot: "Service used" column header present.
    # Text-anchor covers both <table> and div-based legacy layouts.
    DETAIL_SERVICE_TABLE = (By.XPATH,
        "//table[.//*[contains(normalize-space(),'Service')]] | "
        "//*[contains(normalize-space(),'Service used')] | "
        "//*[contains(@class,'service') and "
        "(self::table or self::div or self::section)]")

    # confirmed via screenshot 2026-07-13: action buttons inside the legacy iframe are
    # "Refund invoice", "Send receipt to the customer", "Get receipt".
    DETAIL_ACTION_BUTTONS = (By.XPATH,
        "//button[contains(normalize-space(),'Refund') or "
        "contains(normalize-space(),'receipt') or contains(normalize-space(),'Receipt')]")

    DETAIL_BACK_LINK = (By.XPATH,
        "//a[contains(normalize-space(),'Back') or contains(normalize-space(),'back')] | "
        "//button[contains(normalize-space(),'Back')]")

    # ── Load / spinner ────────────────────────────────────────────────────────
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
        "contains(normalize-space(),'No results')]")

    # ── Lane dropdown (in Date & Location filter tab) ─────────────────────────
    # TODO: Confirm lane dropdown selector and disabled/tooltip attr via DevTools.
    LANE_DROPDOWN = (By.XPATH,
        "//*[contains(normalize-space(),'Lane') or contains(normalize-space(),'lane')]"
        "/following-sibling::*[@role='combobox' or self::select] | "
        "//select[contains(@name,'lane') or contains(@id,'lane')] | "
        "//*[contains(@class,'lane') and (@role='combobox' or contains(@class,'select'))]")

    # ── Frame helpers ─────────────────────────────────────────────────────────

    def _switch_to_detail_frame(self):
        """Switch the driver into the legacy iframe on the detail page.

        The outer page at /reports/transactions_log/{id} is a React shell.
        All panel content (Transaction details, Car details, Customer, etc.)
        is rendered inside a legacy iframe.

        Strategy:
        1. Try known src patterns (fast path).
        2. Enumerate all iframes and switch to the first one that has body text
           (fallback when the src pattern differs from what was confirmed).
        TODO: Once the iframe src is confirmed via DevTools, remove the
              enumeration fallback and update _DETAIL_FRAME_PATTERNS.
        """
        self.driver.switch_to.default_content()
        time.sleep(0.3)

        # Fast path — try known src patterns first.
        for pattern in self._DETAIL_FRAME_PATTERNS:
            try:
                WebDriverWait(self.driver, 6).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.XPATH, f"//iframe[contains(@src,'{pattern}')]")
                    )
                )
                return
            except TimeoutException:
                self.driver.switch_to.default_content()

        # Fallback — enumerate all iframes, switch to the first with content.
        try:
            WebDriverWait(self.driver, 8).until(
                lambda d: len(d.find_elements(By.TAG_NAME, "iframe")) > 0
            )
        except TimeoutException:
            return
        for frame in self.driver.find_elements(By.TAG_NAME, "iframe"):
            try:
                self.driver.switch_to.frame(frame)
                body_text = self.driver.find_element(By.TAG_NAME, "body").text.strip()
                if body_text:
                    return
                self.driver.switch_to.default_content()
            except Exception:
                self.driver.switch_to.default_content()

    # ── Page lifecycle ────────────────────────────────────────────────────────

    def wait_for_table(self):
        """Wait for the transactions table element to be present.

        Row presence is NOT waited for here — the factory default filter ('Today')
        produces 0 rows in the test dataset.  open_transactions_page() handles
        applying 'This month' and waiting for rows after the filter is applied.
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.TABLE))
        except TimeoutException:
            pass
        self._wait_for_load_mask_gone()

    def _wait_for_load_mask_gone(self, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.find_elements(*self.LOAD_MASK)) == 0
            )
        except TimeoutException:
            pass

    # ── Table helpers ─────────────────────────────────────────────────────────

    def get_table_headers(self):
        """Return list of visible column header texts."""
        els = self.driver.find_elements(*self.TABLE_HEADERS)
        result = []
        for el in els:
            try:
                if el.is_displayed():
                    text = el.text.strip()
                    if text:
                        result.append(text)
            except Exception:
                continue
        return result

    def get_table_row_count(self):
        """Return count of visible data rows in the table body."""
        rows = self.driver.find_elements(*self.TABLE_ROWS)
        return sum(1 for r in rows if r.is_displayed())

    def has_horizontal_scroll(self):
        """Return True if the table's parent container overflows horizontally."""
        return self.driver.execute_script("""
            var tables = document.querySelectorAll('table, [role="grid"]');
            for (var i = 0; i < tables.length; i++) {
                var parent = tables[i].parentElement;
                if (parent && parent.scrollWidth > parent.clientWidth + 2) return true;
            }
            return false;
        """)

    def has_pagination(self):
        return len(self.driver.find_elements(*self.PAGINATION)) > 0

    def get_record_count_text(self):
        """Return the raw record count string shown on screen (e.g. '18 records')."""
        els = self.driver.find_elements(*self.RECORD_COUNT_DISPLAY)
        for el in els:
            try:
                text = el.text.strip()
                if text and re.search(r'\d', text):
                    return text
            except Exception:
                continue
        return ""

    def first_row_has_invoice_link(self):
        return len(self.driver.find_elements(*self.INVOICE_LINK)) > 0

    def first_row_has_full_info_link(self):
        return len(self.driver.find_elements(*self.FULL_INFO_LINK)) > 0

    def get_active_quick_filter_label(self):
        """Return the label of the currently-active Quick Filter.

        The active filter is shown in the ACTIVE FILTERS section inside the
        filter panel — not on the main page.  This method opens the panel
        temporarily if it is not already open, reads the label via JS to
        avoid stale-element issues, then closes the panel again.
        """
        was_open = self.filter_panel_is_visible()
        if not was_open:
            self.open_filter_panel()
        label = self.driver.execute_script("""
            var form = document.querySelector('#transactions-report-filter-form');
            if (!form) return '';
            var allDivs = Array.from(form.querySelectorAll('div'));
            var section = allDivs.find(function(d) {
                return d.children.length === 0 && d.textContent.trim() === 'ACTIVE FILTERS';
            });
            if (!section) return '';
            var chip = section.parentElement.querySelector('button');
            if (!chip) return '';
            // Get text from leaf <div> nodes (skips SVG and emoji aria-hidden divs).
            var leaves = Array.from(chip.querySelectorAll('div')).filter(function(d) {
                return d.children.length === 0 && d.getAttribute('aria-hidden') !== 'true';
            });
            return leaves.length > 0 ? leaves[leaves.length - 1].textContent.trim() : '';
        """) or ""
        if not was_open:
            self.close_filter_panel()
        return label

    def page_title_is_visible(self):
        return len(self.driver.find_elements(*self.PAGE_TITLE)) > 0

    def export_icon_is_visible(self):
        els = self.driver.find_elements(*self.EXPORT_ICON)
        return any(el.is_displayed() for el in els)

    def filter_by_button_is_visible(self):
        els = self.driver.find_elements(*self.FILTER_BY_BTN)
        return any(el.is_displayed() for el in els)

    # ── Row interaction ───────────────────────────────────────────────────────

    def click_first_row(self):
        rows = [r for r in self.driver.find_elements(*self.TABLE_ROWS) if r.is_displayed()]
        if rows:
            self.driver.execute_script("arguments[0].click();", rows[0])
            time.sleep(0.3)

    def first_row_is_highlighted(self):
        """Return True if the first row carries a highlight/selected CSS class.

        Covers semantic class names and Tailwind bg-* colour classes used in
        NxtWash React tables (e.g. bg-blue-50, bg-indigo-50, ring-).
        """
        rows = [r for r in self.driver.find_elements(*self.TABLE_ROWS) if r.is_displayed()]
        if not rows:
            return False
        cls = rows[0].get_attribute("class") or ""
        return any(kw in cls for kw in (
            "selected", "highlight", "active", "focused",
            "bg-blue", "bg-indigo", "bg-primary", "bg-sky",
            "ring-", "border-blue", "border-indigo",
        ))

    def click_invoice_link(self):
        """Click the invoice number div and switch to the new tab it opens."""
        links = self.driver.find_elements(*self.INVOICE_LINK)
        if not links:
            return ""
        original_handles = set(self.driver.window_handles)
        try:
            links[0].click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", links[0])
        self._switch_to_new_tab(original_handles)
        return self.driver.current_url

    def _switch_to_new_tab(self, original_handles, timeout=10):
        """Wait for a new browser tab to open then switch to it."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.window_handles) > len(original_handles)
            )
        except TimeoutException:
            return
        new_handle = (set(self.driver.window_handles) - original_handles).pop()
        self.driver.switch_to.window(new_handle)
        time.sleep(0.5)

    def click_full_info_link(self):
        """Click the 'Full info' button — opens the detail page in a new tab."""
        links = self.driver.find_elements(*self.FULL_INFO_LINK)
        if not links:
            return
        el = links[0]
        original_handles = set(self.driver.window_handles)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
            time.sleep(0.2)
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)
        self._switch_to_new_tab(original_handles)

    def is_on_detail_page(self):
        """Return True when the browser has navigated to a transaction detail URL."""
        return "transactions_log" in self.driver.current_url or "transaction/" in self.driver.current_url

    # ── Filter panel ──────────────────────────────────────────────────────────

    def open_filter_panel(self):
        """Click 'Filter by' and wait for the panel to appear.

        Guard: if the panel is already visible, returns immediately without
        clicking — prevents toggle-close when called on an already-open panel.
        """
        if self.filter_panel_is_visible():
            return
        btn = self.wait.until(EC.element_to_be_clickable(self.FILTER_BY_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(0.5)
        try:
            self.wait.until(EC.visibility_of_element_located(self.FILTER_PANEL))
        except TimeoutException:
            pass

    def filter_panel_is_visible(self):
        els = self.driver.find_elements(*self.FILTER_PANEL)
        return any(el.is_displayed() for el in els)

    def close_filter_panel(self):
        """Click the X button to close the filter panel without applying."""
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.CLOSE_PANEL_BTN))
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.4)
        except TimeoutException:
            pass

    def apply_panel_filters(self):
        """Submit the filter form then close the panel via the X button.

        The Apply filters button is type=submit — native click triggers the React
        onSubmit handler.  The panel does not auto-dismiss after submit, so we
        explicitly click the X (lucide-x) close button afterwards.
        """
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.APPLY_FILTERS_BTN))
            btn.click()
        except TimeoutException:
            self.driver.execute_script(
                'var b = document.querySelector('
                '\'button[type="submit"][form="transactions-report-filter-form"]\');'
                'if (b) b.click();'
            )
        time.sleep(0.3)
        # panel stays open after submit — close it via the X button
        if self.filter_panel_is_visible():
            self.close_filter_panel()
        self._wait_for_load_mask_gone()

    def reset_panel_filters(self):
        """Click Reset to clear all filter selections."""
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.RESET_FILTERS_BTN))
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.4)
        except TimeoutException:
            pass

    def _chip_label(self, chip_el):
        """Extract the visible label text from a Quick Filter chip button.

        Each chip contains an emoji <div aria-hidden='true'> and a label <div>.
        We skip the aria-hidden div and read from the leaf div that has no
        aria-hidden attribute.
        """
        try:
            leaves = chip_el.find_elements(
                By.XPATH,
                ".//div[not(@aria-hidden='true') and not(*)]"
            )
            if leaves:
                return leaves[-1].text.strip()
            return chip_el.text.strip()
        except Exception:
            return ""

    def get_quick_filter_labels(self):
        """Return list of chip label texts in the Quick Filters row."""
        chips = self.driver.find_elements(*self.QUICK_FILTER_CHIPS)
        result = []
        for c in chips:
            text = self._chip_label(c)
            if text:
                result.append(text)
        return result

    def click_quick_filter(self, label):
        """Click a Quick Filter chip by its exact label text."""
        chips = self.driver.find_elements(*self.QUICK_FILTER_CHIPS)
        for c in chips:
            if self._chip_label(c) == label:
                self.driver.execute_script("arguments[0].click();", c)
                time.sleep(0.4)
                return

    def _tab_label(self, tab_el):
        """Extract label text from a filter tab button.

        Each tab button contains an SVG icon and a <span> with the label.
        Reading the span avoids including any SVG text content.
        """
        try:
            spans = tab_el.find_elements(By.TAG_NAME, "span")
            if spans:
                return spans[0].text.strip()
            return tab_el.text.strip()
        except Exception:
            return ""

    def get_filter_tab_labels(self):
        """Return list of FILTERS tab labels (e.g. 'Date & Location', 'Transaction', …)."""
        tabs = self.driver.find_elements(*self.FILTER_TABS)
        result = []
        for t in tabs:
            text = self._tab_label(t)
            if text:
                result.append(text)
        return result

    def click_filter_tab(self, tab_name):
        """Click a named tab in the FILTERS tab strip."""
        tabs = self.driver.find_elements(*self.FILTER_TABS)
        for t in tabs:
            if tab_name.lower() in self._tab_label(t).lower():
                self.driver.execute_script("arguments[0].click();", t)
                time.sleep(0.4)
                return

    def get_results_count(self):
        """Return live results count as int (e.g. 18), or None if not found."""
        els = self.driver.find_elements(*self.RESULTS_COUNT)
        for el in els:
            try:
                text = el.text.strip()
                m = re.search(r'\d+', text)
                if m:
                    return int(m.group())
            except Exception:
                continue
        return None

    # ── Date & Location tab ───────────────────────────────────────────────────

    def get_date_preset_labels(self):
        """Return list of date preset option texts in the Date & Location tab.

        Uses leaf-node text search — finds visible elements whose direct text
        matches a known preset label, regardless of element type.
        """
        presets = [
            "Today", "Yesterday", "This week", "Last week",
            "This month", "Last month", "This year",
        ]
        return self.driver.execute_script("""
            var presets = arguments[0];
            var seen = new Set();
            var result = [];
            document.querySelectorAll('*').forEach(function(el) {
                if (el.offsetParent === null) return;
                if (el.children.length > 0) return;
                var text = el.textContent.trim();
                if (presets.indexOf(text) >= 0 && !seen.has(text)) {
                    seen.add(text);
                    result.push(text);
                }
            });
            return result;
        """, presets) or []

    def click_date_preset(self, label):
        """Click a named date preset in the Date & Location filter tab.

        Date presets live inside the Date & Location tab — NOT quick-filter chips.
        Uses the same leaf-node visible scan as get_date_preset_labels because the
        preset elements are not necessarily <button> tags.
        """
        self.driver.execute_script("""
            var label = arguments[0];
            var form = document.querySelector('#transactions-report-filter-form');
            if (!form) return;
            var els = Array.from(form.querySelectorAll('*'));
            for (var i = 0; i < els.length; i++) {
                var el = els[i];
                if (el.offsetParent === null) continue;
                if (el.children.length > 0) continue;
                if (el.textContent.trim() === label) {
                    el.click();
                    return true;
                }
            }
            return false;
        """, label)
        time.sleep(0.3)

    def get_date_range_value(self):
        """Return the current date range string displayed in the filter."""
        els = self.driver.find_elements(By.XPATH,
            "//input[@type='text' and (@placeholder or @value)] | "
            "//*[contains(@class,'date-range') or contains(@class,'dateRange')]")
        for el in els:
            try:
                val = el.get_attribute("value") or el.text or ""
                if "/" in val or "–" in val or "-" in val:
                    return val.strip()
            except Exception:
                continue
        return ""

    def get_site_chips(self):
        """Return list of selected site chip label texts in the filter panel."""
        chips = self.driver.find_elements(By.XPATH,
            "//*[contains(@class,'site-select__multi-value__label') or "
            "contains(@class,'siteSelect__multiValue__label') or "
            "contains(@class,'multiValue') and not(contains(@class,'remove'))]")
        result = []
        seen = set()
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

    def get_lane_options(self):
        """Return list of available lane options from the lane dropdown."""
        return self.driver.execute_script("""
            var sel = document.querySelector('select[name*="lane"], select[id*="lane"]');
            if (sel) {
                return Array.from(sel.options)
                    .filter(function(o) { return o.value !== ''; })
                    .map(function(o) { return o.textContent.trim(); });
            }
            var opts = document.querySelectorAll('[role="option"]');
            return Array.from(opts)
                .filter(function(el) { return el.offsetParent !== null; })
                .map(function(el) { return el.textContent.trim(); });
        """) or []

    def lane_dropdown_is_enabled(self):
        """Return True when the lane dropdown is interactive."""
        els = self.driver.find_elements(*self.LANE_DROPDOWN)
        for el in els:
            try:
                disabled = el.get_attribute("disabled")
                aria_disabled = el.get_attribute("aria-disabled")
                if disabled is None and aria_disabled != "true":
                    return True
            except Exception:
                continue
        return False

    def lane_dropdown_tooltip(self):
        """Return tooltip text on the (disabled) lane dropdown."""
        els = self.driver.find_elements(*self.LANE_DROPDOWN)
        for el in els:
            try:
                tip = el.get_attribute("title") or el.get_attribute("data-tooltip") or ""
                if tip:
                    return tip.strip()
            except Exception:
                continue
        return ""

    # ── Export modal ──────────────────────────────────────────────────────────

    def open_export_modal(self):
        """Click the export icon and wait for the export modal."""
        btn = self.wait.until(EC.element_to_be_clickable(self.EXPORT_ICON))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(0.5)
        try:
            self.wait.until(EC.visibility_of_element_located(self.EXPORT_MODAL))
        except TimeoutException:
            pass

    def export_modal_is_visible(self):
        els = self.driver.find_elements(*self.EXPORT_MODAL)
        return any(el.is_displayed() for el in els)

    def get_export_format_labels(self):
        """Return the currently selected format from the nxt-select 'Export as' dropdown.

        The export modal uses a custom nxt-select (React Select) component.  When
        closed it only renders the selected value in .nxt-select__single-value —
        the other options are portal-rendered and only appear when the dropdown is
        open.  We read the selected value only; the test verifies XLSX is pre-selected.
        """
        els = self.driver.find_elements(*self.EXPORT_FORMAT_SELECTED)
        result = []
        for el in els:
            try:
                if el.is_displayed():
                    t = el.text.strip()
                    if t:
                        result.append(t)
            except Exception:
                continue
        return result

    def get_export_column_toggle_labels(self):
        """Return per-column toggle labels from the export modal.

        Tries role='switch'/'checkbox' (custom React toggles) first, then
        falls back to native input[type='checkbox'].
        """
        return self.driver.execute_script("""
            var seen = new Set();
            var results = [];

            function addLabel(text) {
                text = (text || '').trim();
                if (text && !seen.has(text)) { seen.add(text); results.push(text); }
            }

            function labelForControl(ctrl) {
                // 1. aria-label attribute
                var al = ctrl.getAttribute('aria-label');
                if (al) { addLabel(al); return; }
                // 2. Clone parent, remove the control, read remaining text
                var container = ctrl.closest('label, li, [class*="row"], [class*="item"], [class*="field"]');
                if (container) {
                    var clone = container.cloneNode(true);
                    var copy = clone.querySelector('[role="switch"],[role="checkbox"],input');
                    if (copy) copy.parentNode.removeChild(copy);
                    var t = clone.textContent.trim();
                    if (t) { addLabel(t); return; }
                }
                // 3. Adjacent sibling text
                var prev = ctrl.previousElementSibling;
                if (prev && prev.textContent.trim()) { addLabel(prev.textContent); return; }
                var next = ctrl.nextElementSibling;
                if (next && next.tagName !== 'BUTTON' && next.textContent.trim()) {
                    addLabel(next.textContent); return;
                }
                // 4. Parent text minus control text
                if (ctrl.parentElement) {
                    var pt = ctrl.parentElement.textContent.trim();
                    var ct = ctrl.textContent.trim();
                    addLabel(pt.replace(ct, '').trim());
                }
            }

            // Role-based toggles (custom React switches)
            var switches = document.querySelectorAll('[role="switch"],[role="checkbox"]');
            Array.from(switches).forEach(function(sw) {
                if (sw.offsetParent === null) return;
                labelForControl(sw);
            });

            // Native checkboxes (fallback)
            if (results.length === 0) {
                document.querySelectorAll('input[type="checkbox"]').forEach(function(inp) {
                    if (inp.offsetParent === null) return;
                    var lEl = inp.closest('label')
                        || (inp.id && document.querySelector('[for="' + inp.id + '"]'))
                        || inp.parentElement;
                    addLabel(lEl ? lEl.textContent : '');
                });
            }
            return results;
        """) or []

    def get_export_columns_default_off(self):
        """Return labels of export columns that are toggled OFF by default."""
        return self.driver.execute_script("""
            var seen = new Set();
            var off = [];

            function labelOf(ctrl) {
                var al = ctrl.getAttribute('aria-label');
                if (al) return al.trim();
                var container = ctrl.closest('label, li, [class*="row"], [class*="item"], [class*="field"]');
                if (container) {
                    var clone = container.cloneNode(true);
                    var copy = clone.querySelector('[role="switch"],[role="checkbox"],input');
                    if (copy) copy.parentNode.removeChild(copy);
                    var t = clone.textContent.trim();
                    if (t) return t;
                }
                var prev = ctrl.previousElementSibling;
                if (prev && prev.textContent.trim()) return prev.textContent.trim();
                return (ctrl.parentElement || {textContent:''}).textContent.trim()
                       .replace(ctrl.textContent.trim(), '').trim();
            }

            // Custom toggles with aria-checked='false'
            document.querySelectorAll('[role="switch"][aria-checked="false"],[role="checkbox"][aria-checked="false"]')
                .forEach(function(sw) {
                    if (sw.offsetParent === null) return;
                    var t = labelOf(sw);
                    if (t && !seen.has(t)) { seen.add(t); off.push(t); }
                });

            // Native unchecked checkboxes (fallback)
            if (off.length === 0) {
                document.querySelectorAll('input[type="checkbox"]').forEach(function(inp) {
                    if (inp.offsetParent === null || inp.checked) return;
                    var lEl = inp.closest('label')
                        || (inp.id && document.querySelector('[for="' + inp.id + '"]'))
                        || inp.parentElement;
                    var t = (lEl ? lEl.textContent : '').trim();
                    if (t && !seen.has(t)) { seen.add(t); off.push(t); }
                });
            }
            return off;
        """) or []

    def export_button_is_visible(self):
        els = self.driver.find_elements(*self.EXPORT_BTN)
        return any(el.is_displayed() for el in els)

    def close_export_modal(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.CANCEL_BTN))
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.3)
        except TimeoutException:
            pass

    # ── Detail page ───────────────────────────────────────────────────────────
    # All methods below switch to the legacy iframe before querying elements.

    def get_detail_panel_headings(self):
        """Return visible panel heading texts inside the legacy iframe."""
        self._switch_to_detail_frame()
        els = self.driver.find_elements(*self.DETAIL_PANEL_HEADINGS)
        result = []
        for el in els:
            try:
                if el.is_displayed():
                    text = el.text.strip()
                    if text:
                        result.append(text)
            except Exception:
                continue
        return result

    def get_detail_page_text(self):
        """Return all visible text from the legacy iframe body."""
        self._switch_to_detail_frame()
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except Exception:
            return ""

    def get_body_text(self):
        """Return body text of the current document context (outer page or iframe)."""
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except Exception:
            return ""

    def detail_service_table_is_visible(self):
        self._switch_to_detail_frame()
        els = self.driver.find_elements(*self.DETAIL_SERVICE_TABLE)
        return any(el.is_displayed() for el in els)

    def get_detail_action_button_labels(self):
        """Return list of visible action button texts on the detail page."""
        self._switch_to_detail_frame()
        els = self.driver.find_elements(*self.DETAIL_ACTION_BUTTONS)
        result = []
        for el in els:
            try:
                if el.is_displayed():
                    text = el.text.strip()
                    if text:
                        result.append(text)
            except Exception:
                continue
        return result

    def click_back_from_detail(self):
        """Navigate back to the Transactions Report from the detail page.

        Prefers a Back button/link if one exists; otherwise derives the report
        URL from the current URL and navigates directly — avoids driver.back()
        which goes to the wrong history entry when the fixture navigated directly.
        """
        self.driver.switch_to.default_content()
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.DETAIL_BACK_LINK))
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(1.0)
        except TimeoutException:
            current = self.driver.current_url
            if "/reports/transactions_log" in current:
                base = current.split("/reports/transactions_log")[0]
            else:
                base = current.rsplit("/", 2)[0]
            self.driver.get(base + "/transactions/report")
            time.sleep(1.5)
