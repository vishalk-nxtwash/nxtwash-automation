import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class CompaniesPage(BasePage):

    # ── Page chrome ───────────────────────────────────────────────────────────
    PAGE_TITLE = (By.XPATH, "//div[text()='Companies']")
    ADD_COMPANY_BUTTON = (By.XPATH, "//button[contains(text(),'Add Company')]")

    # ── List / table ──────────────────────────────────────────────────────────
    TABLE_HEADERS = (
        By.XPATH,
        "//th | //*[@role='columnheader']",
    )
    TABLE_ROWS = (
        By.XPATH,
        "//tbody/tr | //*[@role='row' and not(@role='columnheader') and not(ancestor::thead)]",
    )
    PAGINATION_INFO = (
        By.XPATH,
        "//*[contains(normalize-space(),'Page') and contains(normalize-space(),'of')]",
    )
    RESULTS_PER_PAGE_SELECT = (
        By.XPATH,
        "//select[.//option[normalize-space()='10']] | "
        "//*[@aria-label='Rows per page'] | "
        "//*[contains(@class,'per-page')] | "
        "//*[contains(@class,'pageSize')] | "
        "//select[.//option[text()='10']]",
    )
    PREV_PAGE_BTN = (
        By.XPATH,
        "//button[@aria-label='Previous page' or @aria-label='Prev' or @title='Previous page']",
    )
    NEXT_PAGE_BTN = (
        By.XPATH,
        "//button[@aria-label='Next page' or @aria-label='Next' or @title='Next page']",
    )
    FIRST_PAGE_BTN = (
        By.XPATH,
        "//button[@aria-label='First page' or @title='First page']",
    )
    LAST_PAGE_BTN = (
        By.XPATH,
        "//button[@aria-label='Last page' or @title='Last page']",
    )
    EMPTY_STATE = (
        By.XPATH,
        "//*[contains(normalize-space(),'No companies') or "
        "contains(normalize-space(),'No results') or "
        "contains(normalize-space(),'No data found')]",
    )

    # ── Export ────────────────────────────────────────────────────────────────
    EXPORT_ICON_BUTTON = (
        By.XPATH,
        "//button[.//*[contains(@class,'lucide-download')]] | "
        "//button[@aria-label='Export' or @aria-label='Download']",
    )
    EXPORT_MODAL = (
        By.XPATH,
        "//div[@role='dialog']",
    )
    EXPORT_MODAL_TITLE = (
        By.XPATH,
        "//div[@role='dialog']//*[contains(normalize-space(),'Export Companies')]",
    )
    EXPORT_FORMAT_SELECT = (
        By.XPATH,
        "//div[@role='dialog']//select | "
        "//div[@role='dialog']//*[contains(@class,'control')]",
    )
    EXPORT_CONFIRM_BTN = (
        By.XPATH,
        "//div[@role='dialog']//button[contains(normalize-space(),'Export') or "
        "contains(normalize-space(),'Download')]",
    )
    EXPORT_CANCEL_BTN = (
        By.XPATH,
        "//div[@role='dialog']//button[normalize-space()='Cancel']",
    )
    EXPORT_COLUMN_TOGGLES = (
        By.XPATH,
        "//div[@role='dialog']//*[@role='switch' or @type='checkbox']",
    )

    # ── Filter ────────────────────────────────────────────────────────────────
    FILTER_BUTTON = (By.XPATH, "//button[contains(.,'Filter by')]")
    COMPANY_NAME_FILTER = (By.NAME, "companyName")
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']",
    )
    ACTIVE_FILTER_TOGGLE = (
        By.XPATH,
        # Toggle near "Active company" label — try checkbox, switch, and label click.
        "//*[normalize-space(text())='Active company']/following::input[@type='checkbox'][1] | "
        "//*[normalize-space(text())='Active company']/preceding::input[@type='checkbox'][1] | "
        "//*[normalize-space(text())='Active company']/following::*[@role='switch'][1] | "
        "//*[normalize-space(text())='Active company']/preceding::*[@role='switch'][1] | "
        "//*[normalize-space()='Active company' and (self::label or self::button)] | "
        "//*[@role='switch']",
    )
    RESET_FILTERS_BTN = (
        By.XPATH,
        "//button[normalize-space()='Reset filters' or normalize-space()='Reset' "
        "or normalize-space()='Clear all' or normalize-space()='Clear filters']",
    )
    CLOSE_FILTER_BTN = (
        By.XPATH,
        # Try aria-label variants first, then fall back to X icon buttons in filter area.
        "//button[@aria-label='Close' or @aria-label='close' or @aria-label='Dismiss'] | "
        "//*[.//input[@name='companyName']]//button[contains(@class,'close') "
        "or contains(@class,'dismiss') or contains(@class,'CloseButton')] | "
        "//*[.//input[@name='companyName']]//button[not(normalize-space()='Reset filters') "
        "and not(normalize-space()='Apply filters') "
        "and not(.//input[@name='companyName'])]",
    )
    CLEAR_NAME_INPUT_BTN = (
        By.XPATH,
        "//input[@name='companyName']/..//button | "
        "//input[@name='companyName']/following-sibling::button | "
        "//input[@name='companyName']/following::button[1] | "
        "//button[@aria-label='Clear company name' or @aria-label='clear']",
    )
    FILTER_PANEL = (
        By.XPATH,
        "//*[.//input[@name='companyName']]",
    )

    # ── Company row / actions ─────────────────────────────────────────────────
    LOGIN_TO_BUTTON = (By.XPATH, ".//button[normalize-space()='Login to']")
    EDIT_BUTTON = (By.XPATH, ".//button[normalize-space()='Edit']")
    LOGIN_DIALOG = (By.XPATH, "//div[@role='dialog']")
    ADMIN_PORTAL_BUTTON = (
        By.XPATH,
        "//div[@role='dialog']//button[normalize-space()='Admin Portal']",
    )
    AP_STAGING_BUTTON = (
        By.XPATH,
        "//div[@role='dialog']//button[normalize-space()='AP Staging']",
    )
    AP_OVERVIEW_TEXT = (By.XPATH, "//*[normalize-space()='Overview']")

    # ── Waits ─────────────────────────────────────────────────────────────────

    def wait_for_loaded(self):
        """Wait until the Companies list is visible and interactive."""
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))

    # ── Page title ────────────────────────────────────────────────────────────

    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)

    # ── List inspection ───────────────────────────────────────────────────────

    def get_column_headers(self):
        """Return a list of visible column header texts."""
        headers = self.driver.find_elements(*self.TABLE_HEADERS)
        return [h.text.strip() for h in headers if h.text.strip()]

    def get_visible_row_count(self):
        """Return the number of data rows currently displayed."""
        return len(self.driver.find_elements(*self.TABLE_ROWS))

    def get_pagination_text(self):
        """Return the pagination summary text (e.g. 'Page 1 of 1 | out of 8 records')."""
        return self.get_text(self.PAGINATION_INFO)

    def get_results_per_page_options(self):
        """Return available results-per-page option values."""
        select = self.driver.find_element(*self.RESULTS_PER_PAGE_SELECT)
        return [o.text.strip() for o in select.find_elements(By.TAG_NAME, "option")]

    def prev_page_button_is_disabled(self):
        btn = self.driver.find_element(*self.PREV_PAGE_BTN)
        return btn.get_attribute("disabled") is not None or not btn.is_enabled()

    def next_page_button_is_disabled(self):
        btn = self.driver.find_element(*self.NEXT_PAGE_BTN)
        return btn.get_attribute("disabled") is not None or not btn.is_enabled()

    def empty_state_is_visible(self):
        """Return True if the empty-state message is present on the page."""
        return len(self.driver.find_elements(*self.EMPTY_STATE)) > 0

    def get_visible_company_names(self):
        """Return the company names visible in the current table page.

        Retries on StaleElementReferenceException — the table re-renders
        after filter application and rows go stale between calls.
        """
        for _attempt in range(3):
            try:
                rows = self.driver.find_elements(*self.TABLE_ROWS)
                names = []
                for row in rows:
                    cells = row.find_elements(By.XPATH, ".//td | .//*[@role='cell']")
                    if cells:
                        names.append(cells[0].text.strip())
                return [n for n in names if n]
            except StaleElementReferenceException:
                if _attempt == 2:
                    raise
                time.sleep(0.3)
        return []

    # ── Company row helpers ───────────────────────────────────────────────────

    def get_company_row_locator(self, company_name):
        return (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[.//button[normalize-space()='Edit']][1]" % company_name,
        )

    def wait_for_company_row(self, company_name):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_company_row_locator(company_name)
            )
        )

    def company_exists(self, company_name):
        try:
            self.filter_by_company_name(company_name)
            return True
        except TimeoutException:
            return False

    def row_has_login_to_button(self, company_name):
        row = self.wait_for_company_row(company_name)
        return len(row.find_elements(*self.LOGIN_TO_BUTTON)) > 0

    def row_has_edit_button(self, company_name):
        row = self.wait_for_company_row(company_name)
        return len(row.find_elements(*self.EDIT_BUTTON)) > 0

    # ── Add company ───────────────────────────────────────────────────────────

    def click_add_company(self):
        self.click(self.ADD_COMPANY_BUTTON)

    # ── Filter ────────────────────────────────────────────────────────────────

    def open_filters(self):
        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.COMPANY_NAME_FILTER))

    def filter_panel_is_open(self):
        return len(self.driver.find_elements(*self.FILTER_PANEL)) > 0

    def filter_by_company_name(self, company_name):
        self.open_filters()
        self.enter_text(self.COMPANY_NAME_FILTER, company_name)
        self.click(self.APPLY_FILTERS_BUTTON)
        self.wait_for_company_row(company_name)

    def get_company_name_filter_value(self):
        return self.driver.find_element(*self.COMPANY_NAME_FILTER).get_attribute("value")

    def clear_company_name_filter_input(self):
        """Click the X clear icon on the company name filter input."""
        self.click(self.CLEAR_NAME_INPUT_BTN)

    def toggle_active_filter(self):
        """Click the Active toggle in the filter panel."""
        self.click(self.ACTIVE_FILTER_TOGGLE)

    def reset_filters(self):
        """Click the Reset filters button."""
        self.click(self.RESET_FILTERS_BTN)
        self.wait_for_loaded()

    def close_filter_panel(self):
        """Close the filter panel without applying changes."""
        self.click(self.CLOSE_FILTER_BTN)

    def apply_filters(self):
        self.click(self.APPLY_FILTERS_BUTTON)

    # ── Export ────────────────────────────────────────────────────────────────

    def click_export_icon(self):
        """Click the export / download icon to open the Export modal."""
        self.click(self.EXPORT_ICON_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.EXPORT_MODAL))

    def export_modal_is_visible(self):
        return len(self.driver.find_elements(*self.EXPORT_MODAL)) > 0

    def get_export_format_options(self):
        """Return list of export format option texts (e.g. ['XLSX', 'CSV']).

        Handles both a native <select> and a React Select control inside the modal.
        """
        modal = self.driver.find_element(*self.EXPORT_MODAL)
        # Native select
        selects = modal.find_elements(By.TAG_NAME, "select")
        if selects:
            return [o.text.strip() for o in selects[0].find_elements(By.TAG_NAME, "option")]
        # React Select: open the control and read visible options
        ctrl = modal.find_elements(By.XPATH, ".//*[contains(@class,'control')]")
        if ctrl:
            self.driver.execute_script("arguments[0].click();", ctrl[0])
            opts = self.wait.until(
                lambda d: d.find_elements(By.XPATH, "//*[@role='option']")
            )
            texts = [o.text.strip() for o in opts if o.is_displayed() and o.text.strip()]
            # Close the dropdown by clicking elsewhere
            self.driver.find_element(By.TAG_NAME, "body").click()
            return texts
        return []

    def get_default_export_format(self):
        """Return the currently selected export format.

        Handles both a native <select> and a React Select value display.
        """
        modal = self.driver.find_element(*self.EXPORT_MODAL)
        selects = modal.find_elements(By.TAG_NAME, "select")
        if selects:
            for option in selects[0].find_elements(By.TAG_NAME, "option"):
                if option.get_attribute("selected") or option.is_selected():
                    return option.text.strip()
            return None
        # React Select: read the singleValue div inside the control
        single_val = modal.find_elements(
            By.XPATH, ".//*[contains(@class,'singleValue') or contains(@class,'single-value')]"
        )
        if single_val:
            return single_val[0].text.strip()
        # Fallback: read displayed text inside the control
        ctrl = modal.find_elements(By.XPATH, ".//*[contains(@class,'control')]")
        if ctrl:
            return ctrl[0].text.strip() or None
        return None

    def get_export_column_states(self):
        """Return dict of {toggle_index: is_checked} for column toggles in modal."""
        toggles = self.driver.find_elements(*self.EXPORT_COLUMN_TOGGLES)
        return {i: (t.is_selected() or t.get_attribute("aria-checked") == "true")
                for i, t in enumerate(toggles)}

    def export_confirm_button_is_disabled(self):
        btn = self.driver.find_element(*self.EXPORT_CONFIRM_BTN)
        return btn.get_attribute("disabled") is not None or not btn.is_enabled()

    def cancel_export(self):
        """Cancel the export modal without downloading."""
        self.click(self.EXPORT_CANCEL_BTN)
        self.wait.until(EC.invisibility_of_element_located(self.EXPORT_MODAL))

    def confirm_export(self):
        """Click the Export/Download button inside the modal."""
        self.click(self.EXPORT_CONFIRM_BTN)

    # ── Edit / Login-to ───────────────────────────────────────────────────────

    def open_company_edit(self, company_name):
        row = self.wait_for_company_row(company_name)
        edit_button = row.find_element(By.XPATH, ".//button[normalize-space()='Edit']")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", edit_button
        )
        edit_button.click()

    def click_login_to(self, company_name):
        if not self.company_exists(company_name):
            raise AssertionError(
                "Company '%s' was not found in Companies list." % company_name
            )
        row = self.wait_for_company_row(company_name)
        login_to_button = row.find_element(*self.LOGIN_TO_BUTTON)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", login_to_button
        )
        login_to_button.click()
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_DIALOG))

    def select_admin_portal(self):
        try:
            self.click(self.ADMIN_PORTAL_BUTTON)
        except TimeoutException:
            raise AssertionError(
                "Admin Portal option was not available in Login to dialog."
            )

    def select_ap_staging(self):
        try:
            self.click(self.AP_STAGING_BUTTON)
        except TimeoutException:
            raise AssertionError(
                "AP Staging option was not available in Login to dialog."
            )

    def login_to_admin_portal_ap_staging(self, company_name):
        existing_windows = self.driver.window_handles[:]
        self.click_login_to(company_name)
        self.select_admin_portal()
        self.select_ap_staging()
        self.wait.until(
            lambda driver: (
                len(driver.window_handles) > len(existing_windows)
                or driver.current_url.startswith("https://staging.nxtwash.com/")
            )
        )
        if len(self.driver.window_handles) > len(existing_windows):
            new_window = [
                w for w in self.driver.window_handles if w not in existing_windows
            ][0]
            self.driver.switch_to.window(new_window)

    def wait_for_ap_staging_overview(self):
        self.wait.until(
            lambda driver: driver.current_url.startswith("https://staging.nxtwash.com/")
        )
        self.wait.until(EC.visibility_of_element_located(self.AP_OVERVIEW_TEXT))
