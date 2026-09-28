import uuid

import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    ASSIGNMENT_SITE,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
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
def test_wash_package_barcode_persists(isolated_package):
    # Isolated record — see test_wash_packages_edit.py's module note.
    page, name = isolated_package
    # Unique per run: barcodes must be unique across services, and packages
    # cannot be deleted — a fixed value (VK-BAR-001) was permanently taken by
    # packages that test_duplicate_barcode_behaviour created on earlier runs
    # (save rejected: 499 "Barcode already associated with another service").
    barcode = "VK-BAR-%s" % uuid.uuid4().hex[:6].upper()
    page.open_edit_package(name)
    page.enter_barcode(barcode)
    page.save_and_return_to_list()

    page.open_edit_package(name)
    assert page.wait_for_persisted_value(
        page.get_barcode_value, barcode,
        reopen=lambda: page.open_edit_package(name),
    ) == barcode
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
    # Own barcode per run — never the shared BARCODE_VALUE, which this test
    # used to claim permanently for package_a (packages cannot be deleted).
    dup_barcode = "VK-DUP-%s" % uuid.uuid4().hex[:6].upper()

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
    page.enter_barcode(dup_barcode)
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
    page.enter_barcode(dup_barcode)
    page.click_save_package()

    assert page_has_no_broken_state(page)
