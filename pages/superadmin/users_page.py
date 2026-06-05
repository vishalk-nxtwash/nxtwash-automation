from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class UsersPage(BasePage):

    PAGE_TITLE = (By.XPATH, "//div[normalize-space()='Users']")
    ADD_USER_BUTTON = (By.XPATH, "//button[contains(.,'Add User')]")
    FILTER_BUTTON = (By.XPATH, "//button[contains(.,'Filter by')]")

    FIRST_NAME_FILTER = (By.NAME, "firstName")
    LAST_NAME_FILTER = (By.NAME, "lastName")
    EMAIL_FILTER = (By.NAME, "emailId")
    PHONE_FILTER = (By.NAME, "phoneNumber")
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']"
    )
    RESET_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Reset filters']"
    )

    NO_RECORDS_TEXT = (By.XPATH, "//*[contains(.,'out of 0 records')]")

    def wait_for_loaded(self):
        """Wait until the Users page is visible."""
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_USER_BUTTON))

    def click_add_user(self):
        """Open the create user page."""
        self.click(self.ADD_USER_BUTTON)

    def open_filters(self):
        """Open user filters."""
        self.click(self.FILTER_BUTTON)
        self.wait.until(
            EC.visibility_of_element_located(self.EMAIL_FILTER)
        )

    def filter_by_email(self, email):
        """Filter users by email."""
        self.open_filters()
        self.enter_text(self.EMAIL_FILTER, email)
        self.click(self.APPLY_FILTERS_BUTTON)

    def get_user_row_locator(self, email):
        """Build a locator for a user row by visible email."""
        return (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[.//button[normalize-space()='Edit']][1]"
            % email
        )

    def wait_for_user_row(self, email):
        """Wait until the target user row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_user_row_locator(email)
            )
        )

    def user_exists(self, email):
        """Return whether a user exists after filtering by email."""
        self.filter_by_email(email)

        try:
            self.wait_for_user_row(email)
            return True
        except TimeoutException:
            return False


class CreateUserPage(BasePage):

    PAGE_TITLE = (By.XPATH, "//div[normalize-space()='User']")
    NEW_MODE_LABEL = (By.XPATH, "//div[normalize-space()='New']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    SAVE_NEW_BUTTON = (By.XPATH, "//button[normalize-space()='Save new']")

    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    PASSWORD_INPUT = (By.NAME, "password")
    CONFIRM_PASSWORD_INPUT = (By.NAME, "confirmPassword")
    EMAIL_INPUT = (By.NAME, "emailId")
    PHONE_INPUT = (By.NAME, "phoneNumber")
    ROLE_ID_INPUT = (By.NAME, "roleId")
    ROLE_CONTROL = (
        By.XPATH,
        "//input[@name='roleId']/preceding-sibling::div"
    )

    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space()='Yes']")
    CONFIRM_NO_BUTTON = (By.XPATH, "//button[normalize-space()='No']")

    def wait_for_loaded(self):
        """Wait until the create user form is visible."""
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.visibility_of_element_located(self.NEW_MODE_LABEL))
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))

    def enter_first_name(self, first_name):
        """Enter first name."""
        self.enter_text(self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name):
        """Enter last name."""
        self.enter_text(self.LAST_NAME_INPUT, last_name)

    def enter_password(self, password):
        """Enter password."""
        self.enter_text(self.PASSWORD_INPUT, password)

    def enter_confirm_password(self, confirm_password):
        """Enter confirm password."""
        self.enter_text(self.CONFIRM_PASSWORD_INPUT, confirm_password)

    def enter_email(self, email):
        """Enter email."""
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_phone(self, phone):
        """Enter phone number."""
        self.enter_text(self.PHONE_INPUT, phone)

    def select_role(self, role_name):
        """Select a user role."""
        self.click(self.ROLE_CONTROL)
        role_option = (
            By.XPATH,
            "//*[@role='option' and normalize-space()='%s']" % role_name
        )
        self.click(role_option)
        role_id_input = self.wait.until(
            EC.presence_of_element_located(self.ROLE_ID_INPUT)
        )
        self.wait.until(
            lambda driver: role_id_input.get_attribute("value") != ""
        )

    def fill_user_form(
        self,
        first_name,
        last_name,
        password,
        confirm_password,
        email,
        phone,
        role_name
    ):
        """Fill create user form."""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_password(password)
        self.enter_confirm_password(confirm_password)
        self.enter_email(email)
        self.enter_phone(phone)
        self.select_role(role_name)

    def click_save_new(self):
        """Submit the create user form."""
        self.click(self.SAVE_NEW_BUTTON)

    def click_cancel(self):
        """Cancel creating a user."""
        self.click(self.CANCEL_BUTTON)

    def confirm_yes_if_present(self):
        """Confirm the active confirmation dialog if it appears."""
        short_wait = WebDriverWait(self.driver, 2)

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
        """Get visible page text."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def has_validation_text(self, text):
        """Return whether validation text is visible."""
        return text in self.get_body_text()

    def wait_for_any_text(self, expected_texts):
        """Wait until any expected text appears on the page."""
        expected_texts = [text.lower() for text in expected_texts]

        self.wait.until(
            lambda driver: any(
                text in self.get_body_text().lower()
                for text in expected_texts
            )
        )
