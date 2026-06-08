from pages.admin_portal.login_page import AdminLoginPage
from pages.admin_portal.service_categories_page import ServiceCategoriesPage
from pages.admin_portal.sidebar import AdminSidebar


CATEGORY_NAME = "VK wash01"


def open_service_categories_page(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()
    login_page.login()
    login_page.wait_for_overview()

    sidebar = AdminSidebar(browser)
    sidebar.open_service_categories()

    service_categories_page = ServiceCategoriesPage(browser)
    service_categories_page.wait_for_list_loaded()

    return service_categories_page


def create_category_if_missing(browser, category_name=CATEGORY_NAME):

    service_categories_page = open_service_categories_page(browser)

    if service_categories_page.category_exists(category_name):
        return service_categories_page

    service_categories_page.create_category(category_name)
    service_categories_page.search_category(category_name)
    service_categories_page.wait_for_category_row(category_name)

    return service_categories_page


def test_create_service_category_required_name_validation(browser):

    service_categories_page = open_service_categories_page(browser)
    service_categories_page.open_create_category()
    service_categories_page.click_save_new()

    assert not service_categories_page.category_name_input_is_valid()
    assert service_categories_page.get_category_name_validation_message() != ""


def test_create_vk_wash01_active_service_category(browser):

    service_categories_page = create_category_if_missing(browser)
    service_categories_page.wait_for_list_loaded()
    service_categories_page.search_category(CATEGORY_NAME)

    assert service_categories_page.wait_for_category_row(
        CATEGORY_NAME
    ).is_displayed()
    assert service_categories_page.get_category_status(CATEGORY_NAME) == "Active"


def test_create_vk_wash01_does_not_duplicate_existing_category(browser):

    service_categories_page = create_category_if_missing(browser)
    service_categories_page.wait_for_list_loaded()
    service_categories_page.search_category(CATEGORY_NAME)

    assert service_categories_page.wait_for_category_row(
        CATEGORY_NAME
    ).is_displayed()
    assert service_categories_page.get_category_status(CATEGORY_NAME) == "Active"
