from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class AdminOverviewPage(BasePage):

    OVERVIEW_TITLE = (By.XPATH, "//*[normalize-space()='Overview']")
    PROFILE_ROLE = (By.XPATH, "//*[normalize-space()='Admin Portal User']")

    EXPECTED_NAV_LINKS = {
        "Overview": "/",
        "Sites / Locations": "/sites",
        "Customers": "/customers",
        "Kiosk Settings": "/kiosk_settings/kiosks",
        "Gas Pump Settings": "/gas_pump_settings/device_list",
        "POS Settings": "/pos_settings/pos",
        "Tunnel Settings": "/tunnel_settings/tunnels"
    }
    EXPECTED_NAV_BUTTONS = [
        "Services",
        "Users / Employees",
        "Notifications",
        "Reports"
    ]
    BROKEN_STATE_TEXTS = [
        "Something went wrong",
        "Internal Server Error",
        "404",
        "Unauthorized",
        "Failed to fetch"
    ]

    def wait_for_loaded(self):
        """Wait until Overview shell is visible."""
        self.wait.until(EC.visibility_of_element_located(self.OVERVIEW_TITLE))
        self.wait.until(EC.visibility_of_element_located(self.PROFILE_ROLE))

    def get_body_text(self):
        """Get visible page text."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_overview_text(self):
        """Get Overview title text."""
        return self.get_text(self.OVERVIEW_TITLE)

    def has_expected_url(self):
        """Return whether the browser is on the Admin Overview URL."""
        return self.driver.current_url == "https://staging.nxtwash.com/"

    def is_redirected_to_login(self):
        """Return whether the user was redirected back to login."""
        return "/login" in self.driver.current_url

    def get_nav_link_locator(self, label, href):
        return (
            By.XPATH,
            "//a[@href='%s' and normalize-space()='%s']" % (href, label)
        )

    def nav_link_is_visible(self, label, href):
        """Return whether a direct sidebar link is visible."""
        return self.driver.find_element(
            *self.get_nav_link_locator(label, href)
        ).is_displayed()

    def nav_button_is_visible(self, label):
        """Return whether a sidebar dropdown button is visible."""
        return self.driver.find_element(
            By.XPATH,
            "//button[normalize-space()='%s']" % label
        ).is_displayed()

    def expected_navigation_is_visible(self):
        """Return whether all stable sidebar navigation items are visible."""
        for label, href in self.EXPECTED_NAV_LINKS.items():
            if not self.nav_link_is_visible(label, href):
                return False

        for label in self.EXPECTED_NAV_BUTTONS:
            if not self.nav_button_is_visible(label):
                return False

        return True

    def profile_role_is_visible(self):
        """Return whether the logged-in profile role is visible."""
        return self.driver.find_element(*self.PROFILE_ROLE).is_displayed()

    def has_broken_state_text(self):
        """Return whether a known broken/error state is visible."""
        body_text = self.get_body_text()
        return any(text in body_text for text in self.BROKEN_STATE_TEXTS)

    def shell_has_content(self):
        """Return whether the Overview shell has meaningful visible content."""
        body_text = self.get_body_text()
        return (
            "Overview" in body_text
            and "Sites / Locations" in body_text
            and "Admin Portal User" in body_text
        )
