from pages.admin_portal.sites_page import SitesPage

from tests.admin_portal.sites.conftest import open_create_site_page
from tests.admin_portal.sites.conftest import open_sites_page
from tests.admin_portal.sites.conftest import page_has_no_broken_state


def test_sites_locations_page_ui_elements(logged_in_admin_browser):

    sites_page = open_sites_page(logged_in_admin_browser)

    assert "Sites/Locations" in sites_page.get_body_text()
    assert sites_page.get_site_count_from_title() is not None
    assert sites_page.table_headers_are_visible()
    assert sites_page.download_button_is_clickable()
    assert page_has_no_broken_state(sites_page)


def test_sites_filter_panel_ui_elements(logged_in_admin_browser):

    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.open_filters()

    body_text = sites_page.get_body_text()
    assert "Filter by" in body_text
    assert "Site name" in body_text
    assert "Active site" in body_text
    assert "Apply filters" in body_text
    assert "Reset filters" in body_text


def test_create_site_general_settings_ui_elements(logged_in_admin_browser):

    create_page = open_create_site_page(logged_in_admin_browser)

    body_text = create_page.get_body_text()
    assert "Sites/Locations" in body_text
    assert "New" in body_text
    assert "General settings" in body_text
    assert "Basic information" in body_text
    assert "Address information" in body_text
    assert "Tax settings" in body_text
    assert "Site contact info" in body_text
    assert create_page.active_site_switch_is_on()


def test_create_site_cancel_returns_to_list(logged_in_admin_browser):

    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.click_cancel()

    sites_page = SitesPage(logged_in_admin_browser)
    sites_page.wait_for_loaded()
