import allure
import pytest

from tests.admin_portal.customers.conftest import (
    open_customers_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Customers"),
    allure.story("UI"),
]


@allure.title("CUST-LST-001 Customers page loads with all primary controls")
@pytest.mark.smoke
def test_customers_page_loads_with_primary_controls(browser):
    page = open_customers_page(browser)
    body = page.get_body_text()

    assert "Customers" in body
    assert page.search_input_is_visible()
    assert page.filter_button_is_clickable()
    assert page.download_button_is_clickable()
    assert page.add_customer_button_is_clickable()
    assert page_has_no_broken_state(page)


@allure.title("CUST-LST-002 Grid membership status column is present")
@pytest.mark.regression
@pytest.mark.skip(reason="Requires Memberships module fixtures and active member records.")
def test_grid_membership_status_column_visible(browser):
    pass


@allure.title("CUST-LST-003 Pagination and results-per-page controls are visible")
@pytest.mark.regression
def test_pagination_and_results_per_page_visible(browser):
    page = open_customers_page(browser)

    assert page.pagination_controls_are_visible()
    assert page.results_per_page_control_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("CUST-UI Add new customer form shows required fields, save and cancel controls")
@pytest.mark.smoke
def test_add_customer_form_loads_with_required_controls(browser):
    page = open_customers_page(browser)
    page.open_create_customer()
    body = page.get_body_text()

    assert "First Name" in body
    assert "Last Name" in body
    assert page.active_switch_is_on()
    assert page.save_customer_button_is_clickable()
    assert page.cancel_button_is_visible()
    assert page_has_no_broken_state(page)
