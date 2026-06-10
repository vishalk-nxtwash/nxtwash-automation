from pages.admin_portal.service_categories_page import ServiceCategoriesPage
from tests.admin_portal.admin_session import open_admin_path


EXISTING_CATEGORY = CATEGORY_NAME = "VK ASC1"
MISSING_CATEGORY = "category-does-not-exist-automation"
UPDATED_CATEGORY_NAME = "VK ASC1 edited"
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def open_service_categories_page(browser):

    open_admin_path(browser, "/services/serviceCategories")

    page = ServiceCategoriesPage(browser)
    page.wait_for_list_loaded()

    return page


def create_category_if_missing(browser, category_name=CATEGORY_NAME):

    page = open_service_categories_page(browser)

    if page.category_exists(category_name):
        return page

    page.create_category(category_name)
    page.search_category(category_name)
    page.wait_for_category_row(category_name)

    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)
