from pages.admin_portal.coupon_packages_page import CouponPackagesPage
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal.discounts.conftest import DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import create_discount_if_missing


COUPON_PACKAGE_NAME = "VK ACC2"
GIVEAWAY_SERVICE = "vk detail wash"
GIVEAWAY_SERVICES = ("vk detail wash", "Detail cleaning")
MISSING_COUPON_PACKAGE = "coupon-package-does-not-exist-automation"
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def open_coupon_packages_page(browser):

    open_admin_path(browser, "/services/couponPackages")

    page = CouponPackagesPage(browser)
    page.wait_for_list_loaded()

    return page


def create_coupon_package_if_missing(browser):

    create_discount_if_missing(browser, DISCOUNT_NAME)
    page = open_coupon_packages_page(browser)

    if page.coupon_package_exists(COUPON_PACKAGE_NAME):
        page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
        page.ensure_active_switch_on()
        page.click_save_coupon_package()
        return open_coupon_packages_page(browser)

    page.create_coupon_package(
        COUPON_PACKAGE_NAME,
        DISCOUNT_NAME,
        GIVEAWAY_SERVICE
    )
    page.search_coupon_package(COUPON_PACKAGE_NAME)
    page.wait_for_coupon_package_row(COUPON_PACKAGE_NAME)

    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)
