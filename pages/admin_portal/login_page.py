from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from core.config_manager import ConfigManager
from pages.common.base_page import BasePage


class AdminLoginPage(BasePage):

    PORTAL = "admin_portal"

    EMAIL_OR_PHONE_INPUT = (By.NAME, "emailOrPhone")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    OVERVIEW_TITLE = (By.XPATH, "//*[normalize-space()='Overview']")

    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigManager()

    def open(self):
        """Open Admin Portal."""
        self.driver.get(self.config.get_url(self.PORTAL))

    def wait_for_loaded(self):
        """Wait until the Admin login form is visible."""
        self.wait.until(
            EC.visibility_of_element_located(self.EMAIL_OR_PHONE_INPUT)
        )
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))

    def enter_email_or_phone(self, email_or_phone):
        """Enter Admin email or phone."""
        self.enter_text(self.EMAIL_OR_PHONE_INPUT, email_or_phone)

    def enter_password(self, password):
        """Enter Admin password."""
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Submit Admin login form."""
        self.click(self.LOGIN_BUTTON)

    def login(self):
        """Login with configured Admin credentials."""
        self.enter_email_or_phone(self.config.get_username(self.PORTAL))
        self.enter_password(self.config.get_password(self.PORTAL))
        self.click_login()

    def wait_for_overview(self):
        """Wait until Admin Portal overview is visible."""
        self.wait.until(
            lambda driver: driver.current_url == self.config.get_url(self.PORTAL)
        )
        self.wait.until(EC.visibility_of_element_located(self.OVERVIEW_TITLE))

    def get_overview_text(self):
        """Get Admin overview title text."""
        return self.get_text(self.OVERVIEW_TITLE)
