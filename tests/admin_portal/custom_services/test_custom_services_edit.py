import uuid

import allure
import pytest
from selenium.webdriver.common.by import By

from tests.admin_portal.custom_services.conftest import (
    APPLICABLE_DISCOUNT,
    ASSIGNMENT_SITE,
    BARCODE_VALUE,
    DESCRIPTION_TEXT,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    SERVICE_CATEGORY,
    SERVICE_NAME,
    SITE_OVERRIDE_PRICE,
    SITE_OVERRIDE_PRICE_HIGH,
    UPDATED_SERVICE_NAME,
    create_service_if_missing,
    managed_service,
    open_custom_services_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Custom Services"),
    allure.story("Edit"),
]


@allure.title("CS-EDT-001 Edit service name persists after save")
@pytest.mark.regression
def test_edit_service_name_persists(browser):

    original = "VK EDT001-%s" % uuid.uuid4().hex[:6]
    updated = original + "-upd"
    page = open_custom_services_page(browser)
    page.create_service(original, SERVICE_CATEGORY, GLOBAL_PRICE, GLOBAL_COMMISSION, ASSIGNMENT_SITE)

    page.open_edit_service(original)
    page.enter_service_name(updated)
    page.click_save_service()
    page = open_custom_services_page(browser)
    page.search_service(updated)

    assert page.wait_for_service_row(updated).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("CS-EDT-002 Edit global price persists after save")
@pytest.mark.regression
def test_edit_global_price_persists(managed_service):

    page = managed_service
    page.open_edit_service(SERVICE_NAME)
    page.set_global_price(SITE_OVERRIDE_PRICE_HIGH)
    page.click_save_service()
    page.wait_for_list_loaded()

    page.open_edit_service(SERVICE_NAME)
    assert page.get_global_price_value() == SITE_OVERRIDE_PRICE_HIGH
    assert page_has_no_broken_state(page)


@allure.title("CS-EDT-003 Edit site-level price override persists after save")
@pytest.mark.regression
def test_edit_site_price_override_persists(managed_service):

    page = managed_service
    page.open_edit_service(SERVICE_NAME)
    row = page.get_site_row(ASSIGNMENT_SITE)
    price_input = row.find_element(By.NAME, "price")
    page._set_input_value(price_input, SITE_OVERRIDE_PRICE)
    page.click_save_service()
    page.wait_for_list_loaded()

    page.open_edit_service(SERVICE_NAME)
    assert page.get_site_price_value(ASSIGNMENT_SITE) == SITE_OVERRIDE_PRICE
    assert page_has_no_broken_state(page)


@allure.title("CS-EDT-004 Activate an inactive service updates its status to Active")
@pytest.mark.smoke
@pytest.mark.skip(reason="Manual: React switch aria-checked updates DOM but isActive not reflected in save payload. Needs app-level investigation.")
def test_activate_inactive_service(browser):

    inactive = "VK act-%s" % uuid.uuid4().hex[:6]
    page = open_custom_services_page(browser)
    page.open_create_service()
    page.enter_service_name(inactive)
    page.select_service_category(SERVICE_CATEGORY)
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)
    page.ensure_active_switch_off()
    page.assign_site_with_price_and_commission(ASSIGNMENT_SITE, GLOBAL_PRICE, GLOBAL_COMMISSION)
    page.click_save_service()
    page.wait_for_list_loaded()

    # Inactive services are hidden from the default list — show all to find the row.
    page.open_filter_panel()
    page.toggle_active_service_filter()
    page.apply_filters()

    page.open_edit_service(inactive)
    page.ensure_active_switch_on()
    page.click_save_service()
    page.wait_for_list_loaded()
    page.search_service(inactive)

    assert page.wait_for_service_row(inactive).is_displayed()
    assert page.get_service_status(inactive) == "Active"


@allure.title("CS-EDT-005 Deactivate an active service hides it from the default list")
@pytest.mark.regression
def test_deactivate_active_service(browser):

    temp = "VK deact-%s" % uuid.uuid4().hex[:6]
    page = open_custom_services_page(browser)
    page.create_service(temp, SERVICE_CATEGORY, GLOBAL_PRICE, GLOBAL_COMMISSION, ASSIGNMENT_SITE)

    page.open_edit_service(temp)
    page.ensure_active_switch_off()
    page.click_save_service()
    page.wait_for_list_loaded()

    assert temp not in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("CS-EDT-006 Edit form pre-populates existing name, category, price, commission")
@pytest.mark.regression
def test_edit_form_prepopulates_existing_values(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.open_edit_service(SERVICE_NAME)

    assert page.get_service_name_value() == SERVICE_NAME
    assert page.get_service_category_value() == SERVICE_CATEGORY
    assert page.get_global_price_value() == GLOBAL_PRICE
    assert page.get_global_commission_value() == GLOBAL_COMMISSION
    assert page.active_switch_is_on()
    assert page_has_no_broken_state(page)


@allure.title("CS-EDT-007 Cancel out of edit form discards changes")
@pytest.mark.regression
def test_cancel_out_of_edit_form(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.open_edit_service(SERVICE_NAME)
    page.enter_service_name("VK should-not-save")
    page.click_cancel()
    page.wait_for_list_loaded()

    assert page.wait_for_service_row(SERVICE_NAME).is_displayed()
    assert "VK should-not-save" not in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("CS-EDT-008 Edit barcode and description persist after save")
@pytest.mark.regression
@pytest.mark.skip(reason="Manual: description textarea not interactable after barcode entry — likely covered by tooltip/overlay. Needs browser inspection.")
def test_edit_barcode_and_description_persist(managed_service):

    page = managed_service
    barcode = "VK-BC-" + uuid.uuid4().hex[:6]
    page.open_edit_service(SERVICE_NAME)
    page.enter_barcode(barcode)
    page.enter_description(DESCRIPTION_TEXT)
    page.click_save_service()
    page.wait_for_list_loaded()

    page.open_edit_service(SERVICE_NAME)
    assert page.get_barcode_value() == barcode
    assert page.get_description_value() == DESCRIPTION_TEXT
    assert page_has_no_broken_state(page)


@allure.title("CS-PER-001 Created service data persists after page reload")
@pytest.mark.regression
def test_created_service_persists_after_reload(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)

    assert page.wait_for_service_row(SERVICE_NAME).is_displayed()
    assert page.get_service_status(SERVICE_NAME) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("CS-PER-002 Edited service changes persist after page reload")
@pytest.mark.regression
def test_edited_service_persists_after_reload(managed_service):

    page = managed_service
    page.open_edit_service(SERVICE_NAME)
    page.set_global_price(SITE_OVERRIDE_PRICE)
    page.click_save_service()
    page.wait_for_list_loaded()

    page = open_custom_services_page(page.driver)
    page.open_edit_service(SERVICE_NAME)
    assert page.get_global_price_value() == SITE_OVERRIDE_PRICE
    assert page_has_no_broken_state(page)
