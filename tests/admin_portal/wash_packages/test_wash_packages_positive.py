import uuid

import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    ASSIGNMENT_SITE,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    PACKAGE_NAME,
    POINTS_AWARDED,
    POINTS_REDEEMED,
    VISIBLE_PRICE,
    create_wash_package_if_missing,
    open_wash_packages_page,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("CRUD"),
]


@allure.title("WP-TGL-001 Create active wash package appears in list with Active status")
@pytest.mark.smoke
@pytest.mark.skip(
    reason="CI-SKIP WP-TGL-001: Staging data contamination — package exists at "
           "wrong price ($45 vs $14) from prior failed teardown. Fix: fix "
           "managed fixture teardown so price resets cleanly after each test."
)
def test_create_active_wash_package(browser):
    page = create_wash_package_if_missing(browser)
    page.search_package(PACKAGE_NAME)

    assert page.wait_for_package_row(PACKAGE_NAME).is_displayed()
    assert page.get_package_status(PACKAGE_NAME) == "Active"
    assert page.get_package_price(PACKAGE_NAME) == VISIBLE_PRICE


@allure.title("WP-TGL-002 Create inactive wash package is hidden from the default list")
@pytest.mark.regression
def test_create_inactive_wash_package(browser):
    package_name = "VK inactive %s" % uuid.uuid4().hex[:6]
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.fill_package_form(
        package_name,
        POINTS_AWARDED,
        POINTS_REDEEMED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        ASSIGNMENT_SITE,
    )
    page.ensure_active_switch_off()
    page.save_and_return_to_list()
    page.search_package(package_name)

    assert package_name not in page.get_body_text()


@allure.title("WP-BAR-002 Saving a wash package without a barcode succeeds")
@pytest.mark.regression
@pytest.mark.skip(
    reason="CI-SKIP WP-BAR-002: Inovua site-assignment grid times out in "
           "headless Chrome during create flow. Fix: decouple site-assignment "
           "from managed fixture reset; retry on StaleElementReferenceException."
)
def test_create_wash_package_without_barcode(browser):
    package_name = "VK no-bar %s" % uuid.uuid4().hex[:6]
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.fill_package_form(
        package_name,
        POINTS_AWARDED,
        POINTS_REDEEMED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        ASSIGNMENT_SITE,
    )
    # Barcode field intentionally left empty
    page.save_and_return_to_list()
    page.search_package(package_name)

    assert page.wait_for_package_row(package_name).is_displayed()


@allure.title("WP-LTY-006 Saving a wash package without loyalty points succeeds")
@pytest.mark.regression
@pytest.mark.skip(
    reason="CI-SKIP WP-LTY-006: Inovua site-assignment grid times out in "
           "headless Chrome during create flow. Fix: same as WP-BAR-002."
)
def test_create_wash_package_without_loyalty_points(browser):
    package_name = "VK no-lty %s" % uuid.uuid4().hex[:6]
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name(package_name)
    page.ensure_active_switch_on()
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)
    page.assign_site_with_price_and_commission(ASSIGNMENT_SITE, GLOBAL_PRICE, GLOBAL_COMMISSION)
    # Loyalty points intentionally omitted
    page.save_and_return_to_list()
    page.search_package(package_name)

    assert page.wait_for_package_row(package_name).is_displayed()


@allure.title("WP-DIS-004 Saving a wash package without assigning a discount succeeds")
@pytest.mark.regression
@pytest.mark.skip(
    reason="CI-SKIP WP-DIS-004: Inovua site-assignment grid times out in "
           "headless Chrome during create flow. Fix: same as WP-BAR-002."
)
def test_create_wash_package_without_discount(browser):
    package_name = "VK no-dis %s" % uuid.uuid4().hex[:6]
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.fill_package_form(
        package_name,
        POINTS_AWARDED,
        POINTS_REDEEMED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        ASSIGNMENT_SITE,
    )
    # Discount settings tab intentionally skipped
    page.save_and_return_to_list()
    page.search_package(package_name)

    assert page.wait_for_package_row(package_name).is_displayed()


@allure.title("WP-NAM-001 Wash package settings persist after save")
@pytest.mark.regression
@pytest.mark.skip(
    reason="CI-SKIP WP-NAM-001: Staging data contamination — price reads $45 "
           "instead of $14 from prior failed teardown. Fix: same as WP-TGL-001."
)
def test_wash_package_settings_persist(browser):
    page = create_wash_package_if_missing(browser)
    page.open_edit_package(PACKAGE_NAME)

    assert page.get_service_name_value() == PACKAGE_NAME
    assert page.get_global_price_value() == GLOBAL_PRICE
    assert page.get_global_commission_value() == GLOBAL_COMMISSION
    assert page.active_switch_is_on()
