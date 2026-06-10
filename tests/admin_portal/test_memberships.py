from pages.admin_portal.login_page import AdminLoginPage
from pages.admin_portal.memberships_page import MembershipsPage
from pages.admin_portal.sidebar import AdminSidebar


EXISTING_MEMBERSHIP = "Plus membership"
MISSING_MEMBERSHIP = "membership-does-not-exist-automation"


def open_memberships_page(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()
    login_page.login()
    login_page.wait_for_overview()

    sidebar = AdminSidebar(browser)
    sidebar.open_memberships()

    memberships_page = MembershipsPage(browser)
    memberships_page.wait_for_list_loaded()

    return memberships_page


def test_memberships_page_loads(browser):

    memberships_page = open_memberships_page(browser)

    assert "Membership Name" in memberships_page.get_body_text()
    assert "Type" in memberships_page.get_body_text()
    assert "Price" in memberships_page.get_body_text()
    assert "Status" in memberships_page.get_body_text()


def test_memberships_existing_membership_search(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(EXISTING_MEMBERSHIP)

    assert memberships_page.wait_for_membership_row(
        EXISTING_MEMBERSHIP
    ).is_displayed()


def test_memberships_missing_membership_search(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(MISSING_MEMBERSHIP)

    assert MISSING_MEMBERSHIP not in memberships_page.get_body_text()


def test_memberships_filter_panel_shows_controls(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()

    assert "Select site" in memberships_page.get_body_text()
    assert "Apply filters" in memberships_page.get_body_text()
    assert "Reset all" in memberships_page.get_body_text()


def test_memberships_download_button_is_available(browser):

    memberships_page = open_memberships_page(browser)

    assert memberships_page.download_button_is_clickable()
