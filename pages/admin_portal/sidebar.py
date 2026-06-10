from selenium.webdriver.common.by import By

from pages.common.base_page import BasePage


class AdminSidebar(BasePage):

    OVERVIEW_LINK = (
        By.XPATH,
        "//a[@href='/' and normalize-space()='Overview']"
    )
    SITES_LOCATIONS_LINK = (
        By.XPATH,
        "//a[@href='/sites' and normalize-space()='Sites / Locations']"
    )
    CUSTOMERS_LINK = (
        By.XPATH,
        "//a[@href='/customers' and normalize-space()='Customers']"
    )
    KIOSK_SETTINGS_LINK = (
        By.XPATH,
        "//a[@href='/kiosk_settings/kiosks' and "
        "normalize-space()='Kiosk Settings']"
    )
    GAS_PUMP_SETTINGS_LINK = (
        By.XPATH,
        "//a[@href='/gas_pump_settings/device_list' and "
        "normalize-space()='Gas Pump Settings']"
    )
    POS_SETTINGS_LINK = (
        By.XPATH,
        "//a[@href='/pos_settings/pos' and normalize-space()='POS Settings']"
    )
    TUNNEL_SETTINGS_LINK = (
        By.XPATH,
        "//a[@href='/tunnel_settings/tunnels' and "
        "normalize-space()='Tunnel Settings']"
    )
    SERVICES_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Services']"
    )
    SERVICE_CATEGORIES_LINK = (
        By.XPATH,
        "//a[@href='/services/serviceCategories']"
    )
    MEMBERSHIPS_LINK = (
        By.XPATH,
        "//a[@href='/services/memberships']"
    )
    WASH_PACKAGES_LINK = (
        By.XPATH,
        "//a[@href='/services/washPackages']"
    )
    WASH_EXTRAS_LINK = (
        By.XPATH,
        "//a[@href='/services/washExtras']"
    )
    WASH_BOOKS_LINK = (
        By.XPATH,
        "//a[@href='/services/washBooks']"
    )
    COUPON_CODES_LINK = (
        By.XPATH,
        "//a[@href='/services/couponPackages']"
    )
    GIFT_CARDS_LINK = (
        By.XPATH,
        "//a[@href='/services/giftCards']"
    )
    DISCOUNTS_LINK = (
        By.XPATH,
        "//a[@href='/services/discounts']"
    )

    def open_overview(self):
        """Open Overview."""
        self.click(self.OVERVIEW_LINK)

    def open_sites_locations(self):
        """Open Sites / Locations."""
        self.click(self.SITES_LOCATIONS_LINK)

    def open_service_categories(self):
        """Open Services > Service Categories."""
        self.click(self.SERVICES_BUTTON)
        self.click(self.SERVICE_CATEGORIES_LINK)

    def open_memberships(self):
        """Open Services > Memberships."""
        self.click(self.SERVICES_BUTTON)
        self.click(self.MEMBERSHIPS_LINK)

    def open_wash_packages(self):
        """Open Services > Wash Packages."""
        self.click(self.SERVICES_BUTTON)
        self.click(self.WASH_PACKAGES_LINK)

    def open_wash_extras(self):
        """Open Services > Wash Extras."""
        self.click(self.SERVICES_BUTTON)
        self.click(self.WASH_EXTRAS_LINK)

    def open_wash_books(self):
        """Open Services > Wash Books."""
        self.click(self.SERVICES_BUTTON)
        self.click(self.WASH_BOOKS_LINK)

    def open_coupon_codes(self):
        """Open Services > Coupon Codes."""
        self.click(self.SERVICES_BUTTON)
        self.click(self.COUPON_CODES_LINK)

    def open_gift_cards(self):
        """Open Services > Gift Cards."""
        self.click(self.SERVICES_BUTTON)
        self.click(self.GIFT_CARDS_LINK)

    def open_discounts(self):
        """Open Services > Discounts."""
        self.click(self.SERVICES_BUTTON)
        self.click(self.DISCOUNTS_LINK)
