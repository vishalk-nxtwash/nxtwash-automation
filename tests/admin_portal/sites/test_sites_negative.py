import allure
import pytest

from pages.admin_portal.sites_page import CreateSitePage

from tests.admin_portal.sites.conftest import create_site_if_missing
from tests.admin_portal.sites.conftest import open_sites_page
from tests.admin_portal.sites.conftest import site_data_for_number


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Sites / Locations"),
    allure.story("Negative"),
]


@allure.title("SL-VAL-014/015 Duplicate site name or code is rejected on save")
@pytest.mark.edge
def test_create_site_duplicate_site_name_or_code_is_rejected(
    logged_in_admin_browser
):
    existing_site = create_site_if_missing(logged_in_admin_browser)
    duplicate_site = dict(existing_site)
    duplicate_site["street_address"] = "997 Duplicate Way"

    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.click_add_site()

    create_page = CreateSitePage(logged_in_admin_browser)
    create_page.wait_for_loaded()
    create_page.create_site(**duplicate_site)

    assert "create" in logged_in_admin_browser.current_url


@allure.title("SL-CRT-018 Cancel on create does not persist the new site")
@pytest.mark.regression
def test_create_site_cancel_does_not_save_record(logged_in_admin_browser):
    site_data = site_data_for_number(96)
    sites_page = open_sites_page(logged_in_admin_browser)

    if sites_page.get_site_summary_with_api(site_data["site_name"]):
        return

    sites_page.click_add_site()
    create_page = CreateSitePage(logged_in_admin_browser)
    create_page.wait_for_loaded()
    create_page.enter_basic_information(
        site_data["site_name"],
        site_data["site_code"],
        site_data["email"]
    )
    create_page.click_cancel_and_confirm_if_needed()

    sites_page = open_sites_page(logged_in_admin_browser)
    assert sites_page.get_site_summary_with_api(site_data["site_name"]) is None
