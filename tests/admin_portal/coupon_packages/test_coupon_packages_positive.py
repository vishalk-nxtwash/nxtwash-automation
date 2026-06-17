from tests.admin_portal.coupon_packages.conftest import COUPON_PACKAGE_NAME
from tests.admin_portal.coupon_packages.conftest import DISCOUNT_NAME
from tests.admin_portal.coupon_packages.conftest import GIVEAWAY_SERVICE
from tests.admin_portal.coupon_packages.conftest import create_coupon_package_if_missing


def test_create_coupon_package(browser):

    page = create_coupon_package_if_missing(browser)
    page.search_coupon_package(COUPON_PACKAGE_NAME)

    assert page.wait_for_coupon_package_row(COUPON_PACKAGE_NAME).is_displayed()


def test_coupon_package_settings_persist(browser):

    page = create_coupon_package_if_missing(browser)
    page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
    body_text = page.get_body_text().lower()

    assert page.get_coupon_package_name_value() == COUPON_PACKAGE_NAME
    assert DISCOUNT_NAME.lower() in body_text
    assert GIVEAWAY_SERVICE.lower() in body_text
    assert page.active_switch_is_on()
