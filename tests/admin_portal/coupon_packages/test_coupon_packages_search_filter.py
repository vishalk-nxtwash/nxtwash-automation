import allure
import pytest

from tests.admin_portal.coupon_packages.conftest import COUPON_PACKAGE_NAME
from tests.admin_portal.coupon_packages.conftest import MISSING_COUPON_PACKAGE
from tests.admin_portal.coupon_packages.conftest import create_coupon_package_if_missing
from tests.admin_portal.coupon_packages.conftest import create_inactive_coupon_package_if_missing
from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page
from tests.admin_portal.coupon_packages.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Coupon Packages"),
    allure.story("Search and Filter"),
]


@allure.title("CP-SRH-001 Search by exact coupon package name returns the correct row")
@pytest.mark.regression
def test_coupon_packages_exact_search(browser):

    page = create_coupon_package_if_missing(browser)
    page.search_coupon_package(COUPON_PACKAGE_NAME)

    assert page.wait_for_coupon_package_row(COUPON_PACKAGE_NAME).is_displayed()


@allure.title("CP-SRH-002 Search by partial coupon package name returns matching rows")
@pytest.mark.regression
def test_coupon_packages_partial_search(browser):

    partial = COUPON_PACKAGE_NAME[:4]
    page = create_coupon_package_if_missing(browser)
    page.search_coupon_package(partial)

    assert page.wait_for_coupon_package_row(COUPON_PACKAGE_NAME).is_displayed()


@allure.title("CP-SRH-003 Search non-existing name returns empty state")
@pytest.mark.extended
def test_coupon_packages_missing_search(browser):

    page = open_coupon_packages_page(browser)
    page.search_coupon_package(MISSING_COUPON_PACKAGE)

    assert MISSING_COUPON_PACKAGE not in page.get_body_text()


@allure.title("CP-SRH-004 Clear search restores the full coupon packages list")
@pytest.mark.extended
def test_coupon_packages_clear_search_restores_list(browser):

    page = create_coupon_package_if_missing(browser)
    page.search_coupon_package(MISSING_COUPON_PACKAGE)
    page.clear_search()

    assert page.wait_for_coupon_package_row(COUPON_PACKAGE_NAME).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("CP-FLT-001 Active coupon package filter shows only active packages")
@pytest.mark.regression
def test_active_coupon_package_filter_shows_active_only(browser):

    create_coupon_package_if_missing(browser)
    create_inactive_coupon_package_if_missing(browser)
    page = open_coupon_packages_page(browser)
    page.open_filter_panel()
    page.set_active_package_filter(True)
    page.apply_filters()

    statuses = page.get_all_visible_statuses()
    assert statuses, "Expected at least one package after filtering"
    assert all(s == "Active" for s in statuses), statuses


@allure.title("CP-FLT-002 Active toggle off shows all coupon packages")
@pytest.mark.extended
def test_active_toggle_off_shows_all_packages(browser):

    create_coupon_package_if_missing(browser)
    create_inactive_coupon_package_if_missing(browser)
    page = open_coupon_packages_page(browser)
    page.open_filter_panel()
    page.set_active_package_filter(False)
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("CP-FLT-003 Reset all restores the unfiltered coupon packages list")
@pytest.mark.extended
def test_reset_all_restores_unfiltered_list(browser):

    create_coupon_package_if_missing(browser)
    page = open_coupon_packages_page(browser)
    page.open_filter_panel()
    page.set_active_package_filter(True)
    page.apply_filters()

    page.reset_filters()

    assert page.wait_for_coupon_package_row(COUPON_PACKAGE_NAME).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("CP-SEC-002 XSS payload in search does not break the grid")
@pytest.mark.regression
def test_coupon_packages_search_payloads_do_not_break_grid(browser):

    page = open_coupon_packages_page(browser)
    page.search_coupon_package("<script>alert(1)</script>")

    assert page_has_no_broken_state(page)
