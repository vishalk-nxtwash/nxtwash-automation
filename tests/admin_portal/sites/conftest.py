import random

import pytest

from pages.admin_portal.sites_page import CreateSitePage
from pages.admin_portal.sites_page import SitesPage
from tests.admin_portal.admin_session import ensure_admin_logged_in
from tests.admin_portal.admin_session import open_admin_path


BASE_SITE_NAME = "VK AL"
BASE_SITE_CODE = "AL"
BASE_SITE_NUMBER = 1
SITE_EMAIL_TEMPLATE = "vkal%02d@yopmail.com"
SITE_CONTACT_EMAIL_TEMPLATE = "vkal%dsite@yopmail.com"
STATE = "California"
CITY = "Columbia"
ZIP_CODE = "95310"
TIME_ZONE = "(UTC-05:00) Eastern Time (US & Canada)"
PAY_WEEK_START_DAY = "Monday"
STATE_SALES_TAX = "5"
CITY_SALES_TAX = "3"
MISSING_SITE = "VK SITE DOES NOT EXIST"
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


@pytest.fixture
def logged_in_admin_browser(browser):

    ensure_admin_logged_in(browser)

    return browser


def open_sites_page(browser):

    open_admin_path(browser, "/sites")

    sites_page = SitesPage(browser)
    sites_page.wait_for_loaded()

    return sites_page


def open_create_site_page(browser):

    sites_page = open_sites_page(browser)
    sites_page.click_add_site()

    create_page = CreateSitePage(browser)
    create_page.wait_for_loaded()

    return create_page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


def site_data_for_number(number):

    return {
        "site_name": "%s%02d" % (BASE_SITE_NAME, number),
        "site_code": "%s%02d" % (BASE_SITE_CODE, number),
        "email": SITE_EMAIL_TEMPLATE % number,
        "street_address": "%s Automation Way" % random.randint(100, 999),
        "zip_code": ZIP_CODE,
        "state": STATE,
        "city": CITY,
        "time_zone": TIME_ZONE,
        "state_sales_tax": STATE_SALES_TAX,
        "city_sales_tax": CITY_SALES_TAX,
        "site_contact_email": SITE_CONTACT_EMAIL_TEMPLATE % number,
        "pay_week_start_day": PAY_WEEK_START_DAY,
    }


def next_available_site_data(browser):

    sites_page = open_sites_page(browser)
    number = BASE_SITE_NUMBER

    while True:
        candidate = site_data_for_number(number)
        if not sites_page.get_site_summary_with_api(candidate["site_name"]):
            return candidate
        number += 1


def create_site_if_missing(browser):

    sites_page = open_sites_page(browser)
    first_site = site_data_for_number(BASE_SITE_NUMBER)

    if sites_page.get_site_summary_with_api(first_site["site_name"]):
        return first_site

    create_page = CreateSitePage(browser)
    sites_page.click_add_site()
    create_page.wait_for_loaded()
    create_page.create_site(**first_site)

    sites_page = SitesPage(browser)
    sites_page.wait_for_loaded()
    sites_page.wait_for_site_row(first_site["site_name"])

    return first_site
