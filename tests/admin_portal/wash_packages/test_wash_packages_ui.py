import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    EXISTING_PACKAGE,
    open_wash_packages_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("UI"),
]


@allure.title("WP-LST-001 Wash packages list loads with all primary controls")
@pytest.mark.sanity
@pytest.mark.prod_smoke
def test_wash_packages_page_loads_with_primary_controls(browser):
    page = open_wash_packages_page(browser)
    body_text = page.get_body_text()

    assert "Wash packages" in body_text
    assert "Wash package name" in body_text
    assert "Price" in body_text
    assert "Status" in body_text
    assert page.search_input_is_visible()
    assert page.filter_button_is_clickable()
    assert page.download_button_is_clickable()
    assert page.add_package_button_is_clickable()
    assert page_has_no_broken_state(page)


@allure.title("WP-LST-002 Visible package rows display name, price, status and edit action")
@pytest.mark.sanity
def test_wash_packages_grid_columns_are_visible(browser):
    page = open_wash_packages_page(browser)
    body_text = page.get_body_text()

    assert "Wash package name" in body_text
    assert "Price" in body_text
    assert "Status" in body_text
    assert page.every_visible_row_has_edit_action()
    assert page_has_no_broken_state(page)


@allure.title("WP-LST-003 Pagination and results-per-page controls are visible")
@pytest.mark.regression
def test_wash_packages_pagination_controls_are_visible(browser):
    page = open_wash_packages_page(browser)

    assert page.pagination_controls_are_visible()
    assert page.results_per_page_control_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("WP-UI Add wash package form shows service settings, toggles, save and cancel")
@pytest.mark.sanity
def test_add_wash_package_form_loads(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    body_text = page.get_body_text()

    assert "Service settings" in body_text
    assert "Service name" in body_text
    assert "Global price" in body_text
    assert "Global commission" in body_text
    assert page.active_switch_is_on()
    assert page.save_package_button_is_clickable()
    assert page.cancel_button_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("WP-UI Discount settings tab loads with applicable discounts combobox")
@pytest.mark.regression
def test_discount_settings_tab_loads(browser):
    page = open_wash_packages_page(browser)
    page.open_edit_package(EXISTING_PACKAGE)
    page.open_discount_settings()

    assert "Applicable discounts" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("WP-UI Filter panel exposes site dropdown and active service controls")
@pytest.mark.regression
def test_wash_packages_filter_panel_shows_controls(browser):
    page = open_wash_packages_page(browser)

    assert page.filter_panel_controls_are_visible()
    assert page_has_no_broken_state(page)
