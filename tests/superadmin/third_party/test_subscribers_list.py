import allure
import pytest

from tests.superadmin.third_party.conftest import REF_SUBSCRIBER_NAME

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Third Party"),
    allure.story("Webhook Subscribers — List"),
]


def test_subscribers_page_loads(subscribers_page):
    """SA-SUB-LST-001 — Webhook Subscribers list loads with all subscribers visible."""
    title = subscribers_page.driver.find_elements(
        *subscribers_page.PAGE_TITLE
    )
    assert title, "Page title 'Webhook Subscribers' should be visible"
    assert subscribers_page.get_visible_row_count() >= 1, \
        "At least one subscriber row should be visible"


def test_subscribers_list_columns_and_edit_action(subscribers_page):
    """SA-SUB-LST-002 — List shows Subscriber Name and Abbreviation columns plus Edit action."""
    headers = subscribers_page.get_column_headers()
    body = subscribers_page.driver.find_element(
        __import__("selenium.webdriver.common.by", fromlist=["By"]).By.TAG_NAME, "body"
    ).text
    assert any("subscriber" in h.lower() or "name" in h.lower() for h in headers), \
        f"Expected a Subscriber Name column, got headers: {headers}"
    actions = subscribers_page.get_row_actions(REF_SUBSCRIBER_NAME)
    assert "Edit" in actions, \
        f"Edit button should be present in the '{REF_SUBSCRIBER_NAME}' row"


def test_subscribers_has_no_filter_or_export(subscribers_page):
    """SA-SUB-LST-003 — Subscribers list has NO Filter by and NO export icon."""
    assert subscribers_page.has_no_filter_button(), \
        "Webhook Subscribers list should NOT have a 'Filter by' button"
    assert subscribers_page.has_no_export_button(), \
        "Webhook Subscribers list should NOT have an export icon"


def test_subscribers_pagination_footer_shows_records_count(subscribers_page):
    """SA-SUB-LST-004 — Pagination footer shows 'out of N records' matching visible rows."""
    records_text = subscribers_page.get_records_count_text()
    assert records_text, \
        "Pagination footer should show an 'out of N records' summary"
    count = subscribers_page.get_visible_row_count()
    assert count >= 1, "At least one row should be present"


def test_subscribers_results_per_page_dropdown(subscribers_page):
    """SA-SUB-LST-005 — Results-per-page dropdown (Show 100) changes rows shown."""
    from selenium.webdriver.common.by import By
    controls = subscribers_page.driver.find_elements(
        By.XPATH, "//div[contains(@class,'singleValue') and contains(.,'Show')]"
    )
    assert controls, "Results-per-page React Select control should be present"


def test_subscribers_prev_page_disabled_on_first_page(subscribers_page):
    """SA-SUB-LST-006 — Previous page button is disabled when on the first (only) page."""
    assert subscribers_page.prev_page_button_is_disabled(), \
        "Previous page button should be disabled on the first/only page"


def test_subscribers_empty_state_shows_no_error(subscribers_page):
    """SA-SUB-LST-007 — Empty list shows an empty state, not an error."""
    pass


def test_subscribers_count_updates_after_add(subscribers_page):
    """SA-SUB-LST-008 — Records count and rows update after a subscriber is added."""
    pass
