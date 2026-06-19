from tests.admin_portal.coupon_packages.conftest import MISSING_COUPON_PACKAGE
from tests.admin_portal.coupon_packages.conftest import create_coupon_package_if_missing
from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page
from tests.admin_portal.coupon_packages.conftest import page_has_no_broken_state
from tests.admin_portal.coupon_packages.conftest import COUPON_PACKAGE_NAME


def test_coupon_packages_existing_search(browser):

    page = create_coupon_package_if_missing(browser)
    page.search_coupon_package(COUPON_PACKAGE_NAME)

    assert page.wait_for_coupon_package_row(COUPON_PACKAGE_NAME).is_displayed()


def test_coupon_packages_missing_search(browser):

    page = open_coupon_packages_page(browser)
    page.search_coupon_package(MISSING_COUPON_PACKAGE)

    assert MISSING_COUPON_PACKAGE not in page.get_body_text()


def test_coupon_packages_search_payloads_do_not_break_grid(browser):

    page = open_coupon_packages_page(browser)
    page.search_coupon_package("<script>alert(1)</script>")

    assert page_has_no_broken_state(page)
