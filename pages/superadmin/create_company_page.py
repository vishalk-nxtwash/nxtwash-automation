from selenium.webdriver.common.by import By

from pages.common.base_page import BasePage


class CreateCompanyPage(BasePage):

    COMPANY_BASE_SETTINGS_TITLE = (
        By.XPATH,
        "//div[text()='Company Base Settings']"
    )