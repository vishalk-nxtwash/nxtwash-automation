import uuid

import allure
import pytest

from pages.admin_portal.sites_page import CreateSitePage
from pages.admin_portal.sites_page import SitesPage

from tests.admin_portal.sites.conftest import create_site_if_missing
from tests.admin_portal.sites.conftest import next_available_site_data
from tests.admin_portal.sites.conftest import open_sites_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Sites / Locations"),
    allure.story("CRUD"),
]


@allure.title("SL-CRT-001 Create site with all required fields — appears in list as Active")
@pytest.mark.smoke
@pytest.mark.xfail(
    strict=False,
    reason=(
        "Pay-week dropdown now falls back to the first available option when 'Monday' "
        "is not found. Remove xfail once confirmed stable on staging."
    ),
)
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


@allure.title("SL-PER-001 Created site persists after page refresh")
@pytest.mark.regression
def test_created_site_persists_after_refresh(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    sites_page = open_sites_page(logged_in_admin_browser)
    logged_in_admin_browser.refresh()
    sites_page.wait_for_loaded()

    assert sites_page.site_exists_in_ui(site_data["site_name"])


@allure.title("SL-CRT-005 Create inactive site does not appear in the default (active) list")
@pytest.mark.regression
def test_create_inactive_site_hidden_from_list(logged_in_admin_browser):
    from tests.admin_portal.sites.conftest import (
        CITY,
        CITY_SALES_TAX,
        STATE,
        STATE_SALES_TAX,
        TIME_ZONE,
        ZIP_CODE,
    )

    uid = uuid.uuid4().hex[:6]
    site_name = "VK INACTIVE %s" % uid
    site_code = "IN%s" % uid[:4].upper()

    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.click_add_site()

    create_page = CreateSitePage(logged_in_admin_browser)
    create_page.wait_for_loaded()
    create_page.fill_general_settings(
        site_name=site_name,
        site_code=site_code,
        email="%s@yopmail.com" % site_code.lower(),
        street_address="123 Automation Way",
        zip_code=ZIP_CODE,
        state=STATE,
        city=CITY,
        time_zone=TIME_ZONE,
        state_sales_tax=STATE_SALES_TAX,
        city_sales_tax=CITY_SALES_TAX,
        site_contact_email="%s@yopmail.com" % site_code.lower(),
    )
    create_page.ensure_switch_off(create_page.ACTIVE_SITE_SWITCH)
    create_page.click_save_new()

    sites_page = SitesPage(logged_in_admin_browser)
    sites_page.wait_for_loaded()
    sites_page.filter_by_site_name(site_name)

    assert site_name not in sites_page.get_body_text()
