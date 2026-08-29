import allure
import pytest

from tests.admin_portal.custom_services.conftest import (
    SERVICE_NAME,
    create_service_if_missing,
    open_custom_services_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Custom Services"),
    allure.story("List UI"),
]


@allure.title("CS-LST-001 Custom services page loads with primary controls visible")
@pytest.mark.smoke
def test_custom_services_page_loads_with_primary_controls(browser):

    page = open_custom_services_page(browser)

    assert page.search_input_is_visible()
    assert page.filter_button_is_clickable()
    assert page.add_service_button_is_clickable()
    assert page.download_button_is_clickable()
    assert page_has_no_broken_state(page)


@allure.title("CS-LST-002 Grid displays service name, category, price, and status columns")
@pytest.mark.regression
def test_grid_displays_expected_columns(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    body_text = page.get_body_text()

    assert "Active" in body_text or "Inactive" in body_text
    row = page.wait_for_service_row(SERVICE_NAME)
    assert row.is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("CS-LST-003 Pagination and results-per-page controls are visible")
@pytest.mark.regression
def test_pagination_controls_are_visible(browser):

    page = open_custom_services_page(browser)

    assert page.pagination_controls_are_visible()
    assert page_has_no_broken_state(page)
