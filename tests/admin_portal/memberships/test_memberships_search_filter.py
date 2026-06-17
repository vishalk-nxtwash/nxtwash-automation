import logging

import allure
import pytest

from tests.admin_portal.memberships.conftest import EXISTING_MEMBERSHIP
from tests.admin_portal.memberships.conftest import FILTER_SITE_LABEL
from tests.admin_portal.memberships.conftest import FILTER_SITE_QUERY
from tests.admin_portal.memberships.conftest import MISSING_MEMBERSHIP
from tests.admin_portal.memberships.conftest import SITE_MEMBERSHIP
from tests.admin_portal.memberships.conftest import open_memberships_page
from tests.admin_portal.memberships.conftest import page_has_no_broken_state


LOG = logging.getLogger(__name__)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Search")
@allure.title("MB-SRH-001 Verify search using exact membership name")
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
@allure.title("MB-SRH-004 Verify search with invalid membership name")
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
@allure.title("MB-SRH-002 Verify search using partial membership name")
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
@allure.title("MB-SRH-005 Verify clearing search restores records")
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


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Search")
@allure.title("MB-SRH-003 Search inactive membership returns it in results")
@pytest.mark.regression
def test_memberships_search_inactive_membership(browser):

    LOG.info("Searching for an inactive membership")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()
    memberships_page.set_active_membership_filter(False)
    memberships_page.apply_filters()
    inactive_names = memberships_page.get_visible_membership_names()

    if not inactive_names:
        pytest.skip("No inactive memberships available in current data set")

    target = inactive_names[0]
    LOG.info("Searching inactive membership by name: %s", target)
    memberships_page.search_membership(target)

    assert memberships_page.wait_for_membership_row(target).is_displayed()
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Filter")
@allure.title("MB-FLT-001 Filter by recurring type shows only recurring memberships")
@pytest.mark.regression
@pytest.mark.visual
def test_memberships_filter_by_recurring_type(browser, screenshot):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()
    memberships_page.select_membership_type_filter("Recurring")
    memberships_page.apply_filters()
    screenshot("recurring-filtered grid")

    types = memberships_page.get_visible_membership_types()
    assert types, "expected at least one membership after filtering"
    assert all(value == "Recurring" for value in types), types
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Filter")
@allure.title("MB-FLT-002 Filter by prepaid type shows only prepaid memberships")
@pytest.mark.regression
@pytest.mark.visual
def test_memberships_filter_by_prepaid_type(browser, screenshot):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()
    memberships_page.select_membership_type_filter("Prepaid")
    memberships_page.apply_filters()
    screenshot("prepaid-filtered grid")

    types = memberships_page.get_visible_membership_types()
    assert types, "expected at least one membership after filtering"
    assert all(value == "Prepaid" for value in types), types
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Filter")
@allure.title("MB-FLT-003 Filter by site narrows to memberships on that site")
@pytest.mark.regression
@pytest.mark.visual
def test_memberships_filter_by_site(browser, screenshot):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()
    site_label = memberships_page.select_filter_site(FILTER_SITE_QUERY)
    memberships_page.apply_filters()
    screenshot("site-filtered grid: %s" % site_label)

    assert FILTER_SITE_LABEL in site_label
    assert memberships_page.wait_for_membership_row(SITE_MEMBERSHIP).is_displayed()
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Filter")
@allure.title("MB-FLT-005 Filter by active shows only active memberships")
@pytest.mark.regression
@pytest.mark.visual
def test_memberships_filter_active_shows_only_active(browser, screenshot):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()
    memberships_page.set_active_membership_filter(True)
    memberships_page.apply_filters()
    screenshot("active-filtered grid")

    statuses = memberships_page.get_visible_membership_statuses()
    assert statuses, "expected at least one membership after filtering"
    assert all(value == "Active" for value in statuses), statuses
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Filter")
@allure.title("MB-FLT-006 Filter by inactive excludes active memberships")
@pytest.mark.regression
@pytest.mark.visual
def test_memberships_filter_inactive_excludes_active(browser, screenshot):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()
    memberships_page.set_active_membership_filter(False)
    memberships_page.apply_filters()
    screenshot("inactive-filtered grid")

    statuses = memberships_page.get_visible_membership_statuses()
    assert all(value != "Active" for value in statuses), statuses
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Filter")
@allure.title("MB-FLT-007 Apply multiple filters together narrows results")
@pytest.mark.regression
@pytest.mark.visual
def test_memberships_combined_type_and_status_filter(browser, screenshot):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()
    memberships_page.select_membership_type_filter("Recurring")
    memberships_page.set_active_membership_filter(True)
    memberships_page.apply_filters()
    screenshot("recurring-active combined filter")

    types = memberships_page.get_visible_membership_types()
    statuses = memberships_page.get_visible_membership_statuses()
    if types:
        assert all(t == "Recurring" for t in types), types
    if statuses:
        assert all(s == "Active" for s in statuses), statuses
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Filter")
@allure.title("MB-FLT-008 Reset filters restores the full grid")
@pytest.mark.regression
@pytest.mark.visual
def test_memberships_reset_filters_restores_grid(browser, screenshot):

    memberships_page = open_memberships_page(browser)
    initial_count = memberships_page.get_visible_membership_count()

    memberships_page.open_filter_panel()
    memberships_page.select_membership_type_filter("Recurring")
    memberships_page.apply_filters()
    filtered_count = memberships_page.get_visible_membership_count()
    screenshot("filtered before reset")

    memberships_page.reset_filters()
    memberships_page.apply_filters()
    screenshot("grid after reset")

    assert memberships_page.get_visible_membership_count() >= filtered_count
    assert memberships_page.get_visible_membership_count() >= min(initial_count, 1)
    assert page_has_no_broken_state(memberships_page)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Filter")
@allure.title("MB-FLT-007 Apply multiple filters together (type + active)")
@pytest.mark.regression
@pytest.mark.visual
def test_memberships_apply_multiple_filters(browser, screenshot):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_filter_panel()
    memberships_page.select_membership_type_filter("Recurring")
    memberships_page.set_active_membership_filter(True)
    memberships_page.apply_filters()
    screenshot("recurring + active filtered grid")

    types = memberships_page.get_visible_membership_types()
    statuses = memberships_page.get_visible_membership_statuses()
    assert types, "expected at least one membership after filtering"
    assert all(value == "Recurring" for value in types), types
    assert all(value == "Active" for value in statuses), statuses
    assert page_has_no_broken_state(memberships_page)
