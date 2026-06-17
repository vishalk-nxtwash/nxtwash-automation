from pages.admin_portal.wash_packages_page import WashPackagesPage
from tests.admin_portal.admin_session import open_admin_path


EXISTING_PACKAGE = "Plus Wash"
MISSING_PACKAGE = "wash-package-does-not-exist-automation"
ASSIGNMENT_SITE = "VK Test carwash 2"
PACKAGE_NAME = "VK AWP1"
UPDATED_PACKAGE_NAME = "VK AWP1 edited"
POINTS_AWARDED = "3"
POINTS_REDEEMED = "1"
GLOBAL_PRICE = "30"
GLOBAL_COMMISSION = "5"
VISIBLE_PRICE = "$30.00"
APPLICABLE_DISCOUNT = "Basic Discount"
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def open_wash_packages_page(browser):

    open_admin_path(browser, "/services/washPackages")

    page = WashPackagesPage(browser)
    page.wait_for_list_loaded()

    return page


def create_wash_package_if_missing(browser, package_name=PACKAGE_NAME):

    page = open_wash_packages_page(browser)

    if page.package_exists(package_name):
        page.open_edit_package(package_name)
        page.fill_package_form(
            package_name,
            POINTS_AWARDED,
            POINTS_REDEEMED,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION,
            ASSIGNMENT_SITE
        )
        page.click_save_package()
        return open_wash_packages_page(browser)

    page.create_package(
        package_name,
        POINTS_AWARDED,
        POINTS_REDEEMED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        ASSIGNMENT_SITE
    )
    page = open_wash_packages_page(browser)
    page.search_package(package_name)
    page.wait_for_package_row(package_name)

    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)
