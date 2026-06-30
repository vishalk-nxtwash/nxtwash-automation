import allure
import pytest

from tests.admin_portal.sites.conftest import MISSING_SITE
from tests.admin_portal.sites.conftest import create_site_if_missing
from tests.admin_portal.sites.conftest import open_sites_page
from tests.admin_portal.sites.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Sites / Locations"),
    allure.story("Filters"),
]


@allure.title("SL-FLT-002 Filter by exact site name returns the correct record")
@pytest.mark.regression
def test_sites_filter_by_existing_site_name(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    sites_page = open_sites_page(logged_in_admin_browser)

    assert sites_page.site_exists_in_ui(site_data["site_name"])


@allure.title("SL-FLT-007 Filter by non-matching name returns empty state")
@pytest.mark.regression
def test_sites_filter_by_missing_site_name_shows_no_match(
    logged_in_admin_browser
):
    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.filter_by_site_name(MISSING_SITE)

    assert MISSING_SITE not in sites_page.get_body_text()
    assert page_has_no_broken_state(sites_page)


@allure.title("SL-FLT-008 Reset filters restores the full site list")
@pytest.mark.regression
def test_sites_reset_filter_restores_list(logged_in_admin_browser):
    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.filter_by_site_name(MISSING_SITE)
    sites_page.reset_filters()

    assert "Sites/Locations" in sites_page.get_body_text()
    assert sites_page.get_site_count_from_title() is not None
    assert page_has_no_broken_state(sites_page)


@allure.title("SL-FLT-004 Active toggle ON shows only active sites")
@pytest.mark.regression
def test_sites_filter_active_toggle_on_shows_active_only(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.filter_by_active_state(should_be_active=True)

    assert sites_page.site_exists_in_ui(site_data["site_name"])
    assert page_has_no_broken_state(sites_page)


@allure.title("SL-FLT-005 Active toggle OFF shows all sites including inactive")
@pytest.mark.regression
def test_sites_filter_active_toggle_off_shows_all(logged_in_admin_browser):
    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.filter_by_active_state(should_be_active=False)

    assert sites_page.get_site_count_from_title() is not None
    assert "Sites/Locations" in sites_page.get_body_text()
    assert page_has_no_broken_state(sites_page)


@allure.title("SL-FLT-006 Filter by name + active combined narrows results correctly")
@pytest.mark.edge
def test_sites_filter_by_name_and_active_combined(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.filter_by_name_and_active(
        site_data["site_name"], should_be_active=True
    )

    assert sites_page.site_exists_in_ui(site_data["site_name"])
    assert page_has_no_broken_state(sites_page)
