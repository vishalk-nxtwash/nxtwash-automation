from tests.admin_portal.coupon_packages.conftest import MISSING_COUPON_PACKAGE
from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page
from tests.admin_portal.coupon_packages.conftest import page_has_no_broken_state


def test_missing_coupon_package_is_not_returned(browser):

    page = open_coupon_packages_page(browser)
    page.search_coupon_package(MISSING_COUPON_PACKAGE)

    assert MISSING_COUPON_PACKAGE not in page.get_body_text()


def test_coupon_packages_special_character_search_stays_usable(browser):

    page = open_coupon_packages_page(browser)
    page.search_coupon_package("' OR 1=1 --")

    assert page_has_no_broken_state(page)
