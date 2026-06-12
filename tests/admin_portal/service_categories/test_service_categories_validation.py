import allure
import pytest

from tests.admin_portal.service_categories.conftest import open_service_categories_page
from tests.admin_portal.service_categories.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Validation"),
]


@allure.title("SC-VAL-001 Category name is mandatory")
@pytest.mark.validation
def test_service_category_required_name_validation(browser):

    page = open_service_categories_page(browser)
    page.open_create_category()
    page.click_save_new()

    assert not page.category_name_input_is_valid()
    assert page.get_category_name_validation_message() != ""


@allure.title("SC-VAL-002 Blank required form remains on create page")
@pytest.mark.validation
def test_service_category_blank_required_form_stays_on_form(browser):

    page = open_service_categories_page(browser)
    page.open_create_category()
    page.click_save_new()

    assert "Category name" in page.get_body_text()
    assert page_has_no_broken_state(page)
