from selenium.common.exceptions import TimeoutException

from pages.admin_portal.coupon_packages_page import CouponPackagesPage
from pages.admin_portal.login_page import AdminLoginPage
from tests.admin_portal.test_discounts import create_discount_if_missing


COUPON_PACKAGE_NAME = "VK ACC2"
DISCOUNT_NAME = "VK AD02"
GIVEAWAY_SERVICE = "vk detail wash"
MISSING_COUPON_PACKAGE = "coupon-package-does-not-exist-automation"


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


def create_coupon_package_if_missing(browser):

    create_discount_if_missing(browser, DISCOUNT_NAME)
    coupon_packages_page = open_coupon_packages_page(browser)

    if coupon_packages_page.coupon_package_exists(COUPON_PACKAGE_NAME):
        coupon_packages_page.search_coupon_package(COUPON_PACKAGE_NAME)
        coupon_packages_page.wait_for_coupon_package_row(COUPON_PACKAGE_NAME)
        return coupon_packages_page

    coupon_packages_page.create_coupon_package(
        COUPON_PACKAGE_NAME,
        DISCOUNT_NAME,
        GIVEAWAY_SERVICE
    )
    coupon_packages_page.search_coupon_package(COUPON_PACKAGE_NAME)
    coupon_packages_page.wait_for_coupon_package_row(COUPON_PACKAGE_NAME)

    return coupon_packages_page


def test_coupon_packages_page_loads(browser):

    coupon_packages_page = open_coupon_packages_page(browser)
    body_text = coupon_packages_page.get_body_text()

    assert "Coupon package name" in body_text
    assert "Discount assigned" in body_text
    assert "Services assigned" in body_text
    assert "Status" in body_text


def test_coupon_packages_missing_search(browser):

    coupon_packages_page = open_coupon_packages_page(browser)
    coupon_packages_page.search_coupon_package(MISSING_COUPON_PACKAGE)

    assert MISSING_COUPON_PACKAGE not in coupon_packages_page.get_body_text()


def test_create_coupon_package_required_name_validation(browser):

    coupon_packages_page = open_coupon_packages_page(browser)
    coupon_packages_page.open_create_coupon_package()
    coupon_packages_page.click_save_coupon_package()

    assert not coupon_packages_page.coupon_package_name_input_is_valid()
    assert coupon_packages_page.get_coupon_package_name_validation_message() != ""


def test_create_vk_acc2_coupon_package(browser):

    coupon_packages_page = create_coupon_package_if_missing(browser)
    coupon_packages_page.wait_for_list_loaded()
    coupon_packages_page.search_coupon_package(COUPON_PACKAGE_NAME)

    assert coupon_packages_page.wait_for_coupon_package_row(
        COUPON_PACKAGE_NAME
    ).is_displayed()


def test_vk_acc2_coupon_package_settings_persist(browser):

    coupon_packages_page = create_coupon_package_if_missing(browser)
    coupon_packages_page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
    body_text = coupon_packages_page.get_body_text().lower()

    assert coupon_packages_page.get_coupon_package_name_value() == COUPON_PACKAGE_NAME
    assert DISCOUNT_NAME.lower() in body_text
    assert GIVEAWAY_SERVICE.lower() in body_text
    assert coupon_packages_page.active_switch_is_on()
