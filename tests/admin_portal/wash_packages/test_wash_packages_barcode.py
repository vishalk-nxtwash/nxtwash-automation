import uuid

import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    ASSIGNMENT_SITE,
    BARCODE_VALUE,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    PACKAGE_NAME,
    POINTS_AWARDED,
    POINTS_REDEEMED,
    open_wash_packages_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("Barcode"),
]


@allure.title("WP-BAR-001 Wash package with a barcode saves and barcode persists")
@pytest.mark.regression
def test_wash_package_barcode_persists(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.enter_barcode(BARCODE_VALUE)
    page.save_and_return_to_list()

    page.open_edit_package(PACKAGE_NAME)
    assert page.get_barcode_value() == BARCODE_VALUE
    assert page_has_no_broken_state(page)


@allure.title("WP-BAR-003 Creating a second package with a duplicate barcode is blocked or accepted")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason="Staging shows 'Something went wrong' server error for duplicate barcode (product defect).",
)
def test_duplicate_barcode_behaviour(browser):
    package_a = "VK bar-a %s" % uuid.uuid4().hex[:6]
    package_b = "VK bar-b %s" % uuid.uuid4().hex[:6]

    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.fill_package_form(
        package_a,
        POINTS_AWARDED,
        POINTS_REDEEMED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        ASSIGNMENT_SITE,
    )
    page.enter_barcode(BARCODE_VALUE)
    page.click_save_package()
    page = open_wash_packages_page(browser)

    page.open_create_package()
    page.fill_package_form(
        package_b,
        POINTS_AWARDED,
        POINTS_REDEEMED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        ASSIGNMENT_SITE,
    )
    page.enter_barcode(BARCODE_VALUE)
    page.click_save_package()

    assert page_has_no_broken_state(page)
