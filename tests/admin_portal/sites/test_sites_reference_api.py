import pytest

from core.config_manager import ConfigManager
from pages.admin_portal.login_page import AdminLoginPage
from pages.admin_portal.sidebar import AdminSidebar
from pages.admin_portal.sites_page import SitesPage


SITE_NAME = "vkauto1"
REFERENCE_SITE_NAME = "VK Test carwash 2"
REFERENCE_SITE_CODE = "02"


def sites_url():
    """Admin Portal sites URL for the active environment."""
    return ConfigManager().get_url("admin_portal").rstrip("/") + "/sites"


@pytest.fixture
def logged_in_admin_browser(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()
    login_page.login()
    login_page.wait_for_overview()

    return browser


def open_sites_page(browser):

    sidebar = AdminSidebar(browser)
    sidebar.open_sites_locations()

    sites_page = SitesPage(browser)
    sites_page.wait_for_loaded()

    return sites_page


def test_create_vkauto1_site_from_reference(logged_in_admin_browser):

    sites_page = open_sites_page(logged_in_admin_browser)

    if sites_page.get_site_summary_with_api(SITE_NAME):
        assert sites_page.site_exists_in_ui(SITE_NAME)
        return

    reference_site = sites_page.get_site_details_by_name_and_code_with_api(
        REFERENCE_SITE_NAME,
        REFERENCE_SITE_CODE
    )

    if reference_site is None:
        pytest.skip(
            "Reference site '%s' with site code '%s' was not found; "
            "'%s' was not created."
            % (REFERENCE_SITE_NAME, REFERENCE_SITE_CODE, SITE_NAME)
        )

    sites_page.create_site_from_reference_with_api(SITE_NAME, reference_site)

    logged_in_admin_browser.get(sites_url())
    sites_page = SitesPage(logged_in_admin_browser)
    sites_page.wait_for_loaded()

    assert sites_page.site_exists_in_ui(SITE_NAME)
