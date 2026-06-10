from selenium.common.exceptions import TimeoutException

from pages.admin_portal.coupon_packages_page import CouponPackagesPage
from pages.admin_portal.login_page import AdminLoginPage


COUPON_PACKAGE_NAME = "VK ACC2"
GIVEAWAY_SERVICES = ("vk detail wash", "Detail cleaning")


def open_coupon_packages_page(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()
    login_page.login()
    try:
        login_page.wait_for_overview()
    except TimeoutException:
        pass
    browser.get(
        login_page.config.get_url(login_page.PORTAL).rstrip("/")
        + "/services/couponPackages"
    )

    coupon_packages_page = CouponPackagesPage(browser)
    coupon_packages_page.wait_for_list_loaded()

    return coupon_packages_page


def test_edit_vk_acc2_coupon_giveaway_services(browser):

    coupon_packages_page = open_coupon_packages_page(browser)

    assert coupon_packages_page.coupon_package_exists(
        COUPON_PACKAGE_NAME
    ), "Expected existing coupon package '%s' before running edit script" % (
        COUPON_PACKAGE_NAME
    )

    coupon_packages_page.update_coupon_giveaway_services(
        COUPON_PACKAGE_NAME,
        GIVEAWAY_SERVICES
    )
    coupon_packages_page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
    selected_values = coupon_packages_page.checked_giveaway_values()

    assert "vk detail wash" in selected_values
    assert "detail cleaning" in selected_values
