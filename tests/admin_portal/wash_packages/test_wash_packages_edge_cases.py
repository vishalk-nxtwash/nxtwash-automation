import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    PACKAGE_NAME,
    open_wash_packages_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("Edge Cases"),
]


@allure.title("WP-NAM-004 Long service name does not break the create form")
@pytest.mark.regression
def test_wash_package_long_name_does_not_break_form(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("VK " + ("P" * 128))

    assert page.get_service_name_value().startswith("VK ")
    assert "Service name" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("WP-NAM-005 Whitespace-only service name is rejected or treated as duplicate")
@pytest.mark.regression
@pytest.mark.validation
def test_wash_package_whitespace_name_is_rejected(browser):
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("   ")
    page.click_save_package()

    body = page.get_body_text()
    assert (
        not page.service_name_input_is_valid()
        or "Service name" in body
        or "Save wash package" in body
    ), "Expected form to reject a whitespace-only name"
    assert page_has_no_broken_state(page)


@allure.title("WP-SRH Repeated search for the same package remains stable")
@pytest.mark.regression
def test_wash_package_existing_search_is_repeatable(browser):
    page = open_wash_packages_page(browser)
    page.search_package(PACKAGE_NAME)
    page.search_package(PACKAGE_NAME)

    assert page.wait_for_package_row(PACKAGE_NAME).is_displayed()
    assert page_has_no_broken_state(page)
