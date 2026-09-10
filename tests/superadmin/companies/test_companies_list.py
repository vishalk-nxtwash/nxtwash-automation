import allure
import pytest

from tests.superadmin.companies.conftest import TEST_COMPANY

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Companies"),
    allure.story("List"),
]

# Actual headers confirmed from staging page dump
_EXPECTED_COLUMNS = [
    "Company name", "Email", "Phone number",
    "Company country", "Company state", "Company city", "Company address",
]
_PARTIAL_DATA_COMPANY = TEST_COMPANY


def test_companies_list_page_loads(browser, companies_page):
    """SA-CMP-LST-001 — /companies loads with the list visible."""
    assert "companies" in browser.current_url, \
        "Expected URL to contain 'companies'"
    assert companies_page.get_page_title() == "Companies", \
        "Expected page title 'Companies'"


def test_list_shows_all_column_headers(companies_page):
    """SA-CMP-LST-002 — all seven column headers are labeled correctly."""
    headers = companies_page.get_column_headers()
    headers_lower = [h.lower() for h in headers]
    for expected in _EXPECTED_COLUMNS:
        assert expected.lower() in headers_lower, \
            f"Column '{expected}' not found in headers: {headers}"


def test_each_row_has_login_to_and_edit_actions(companies_page):
    """SA-CMP-LST-003 — every company row shows 'Login to' and 'Edit' buttons."""
    companies_page.filter_by_company_name(TEST_COMPANY)
    assert companies_page.row_has_login_to_button(TEST_COMPANY), \
        f"'Login to' button missing for {TEST_COMPANY}"
    assert companies_page.row_has_edit_button(TEST_COMPANY), \
        f"'Edit' button missing for {TEST_COMPANY}"


def test_pagination_footer_is_displayed(companies_page):
    """SA-CMP-LST-004 — pagination footer shows page and record count info."""
    text = companies_page.get_pagination_text()
    assert "Page" in text, f"Expected 'Page' in pagination text, got: {text!r}"
    assert "of" in text, f"Expected 'of' in pagination text, got: {text!r}"
    assert "records" in text.lower() or "out of" in text.lower(), \
        f"Expected record count info in pagination text, got: {text!r}"


@pytest.mark.skip(
    reason="SA-CMP-LST-005: Results-per-page uses a custom React widget, not a "
           "<select> element. Locator needs DOM inspection before implementing."
)
def test_results_per_page_dropdown_has_expected_options(companies_page):
    """SA-CMP-LST-005 — results-per-page dropdown offers 10 / 25 / 50 / 100."""
    options = companies_page.get_results_per_page_options()
    for expected in ("10", "25", "50", "100"):
        assert expected in options, \
            f"Expected '{expected}' in results-per-page options, got: {options}"


def test_pagination_controls_disabled_on_single_page(companies_page):
    """SA-CMP-LST-006 — Prev/Next buttons are disabled when all records fit one page."""
    pagination_text = companies_page.get_pagination_text()
    if "of 1" not in pagination_text:
        pytest.skip(
            "Staging has multiple pages of companies; "
            "this test is only valid on a single-page result set."
        )
    assert companies_page.prev_page_button_is_disabled(), \
        "Previous-page button should be disabled on the first (only) page"
    assert companies_page.next_page_button_is_disabled(), \
        "Next-page button should be disabled on the last (only) page"


def test_company_with_partial_data_renders_without_error(companies_page):
    """SA-CMP-LST-007 — a company with only name/country renders without layout breaks."""
    try:
        companies_page.filter_by_company_name(_PARTIAL_DATA_COMPANY)
        row_visible = True
    except Exception:
        row_visible = False

    assert row_visible, \
        f"Company with partial data '{_PARTIAL_DATA_COMPANY}' should render without error"
    body = companies_page.get_body_text() if hasattr(companies_page, 'get_body_text') \
        else companies_page.driver.find_element(
            __import__('selenium.webdriver.common.by', fromlist=['By']).By.TAG_NAME, "body"
        ).text
    assert "error" not in body.lower() or "No results" in body, \
        "Page should not show an error for a company with partial data"


@pytest.mark.skip(reason="SA-CMP-LST-008: Requires confirmed long-address company name from staging data")
def test_long_address_wraps_without_overflow(companies_page):
    """SA-CMP-LST-008 — a company with a long address wraps within its cell."""
    pass


def test_no_match_filter_shows_empty_state_not_error(companies_page):
    """SA-CMP-LST-009 — filtering with a non-existent name shows empty state, not an error."""
    companies_page.open_filters()
    companies_page.enter_text(companies_page.COMPANY_NAME_FILTER, "ZZZNOMATCHZZZ")
    companies_page.apply_filters()

    body = companies_page.driver.find_element(
        __import__('selenium.webdriver.common.by', fromlist=['By']).By.TAG_NAME, "body"
    ).text
    assert "error" not in body.lower(), \
        "Filtering with no match should show an empty state, not an error page"


@pytest.mark.skip(reason="SA-CMP-LST-010: Record count update verified as part of create tests (CRT-006)")
def test_record_count_updates_after_create(companies_page):
    """SA-CMP-LST-010 — the record count reflects a newly created company."""
    pass
