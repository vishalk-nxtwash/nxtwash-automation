from pages.admin_portal.login_page import AdminLoginPage
from pages.admin_portal.service_categories_page import ServiceCategoriesPage
from pages.admin_portal.sidebar import AdminSidebar


EXISTING_CATEGORY = "Drinks!!!!"
MISSING_CATEGORY = "category-does-not-exist-automation"


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


def test_service_categories_page_loads(browser):

    service_categories_page = open_service_categories_page(browser)

    assert "Service category" in service_categories_page.get_body_text()
    assert "Status" in service_categories_page.get_body_text()


def test_service_categories_existing_category_search(browser):

    service_categories_page = open_service_categories_page(browser)
    service_categories_page.search_category(EXISTING_CATEGORY)

    assert service_categories_page.wait_for_category_row(
        EXISTING_CATEGORY
    ).is_displayed()


def test_service_categories_missing_category_search(browser):

    service_categories_page = open_service_categories_page(browser)
    service_categories_page.search_category(MISSING_CATEGORY)

    assert MISSING_CATEGORY not in service_categories_page.get_body_text()
