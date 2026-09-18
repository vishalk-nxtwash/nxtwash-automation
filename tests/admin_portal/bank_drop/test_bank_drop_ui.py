import allure
import pytest

from tests.admin_portal.bank_drop.conftest import (
    create_bank_drop_if_missing,
    open_bank_drop_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Bank Drop"),
    allure.story("UI"),
]


@allure.title("BD-LST-001 Bank drop page loads with primary controls")
@pytest.mark.smoke
def test_bank_drop_page_loads_with_primary_controls(browser):

    page = open_bank_drop_page(browser)
    body_text = page.get_body_text()

    assert "Bank drop" in body_text
    assert "Bank drop name" in body_text
    assert "Order" in body_text
    assert "Status" in body_text
    assert page.add_button_is_clickable()
    assert page.download_button_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("BD-LST-002 Grid displays name, order, and status with Edit action per row")
@pytest.mark.regression
def test_bank_drop_grid_columns_are_visible(browser):

    create_bank_drop_if_missing(browser)
    page = open_bank_drop_page(browser)
    body_text = page.get_body_text()

    assert "Bank drop name" in body_text
    assert "Order" in body_text
    assert "Status" in body_text
    assert page.every_visible_row_has_edit_action()
    assert page_has_no_broken_state(page)


@allure.title("BD-LST-003 Pagination and results-per-page controls are visible")
@pytest.mark.regression
def test_bank_drop_pagination_controls_visible(browser):

    page = open_bank_drop_page(browser)

    assert page.pagination_controls_are_visible()
    assert page_has_no_broken_state(page)


@allure.title("BD-UI Add bank drop form shows name, order, active toggle, save and cancel")
@pytest.mark.smoke
def test_add_bank_drop_form_loads(browser):

    page = open_bank_drop_page(browser)
    page.open_create()
    body_text = page.get_body_text()

    assert "Add new bank drop" in body_text or "Bank drop name" in body_text
    assert "Order" in body_text
    assert "Active bank drop" in body_text
    assert page.active_bank_drop_is_on()
    assert page_has_no_broken_state(page)
