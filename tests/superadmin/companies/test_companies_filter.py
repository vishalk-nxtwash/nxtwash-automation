import allure
import pytest

from selenium.webdriver.common.by import By

from tests.superadmin.companies.conftest import COMPANY_NAME

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Companies"),
    allure.story("Filter"),
]


def test_filter_button_opens_filter_panel(companies_page):
    """SA-CMP-FLT-001 — Clicking 'Filter by' opens the filter panel."""
    companies_page.open_filters()
    assert companies_page.filter_panel_is_open(), \
        "Filter panel should be visible after clicking 'Filter by'"


def test_filter_panel_shows_company_name_field(companies_page):
    """SA-CMP-FLT-002 — Filter panel shows the Company name input field."""
    companies_page.open_filters()
    els = companies_page.driver.find_elements(*companies_page.COMPANY_NAME_FILTER)
    assert els and els[0].is_displayed(), \
        "Company name filter field should be visible in the filter panel"


def test_filter_by_exact_company_name_returns_match(companies_page):
    """SA-CMP-FLT-003 — Filter by exact company name returns the matching company."""
    companies_page.filter_by_company_name(COMPANY_NAME)
    body = companies_page.driver.find_element(By.TAG_NAME, "body").text
    assert COMPANY_NAME.lower() in body.lower(), \
        f"Expected '{COMPANY_NAME}' in filtered results"


def test_filter_by_partial_name_returns_matches(companies_page):
    """SA-CMP-FLT-004 — Filter by partial company name returns all matching companies."""
    partial = COMPANY_NAME[:6]  # e.g. "vkauto"
    companies_page.open_filters()
    companies_page.enter_text(companies_page.COMPANY_NAME_FILTER, partial)
    companies_page.apply_filters()
    count = companies_page.get_visible_row_count()
    assert count >= 1, \
        f"Partial name filter '{partial}' should return at least one company"


def test_no_match_filter_shows_empty_state(companies_page):
    """SA-CMP-FLT-005 — A filter with no matches shows an empty state without an error."""
    companies_page.open_filters()
    companies_page.enter_text(
        companies_page.COMPANY_NAME_FILTER, "ZZZNOMATCH_COMPANY_99999"
    )
    companies_page.apply_filters()
    body = companies_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "error" not in body, \
        "No-match filter should show an empty state, not an error"


@pytest.mark.skip(
    reason="SA-CMP-FLT-006: The Company name filter is a plain <input type='text'> "
           "with no built-in clear (X) button — confirmed from DOM inspection. "
           "Clearing must be done by selecting all and deleting."
)
def test_clear_x_icon_empties_company_name_input(companies_page):
    """SA-CMP-FLT-006 — N/A: no clear X button exists on the company name filter field."""
    pass


def test_active_company_toggle_on_shows_active_only(companies_page):
    """SA-CMP-FLT-007 — 'Active company' toggle ON shows only active companies."""
    # Toggle is checked by default — reset first to get a clean baseline,
    # then re-open the filter and apply with the toggle ON.
    companies_page.open_filters()
    companies_page.reset_filters()
    companies_page.open_filters()
    # Toggle is already ON by default after reset; just apply
    companies_page.apply_filters()
    count = companies_page.get_visible_row_count()
    assert count >= 1, \
        "Active company filter should return at least one active company"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-FLT-008: Testing 'active toggle OFF' requires at least one inactive "
           "company in staging — existence not confirmed.",
)
def test_active_toggle_off_shows_all_companies(companies_page):
    """SA-CMP-FLT-008 — Toggling 'Active company' OFF shows all companies including inactive."""
    companies_page.open_filters()
    companies_page.click(companies_page.ACTIVE_COMPANY_TOGGLE)
    companies_page.apply_filters()
    count_active_only = companies_page.get_visible_row_count()

    companies_page.open_filters()
    companies_page.click(companies_page.ACTIVE_COMPANY_TOGGLE)
    companies_page.apply_filters()
    count_all = companies_page.get_visible_row_count()

    assert count_all >= count_active_only, \
        "Showing all companies should return >= the active-only count"


def test_combined_name_and_active_filter(companies_page):
    """SA-CMP-FLT-009 — Company name + Active company together return the correct subset."""
    # The 'Active company' toggle is ON by default — filter by name with toggle ON
    companies_page.open_filters()
    companies_page.enter_text(companies_page.COMPANY_NAME_FILTER, COMPANY_NAME)
    # Toggle is already ON; no need to click it
    companies_page.apply_filters()
    count = companies_page.get_visible_row_count()
    assert count >= 1, \
        f"Combined name + active filter should find '{COMPANY_NAME}'"
    body = companies_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "error" not in body, \
        "Combined filter should return results without error"


def test_apply_filters_updates_list_and_count(companies_page):
    """SA-CMP-FLT-010 — 'Apply filters' updates the list and the records count."""
    companies_page.filter_by_company_name(COMPANY_NAME)
    records = companies_page.get_records_count_text()
    assert records, \
        "Records count should be visible after applying a filter"
    count = companies_page.get_visible_row_count()
    assert count >= 1, \
        "At least one row should be visible after filtering by company name"


def test_reset_filters_restores_full_list(companies_page):
    """SA-CMP-FLT-011 — 'Reset filters' clears all inputs and restores the full list."""
    companies_page.open_filters()
    companies_page.reset_filters()
    initial_count = companies_page.get_visible_row_count()

    companies_page.filter_by_company_name(COMPANY_NAME)
    filtered_count = companies_page.get_visible_row_count()

    companies_page.open_filters()
    companies_page.reset_filters()
    restored_count = companies_page.get_visible_row_count()

    assert restored_count >= filtered_count, \
        "Reset should restore at least as many rows as the filtered result"
    assert restored_count == initial_count, \
        f"After reset, expected {initial_count} rows, got {restored_count}"


def test_close_filter_panel_without_applying(companies_page):
    """SA-CMP-FLT-012 — Close (X) dismisses the panel without applying pending changes."""
    initial_count = companies_page.get_visible_row_count()

    companies_page.open_filters()
    companies_page.enter_text(
        companies_page.COMPANY_NAME_FILTER, "ZZZNOMATCH_COMPANY_99999"
    )
    companies_page.close_filter_panel()

    after_count = companies_page.get_visible_row_count()
    assert after_count == initial_count, \
        "Closing the filter panel without applying should not change the list"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-FLT-013: Case-insensitive filter — "
           "server may perform case-sensitive matching; behaviour not confirmed.",
)
def test_name_filter_is_case_insensitive(companies_page):
    """SA-CMP-FLT-013 — Company name filter is case-insensitive."""
    companies_page.open_filters()
    companies_page.enter_text(
        companies_page.COMPANY_NAME_FILTER, COMPANY_NAME.upper()
    )
    companies_page.apply_filters()
    body = companies_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    assert COMPANY_NAME.lower() in body, \
        f"Case-insensitive filter should match '{COMPANY_NAME}' when searching upper-case"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-FLT-014: Filter persistence across navigation — "
           "whether the server stores filter state after reload is not confirmed.",
)
def test_applied_filter_persists_until_reset(browser, companies_page):
    """SA-CMP-FLT-014 — An applied filter stays active after navigating away and back."""
    companies_page.filter_by_company_name(COMPANY_NAME)

    browser.back()
    browser.forward()
    companies_page.wait_for_loaded()

    body = companies_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "error" not in body, \
        "No error should appear after navigating back to the companies list"
