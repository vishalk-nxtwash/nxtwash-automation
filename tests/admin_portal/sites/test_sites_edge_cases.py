import allure
import pytest

from pages.admin_portal.sites_page import CreateSitePage

from tests.admin_portal.sites.conftest import open_create_site_page
from tests.admin_portal.sites.conftest import open_sites_page
from tests.admin_portal.sites.conftest import page_has_no_broken_state
from tests.admin_portal.sites.conftest import site_data_for_number


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Sites / Locations"),
    allure.story("Edge Cases"),
]


@allure.title("SL-EDGE Long site name does not crash the create form")
@pytest.mark.edge
def test_create_site_long_site_name_does_not_break_ui(logged_in_admin_browser):
    site_data = site_data_for_number(95)
    site_data["site_name"] = "VK AL LONG NAME " + ("A" * 80)
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.enter_basic_information(
        site_data["site_name"],
        site_data["site_code"],
        site_data["email"]
    )

    assert page_has_no_broken_state(create_page)
    assert create_page.get_site_name_value() == site_data["site_name"]


@allure.title("SL-EDGE Sites list recovers cleanly after a full page refresh")
@pytest.mark.edge
def test_sites_list_handles_refresh(logged_in_admin_browser):
    sites_page = open_sites_page(logged_in_admin_browser)
    logged_in_admin_browser.refresh()
    sites_page.wait_for_loaded()

    assert page_has_no_broken_state(sites_page)
    assert "Sites/Locations" in sites_page.get_body_text()


@allure.title("SL-EDGE Address fields accept a random valid address without crashing")
@pytest.mark.edge
def test_create_site_form_handles_random_address_value(
    logged_in_admin_browser
):
    site_data = site_data_for_number(94)
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.enter_basic_information(
        site_data["site_name"],
        site_data["site_code"],
        site_data["email"]
    )
    create_page.enter_address_information(
        site_data["street_address"],
        site_data["zip_code"],
        site_data["state"],
        site_data["city"],
        site_data["time_zone"]
    )

    assert page_has_no_broken_state(create_page)
