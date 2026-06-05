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
