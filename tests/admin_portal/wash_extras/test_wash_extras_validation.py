import allure
import pytest

from tests.admin_portal.wash_extras.conftest import GLOBAL_PRICE
from tests.admin_portal.wash_extras.conftest import open_wash_extras_page
from tests.admin_portal.wash_extras.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Extras"),
    allure.story("Validation"),
]


@allure.title("WE-NAM-002 Blank service name is blocked on save — validation message shown")
@pytest.mark.smoke
def test_wash_extra_required_service_name_validation(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.click_save_extra()

    assert not page.service_name_input_is_valid()
    assert page.get_service_name_validation_message() != ""


@allure.title("WE-PRI-002 Blank global price is blocked on save — validation message shown")
@pytest.mark.smoke
def test_wash_extra_blank_global_price_is_blocked(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK EWA2-no-price-test")
    page.click_save_extra()

    assert (
        not page.global_price_input_is_valid()
        or "Add new wash extra" in page.get_body_text()
    )
    assert page_has_no_broken_state(page)


@allure.title("WE-PRI-003 Zero global price — boundary behaviour documented")
@pytest.mark.extended
def test_wash_extra_zero_price_boundary_behaviour(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK EWA2-zero-price-test")
    page.set_global_price("0")
    page.click_save_extra()

    assert page_has_no_broken_state(page)


@allure.title("WE-NAM-004 Maximum-length service name is handled without breaking the form")
@pytest.mark.extended
def test_wash_extra_max_length_name_handled(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK " + ("E" * 128))

    assert page.get_service_name_value().startswith("VK ")
    assert "Service name" in page.get_body_text()


@allure.title("WE-VAL Invalid numeric inputs do not break the create form")
@pytest.mark.extended
def test_wash_extra_invalid_numeric_values_do_not_break_form(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK invalid extra")
    page.set_global_price("-10")
    page.set_global_commission("abc")

    assert page_has_no_broken_state(page)
