import uuid

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.admin_portal.custom_services.conftest import (
    ASSIGNMENT_SITE,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    INACTIVE_CATEGORY,
    SERVICE_CATEGORY,
    SERVICE_NAME,
    create_service_if_missing,
    open_custom_services_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Custom Services"),
    allure.story("Category"),
]


@allure.title("CS-CAT-001 Service category dropdown lists active categories only")
@pytest.mark.regression
def test_service_category_dropdown_lists_active_categories_only(browser):

    page = open_custom_services_page(browser)
    page.open_create_service()
    page.click(page.SERVICE_CATEGORY_INPUT)

    options = page.wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[@role='option']"))
    )
    option_texts = [o.text.strip() for o in options if o.is_displayed()]

    assert SERVICE_CATEGORY in option_texts
    assert INACTIVE_CATEGORY not in option_texts
    assert page_has_no_broken_state(page)


@allure.title("CS-CAT-002 Selected service category persists after save and reopen")
@pytest.mark.regression
def test_selected_category_persists_after_save(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.open_edit_service(SERVICE_NAME)

    assert page.get_service_category_value() == SERVICE_CATEGORY
    assert page_has_no_broken_state(page)


@allure.title("CS-CAT-003 Service category field can be re-selected and persists after save")
@pytest.mark.regression
def test_service_category_can_be_changed(browser):

    name = "VK cat-%s" % uuid.uuid4().hex[:6]
    page = open_custom_services_page(browser)
    page.create_service(name, SERVICE_CATEGORY, GLOBAL_PRICE, GLOBAL_COMMISSION, ASSIGNMENT_SITE)

    page.open_edit_service(name)
    page.select_service_category(SERVICE_CATEGORY)
    page.click_save_service()
    page.wait_for_list_loaded()

    page.open_edit_service(name)
    assert page.get_service_category_value() == SERVICE_CATEGORY
    assert page_has_no_broken_state(page)
