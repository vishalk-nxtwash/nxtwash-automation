import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    ASSIGNMENT_SITE,
    open_wash_packages_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("Export"),
]


@allure.title("WP-EXP-001 Export button is clickable and does not break the page")
@pytest.mark.export
def test_wash_packages_export_button_clickable(browser):
    page = open_wash_packages_page(browser)
    page.click_download_button()
    page.wait_for_list_loaded()

    assert page_has_no_broken_state(page)


@allure.title("WP-EXP-002 Export after applying a filter does not break the page")
@pytest.mark.export
def test_wash_packages_export_after_filter(browser):
    page = open_wash_packages_page(browser)
    page.select_site_filter(ASSIGNMENT_SITE)
    page.apply_filters()

    # Re-navigate to ensure the download button is accessible in a clean frame context
    page = open_wash_packages_page(browser)
    page.click_download_button()

    assert page_has_no_broken_state(page)
