import allure
import pytest

from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("UI"),
]


@allure.title("DS-UI-001 Discounts page loads with primary controls")
@pytest.mark.sanity
@pytest.mark.prod_smoke
def test_discounts_page_loads_with_primary_controls(browser):

    discounts_page = open_discounts_page(browser)
    body_text = discounts_page.get_body_text()

    assert "Discounts" in body_text
    assert discounts_page.driver.find_element(
        *discounts_page.SEARCH_INPUT
    ).is_displayed()
    assert discounts_page.driver.find_element(
        *discounts_page.FILTER_BUTTON
    ).is_displayed()
    assert discounts_page.download_button_is_clickable()
    assert discounts_page.driver.find_element(
        *discounts_page.ADD_DISCOUNT_BUTTON
    ).is_displayed()
    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-UI-002 Discounts grid columns are visible")
@pytest.mark.sanity
@pytest.mark.prod_smoke
def test_discounts_grid_columns_are_visible(browser):

    discounts_page = open_discounts_page(browser)
    body_text = discounts_page.get_body_text()

    assert "Discount name" in body_text
    assert "Status" in body_text


@allure.title("DS-UI-003 Add discount form loads")
@pytest.mark.sanity
def test_add_discount_form_loads(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    body_text = discounts_page.get_body_text()

    assert "Add new discount" in body_text
    assert "Discount name" in body_text
    assert "Select service category" in body_text
    assert "Discount amount" in body_text
