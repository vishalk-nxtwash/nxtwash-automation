from selenium.webdriver.common.by import By

from pages.common.base_page import BasePage


class OverviewPage(BasePage):

    OVERVIEW_TITLE = (
        By.XPATH,
        "//div[text()='Overview']"
    )

    def get_overview_text(self):
        return self.get_text(self.OVERVIEW_TITLE)