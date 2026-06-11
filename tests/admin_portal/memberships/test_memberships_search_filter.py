import logging

import allure
import pytest

from tests.admin_portal.memberships.conftest import EXISTING_MEMBERSHIP
from tests.admin_portal.memberships.conftest import MISSING_MEMBERSHIP
from tests.admin_portal.memberships.conftest import open_memberships_page
from tests.admin_portal.memberships.conftest import page_has_no_broken_state


LOG = logging.getLogger(__name__)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Search")
@allure.title("MEM-SRCH-001 Verify search using exact membership name")
@pytest.mark.sanity
def test_memberships_existing_search(browser):

    LOG.info("Searching membership by exact name: %s", EXISTING_MEMBERSHIP)
    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(EXISTING_MEMBERSHIP)

    assert memberships_page.wait_for_membership_row(
        EXISTING_MEMBERSHIP
    ).is_displayed()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Search")
@allure.title("MEM-SRCH-006 Verify search with invalid membership name")
@pytest.mark.sanity
def test_memberships_missing_search(browser):

    LOG.info("Searching missing membership: %s", MISSING_MEMBERSHIP)
    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(MISSING_MEMBERSHIP)

    assert MISSING_MEMBERSHIP not in memberships_page.get_body_text()
    assert memberships_page.search_input_value() == MISSING_MEMBERSHIP
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Search")
@allure.title("MEM-SRCH-002 Verify search using partial membership name")
@pytest.mark.sanity
def test_memberships_partial_search(browser):

    partial_text = "Plus"
    LOG.info("Searching membership by partial text: %s", partial_text)
    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(partial_text)

    names = memberships_page.get_visible_membership_names()

    assert names
    assert any(partial_text.lower() in name.lower() for name in names)
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Search")
@allure.title("MEM-SRCH-003 Verify case-insensitive search")
@pytest.mark.sanity
def test_memberships_case_insensitive_search(browser):

    search_text = EXISTING_MEMBERSHIP.upper()
    LOG.info("Searching membership using uppercase value: %s", search_text)
    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(search_text)

    assert memberships_page.wait_for_membership_row(
        EXISTING_MEMBERSHIP
    ).is_displayed()
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Search")
@allure.title("MEM-SRCH-005 Verify search trims surrounding spaces")
@pytest.mark.sanity
def test_memberships_search_with_surrounding_spaces(browser):

    search_text = "  %s  " % EXISTING_MEMBERSHIP
    LOG.info("Searching membership with surrounding spaces: %r", search_text)
    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(search_text)

    assert memberships_page.wait_for_membership_row(
        EXISTING_MEMBERSHIP
    ).is_displayed()
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Search")
@allure.title("MEM-SRCH-008 Verify clearing search restores records")
@pytest.mark.sanity
def test_memberships_clear_search_restores_records(browser):

    LOG.info("Validating clear search restores membership records")
    memberships_page = open_memberships_page(browser)
    initial_count = memberships_page.get_visible_membership_count()
    memberships_page.search_membership(EXISTING_MEMBERSHIP)

    assert memberships_page.wait_for_membership_row(
        EXISTING_MEMBERSHIP
    ).is_displayed()

    memberships_page.clear_membership_search()

    assert memberships_page.search_input_value() == ""
    assert memberships_page.get_visible_membership_count() >= initial_count
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Filter")
@allure.title("MEM-FLTR-001 Verify Filter popup opens successfully")
@pytest.mark.regression
def test_memberships_filter_panel_shows_controls(browser):

    LOG.info("Opening memberships filter panel")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()
    body_text = memberships_page.get_body_text()

    assert "Select site" in body_text
    assert "Apply filters" in body_text
    assert "Reset all" in body_text


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Search")
@allure.title("MEM-SRCH-004 Verify search payloads do not break grid")
@pytest.mark.sanity
def test_memberships_search_payloads_do_not_break_grid(browser):

    memberships_page = open_memberships_page(browser)

    for payload in ("' OR 1=1 --", "<script>alert(1)</script>"):
        LOG.info("Searching membership with payload: %s", payload)
        memberships_page.search_membership(payload)
        assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Search")
@allure.title("MEM-SRCH-007 Verify search with very long string")
@pytest.mark.sanity
def test_memberships_long_search_text_does_not_break_grid(browser):

    search_text = "membership-" + ("x" * 256)
    LOG.info("Searching membership with very long text")
    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(search_text)

    assert memberships_page.search_input_value() == search_text
    assert page_has_no_broken_state(memberships_page)
