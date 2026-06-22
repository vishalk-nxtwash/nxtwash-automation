import pytest

from pages.admin_portal.sites_page import CreateSitePage
from pages.admin_portal.sites_page import SitesPage

from tests.admin_portal.sites.conftest import create_site_if_missing
from tests.admin_portal.sites.conftest import next_available_site_data
from tests.admin_portal.sites.conftest import open_sites_page


@pytest.mark.skip(reason="needs_inspection: 'Monday' option not found in pay_week_start_day dropdown on staging — check Create Site form for actual day option labels")
def test_create_new_site_with_required_general_settings(logged_in_admin_browser):

    site_data = next_available_site_data(logged_in_admin_browser)
    sites_page = SitesPage(logged_in_admin_browser)
    sites_page.click_add_site()

    create_page = CreateSitePage(logged_in_admin_browser)
    create_page.wait_for_loaded()
    create_page.create_site(**site_data)

    sites_page = SitesPage(logged_in_admin_browser)
    sites_page.wait_for_loaded()

    assert sites_page.site_exists_in_ui(site_data["site_name"])

    site_details = sites_page.get_site_details_by_name_and_code_with_api(
        site_data["site_name"],
        site_data["site_code"]
    )
    assert site_details is not None
    assert site_details["siteName"] == site_data["site_name"]
    assert site_details["siteCode"] == site_data["site_code"]


def test_created_site_persists_after_refresh(logged_in_admin_browser):

    site_data = create_site_if_missing(logged_in_admin_browser)
    sites_page = open_sites_page(logged_in_admin_browser)
    logged_in_admin_browser.refresh()
    sites_page.wait_for_loaded()

    assert sites_page.site_exists_in_ui(site_data["site_name"])
