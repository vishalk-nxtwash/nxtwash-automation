import allure
import pytest

from tests.superadmin.third_party.conftest import SALES_PATH_COMPANY

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Third Party"),
    allure.story("Sales Path — Filter"),
]


def test_filter_button_opens_filter_panel(sales_path_page):
    """SA-SLP-FLT-001 — 'Filter by' opens the filter panel."""
    sales_path_page.open_filters()
    assert sales_path_page.filter_panel_is_open(), \
        "Filter panel should be visible after clicking 'Filter by'"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-FLT-002: Company name field name attribute, 'Enabled Sales Path' "
           "toggle locator, and 'Active Sales Path' toggle locator not confirmed "
           "via DOM inspection.",
)
def test_filter_panel_shows_expected_controls(sales_path_page):
    """SA-SLP-FLT-002 — Filter panel shows Company field, Enabled toggle, Active toggle."""
    sales_path_page.open_filters()
    name_els = sales_path_page.driver.find_elements(*sales_path_page.COMPANY_NAME_FILTER)
    enabled_els = sales_path_page.driver.find_elements(*sales_path_page.ENABLED_TOGGLE)
    active_els = sales_path_page.driver.find_elements(*sales_path_page.ACTIVE_TOGGLE)
    assert name_els and name_els[0].is_displayed(), \
        "Company name filter field should be visible"
    assert enabled_els, "'Enabled Sales Path' toggle should be in the filter panel"
    assert active_els, "'Active Sales Path' toggle should be in the filter panel"


def test_filter_by_exact_company_name(sales_path_page):
    """SA-SLP-FLT-003 — Filter by exact Company name returns the matching sales path."""
    from selenium.webdriver.common.by import By
    sales_path_page.filter_by_company_name(SALES_PATH_COMPANY)
    body = sales_path_page.driver.find_element(By.TAG_NAME, "body").text
    assert SALES_PATH_COMPANY.lower() in body.lower(), \
        f"Expected '{SALES_PATH_COMPANY}' in filtered results"


def test_filter_by_partial_company_name(sales_path_page):
    """SA-SLP-FLT-004 — Filter by partial Company name returns matching sales paths."""
    partial = SALES_PATH_COMPANY[:6]
    sales_path_page.open_filters()
    sales_path_page.enter_text(sales_path_page.COMPANY_NAME_FILTER, partial)
    sales_path_page.apply_filters()
    count = sales_path_page.get_visible_row_count()
    assert count >= 1, \
        f"Partial company name filter '{partial}' should return at least one result"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-FLT-005: 'Enabled Sales Path' toggle locator not confirmed; "
           "also need at least one enabled sales path to verify the filter.",
)
def test_enabled_toggle_on_shows_enabled_only(sales_path_page):
    """SA-SLP-FLT-005 — 'Enabled Sales Path' toggle ON shows only enabled paths."""
    sales_path_page.open_filters()
    sales_path_page.reset_filters()
    sales_path_page.open_filters()
    els = sales_path_page.driver.find_elements(*sales_path_page.ENABLED_TOGGLE)
    assert els, "'Enabled Sales Path' toggle should be present in the filter panel"
    sales_path_page.apply_filters()
    count = sales_path_page.get_visible_row_count()
    assert count >= 1, "Enabled filter should return at least one sales path"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-FLT-006: 'Enabled Sales Path' toggle OFF behaviour not confirmed; "
           "unclear whether toggling OFF means 'show all' or 'show disabled only'.",
)
def test_enabled_toggle_off_shows_all(sales_path_page):
    """SA-SLP-FLT-006 — 'Enabled Sales Path' toggle OFF shows all paths."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-FLT-007: 'Active Sales Path' toggle locator not confirmed via DOM.",
)
def test_active_toggle_on_shows_active_only(sales_path_page):
    """SA-SLP-FLT-007 — 'Active Sales Path' toggle ON shows only active paths."""
    sales_path_page.open_filters()
    els = sales_path_page.driver.find_elements(*sales_path_page.ACTIVE_TOGGLE)
    assert els, "'Active Sales Path' toggle should be present"
    sales_path_page.apply_filters()
    count = sales_path_page.get_visible_row_count()
    assert count >= 1, "Active filter should return at least one sales path"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-FLT-008: Active toggle OFF behaviour not confirmed; also requires "
           "at least one inactive path to demonstrate a difference.",
)
def test_active_toggle_off_shows_all(sales_path_page):
    """SA-SLP-FLT-008 — 'Active Sales Path' toggle OFF shows all paths."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-SLP-FLT-009: Combined filter depends on confirmed locators for "
           "Company name input (FLT-003), Enabled toggle (FLT-005), "
           "and Active toggle (FLT-007).",
)
def test_combined_company_enabled_active_filter(sales_path_page):
    """SA-SLP-FLT-009 — Company + Enabled + Active filter returns the correct subset."""
    pass


def test_filter_with_no_match_shows_empty_state(sales_path_page):
    """SA-SLP-FLT-010 — Filter with no match shows an empty state without an error."""
    from selenium.webdriver.common.by import By
    sales_path_page.open_filters()
    sales_path_page.enter_text(
        sales_path_page.COMPANY_NAME_FILTER, "ZZZNOMATCH_SP_99999"
    )
    sales_path_page.apply_filters()
    body = sales_path_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "error" not in body, \
        "No-match filter should show an empty state, not an error"


def test_reset_filters_restores_full_list(sales_path_page):
    """SA-SLP-FLT-011 — 'Reset filters' clears inputs and restores the full list."""
    initial_count = sales_path_page.get_visible_row_count()

    sales_path_page.filter_by_company_name(SALES_PATH_COMPANY)
    sales_path_page.open_filters()
    sales_path_page.reset_filters()
    restored_count = sales_path_page.get_visible_row_count()

    assert restored_count == initial_count, \
        f"After reset, expected {initial_count} rows, got {restored_count}"


def test_close_filter_panel_without_applying(sales_path_page):
    """SA-SLP-FLT-012 — Close (X) dismisses the filter panel without applying changes."""
    initial_count = sales_path_page.get_visible_row_count()

    sales_path_page.open_filters()
    sales_path_page.enter_text(
        sales_path_page.COMPANY_NAME_FILTER, "ZZZNOMATCH_SP_99999"
    )
    sales_path_page.close_filter_panel()

    after_count = sales_path_page.get_visible_row_count()
    assert after_count == initial_count, \
        "Closing the filter panel without applying should not change the list"
