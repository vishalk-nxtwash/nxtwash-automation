import pytest

from pages.admin_portal.custom_services_page import CustomServicesPage
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._data import load as _load

_D = _load("custom_services")

EXISTING_SERVICE            = _D["reference"]["existing_service"]
MISSING_SERVICE             = _D["search"]["nonexistent"]
ASSIGNMENT_SITE             = _D["reference"]["assignment_site"]
SERVICE_NAME                = _D["template"]["service_name"]
UPDATED_SERVICE_NAME        = _D["updated"]["service_name"]
SERVICE_CATEGORY            = _D["reference"]["service_category"]
INACTIVE_CATEGORY           = _D["reference"]["inactive_category"]
GLOBAL_PRICE                = _D["template"]["global_price"]
GLOBAL_COMMISSION           = _D["template"]["global_commission"]
VISIBLE_PRICE               = _D["template"]["visible_price"]
SITE_OVERRIDE_PRICE         = _D["updated"]["site_override_price"]
SITE_OVERRIDE_PRICE_HIGH    = _D["updated"]["site_override_price_high"]
SITE_OVERRIDE_COMMISSION    = _D["updated"]["site_override_commission"]
APPLICABLE_DISCOUNT         = _D["reference"]["applicable_discount"]
SECOND_APPLICABLE_DISCOUNT  = _D["reference"]["second_applicable_discount"]
BARCODE_VALUE               = _D["template"]["barcode"]
DESCRIPTION_TEXT            = _D["template"]["description"]
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def open_custom_services_page(browser):

    open_admin_path(browser, "/services/customServices")

    page = CustomServicesPage(browser)
    page.wait_for_list_loaded()

    return page


def create_service_if_missing(browser, service_name=SERVICE_NAME):

    page = open_custom_services_page(browser)

    if page.service_exists(service_name):
        page.open_edit_service(service_name)
        page.ensure_active_switch_on()
        page.set_global_price(GLOBAL_PRICE)
        page.click_save_service()
        return open_custom_services_page(browser)

    # service_exists() only scans the active-filter view.  A deactivate test may
    # have left the service inactive; a create attempt on a duplicate name fails
    # silently, then wait_for_service_row() burns the full timeout.  Reset filters
    # and re-check with a short timeout before falling through to create.
    from selenium.common.exceptions import TimeoutException as _TE
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    page.reset_filters()
    page.search_service(service_name)
    locator = page.get_service_row_locator(service_name)
    try:
        WebDriverWait(page.driver, 10).until(EC.visibility_of_element_located(locator))
        inactive_found = True
    except _TE:
        inactive_found = False

    if inactive_found:
        page.open_edit_service(service_name)
        page.ensure_active_switch_on()
        page.set_global_price(GLOBAL_PRICE)
        page.click_save_service()
        return open_custom_services_page(browser)

    page.create_service(
        service_name,
        SERVICE_CATEGORY,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        ASSIGNMENT_SITE,
    )
    page = open_custom_services_page(browser)
    page.search_service(service_name)
    page.wait_for_service_row(service_name)

    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


@pytest.fixture
def managed_service(browser):
    """Ensure SERVICE_NAME exists at baseline before the test and restore after."""
    page = create_service_if_missing(browser)
    yield page
    create_service_if_missing(browser)
