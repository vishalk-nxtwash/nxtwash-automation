from tests.admin_portal.test_create_wash_package import PACKAGE_NAME
from tests.admin_portal.test_create_wash_package import create_wash_package_if_missing


UPDATED_PACKAGE_NAME = "Vk detail wash edited"
APPLICABLE_DISCOUNT = "Basic Discount"


def test_open_edit_wash_package(browser):

    wash_packages_page = create_wash_package_if_missing(browser)
    wash_packages_page.open_edit_package(PACKAGE_NAME)

    assert wash_packages_page.get_service_name_value() == PACKAGE_NAME
    assert wash_packages_page.active_switch_is_on()


def test_cancel_edit_wash_package_does_not_change_package(browser):

    wash_packages_page = create_wash_package_if_missing(browser)
    wash_packages_page.open_edit_package(PACKAGE_NAME)
    wash_packages_page.enter_service_name(UPDATED_PACKAGE_NAME)
    wash_packages_page.click_cancel()
    wash_packages_page.wait_for_list_loaded()
    wash_packages_page.search_package(PACKAGE_NAME)

    assert wash_packages_page.wait_for_package_row(PACKAGE_NAME).is_displayed()


def test_link_basic_discount_to_vk_detail_wash_package(browser):

    wash_packages_page = create_wash_package_if_missing(browser)
    wash_packages_page.open_edit_package(PACKAGE_NAME)
    wash_packages_page.open_discount_settings()
    wash_packages_page.select_applicable_discount(APPLICABLE_DISCOUNT)
    wash_packages_page.click_save_package()
    wash_packages_page.wait_for_list_loaded()

    wash_packages_page.open_edit_package(PACKAGE_NAME)
    wash_packages_page.open_discount_settings()

    assert wash_packages_page.discount_is_selected(APPLICABLE_DISCOUNT)
