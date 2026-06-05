from selenium.webdriver.common.by import By

from pages.common.base_page import BasePage
from core.config_manager import ConfigManager


class LoginPage(BasePage):

    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Overview page title
    OVERVIEW_TITLE = (By.XPATH,"//div[text()='Overview']")

    def __init__(self, driver):

        super().__init__(driver)

        # Load configuration data.
        self.config = ConfigManager()

    def open(self):

        # Open SuperAdmin login page.
        self.driver.get(
            self.config.get_url("superadmin")
        )

    def enter_email(self, email):

        # Enter email address.
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):

        # Enter password.
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):

        # Click login button.
        self.click(self.LOGIN_BUTTON)

    def get_overview_text(self):
        # Get Overview page title text.
        return self.get_text(self.OVERVIEW_TITLE)

    def login(self):

        print("Entering email...")
        self.enter_email(
        self.config.get_username("superadmin")
    )

        print("Entering password...")
        self.enter_password(
        self.config.get_password("superadmin")
    )

        print("Clicking login button...")
        self.click_login()

    def is_login_successful(self):

        current_url = self.driver.current_url

        overview_text = self.get_overview_text()

        return (
            current_url == "https://superadmin.nxtwash.com/"
            and overview_text == "Overview"
    )