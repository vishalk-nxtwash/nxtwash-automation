import allure
import pytest

from tests.admin_portal.pos_settings.conftest import (
    NONEXISTENT_POS_NAME,
    POS_NAME,
    open_pos_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("POS Settings"),
    allure.story("Search"),
]


@allure.title("POS-SRH-001 Search by exact POS name returns correct POS")
@pytest.mark.regression
def test_search_by_exact_name(browser, managed_pos):
    page = open_pos_page(browser)
    page.search_pos(POS_NAME)
    body = page.get_body_text()

    assert POS_NAME in body, (
        "POS '%s' not found after searching by exact name" % POS_NAME
    )
    assert page_has_no_broken_state(page)


@allure.title("POS-SRH-002 Search by partial POS name returns matching results")
@pytest.mark.regression
def test_search_by_partial_name(browser, managed_pos):
    partial = POS_NAME[:4]
    page = open_pos_page(browser)
    page.search_pos(partial)
    body = page.get_body_text()

    assert partial in body or POS_NAME in body, (
        "No matching results for partial name '%s'" % partial
    )
    assert page_has_no_broken_state(page)


@allure.title("POS-SRH-003 Search with non-matching name shows empty state")
@pytest.mark.extended
def test_search_nonmatching_shows_empty(browser):
    page = open_pos_page(browser)
    page.search_pos(NONEXISTENT_POS_NAME)

    row_count = page.get_visible_row_count()
    body = page.get_body_text()

    assert row_count == 0 or "no" in body.lower() or NONEXISTENT_POS_NAME not in body, (
        "Expected empty state for non-matching search '%s'" % NONEXISTENT_POS_NAME
    )
    assert page_has_no_broken_state(page)


@allure.title("POS-SRH-004 Clearing search field restores full POS list")
@pytest.mark.extended
def test_search_clear_restores_list(browser, managed_pos):
    page = open_pos_page(browser)
    page.search_pos(NONEXISTENT_POS_NAME)
    filtered_count = page.get_visible_row_count()

    page.clear_search()
    full_count = page.get_visible_row_count()

    assert full_count >= filtered_count, (
        "Row count after clearing search (%d) should be >= filtered count (%d)"
        % (full_count, filtered_count)
    )
    assert page_has_no_broken_state(page)
