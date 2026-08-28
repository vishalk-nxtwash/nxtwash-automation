from selenium.webdriver.common.by import By

from pages.admin_portal.service_categories_page import ServiceCategoriesPage
from tests.admin_portal._managed import managed_name
from tests.admin_portal._managed import managed_resource
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._data import load as _load

_D = _load("service_categories")

CATEGORY_NAME          = _D["reference"]["active_category"]
INACTIVE_CATEGORY_NAME = _D["reference"]["inactive_category"]
MISSING_CATEGORY       = _D["search"]["nonexistent"]
UPDATED_CATEGORY_NAME  = _D["updated"]["category_name"]

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
    import time
    page = open_service_categories_page(browser)

    # Fast path: the default list only shows Active categories, so if the
    # managed name appears in a quick probe the state is already correct.
    # Skipping the two full category_exists() calls saves ~200 s per call.
    page.search_category(MANAGED_CATEGORY)
    if page._quick_category_row(MANAGED_CATEGORY, timeout=6) is not None:
        return page

    # Full reset: category is missing, renamed, or inactive.
    # Check MANAGED_CATEGORY_EDITED in the active list first (fast 6-second probe).
    page.search_category(MANAGED_CATEGORY_EDITED)
    edited_active = page._quick_category_row(MANAGED_CATEGORY_EDITED, timeout=6)

    if edited_active is not None:
        # Test renamed the category and left it active.
        edit_btn = edited_active.find_element(
            By.XPATH, ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        page.driver.execute_script("arguments[0].click();", edit_btn)
        page.wait_for_edit_loaded()
        page.enter_category_name(MANAGED_CATEGORY)
        page.ensure_active_switch_on()
        page.click_save_changes()
        time.sleep(3)
        return open_service_categories_page(browser)

    # Neither MANAGED_CATEGORY nor MANAGED_CATEGORY_EDITED in the active list.
    # Apply the inactive filter ONCE and check both names in a single pass —
    # avoids the two expensive category_exists() calls that each open/reset
    # the filter panel independently (~130 s each).
    inactive_row, found_name = page._find_first_matching_inactive(
        MANAGED_CATEGORY_EDITED, MANAGED_CATEGORY
    )

    if found_name == MANAGED_CATEGORY_EDITED:
        # Deactivated and renamed by a previous test.
        edit_btn = inactive_row.find_element(
            By.XPATH, ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        page.driver.execute_script("arguments[0].click();", edit_btn)
        page.wait_for_edit_loaded()
        page.enter_category_name(MANAGED_CATEGORY)
        page.ensure_active_switch_on()
        page.click_save_changes()
        time.sleep(3)
        return open_service_categories_page(browser)

    if found_name == MANAGED_CATEGORY:
        # Exists but was deactivated by a previous test.
        edit_btn = inactive_row.find_element(
            By.XPATH, ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        page.driver.execute_script("arguments[0].click();", edit_btn)
        page.wait_for_edit_loaded()
        page.ensure_active_switch_on()
        page.click_save_changes()
        time.sleep(3)
        return open_service_categories_page(browser)

    # Neither name found anywhere — create fresh.
    page = open_service_categories_page(browser)
    page.create_category(MANAGED_CATEGORY)
    page.search_category(MANAGED_CATEGORY)
    page.wait_for_category_row(MANAGED_CATEGORY)
    return page


managed_category = managed_resource(reset_managed_category)
