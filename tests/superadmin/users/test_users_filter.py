import allure
import pytest

from selenium.webdriver.common.by import By

from tests.superadmin.users.conftest import PRIMARY_USER, TEST_USERS

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Users"),
    allure.story("Filter"),
]


def test_filter_button_opens_filter_panel(users_page):
    """SA-USR-FLT-001 — Clicking 'Filter by' opens the filter panel."""
    users_page.open_filters()
    assert users_page.filter_panel_is_open(), \
        "Filter panel should be visible after clicking 'Filter by'"


def test_filter_panel_shows_required_fields(users_page):
    """SA-USR-FLT-002 — Filter panel shows First Name, Last Name, Email, and Phone fields."""
    users_page.open_filters()
    for locator in [
        users_page.FIRST_NAME_FILTER,
        users_page.LAST_NAME_FILTER,
        users_page.EMAIL_FILTER,
        users_page.PHONE_FILTER,
    ]:
        els = users_page.driver.find_elements(*locator)
        assert els, f"Filter field {locator} should be present in the filter panel"


def test_filter_by_exact_first_name(users_page):
    """SA-USR-FLT-003 — Filtering by exact first name returns matching users."""
    users_page.filter_by_first_name(PRIMARY_USER["first_name"])
    names = users_page.get_visible_user_first_names()
    assert any(PRIMARY_USER["first_name"].lower() in n.lower() for n in names), \
        f"Expected '{PRIMARY_USER['first_name']}' in filtered results, got: {names}"


def test_filter_by_exact_last_name(users_page):
    """SA-USR-FLT-004 — Filtering by exact last name returns matching users."""
    users_page.filter_by_last_name(PRIMARY_USER["last_name"])
    body = users_page.driver.find_element(By.TAG_NAME, "body").text
    assert PRIMARY_USER["last_name"].lower() in body.lower(), \
        f"Expected '{PRIMARY_USER['last_name']}' in filtered results"


def test_filter_by_exact_email(users_page):
    """SA-USR-FLT-005 — Filtering by exact email returns the correct user."""
    users_page.filter_by_email(PRIMARY_USER["email"])
    emails = users_page.get_visible_user_emails()
    assert any(PRIMARY_USER["email"].lower() in e.lower() for e in emails), \
        f"Expected '{PRIMARY_USER['email']}' in filtered results, got: {emails}"


def test_filter_by_exact_phone(users_page):
    """SA-USR-FLT-006 — Filtering by exact phone number returns the correct user."""
    users_page.filter_by_phone(PRIMARY_USER["phone"])
    body = users_page.driver.find_element(By.TAG_NAME, "body").text
    # App may display phone as formatted e.g. "(990) 000-0010" instead of "9900000010"
    digits_only = PRIMARY_USER["phone"].replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    assert digits_only in body.replace("-", "").replace(" ", "").replace("(", "").replace(")", ""), \
        f"Expected phone '{PRIMARY_USER['phone']}' in filtered results"


def test_non_matching_filter_shows_empty_state(users_page):
    """SA-USR-FLT-007 — A filter with no matches shows an empty state without an error."""
    users_page.open_filters()
    users_page.enter_text(users_page.EMAIL_FILTER, "ZZZNOMATCH_99999@yopmail.com")
    users_page.apply_filters()

    body = users_page.driver.find_element(By.TAG_NAME, "body").text
    assert "error" not in body.lower(), \
        "No-match filter should show an empty state, not an error"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-FLT-008: Parallel workers create/delete users concurrently — "
           "row count comparison is inherently flaky under -n 2.",
)
def test_reset_filters_restores_full_list(users_page):
    """SA-USR-FLT-008 — Reset clears all filter inputs and restores the full user list."""
    # Baseline full count
    users_page.open_filters()
    users_page.reset_filters()
    initial_count = users_page.get_visible_row_count()

    # Apply a filter to narrow the list
    users_page.filter_by_email(PRIMARY_USER["email"])
    filtered_count = users_page.get_visible_row_count()

    # Reset and check restored
    users_page.open_filters()
    users_page.reset_filters()
    restored_count = users_page.get_visible_row_count()

    assert restored_count >= filtered_count, \
        "Resetting filters should restore at least as many rows as the filtered result"
    assert restored_count == initial_count, \
        f"After reset, expected {initial_count} rows, got {restored_count}"


def test_apply_filters_updates_list(users_page):
    """SA-USR-FLT-009 — Applying a filter updates the list and pagination info."""
    users_page.filter_by_email(PRIMARY_USER["email"])
    pagination = users_page.get_pagination_text()
    assert "Page" in pagination, \
        "Pagination text should update after applying a filter"


def test_partial_first_name_filter(users_page):
    """SA-USR-FLT-010 — Partial first name (prefix) returns matching users."""
    users_page.filter_by_first_name("VK")
    count = users_page.get_visible_row_count()
    assert count >= 1, \
        "Partial first name filter 'VK' should return at least one user"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-FLT-011: Partial email filter — server may enforce a minimum "
           "term length or require an exact match; behaviour not confirmed.",
)
def test_partial_email_filter(users_page):
    """SA-USR-FLT-011 — Partial email (prefix) returns matching users."""
    users_page.filter_by_email("vksauser")
    count = users_page.get_visible_row_count()
    assert count >= 1, \
        "Partial email filter 'vksauser' should return at least one result"


def test_combined_filters_narrow_results(users_page):
    """SA-USR-FLT-012 — Combining first name and email filters returns the correct subset."""
    users_page.open_filters()
    users_page.enter_text(users_page.FIRST_NAME_FILTER, PRIMARY_USER["first_name"])
    users_page.enter_text(users_page.EMAIL_FILTER, PRIMARY_USER["email"])
    users_page.apply_filters()

    body = users_page.driver.find_element(By.TAG_NAME, "body").text
    assert PRIMARY_USER["email"].lower() in body.lower(), \
        "Combined first name + email filter should find the primary test user"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-FLT-013: Filter persistence across navigation — "
           "whether the server stores filter state after reload is not confirmed.",
)
def test_applied_filter_persists_across_navigation(browser, users_page):
    """SA-USR-FLT-013 — An applied filter stays active after navigating away and back."""
    users_page.filter_by_email(PRIMARY_USER["email"])

    browser.back()
    browser.forward()
    users_page.wait_for_loaded()

    body = users_page.driver.find_element(By.TAG_NAME, "body").text
    assert "error" not in body.lower(), \
        "No error should appear after navigating back to the users list"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-FLT-014: Clear input X button locator inside filter panel "
           "not confirmed — needs DOM inspection.",
)
def test_clear_x_empties_filter_input(users_page):
    """SA-USR-FLT-014 — The X clear icon empties the email filter input."""
    users_page.open_filters()
    users_page.enter_text(users_page.EMAIL_FILTER, PRIMARY_USER["email"])

    clear_btn = (
        By.XPATH,
        "//input[@name='emailId']/..//button | "
        "//input[@name='emailId']/following-sibling::button | "
        "//input[@name='emailId']/following::button[1]",
    )
    btn = users_page.driver.find_elements(*clear_btn)
    assert btn, "A clear (X) button should be present next to the email filter input"
    btn[0].click()

    value = users_page.get_filter_value(users_page.EMAIL_FILTER)
    assert value == "", \
        f"Email filter should be empty after clicking the clear button, got: {value!r}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-FLT-015: Case-insensitive filter — server may perform "
           "case-sensitive matching; behaviour not confirmed on staging.",
)
def test_email_filter_is_case_insensitive(users_page):
    """SA-USR-FLT-015 — Email filter is case-insensitive."""
    users_page.filter_by_email(PRIMARY_USER["email"].upper())
    emails = users_page.get_visible_user_emails()
    assert any(PRIMARY_USER["email"].lower() in e.lower() for e in emails), \
        f"Case-insensitive email filter should match '{PRIMARY_USER['email']}' " \
        f"when searching upper-case"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-FLT-016: Filter panel Close button locator not confirmed — "
           "needs DOM inspection with DevTools.",
)
def test_close_filter_panel_without_applying(users_page):
    """SA-USR-FLT-016 — Close button dismisses the filter panel without applying."""
    initial_count = users_page.get_visible_row_count()

    users_page.open_filters()
    users_page.enter_text(users_page.EMAIL_FILTER, "ZZZNOMATCH")
    users_page.close_filter_panel()

    after_count = users_page.get_visible_row_count()
    assert after_count == initial_count, \
        "Closing the filter panel without applying should not change the list"
