import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.admin_portal.custom_services.conftest import (
    APPLICABLE_DISCOUNT,
    SECOND_APPLICABLE_DISCOUNT,
    SERVICE_NAME,
    create_service_if_missing,
    managed_service,
    open_custom_services_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Custom Services"),
    allure.story("Discount Settings"),
]


@allure.title("CS-DSC-001 Discount settings tab is visible on the create form")
@pytest.mark.regression
def test_discount_settings_tab_is_visible_on_create(browser):

    page = open_custom_services_page(browser)
    page.open_create_service()
    page.open_discount_settings()

    assert page.wait.until(
        EC.visibility_of_element_located(page.APPLICABLE_DISCOUNTS_TITLE)
    )
    assert page_has_no_broken_state(page)


@allure.title("CS-DSC-002 Applicable discount can be selected and persists after save")
@pytest.mark.regression
def test_applicable_discount_persists_after_save(managed_service):

    page = managed_service
    page.open_edit_service(SERVICE_NAME)
    page.open_discount_settings()
    page.select_applicable_discount(APPLICABLE_DISCOUNT)
    page.click_save_service()
    page.wait_for_list_loaded()

    page.open_edit_service(SERVICE_NAME)
    page.open_discount_settings()
    assert page.discount_is_selected(APPLICABLE_DISCOUNT)
    assert page_has_no_broken_state(page)


@allure.title("CS-DSC-003 Multiple applicable discounts can be selected")
@pytest.mark.regression
def test_multiple_applicable_discounts_can_be_selected(managed_service):

    page = managed_service
    page.open_edit_service(SERVICE_NAME)
    page.open_discount_settings()
    page.select_applicable_discount(APPLICABLE_DISCOUNT)
    page.select_applicable_discount(SECOND_APPLICABLE_DISCOUNT)
    page.click_save_service()
    page.wait_for_list_loaded()

    page.open_edit_service(SERVICE_NAME)
    page.open_discount_settings()
    assert page.discount_is_selected(APPLICABLE_DISCOUNT)
    assert page.discount_is_selected(SECOND_APPLICABLE_DISCOUNT)
    assert page_has_no_broken_state(page)


@allure.title("CS-DSC-004 Removing an applicable discount persists after save")
@pytest.mark.regression
def test_remove_applicable_discount_persists(managed_service):

    page = managed_service
    page.open_edit_service(SERVICE_NAME)
    page.open_discount_settings()
    page.select_applicable_discount(APPLICABLE_DISCOUNT)
    page.click_save_service()
    page.wait_for_list_loaded()

    page.open_edit_service(SERVICE_NAME)
    page.open_discount_settings()
    page.remove_applicable_discount(APPLICABLE_DISCOUNT)
    page.click_save_service()
    page.wait_for_list_loaded()

    page.open_edit_service(SERVICE_NAME)
    page.open_discount_settings()
    assert not page.discount_is_selected(APPLICABLE_DISCOUNT)
    assert page_has_no_broken_state(page)


@allure.title("CS-DSC-005 Discount tab is accessible on the edit form")
@pytest.mark.regression
def test_discount_tab_accessible_on_edit_form(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.open_edit_service(SERVICE_NAME)
    page.open_discount_settings()

    assert page.wait.until(
        EC.visibility_of_element_located(page.APPLICABLE_DISCOUNTS_TITLE)
    )
    assert page_has_no_broken_state(page)


@allure.title("CS-DSC-006 Discount combobox filters options by typing")
@pytest.mark.regression
def test_discount_combobox_filters_by_typing(browser):

    page = open_custom_services_page(browser)
    page.open_create_service()
    page.open_discount_settings()

    combobox = page.wait.until(EC.element_to_be_clickable(page.DISCOUNTS_COMBOBOX))
    combobox.click()
    combobox.send_keys("Basic")

    # Wait for at least one option to appear before collecting, then read text
    # directly from the DOM to avoid StaleElementReferenceException caused by
    # React Select re-rendering the options list while we iterate.
    page.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@role='option']")))
    visible_options = page.driver.execute_script(
        "return Array.from(document.querySelectorAll('[role=option]'))"
        ".filter(el => el.offsetParent !== null)"
        ".map(el => el.textContent.trim());"
    )
    assert any("Basic" in opt for opt in visible_options)
    assert page_has_no_broken_state(page)
