import pytest

from pages.admin_portal.login_page import AdminLoginPage
from pages.admin_portal.overview_page import AdminOverviewPage
from pages.admin_portal.sidebar import AdminSidebar
from pages.admin_portal.sites_page import SitesPage


@pytest.fixture
def logged_in_admin_browser(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()
    login_page.login()
    login_page.wait_for_overview()

    return browser


def test_admin_overview_loaded(logged_in_admin_browser):

    overview_page = AdminOverviewPage(logged_in_admin_browser)
    overview_page.wait_for_loaded()

    assert overview_page.has_expected_url()
    assert not overview_page.is_redirected_to_login()
    assert overview_page.get_overview_text() == "Overview"
    assert overview_page.shell_has_content()
    assert not overview_page.has_broken_state_text()


def test_admin_overview_sidebar_navigation_visible(logged_in_admin_browser):

    overview_page = AdminOverviewPage(logged_in_admin_browser)
    overview_page.wait_for_loaded()

    assert overview_page.expected_navigation_is_visible()


def test_admin_overview_profile_visible(logged_in_admin_browser):

    overview_page = AdminOverviewPage(logged_in_admin_browser)
    overview_page.wait_for_loaded()

    assert overview_page.profile_role_is_visible()


def test_admin_overview_refresh_keeps_user_on_overview(logged_in_admin_browser):

    logged_in_admin_browser.refresh()

    overview_page = AdminOverviewPage(logged_in_admin_browser)
    overview_page.wait_for_loaded()

    assert overview_page.has_expected_url()
    assert overview_page.shell_has_content()
    assert not overview_page.has_broken_state_text()


def test_admin_overview_accessible_after_navigation(logged_in_admin_browser):

    sidebar = AdminSidebar(logged_in_admin_browser)
    sidebar.open_sites_locations()

    sites_page = SitesPage(logged_in_admin_browser)
    sites_page.wait_for_loaded()

    sidebar.open_overview()

    overview_page = AdminOverviewPage(logged_in_admin_browser)
    overview_page.wait_for_loaded()

    assert overview_page.has_expected_url()
    assert overview_page.shell_has_content()
    assert not overview_page.has_broken_state_text()
