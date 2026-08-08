from pages.admin_portal.coupon_packages_page import CouponPackagesPage
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal.discounts.conftest import DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import PERCENTAGE_DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import create_discount_if_missing
from tests.admin_portal.discounts.conftest import create_percentage_discount_if_missing
from tests.admin_portal._managed import managed_name, managed_resource
from tests.admin_portal._data import load as _load

_D = _load("coupon_packages")

COUPON_PACKAGE_NAME          = _D["reference"]["existing_package"]
COUPON_PACKAGE_INACTIVE_NAME = _D["reference"]["inactive_package"]
GIVEAWAY_SERVICE             = _D["reference"]["giveaway_service"]
GIVEAWAY_SERVICES            = tuple(_D["reference"]["giveaway_services"])
MISSING_COUPON_PACKAGE       = _D["search"]["nonexistent"]
EXPIRATION_DAYS              = _D["reference"]["expiration_days"]
SECOND_DISCOUNT_NAME         = PERCENTAGE_DISCOUNT_NAME

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
    page.reset_filters()

    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


def create_coupon_package_if_missing(browser):

    create_discount_if_missing(browser, DISCOUNT_NAME)
    page = open_coupon_packages_page(browser)

    if page.coupon_package_exists(COUPON_PACKAGE_NAME):
        page = open_coupon_packages_page(browser)
        page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
        page.clear_assign_discount()
        page.select_assign_discount(DISCOUNT_NAME)
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


def create_inactive_coupon_package_if_missing(browser):

    create_discount_if_missing(browser, DISCOUNT_NAME)
    page = open_coupon_packages_page(browser)
    page.show_all_packages()

    if page.coupon_package_exists(COUPON_PACKAGE_INACTIVE_NAME):
        if page.get_coupon_package_status(COUPON_PACKAGE_INACTIVE_NAME) == "Active":
            page.deactivate_coupon_package(COUPON_PACKAGE_INACTIVE_NAME)
            page.show_all_packages()
        return page

    page.create_inactive_coupon_package(
        COUPON_PACKAGE_INACTIVE_NAME,
        DISCOUNT_NAME,
        GIVEAWAY_SERVICE
    )
    page.show_all_packages()
    page.search_coupon_package(COUPON_PACKAGE_INACTIVE_NAME)
    page.wait_for_coupon_package_row(COUPON_PACKAGE_INACTIVE_NAME)

    return page


MANAGED_COUPON_PACKAGE = managed_name("Coupon Pkg")


def _reset_managed_coupon_package(browser):
    create_discount_if_missing(browser, DISCOUNT_NAME)
    page = open_coupon_packages_page(browser)
    if page.coupon_package_exists(MANAGED_COUPON_PACKAGE):
        page = open_coupon_packages_page(browser)
        page.open_edit_coupon_package(MANAGED_COUPON_PACKAGE)
        page.clear_assign_discount()
        page.select_assign_discount(DISCOUNT_NAME)
        page.ensure_active_switch_on()
        page.click_save_coupon_package()
        return open_coupon_packages_page(browser)
    page.create_coupon_package(MANAGED_COUPON_PACKAGE, DISCOUNT_NAME, GIVEAWAY_SERVICE)
    return open_coupon_packages_page(browser)


managed_coupon_package = managed_resource(_reset_managed_coupon_package)
