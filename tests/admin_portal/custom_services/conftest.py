import pytest

from pages.admin_portal.custom_services_page import CustomServicesPage
from tests.admin_portal.admin_session import open_admin_path


EXISTING_SERVICE = "VK ACS1"
MISSING_SERVICE = "custom-service-does-not-exist-automation"
ASSIGNMENT_SITE = "VK AL11"
SERVICE_NAME = "VK ACS1"
UPDATED_SERVICE_NAME = "VK ACS1 edited"
SERVICE_CATEGORY = "VK ASC1"
INACTIVE_CATEGORY = "VK ASC2"
GLOBAL_PRICE = "15"
GLOBAL_COMMISSION = "3"
VISIBLE_PRICE = "$15.00"
SITE_OVERRIDE_PRICE = "10"
SITE_OVERRIDE_PRICE_HIGH = "20"
SITE_OVERRIDE_COMMISSION = "6"
APPLICABLE_DISCOUNT = "Basic Discount"
SECOND_APPLICABLE_DISCOUNT = "VK AD01"
BARCODE_VALUE = "VK-SVC-001"
DESCRIPTION_TEXT = "VK automation test description"
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
        page = open_custom_services_page(browser)
        page.open_edit_service(service_name)
        page.fill_service_form(
            service_name,
            SERVICE_CATEGORY,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION,
            ASSIGNMENT_SITE,
        )
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
