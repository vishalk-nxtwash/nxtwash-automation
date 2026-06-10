from tests.admin_portal.memberships.conftest import EXISTING_MEMBERSHIP
from tests.admin_portal.memberships.conftest import MISSING_MEMBERSHIP
from tests.admin_portal.memberships.conftest import open_memberships_page
from tests.admin_portal.memberships.conftest import page_has_no_broken_state


def test_memberships_existing_search(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(EXISTING_MEMBERSHIP)

    assert memberships_page.wait_for_membership_row(
        EXISTING_MEMBERSHIP
    ).is_displayed()


def test_memberships_missing_search(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(MISSING_MEMBERSHIP)

    assert MISSING_MEMBERSHIP not in memberships_page.get_body_text()
    assert page_has_no_broken_state(memberships_page)


def test_memberships_filter_panel_shows_controls(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()
    body_text = memberships_page.get_body_text()

    assert "Select site" in body_text
    assert "Apply filters" in body_text
    assert "Reset all" in body_text


def test_memberships_search_payloads_do_not_break_grid(browser):

    memberships_page = open_memberships_page(browser)

    for payload in ("' OR 1=1 --", "<script>alert(1)</script>"):
        memberships_page.search_membership(payload)
        assert page_has_no_broken_state(memberships_page)
