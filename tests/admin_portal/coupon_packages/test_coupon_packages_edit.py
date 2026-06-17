from tests.admin_portal.coupon_packages.conftest import COUPON_PACKAGE_NAME
from tests.admin_portal.coupon_packages.conftest import GIVEAWAY_SERVICES
from tests.admin_portal.coupon_packages.conftest import create_coupon_package_if_missing


def test_edit_coupon_package_giveaway_services(browser):

    page = create_coupon_package_if_missing(browser)
    page.update_coupon_giveaway_services(COUPON_PACKAGE_NAME, GIVEAWAY_SERVICES)
    page.open_edit_coupon_package(COUPON_PACKAGE_NAME)
    selected_values = page.checked_giveaway_values()

    assert "vk detail wash" in selected_values
    assert "detail cleaning" in selected_values
