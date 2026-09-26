from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class CompaniesPage(BasePage):

    # Page identifiers
    PAGE_TITLE = (By.XPATH, "//div[text()='Companies']")
    ADD_COMPANY_BUTTON = (By.XPATH, "//button[contains(text(),'Add Company')]")

    # Filter controls
    FILTER_BUTTON = (By.XPATH, "//button[contains(.,'Filter by')]")
    COMPANY_NAME_FILTER = (By.NAME, "companyName")
    ACTIVE_COMPANY_TOGGLE = (By.NAME, "isActive")  # unconfirmed field name
    APPLY_FILTERS_BUTTON = (By.XPATH, "//button[normalize-space()='Apply filters']")
    RESET_FILTERS_BUTTON = (By.XPATH, "//button[normalize-space()='Reset filters']")

    # Row-level action buttons (relative to a row element)
    LOGIN_TO_BUTTON = (By.XPATH, ".//button[normalize-space()='Login to']")

    # Login / App launcher dialog
    LOGIN_DIALOG = (By.XPATH, "//div[@role='dialog']")
    ADMIN_PORTAL_BUTTON = (
        By.XPATH,
        "//div[@role='dialog']//button[normalize-space()='Admin Portal']"
    )
    AP_STAGING_BUTTON = (
        By.XPATH,
        "//div[@role='dialog']//button[normalize-space()='AP Staging']"
    )
    AP_OVERVIEW_TEXT = (By.XPATH, "//*[normalize-space()='Overview']")

    # Export
    EXPORT_ICON_BUTTON = (
        By.XPATH,
        "//button[.//svg[contains(@class,'lucide-download')]]"
    )
    EXPORT_MODAL = (
        By.XPATH,
        "//div[@role='dialog'] | "
        "//div[contains(@class,'modal') and contains(.,'Export')]"
    )
    EXPORT_MODAL_TITLE = (
        By.XPATH,
        "//div[@role='dialog']//*[contains(.,'Export Companies')] | "
        "//div[contains(@class,'modal')]//*[contains(.,'Export Companies')]"
    )
    EXPORT_COLUMN_TOGGLES = (
        By.XPATH,
        "//div[@role='dialog']//label//input[@type='checkbox']"
    )

    # ── Page load ─────────────────────────────────────────────────────────────

    def wait_for_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))

    def get_page_title(self):
        return self.get_text(self.PAGE_TITLE)

    def click_add_company(self):
        self.click(self.ADD_COMPANY_BUTTON)

    # ── Filter panel ─────────────────────────────────────────────────────────

    def open_filters(self):
        if not self.filter_panel_is_open():
            self.click(self.FILTER_BUTTON)
            self.wait.until(
                EC.visibility_of_element_located(self.COMPANY_NAME_FILTER)
            )

    def filter_panel_is_open(self):
        els = self.driver.find_elements(*self.COMPANY_NAME_FILTER)
        return bool(els) and els[0].is_displayed()

    def apply_filters(self):
        self.click(self.APPLY_FILTERS_BUTTON)

    def reset_filters(self):
        self.click(self.RESET_FILTERS_BUTTON)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//tbody")))

    def close_filter_panel(self):
        close_btn = (By.XPATH, "//button[.//svg[contains(@class,'lucide-x')]]")
        els = self.driver.find_elements(*close_btn)
        if els:
            self.driver.execute_script("arguments[0].click();", els[0])

    def get_filter_value(self, locator):
        el = self.driver.find_element(*locator)
        return el.get_attribute("value") or ""

    def filter_by_company_name(self, company_name):
        self.open_filters()
        self.enter_text(self.COMPANY_NAME_FILTER, company_name)
        self.click(self.APPLY_FILTERS_BUTTON)
        self.wait_for_company_row(company_name)

    def company_exists(self, company_name):
        try:
            self.filter_by_company_name(company_name)
            return True
        except TimeoutException:
            return False

    # ── Row helpers ───────────────────────────────────────────────────────────

    def get_company_row_locator(self, company_name):
        return (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[.//button[normalize-space()='Edit']][1]"
            % company_name
        )

    def wait_for_company_row(self, company_name):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_company_row_locator(company_name)
            )
        )

    def open_company_edit(self, company_name):
        row = self.wait_for_company_row(company_name)
        edit_button = row.find_element(
            By.XPATH, ".//button[normalize-space()='Edit']"
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", edit_button
        )
        edit_button.click()

    def get_row_actions(self, company_name):
        """Return text labels of all buttons in the row for company_name."""
        row = self.wait_for_company_row(company_name)
        buttons = row.find_elements(By.XPATH, ".//button")
        return [btn.text.strip() for btn in buttons if btn.text.strip()]

    # ── Table / Pagination ────────────────────────────────────────────────────

    def get_column_headers(self):
        headers = self.driver.find_elements(
            By.XPATH, "//th | //thead//td | //div[@role='columnheader']"
        )
        return [h.text.strip() for h in headers if h.text.strip()]

    def get_visible_row_count(self):
        rows = self.driver.find_elements(By.XPATH, "//tbody/tr[td]")
        if rows:
            return len(rows)
        return len(self.driver.find_elements(By.XPATH, "//tbody/tr"))

    def get_pagination_text(self):
        locators = [
            (By.XPATH, "//*[contains(.,'Page') and contains(.,' of ')]"),
            (By.XPATH, "//nav[contains(.,'Page')] | //div[contains(@class,'pagination')]"),
        ]
        for loc in locators:
            els = self.driver.find_elements(*loc)
            if els:
                return els[0].text.strip()
        return ""

    def get_records_count_text(self):
        """Return the 'out of N records' summary text, or empty string."""
        els = self.driver.find_elements(
            By.XPATH, "//*[contains(.,'out of') and contains(.,'records')]"
        )
        return els[0].text.strip() if els else ""

    def prev_page_button_is_disabled(self):
        btn_loc = (
            By.XPATH,
            "//button[.//svg[contains(@class,'lucide-chevron-left') "
            "and not(contains(@class,'lucide-chevrons-left'))]]"
        )
        els = self.driver.find_elements(*btn_loc)
        if els:
            return els[0].get_attribute("disabled") is not None
        return True

    def get_results_per_page_options(self):
        control_loc = (
            By.XPATH,
            "//div[contains(@class,'singleValue') and contains(.,'Show')]"
        )
        controls = self.driver.find_elements(*control_loc)
        if controls:
            try:
                controls[0].click()
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@role='option']"))
                )
                opts = self.driver.find_elements(By.XPATH, "//*[@role='option']")
                result = [o.text.strip() for o in opts if o.text.strip()]
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                return result
            except Exception:
                pass
        return []

    # ── Login To ──────────────────────────────────────────────────────────────

    def click_login_to(self, company_name):
        if not self.company_exists(company_name):
            raise AssertionError(
                "Company '%s' was not found in the Companies list." % company_name
            )
        row = self.wait_for_company_row(company_name)
        login_to_button = row.find_element(*self.LOGIN_TO_BUTTON)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", login_to_button
        )
        login_to_button.click()
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_DIALOG))

    def get_login_dialog_options(self):
        """Return button labels visible inside the Login To dialog."""
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_DIALOG))
        buttons = self.driver.find_elements(
            By.XPATH, "//div[@role='dialog']//button"
        )
        return [btn.text.strip() for btn in buttons if btn.text.strip()]

    def dismiss_login_dialog(self):
        """Close the Login To dialog via the Close button."""
        close = (
            By.XPATH,
            "//div[@role='dialog']//button[normalize-space()='Close'] | "
            "//div[@role='dialog']//button[.//svg[contains(@class,'lucide-x')]]"
        )
        els = self.driver.find_elements(*close)
        if els:
            self.driver.execute_script("arguments[0].click();", els[0])
        self.wait.until(EC.invisibility_of_element_located(self.LOGIN_DIALOG))

    def select_admin_portal(self):
        try:
            self.click(self.ADMIN_PORTAL_BUTTON)
        except TimeoutException:
            raise AssertionError(
                "Admin Portal option was not available in the Login to dialog."
            )

    def select_ap_staging(self):
        try:
            self.click(self.AP_STAGING_BUTTON)
        except TimeoutException:
            raise AssertionError(
                "AP Staging option was not available in the Login to dialog."
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
                w for w in self.driver.window_handles
                if w not in existing_windows
            ][0]
            self.driver.switch_to.window(new_window)

    def wait_for_ap_staging_overview(self):
        self.wait.until(
            lambda driver: driver.current_url.startswith(
                "https://staging.nxtwash.com/"
            )
        )
        self.wait.until(EC.visibility_of_element_located(self.AP_OVERVIEW_TEXT))

    # ── Export ────────────────────────────────────────────────────────────────

    def click_export_icon(self):
        self.click(self.EXPORT_ICON_BUTTON)

    def export_modal_is_visible(self):
        els = self.driver.find_elements(*self.EXPORT_MODAL)
        return bool(els) and els[0].is_displayed()

    def get_export_format_options(self):
        control_loc = (
            By.XPATH,
            "//div[@role='dialog']//div[contains(@class,'singleValue')]"
        )
        controls = self.driver.find_elements(*control_loc)
        if controls:
            try:
                controls[0].click()
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@role='dialog']//*[@role='option']")
                    )
                )
                opts = self.driver.find_elements(
                    By.XPATH, "//div[@role='dialog']//*[@role='option']"
                )
                result = [o.text.strip() for o in opts if o.text.strip()]
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                return result
            except Exception:
                pass
        return []

    def get_default_export_format(self):
        els = self.driver.find_elements(
            By.XPATH, "//div[@role='dialog']//div[contains(@class,'singleValue')]"
        )
        return els[0].text.strip() if els else None

    def get_export_column_states(self):
        toggles = self.driver.find_elements(*self.EXPORT_COLUMN_TOGGLES)
        states = {}
        for i, toggle in enumerate(toggles):
            name = toggle.get_attribute("name") or "column_%d" % i
            states[name] = toggle.is_selected()
        return states

    def export_confirm_button_is_disabled(self):
        locators = [
            (By.XPATH,
             "//div[@role='dialog']//button[contains(.,'Export') "
             "and not(contains(.,'Cancel'))]"),
            (By.XPATH,
             "//div[@role='dialog']//button[contains(@class,'primary') or "
             "contains(@class,'confirm')]"),
        ]
        for loc in locators:
            els = self.driver.find_elements(*loc)
            if els:
                btn = els[0]
                return (
                    btn.get_attribute("disabled") is not None
                    or btn.get_attribute("aria-disabled") == "true"
                )
        return False

    def cancel_export(self):
        self.click((
            By.XPATH,
            "//div[@role='dialog']//button[normalize-space()='Cancel'] | "
            "//div[contains(@class,'modal')]//button[normalize-space()='Cancel']"
        ))
