import logging
import random

import pytest

from pages.admin_portal.sites_page import CreateSitePage
from pages.admin_portal.sites_page import EditSitePage
from pages.admin_portal.sites_page import SitesPage
from tests.admin_portal.admin_session import ensure_admin_logged_in
from tests.admin_portal.admin_session import open_admin_path


LOG = logging.getLogger("nxtwash")


from tests.admin_portal._data import load as _load

_D = _load("sites")

BASE_SITE_NAME              = _D["template"]["base_name"]
BASE_SITE_CODE              = _D["template"]["base_code"]
BASE_SITE_NUMBER            = _D["template"]["base_number"]
SITE_EMAIL_TEMPLATE         = _D["template"]["email_template"]
SITE_CONTACT_EMAIL_TEMPLATE = _D["template"]["contact_email_template"]
STATE                       = _D["template"]["state"]
CITY                        = _D["template"]["city"]
ZIP_CODE                    = _D["template"]["zip_code"]
TIME_ZONE                   = _D["template"]["time_zone"]
PAY_WEEK_START_DAY          = _D["template"]["pay_week_start_day"]
STATE_SALES_TAX = _D["template"]["state_sales_tax"]
CITY_SALES_TAX  = _D["template"]["city_sales_tax"]
MISSING_SITE    = _D["search"]["nonexistent"]
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


@pytest.fixture
def managed_site(logged_in_admin_browser):
    """Ensure the baseline site (VK AL01) exists before the test; restore active state after."""
    site_data = create_site_if_missing(logged_in_admin_browser)
    yield site_data

    try:
        sites_page = open_sites_page(logged_in_admin_browser)
        if not sites_page.site_exists_in_ui(site_data["site_name"]):
            sites_page.open_edit_site(site_data["site_name"], include_inactive=True)
            edit_page = EditSitePage(logged_in_admin_browser)
            edit_page.wait_for_loaded()
            edit_page.ensure_active_switch_on()
            edit_page.click_save()
            open_sites_page(logged_in_admin_browser)
    except Exception as exc:
        LOG.warning(
            "managed_site teardown could not restore '%s': %s",
            site_data["site_name"],
            exc,
        )


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
