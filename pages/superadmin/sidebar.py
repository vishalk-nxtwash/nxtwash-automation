from selenium.webdriver.common.by import By

from pages.common.base_page import BasePage


class Sidebar(BasePage):

    HAMBURGER_MENU = (
        By.XPATH,
        "//button[.//*[contains(@class,'lucide-menu')]]"
    )

    COMPANIES_MENU = (
        By.XPATH,
        "//a[@href='/companies']"
    )

    USERS_MENU = (
        By.XPATH,
        "//a[@href='/users']"
    )

    USER_ROLES_MENU = (
        By.XPATH,
        "//a[@href='/user-roles']"
    )

    THIRD_PARTY_DROPDOWN = (
        By.XPATH,
        "//button[.//div[text()='Third Party']]"
    )

    THIRD_PARTY_MENU = (
        By.XPATH,
        "//a[@href='/third-party/apps']"
    )

    THIRD_PARTY_KEYS_MENU = (
        By.XPATH,
        "//a[@href='/third-party/keys']"
    )

    def expand_sidebar(self):

        self.click(self.HAMBURGER_MENU)

    def open_companies(self):

        self.click(self.COMPANIES_MENU)

    def open_users(self):

        self.click(self.USERS_MENU)

    def open_user_roles(self):

        self.click(self.USER_ROLES_MENU)

    def open_third_party(self):

        self.click(self.THIRD_PARTY_DROPDOWN)

        self.click(self.THIRD_PARTY_MENU)

    def open_third_party_keys(self):

        self.click(self.THIRD_PARTY_DROPDOWN)

        self.click(self.THIRD_PARTY_KEYS_MENU)