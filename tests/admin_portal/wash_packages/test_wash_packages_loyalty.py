import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    PACKAGE_NAME,
    POINTS_AWARDED,
    POINTS_REDEEMED,
    UPDATED_POINTS_AWARDED,
    UPDATED_POINTS_REDEEMED,
    open_wash_packages_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("Loyalty"),
    pytest.mark.xdist_group(name="managed_package"),
]


@allure.title("WP-LTY-001 Valid points awarded value persists after save")
@pytest.mark.regression
def test_loyalty_points_awarded_persists(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.set_loyalty_points(UPDATED_POINTS_AWARDED, POINTS_REDEEMED)
    page.save_and_return_to_list()

    page.open_edit_package(PACKAGE_NAME)
    assert page.get_points_awarded_value() == UPDATED_POINTS_AWARDED
    assert page_has_no_broken_state(page)


@allure.title("WP-LTY-002 Valid points to redeem value persists after save")
@pytest.mark.regression
def test_loyalty_points_redeemed_persists(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.set_loyalty_points(POINTS_AWARDED, UPDATED_POINTS_REDEEMED)
    page.save_and_return_to_list()

    page.open_edit_package(PACKAGE_NAME)
    assert page.get_points_redeemed_value() == UPDATED_POINTS_REDEEMED
    assert page_has_no_broken_state(page)


@allure.title("WP-LTY-007 Info tooltip for Points awarded field is visible and contains text")
@pytest.mark.regression
def test_points_awarded_info_tooltip_is_visible(browser):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains

    page = open_wash_packages_page(browser)
    page.open_create_package()

    tooltip_trigger = page.driver.find_element(
        By.XPATH,
        "//*[normalize-space()='Points awarded']/following-sibling::*[contains(@class,'info') or @title]"
    )
    ActionChains(page.driver).move_to_element(tooltip_trigger).perform()

    body = page.get_body_text()
    assert len(body) > 0
    assert page_has_no_broken_state(page)


@allure.title("WP-LTY-008 Info tooltip for Points to redeem field is visible and contains text")
@pytest.mark.regression
def test_points_redeemed_info_tooltip_is_visible(browser):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains

    page = open_wash_packages_page(browser)
    page.open_create_package()

    tooltip_trigger = page.driver.find_element(
        By.XPATH,
        "//*[normalize-space()='Points to redeem']/following-sibling::*[contains(@class,'info') or @title]"
    )
    ActionChains(page.driver).move_to_element(tooltip_trigger).perform()

    body = page.get_body_text()
    assert len(body) > 0
    assert page_has_no_broken_state(page)
