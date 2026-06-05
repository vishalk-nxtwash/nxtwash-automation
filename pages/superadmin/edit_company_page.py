from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class EditCompanyPage(BasePage):

    PAGE_TITLE = (By.XPATH, "//div[normalize-space()='Company']")
    EDIT_MODE_LABEL = (By.XPATH, "//div[normalize-space()='Edit']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    SAVE_CHANGES_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save changes']"
    )
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space()='Yes']")
    CONFIRM_NO_BUTTON = (By.XPATH, "//button[normalize-space()='No']")

    COMPANY_NAME_INPUT = (By.NAME, "companyName")
    TERMS_CONDITION_TEXTAREA = (By.NAME, "termsCondition")
    PRIVACY_POLICY_TEXTAREA = (By.NAME, "privacyPolicyText")

    def wait_for_loaded(self, company_name):
        """Wait until the edit form has finished hydrating values."""
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.visibility_of_element_located(self.EDIT_MODE_LABEL))
        self.wait.until(
            EC.text_to_be_present_in_element_value(
                self.COMPANY_NAME_INPUT,
                company_name
            )
        )
        self.wait.until(
            EC.visibility_of_element_located(
                self.TERMS_CONDITION_TEXTAREA
            )
        )

    def get_company_name(self):
        """Get the company name input value."""
        return self.wait.until(
            EC.visibility_of_element_located(self.COMPANY_NAME_INPUT)
        ).get_attribute("value")

    def get_terms_condition(self):
        """Get the company terms and conditions value."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.TERMS_CONDITION_TEXTAREA
            )
        ).get_attribute("value")

    def set_terms_condition(self, terms_condition):
        """Set the company terms and conditions value."""
        element = self.wait.until(
            EC.visibility_of_element_located(
                self.TERMS_CONDITION_TEXTAREA
            )
        )
        element.send_keys(Keys.COMMAND, "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(terms_condition)

    def click_cancel(self):
        """Cancel editing company details."""
        self.click(self.CANCEL_BUTTON)

    def click_save_changes(self):
        """Save company details."""
        self.click(self.SAVE_CHANGES_BUTTON)

    def confirm_yes(self):
        """Confirm the active confirmation dialog."""
        self.click(self.CONFIRM_YES_BUTTON)

    def confirm_no(self):
        """Dismiss the active confirmation dialog."""
        self.click(self.CONFIRM_NO_BUTTON)

    def wait_for_confirmation_closed(self):
        """Wait until the active confirmation dialog is closed."""
        self.wait.until(
            EC.invisibility_of_element_located(self.CONFIRM_YES_BUTTON)
        )

    def wait_for_terms_condition(self, terms_condition):
        """Wait until the terms and conditions field has the expected value."""
        self.wait.until(
            EC.text_to_be_present_in_element_value(
                self.TERMS_CONDITION_TEXTAREA,
                terms_condition
            )
        )
