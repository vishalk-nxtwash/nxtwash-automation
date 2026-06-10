from tests.admin_portal.test_wash_packages import ASSIGNMENT_SITE
from tests.admin_portal.test_wash_packages import open_wash_packages_page


PACKAGE_NAME = "Vk detail wash"
POINTS_AWARDED = "3"
POINTS_REDEEMED = "1"
GLOBAL_PRICE = "30"
GLOBAL_COMMISSION = "5"
VISIBLE_PRICE = "$30.00"


def create_wash_package_if_missing(browser, package_name=PACKAGE_NAME):

    wash_packages_page = open_wash_packages_page(browser)

    if wash_packages_page.package_exists(package_name):
        return wash_packages_page

    wash_packages_page.create_package(
        package_name,
        POINTS_AWARDED,
        POINTS_REDEEMED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        ASSIGNMENT_SITE
    )
    wash_packages_page.search_package(package_name)
    wash_packages_page.wait_for_package_row(package_name)

    return wash_packages_page


def test_create_wash_package_required_service_name_validation(browser):

    wash_packages_page = open_wash_packages_page(browser)
    wash_packages_page.open_create_package()
    wash_packages_page.click_save_package()

    assert not wash_packages_page.service_name_input_is_valid()
    assert wash_packages_page.get_service_name_validation_message() != ""


def test_create_vk_detail_wash_active_package(browser):

    wash_packages_page = create_wash_package_if_missing(browser)
    wash_packages_page.wait_for_list_loaded()
    wash_packages_page.search_package(PACKAGE_NAME)

    assert wash_packages_page.wait_for_package_row(PACKAGE_NAME).is_displayed()
    assert wash_packages_page.get_package_price(PACKAGE_NAME) == VISIBLE_PRICE
    assert wash_packages_page.get_package_status(PACKAGE_NAME) == "Active"


def test_create_vk_detail_wash_does_not_duplicate_existing_package(browser):

    wash_packages_page = create_wash_package_if_missing(browser)
    wash_packages_page.wait_for_list_loaded()
    wash_packages_page.search_package(PACKAGE_NAME)

    assert wash_packages_page.wait_for_package_row(PACKAGE_NAME).is_displayed()
    assert wash_packages_page.get_package_price(PACKAGE_NAME) == VISIBLE_PRICE
    assert wash_packages_page.get_package_status(PACKAGE_NAME) == "Active"
