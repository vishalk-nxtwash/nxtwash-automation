from tests.admin_portal.coupon_packages.conftest import COUPON_PACKAGE_NAME
from tests.admin_portal.coupon_packages.conftest import create_coupon_package_if_missing


def test_coupon_package_create_is_idempotent(browser):

    page = create_coupon_package_if_missing(browser)
    page.search_coupon_package(COUPON_PACKAGE_NAME)

    assert page.wait_for_coupon_package_row(COUPON_PACKAGE_NAME).is_displayed()


def test_coupon_package_long_name_does_not_break_form(browser):

    page = create_coupon_package_if_missing(browser)
    page.open_create_coupon_package()
    page.enter_coupon_package_name("VK " + ("C" * 128))

    assert page.get_coupon_package_name_value().startswith("VK ")
    assert "Coupon package name" in page.get_body_text()
