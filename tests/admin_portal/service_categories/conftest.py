from pages.admin_portal.service_categories_page import ServiceCategoriesPage
from tests.admin_portal._managed import managed_name
from tests.admin_portal._managed import managed_resource
from tests.admin_portal.admin_session import open_admin_path


CATEGORY_NAME = "VK ASC1"
INACTIVE_CATEGORY_NAME = "VK ASC2"
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
    """Ensure an active category exists and return the page."""
    page = open_service_categories_page(browser)

    if page.category_exists(category_name):
        return page

    page.create_category(category_name)
    page.search_category(category_name)
    page.wait_for_category_row(category_name)

    return page


def create_inactive_category_if_missing(browser, category_name=INACTIVE_CATEGORY_NAME):
    """Ensure an inactive category exists and is actually inactive.

    If the category was accidentally activated by a previous test it is
    deactivated before returning, so callers always get a truly inactive record.
    """
    page = open_service_categories_page(browser)

    if not page.category_exists(category_name):
        page.create_inactive_category(category_name)
        return page

    if page.get_category_status(category_name) != "Inactive":
        import time
        page.open_edit_category(category_name)
        page.ensure_active_switch_off()
        page.click_save_changes()
        time.sleep(3)
        page = open_service_categories_page(browser)

    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


# ------------------------------------------------------------------ Managed

MANAGED_CATEGORY = managed_name("Category")
MANAGED_CATEGORY_EDITED = "%s edited" % MANAGED_CATEGORY


def reset_managed_category(browser):
    """Ensure the managed category exists at its baseline name and is Active.

    Handles three cases:
    - Renamed by a test   → rename back to baseline
    - Does not exist yet  → create it
    - Deactivated by test → re-activate it
    """
    page = open_service_categories_page(browser)

    if page.category_exists(MANAGED_CATEGORY_EDITED):
        # Rename back — bypass update_category_name to avoid wait_for_list_loaded
        # failing when the category was opened via the inactive-filter fallback.
        # A brief sleep after save gives the API time to complete before we
        # force-navigate fresh.
        import time
        page.open_edit_category(MANAGED_CATEGORY_EDITED)
        page.enter_category_name(MANAGED_CATEGORY)
        page.ensure_active_switch_on()
        page.click_save_changes()
        time.sleep(3)
        page = open_service_categories_page(browser)
    elif not page.category_exists(MANAGED_CATEGORY):
        page.create_category(MANAGED_CATEGORY)
        page.search_category(MANAGED_CATEGORY)
        page.wait_for_category_row(MANAGED_CATEGORY)
        return page

    # Restore active status if a test deactivated the category
    page.search_category(MANAGED_CATEGORY)
    if page.get_category_status(MANAGED_CATEGORY) != "Active":
        import time
        page.open_edit_category(MANAGED_CATEGORY)
        page.ensure_active_switch_on()
        page.click_save_changes()
        time.sleep(3)
        page = open_service_categories_page(browser)

    return page


managed_category = managed_resource(reset_managed_category)
