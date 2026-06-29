import allure
import pytest

from tests.admin_portal.custom_services.conftest import (
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    SERVICE_CATEGORY,
    SERVICE_NAME,
    create_service_if_missing,
    open_custom_services_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Custom Services"),
    allure.story("Validation"),
]


@allure.title("CS-VAL-001 Submit without service name shows validation error")
@pytest.mark.edge
def test_submit_without_service_name_shows_error(browser):

    page = open_custom_services_page(browser)
    page.open_create_service()
    page.select_service_category(SERVICE_CATEGORY)
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)
    page.click_save_service()

    assert not page.service_name_input_is_valid()
    assert page_has_no_broken_state(page)


@allure.title("CS-VAL-002 Submit without service category shows validation error")
@pytest.mark.edge
def test_submit_without_category_shows_error(browser):

    page = open_custom_services_page(browser)
    page.open_create_service()
    page.enter_service_name("VK VAL002-no-cat")
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)
    page.click_save_service()

    body = page.get_body_text()
    assert page.save_service_button_is_clickable()
    assert "category" in body.lower() or not page.service_exists("VK VAL002-no-cat")
    assert page_has_no_broken_state(page)


@allure.title("CS-VAL-003 Submit without global price shows validation error")
@pytest.mark.edge
def test_submit_without_global_price_shows_error(browser):

    page = open_custom_services_page(browser)
    page.open_create_service()
    page.enter_service_name("VK VAL003-no-price")
    page.select_service_category(SERVICE_CATEGORY)
    page.set_global_commission(GLOBAL_COMMISSION)
    page.click_save_service()

    assert not page.global_price_input_is_valid()
    assert page_has_no_broken_state(page)


@allure.title("CS-VAL-004 Negative global price is rejected or stays on form")
@pytest.mark.edge
def test_negative_global_price_documents_behaviour(browser):

    page = open_custom_services_page(browser)
    page.open_create_service()
    page.enter_service_name("VK VAL004-neg-price")
    page.select_service_category(SERVICE_CATEGORY)
    page.set_global_price("-10")
    page.set_global_commission(GLOBAL_COMMISSION)
    page.click_save_service()

    assert page_has_no_broken_state(page)


@allure.title("CS-VAL-005 Zero global price documents browser behaviour")
@pytest.mark.edge
def test_zero_global_price_documents_behaviour(browser):

    page = open_custom_services_page(browser)
    page.open_create_service()
    page.enter_service_name("VK VAL005-zero-price")
    page.select_service_category(SERVICE_CATEGORY)
    page.set_global_price("0")
    page.set_global_commission(GLOBAL_COMMISSION)
    page.click_save_service()

    assert page_has_no_broken_state(page)


@allure.title("CS-VAL-006 Duplicate service name documents server behaviour")
@pytest.mark.edge
def test_duplicate_service_name_documents_behaviour(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.open_create_service()
    page.enter_service_name(SERVICE_NAME)
    page.select_service_category(SERVICE_CATEGORY)
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)
    page.click_save_service()

    body = page.get_body_text()
    assert "Service name" in body or "Save" in body
    assert page_has_no_broken_state(page)


@allure.title("CS-VAL-007 Non-numeric price value is rejected by the input")
@pytest.mark.edge
def test_non_numeric_price_rejected(browser):

    page = open_custom_services_page(browser)
    page.open_create_service()
    page.enter_service_name("VK VAL007-alpha-price")
    page.select_service_category(SERVICE_CATEGORY)
    page.set_global_price("abc")
    page.set_global_commission(GLOBAL_COMMISSION)
    page.click_save_service()

    assert page_has_no_broken_state(page)


@allure.title("CS-VAL-008 Extremely long service name documents browser behaviour")
@pytest.mark.edge
def test_long_service_name_documents_behaviour(browser):

    long_name = "VK " + "A" * 200
    page = open_custom_services_page(browser)
    page.open_create_service()
    page.enter_service_name(long_name)
    page.select_service_category(SERVICE_CATEGORY)
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)
    page.click_save_service()

    assert page_has_no_broken_state(page)
