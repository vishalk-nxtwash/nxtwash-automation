import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    ASSIGNMENT_SITE,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    PACKAGE_NAME,
    POINTS_AWARDED,
    POINTS_REDEEMED,
    create_wash_package_if_missing,
    open_wash_packages_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("Negative"),
]


@allure.title("WP-NAM-002 Blank service name blocks save and shows validation")
@pytest.mark.regression
@pytest.mark.validation
def test_wash_package_required_name_validation(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.click_save_package()

    assert not page.service_name_input_is_valid()
    assert page.get_service_name_validation_message() != ""
    assert page_has_no_broken_state(page)


@allure.title("WP-NAM-003 Duplicate wash package name is blocked")
@pytest.mark.regression
def test_create_duplicate_wash_package_is_blocked(browser):
    create_wash_package_if_missing(browser)
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.fill_package_form(
        PACKAGE_NAME,
        POINTS_AWARDED,
        POINTS_REDEEMED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        ASSIGNMENT_SITE,
    )
    page.click_save_package()

    body = page.get_body_text()
    assert "Service name" in body or "Save wash package" in body, (
        "Expected to stay on create form after submitting a duplicate name"
    )
    assert page_has_no_broken_state(page)


@allure.title("WP-PRI-002 Blank global price blocks save and shows validation")
@pytest.mark.regression
@pytest.mark.validation
def test_wash_package_required_price_validation(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("VK no-price test")
    page.click_save_package()

    assert not page.global_price_input_is_valid()
    assert page.get_global_price_validation_message() != ""
    assert page_has_no_broken_state(page)


@allure.title("WP-PRI-005 Negative global price is rejected by the form")
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.xfail(
    reason=(
        "WP-PRI-005: Price input has no min=0 HTML5 constraint — negative values "
        "pass checkValidity(). Product should enforce min=0. Remove xfail once fixed."
    ),
    strict=True,
)
def test_negative_global_price_is_rejected(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("VK negative price test")
    page.set_global_price("-10")
    page.click_save_package()

    assert not page.global_price_input_is_valid()
    assert page_has_no_broken_state(page)


@allure.title("WP-COM-003 Negative global commission is rejected by the form")
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.xfail(
    reason=(
        "WP-COM-003: Commission input has no min=0 HTML5 constraint — negative values "
        "pass checkValidity(). Product should enforce min=0. Remove xfail once fixed."
    ),
    strict=True,
)
def test_negative_global_commission_is_rejected(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("VK negative commission test")
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission("-5")
    page.click_save_package()

    assert not page.global_commission_input_is_valid()
    assert page_has_no_broken_state(page)


@allure.title("WP-SRCH Special-character search does not break the grid")
@pytest.mark.regression
def test_wash_packages_special_character_search_stays_usable(browser):
    page = open_wash_packages_page(browser)
    page.search_package("' OR 1=1 --")

    assert page_has_no_broken_state(page)
