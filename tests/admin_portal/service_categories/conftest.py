from pages.admin_portal.service_categories_page import ServiceCategoriesPage
from tests.admin_portal._managed import managed_name
from tests.admin_portal._managed import managed_resource
from tests.admin_portal.admin_session import open_admin_path


CATEGORY_NAME = "VK ASC1"
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


# --- Managed (self-cleaning) service category ------------------------------
# A dedicated record reset to baseline before and after each mutating test.
# Service categories cannot be deleted in the product; the only mutable field
# is the name, so the reset renames the record back to baseline (handling the
# case where a test renamed it). See tests/admin_portal/_managed.py.

MANAGED_CATEGORY = managed_name("Category")
MANAGED_CATEGORY_EDITED = "%s edited" % MANAGED_CATEGORY


def reset_managed_category(browser):
    """Ensure the managed category exists at its baseline name."""
    page = open_service_categories_page(browser)

    if page.category_exists(MANAGED_CATEGORY):
        return page

    # A previous test may have left it renamed; restore the baseline name.
    if page.category_exists(MANAGED_CATEGORY_EDITED):
        page.update_category_name(MANAGED_CATEGORY_EDITED, MANAGED_CATEGORY)
        return page

    page.create_category(MANAGED_CATEGORY)
    page.search_category(MANAGED_CATEGORY)
    page.wait_for_category_row(MANAGED_CATEGORY)

    return page


managed_category = managed_resource(reset_managed_category)
