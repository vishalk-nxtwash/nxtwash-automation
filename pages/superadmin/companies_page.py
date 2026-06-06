from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class CompaniesPage(BasePage):

    # Page Title
    PAGE_TITLE = (By.XPATH,"//div[text()='Companies']")

    # Add Company Button
    ADD_COMPANY_BUTTON = (By.XPATH,"//button[contains(text(),'Add Company')]")

    FILTER_BUTTON = (By.XPATH, "//button[contains(.,'Filter by')]")
    COMPANY_NAME_FILTER = (By.NAME, "companyName")
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']"
    )
    LOGIN_TO_BUTTON = (By.XPATH, ".//button[normalize-space()='Login to']")
    LOGIN_DIALOG = (By.XPATH, "//div[@role='dialog']")
    ADMIN_PORTAL_BUTTON = (
        By.XPATH,
        "//div[@role='dialog']//button[normalize-space()='Admin Portal']"
    )
    AP_STAGING_BUTTON = (
        By.XPATH,
        "//div[@role='dialog']//button[normalize-space()='AP Staging']"
    )
    AP_OVERVIEW_TEXT = (
        By.XPATH,
        "//*[normalize-space()='Overview']"
    )

    def wait_for_loaded(self):
        """Wait until the Companies page is visible."""
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))

    def get_page_title(self):
        """Get Companies page title."""
        return self.get_text(self.PAGE_TITLE)

    def click_add_company(self):
        """Click Add Company button."""
        self.click(self.ADD_COMPANY_BUTTON)

    def open_filters(self):
        """Open company filters."""
        self.click(self.FILTER_BUTTON)
        self.wait.until(
            EC.visibility_of_element_located(self.COMPANY_NAME_FILTER)
        )

    def filter_by_company_name(self, company_name):
        """Filter companies by company name."""
        self.open_filters()
        self.enter_text(self.COMPANY_NAME_FILTER, company_name)
        self.click(self.APPLY_FILTERS_BUTTON)
        self.wait_for_company_row(company_name)

    def company_exists(self, company_name):
        """Return whether a company exists after filtering by name."""
        try:
            self.filter_by_company_name(company_name)
            return True
        except TimeoutException:
            return False

    def get_company_row_locator(self, company_name):
        """Build a locator for a company row by visible company name."""
        return (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[.//button[normalize-space()='Edit']][1]"
            % company_name
        )

    def wait_for_company_row(self, company_name):
        """Wait until the target company row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_company_row_locator(company_name)
            )
        )

    def open_company_edit(self, company_name):
        """Open the edit page for a company."""
        row = self.wait_for_company_row(company_name)
        edit_button = row.find_element(
            By.XPATH,
            ".//button[normalize-space()='Edit']"
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            edit_button
        )
        edit_button.click()

    def click_login_to(self, company_name):
        """Open the Login to dialog for a company."""
        if not self.company_exists(company_name):
            raise AssertionError(
                "Company '%s' was not found in Companies list."
                % company_name
            )

        row = self.wait_for_company_row(company_name)
        login_to_button = row.find_element(*self.LOGIN_TO_BUTTON)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            login_to_button
        )
        login_to_button.click()
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_DIALOG))

    def select_admin_portal(self):
        """Select Admin Portal in the Login to dialog."""
        try:
            self.click(self.ADMIN_PORTAL_BUTTON)
        except TimeoutException:
            raise AssertionError(
                "Admin Portal option was not available in Login to dialog."
            )

    def select_ap_staging(self):
        """Select AP Staging in the domain dialog."""
        try:
            self.click(self.AP_STAGING_BUTTON)
        except TimeoutException:
            raise AssertionError(
                "AP Staging option was not available in Login to dialog."
            )

    def login_to_admin_portal_ap_staging(self, company_name):
        """Login to the company's AP Staging admin portal."""
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
                window
                for window in self.driver.window_handles
                if window not in existing_windows
            ][0]
            self.driver.switch_to.window(new_window)

    def wait_for_ap_staging_overview(self):
        """Wait until the AP Staging overview page is loaded."""
        self.wait.until(
            lambda driver: driver.current_url.startswith(
                "https://staging.nxtwash.com/"
            )
        )
        self.wait.until(EC.visibility_of_element_located(self.AP_OVERVIEW_TEXT))
