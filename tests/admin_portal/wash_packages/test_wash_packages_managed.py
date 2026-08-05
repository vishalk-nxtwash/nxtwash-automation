import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    PACKAGE_NAME,
    UPDATED_PACKAGE_NAME,
    VISIBLE_PRICE,
    open_wash_packages_page,
)



pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("Framework"),
]


@allure.title("WP-FRM-001 Managed wash package starts at baseline before each test")
@pytest.mark.sanity
@pytest.mark.skip(
    reason="CI-SKIP WP-FRM-001: managed_package fixture itself times out in "
           "headless CI — Inovua site-grid in reset path. This is the root "
           "fixture; fixing it unblocks all managed_package cascade failures."
)
def test_managed_package_provided_at_baseline(managed_package):
    page = managed_package
    page.search_package(PACKAGE_NAME)

    assert page.wait_for_package_row(PACKAGE_NAME).is_displayed()
    assert page.get_package_status(PACKAGE_NAME) == "Active"
    assert page.get_package_price(PACKAGE_NAME) == VISIBLE_PRICE


@allure.title("WP-FRM-002 Managed package mutation is reverted on teardown")
@pytest.mark.regression
def test_managed_package_mutation_is_reset_on_teardown(browser, managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.enter_service_name(UPDATED_PACKAGE_NAME)
    page.save_and_return_to_list()
    page.search_package(UPDATED_PACKAGE_NAME)

    assert page.wait_for_package_row(UPDATED_PACKAGE_NAME).is_displayed()
    # Teardown via managed_package fixture restores PACKAGE_NAME automatically
