from tests.admin_portal.sites.conftest import MISSING_SITE
from tests.admin_portal.sites.conftest import create_site_if_missing
from tests.admin_portal.sites.conftest import open_sites_page


def test_sites_filter_by_existing_site_name(logged_in_admin_browser):

    site_data = create_site_if_missing(logged_in_admin_browser)
    sites_page = open_sites_page(logged_in_admin_browser)

    assert sites_page.site_exists_in_ui(site_data["site_name"])


def test_sites_filter_by_missing_site_name_shows_no_match(
    logged_in_admin_browser
):

    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.filter_by_site_name(MISSING_SITE)

    assert MISSING_SITE not in sites_page.get_body_text()


def test_sites_reset_filter_restores_list(logged_in_admin_browser):

    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.filter_by_site_name(MISSING_SITE)
    sites_page.reset_filters()

    assert "Sites/Locations" in sites_page.get_body_text()
    assert sites_page.get_site_count_from_title() is not None
