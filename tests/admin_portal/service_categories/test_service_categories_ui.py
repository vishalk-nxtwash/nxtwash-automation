import logging

import allure
import pytest

from tests.admin_portal.service_categories.conftest import open_service_categories_page
from tests.admin_portal.service_categories.conftest import page_has_no_broken_state


LOG = logging.getLogger("nxtwash")


@allure.epic("Admin Portal")
@allure.feature("Service Categories")
@allure.story("UI")
@allure.title("SC-UI list shell, controls, grid, and pagination")
@pytest.mark.sanity
def test_service_categories_list_shell_controls_and_grid(browser):
    LOG.info("Verifying Service Categories list shell and controls")
    page = open_service_categories_page(browser)
    body_text = page.get_body_text()

    assert "Service categories" in body_text
    assert "Service category" in body_text
    assert "Status" in body_text
    assert page.search_input_is_visible()
    assert page.filter_button_is_clickable()
    assert page.download_button_is_clickable()
    assert page.add_category_button_is_clickable()
    assert page.pagination_controls_are_visible()
    assert page.results_per_page_control_is_visible()
    assert page_has_no_broken_state(page)


@allure.epic("Admin Portal")
@allure.feature("Service Categories")
@allure.story("UI")
@allure.title("SC-UI add service category form controls")
@pytest.mark.sanity
def test_add_service_category_form_controls(browser):
    LOG.info("Verifying Add Service Category form controls")
    page = open_service_categories_page(browser)
    page.open_create_category()

    assert "Category name" in page.get_body_text()
    assert "Active service" in page.get_body_text()
    assert page.active_switch_is_on()
    assert page.save_new_button_is_clickable()
    assert page.cancel_button_is_visible()


@allure.title("SC-UI legacy page load with primary controls")
@pytest.mark.sanity
def test_service_categories_page_loads_with_primary_controls(browser):

    page = open_service_categories_page(browser)
    body_text = page.get_body_text()

    assert "Service category" in body_text
    assert "Status" in body_text
    assert "Add new category" in body_text
    assert page_has_no_broken_state(page)


@allure.title("SC-UI legacy add service category form loads")
@pytest.mark.sanity
def test_add_service_category_form_loads(browser):

    page = open_service_categories_page(browser)
    page.open_create_category()

    assert "Category name" in page.get_body_text()
    assert "Active service" in page.get_body_text()
    assert page.active_switch_is_on()
