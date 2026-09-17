import pytest

from core.config_manager import ConfigManager
from pages.admin_portal.sidebar import AdminSidebar
from pages.admin_portal.sites_page import SitesPage
from tests.admin_portal.admin_session import ensure_admin_logged_in


SITE_NAME = "vkauto1"
REFERENCE_SITE_NAME = "VK Test carwash 2"
REFERENCE_SITE_CODE = "02"


def sites_url():
    """Admin Portal sites URL for the active environment."""
    return ConfigManager().get_url("admin_portal").rstrip("/") + "/sites"


@pytest.fixture
def logged_in_admin_browser(browser):
    # The browser fixture pre-injects auth state (cookies + localStorage).
    # Navigating directly to the portal and calling ensure_admin_logged_in
    # is more reliable than a manual login flow, which times out when the
    # app redirects an already-authenticated session away from /login.
    base_url = ConfigManager().get_url("admin_portal").rstrip("/")
    browser.get(base_url)
    ensure_admin_logged_in(browser)
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
