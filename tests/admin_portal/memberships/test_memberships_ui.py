import logging

import allure
import pytest
from selenium.webdriver.common.by import By

from tests.admin_portal.memberships.conftest import open_memberships_page
from tests.admin_portal.memberships.conftest import page_has_no_broken_state


LOG = logging.getLogger(__name__)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("UI")
@allure.title("MB-LST-001 Memberships page primary controls")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.sanity
@pytest.mark.prod_smoke
def test_memberships_page_loads_with_primary_controls(browser):

    LOG.info("Verifying Memberships list page primary controls")
    memberships_page = open_memberships_page(browser)
    body_text = memberships_page.get_body_text()

    assert "Memberships" in body_text
    assert memberships_page.driver.find_element(
        *memberships_page.SEARCH_INPUT
    ).is_displayed()
    assert memberships_page.driver.find_element(
        *memberships_page.FILTER_BUTTON
    ).is_displayed()
    assert memberships_page.download_button_is_clickable()
    assert memberships_page.driver.find_element(
        *memberships_page.ADD_MEMBERSHIP_BUTTON
    ).is_displayed()
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("UI")
@allure.title("MB-LST-002 Memberships grid columns")
@pytest.mark.sanity
@pytest.mark.prod_smoke
def test_memberships_grid_columns_are_visible(browser):

    LOG.info("Verifying Memberships grid columns")
    memberships_page = open_memberships_page(browser)
    body_text = memberships_page.get_body_text()

    assert "Membership Name" in body_text
    assert "Type" in body_text
    assert "Price" in body_text
    assert "Status" in body_text


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("UI")
@allure.title("MEM-UI-009 Edit action is available for visible memberships")
@pytest.mark.sanity
def test_visible_membership_rows_have_edit_action(browser):

    LOG.info("Verifying visible membership rows expose Edit action")
    memberships_page = open_memberships_page(browser)

    assert memberships_page.every_visible_row_has_edit_action()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("UI")
@allure.title("MEM-UI-014/015 Pagination and results-per-page controls")
@pytest.mark.regression
def test_memberships_pagination_results_and_support_controls(browser):

    LOG.info("Verifying Memberships pagination/results controls")
    memberships_page = open_memberships_page(browser)

    assert memberships_page.pagination_controls_are_visible()
    assert memberships_page.results_per_page_control_is_visible()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("UI")
@allure.title("MEM-UI-016/017 Add Membership page and Membership Settings UI")
@pytest.mark.sanity
def test_add_membership_form_loads(browser):

    LOG.info("Verifying Add Membership form loads")
    memberships_page = open_memberships_page(browser)

    memberships_page.open_create_membership()
    body_text = memberships_page.get_body_text()

    assert "Add new membership" in body_text
    assert "Membership name" in body_text
    assert "Global price" in body_text
    assert "Global commission" in body_text
    assert memberships_page.driver.find_element(
        By.NAME,
        "membershipName"
    ).is_displayed()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("UI")
@allure.title("MEM-UI-018 Redemption Settings tab UI")
@pytest.mark.regression
def test_redemption_settings_tab_loads(browser):

    LOG.info("Verifying Redemption Settings tab")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.open_redemption_settings()
    body_text = memberships_page.get_body_text()

    assert "Redeem at" in body_text
    assert "Redeem as" in body_text


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("UI")
@allure.title("MEM-UI-019 Discount Settings tab UI")
@pytest.mark.regression
def test_discount_settings_tab_loads(browser):

    LOG.info("Verifying Discount Settings tab")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.open_discount_settings()
    body_text = memberships_page.get_body_text()

    assert "Applicable discounts" in body_text
    assert "Multiple months discount" in body_text


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("UI")
@allure.title("MEM-UI-020/021 Save and Cancel buttons are visible")
@pytest.mark.sanity
def test_save_and_cancel_buttons_are_visible_on_create_form(browser):

    LOG.info("Verifying Save and Cancel buttons on Add Membership form")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()

    assert memberships_page.driver.find_element(
        *memberships_page.SAVE_MEMBERSHIP_BUTTON
    ).is_displayed()
    assert memberships_page.driver.find_element(
        *memberships_page.CANCEL_BUTTON
    ).is_displayed()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("UI")
@allure.title("MEM-UI-022 Filter panel exposes site, type and status controls")
@pytest.mark.regression
def test_memberships_filter_panel_shows_controls(browser):

    LOG.info("Opening memberships filter panel")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()
    body_text = memberships_page.get_body_text()

    assert "Select site" in body_text
    assert "Apply filters" in body_text
    assert "Reset all" in body_text
