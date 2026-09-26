from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class CreateCompanyPage(BasePage):

    # Section headings
    COMPANY_BASE_SETTINGS_TITLE = (
        By.XPATH,
        "//div[text()='Company Base Settings']"
    )
    COMPANY_LOCATION_SETTINGS_TITLE = (
        By.XPATH,
        "//div[text()='Company Location Settings']"
    )

    # Page mode labels
    PAGE_TITLE = (By.XPATH, "//div[normalize-space()='Company']")
    NEW_MODE_LABEL = (By.XPATH, "//div[normalize-space()='New']")

    # Text inputs (confirmed names match edit form where overlap exists)
    COMPANY_NAME_INPUT = (By.NAME, "companyName")
    EMAIL_INPUT = (By.NAME, "email")           # field name unconfirmed
    PHONE_INPUT = (By.NAME, "phoneNumber")     # field name unconfirmed
    PASSWORD_INPUT = (By.NAME, "password")     # field name unconfirmed
    SITE_NAME_INPUT = (By.NAME, "siteName")    # field name unconfirmed
    ADDRESS1_INPUT = (By.NAME, "address1")     # field name unconfirmed
    ADDRESS2_INPUT = (By.NAME, "address2")     # field name unconfirmed
    ZIP_INPUT = (By.NAME, "zip")               # field name unconfirmed

    # Action buttons
    SAVE_NEW_BUTTON = (By.XPATH, "//button[normalize-space()='Save new']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space()='Yes']")
    CONFIRM_NO_BUTTON = (By.XPATH, "//button[normalize-space()='No']")

    def wait_for_loaded(self):
        self.wait.until(
            EC.visibility_of_element_located(self.COMPANY_BASE_SETTINGS_TITLE)
        )

    def enter_company_name(self, name):
        self.enter_text(self.COMPANY_NAME_INPUT, name)

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def click_save_new(self):
        self.click(self.SAVE_NEW_BUTTON)

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)

    def confirm_yes_if_present(self, timeout=5):
        short_wait = WebDriverWait(self.driver, timeout)
        try:
            short_wait.until(
                EC.element_to_be_clickable(self.CONFIRM_YES_BUTTON)
            ).click()
            short_wait.until(
                EC.invisibility_of_element_located(self.CONFIRM_YES_BUTTON)
            )
        except TimeoutException:
            return

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def has_validation_text(self, text):
        return text in self.get_body_text()
