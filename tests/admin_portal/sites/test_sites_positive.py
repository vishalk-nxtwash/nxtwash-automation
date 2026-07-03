import uuid

import allure
import pytest

from pages.admin_portal.sites_page import CreateSitePage
from pages.admin_portal.sites_page import SitesPage

from tests.admin_portal.sites.conftest import CITY
from tests.admin_portal.sites.conftest import CITY_SALES_TAX
from tests.admin_portal.sites.conftest import PAY_WEEK_START_DAY
from tests.admin_portal.sites.conftest import STATE
from tests.admin_portal.sites.conftest import STATE_SALES_TAX
from tests.admin_portal.sites.conftest import TIME_ZONE
from tests.admin_portal.sites.conftest import ZIP_CODE
from tests.admin_portal.sites.conftest import create_site_if_missing
from tests.admin_portal.sites.conftest import next_available_site_data
from tests.admin_portal.sites.conftest import open_sites_page
from tests.admin_portal.sites.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Sites / Locations"),
    allure.story("CRUD"),
]


@allure.title("SL-CRT-001 Create site with all required fields — appears in list as Active")
@pytest.mark.smoke
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


@allure.title("SL-CRT-002 Created site shows state and city in the list grid columns")
@pytest.mark.regression
def test_created_site_shows_state_and_city_in_list(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.filter_by_site_name(site_data["site_name"])

    body_text = sites_page.get_body_text()
    assert STATE in body_text
    assert CITY in body_text
    assert page_has_no_broken_state(sites_page)


@allure.title("SL-CRT-007 Create site with zero state and city tax rates saves successfully")
@pytest.mark.regression
def test_create_site_with_zero_tax_rates(logged_in_admin_browser):
    uid = uuid.uuid4().hex[:6]
    site_data = {
        "site_name": "VK ZT %s" % uid,
        "site_code": "ZT%s" % uid[:4].upper(),
        "email": "vkzt%s@yopmail.com" % uid,
        "street_address": "500 Zero Tax Blvd",
        "zip_code": ZIP_CODE,
        "state": STATE,
        "city": CITY,
        "time_zone": TIME_ZONE,
        "state_sales_tax": "0",
        "city_sales_tax": "0",
        "site_contact_email": "vkzt%sc@yopmail.com" % uid,
        "pay_week_start_day": PAY_WEEK_START_DAY,
    }

    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.click_add_site()

    create_page = CreateSitePage(logged_in_admin_browser)
    create_page.wait_for_loaded()
    create_page.create_site(**site_data)

    sites_page = SitesPage(logged_in_admin_browser)
    sites_page.wait_for_loaded()

    assert sites_page.site_exists_in_ui(site_data["site_name"])


@allure.title("SL-CRT-016 Site count in page title increments after creating a new site")
@pytest.mark.regression
def test_site_count_increments_after_create(logged_in_admin_browser):
    sites_page = open_sites_page(logged_in_admin_browser)
    initial_count = sites_page.get_site_count_from_title()

    site_data = next_available_site_data(logged_in_admin_browser)

    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.click_add_site()

    create_page = CreateSitePage(logged_in_admin_browser)
    create_page.wait_for_loaded()
    create_page.create_site(**site_data)

    sites_page = SitesPage(logged_in_admin_browser)
    sites_page.wait_for_loaded()
    new_count = sites_page.get_site_count_from_title()

    assert new_count is not None
    if initial_count is not None:
        assert new_count > initial_count
    assert page_has_no_broken_state(sites_page)
