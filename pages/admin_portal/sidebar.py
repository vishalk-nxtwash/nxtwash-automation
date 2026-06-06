from selenium.webdriver.common.by import By

from pages.common.base_page import BasePage


class AdminSidebar(BasePage):

    SITES_LOCATIONS_LINK = (
        By.XPATH,
        "//a[@href='/sites' and normalize-space()='Sites / Locations']"
    )

    def open_sites_locations(self):
        """Open Sites / Locations."""
        self.click(self.SITES_LOCATIONS_LINK)
