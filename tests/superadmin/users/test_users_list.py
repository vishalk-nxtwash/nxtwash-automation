import allure
import pytest

from tests.superadmin.users.conftest import PRIMARY_USER

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Users"),
    allure.story("List"),
]


def test_users_list_page_loads(users_page):
    """SA-USR-LST-001 — Users list page loads with the 'Users' title visible."""
    title = users_page.get_text(users_page.PAGE_TITLE)
    assert title == "Users", f"Expected page title 'Users', got: {title!r}"


def test_users_table_has_required_columns(users_page):
    """SA-USR-LST-002 — Users table shows expected column headers."""
    headers = users_page.get_column_headers()
    headers_lower = [h.lower() for h in headers]
    expected = ["email", "phone"]
    for col in expected:
        assert any(col in h for h in headers_lower), \
            f"Expected a column containing '{col}' in headers: {headers}"


def test_users_list_shows_at_least_one_user(users_page):
    """SA-USR-LST-003 — Users list has at least one user row visible."""
    count = users_page.get_visible_row_count()
    assert count >= 1, \
        f"Expected at least 1 user row on the list, got: {count}"


def test_pagination_info_is_present(users_page):
    """SA-USR-LST-004 — Pagination summary (e.g. 'Page 1 of N') is displayed."""
    assert users_page.pagination_controls_present(), \
        "Pagination info should be visible on the Users list page"


def test_pagination_info_contains_page_and_of(users_page):
    """SA-USR-LST-005 — Pagination text contains 'Page' and 'of'."""
    text = users_page.get_pagination_text()
    assert "Page" in text and "of" in text, \
        f"Pagination text should contain 'Page ... of ...', got: {text!r}"


def test_previous_page_button_disabled_on_page_1(users_page):
    """SA-USR-LST-006 — Previous page button is disabled when on page 1."""
    assert users_page.prev_page_button_is_disabled(), \
        "Previous page button should be disabled on the first page"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-LST-007: Results-per-page selector locator not confirmed — "
           "may render as a React Select or native <select>; needs DOM inspection.",
)
def test_results_per_page_options(users_page):
    """SA-USR-LST-007 — Results-per-page selector offers standard page-size options."""
    options = users_page.get_results_per_page_options()
    assert "10" in options, \
        f"Expected '10' among page-size options, got: {options}"


def test_add_user_button_is_present(users_page):
    """SA-USR-LST-008 — 'Add User' button is visible on the Users list page."""
    assert users_page.driver.find_elements(*users_page.ADD_USER_BUTTON), \
        "'Add User' button should be present on the Users list page"


def test_direct_url_loads_users_list(browser):
    """SA-USR-LST-009 — Direct navigation to /users renders the Users list."""
    from pages.superadmin.login_page import LoginPage
    from pages.superadmin.users_page import UsersPage

    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()
    login_page.wait_for_overview()

    browser.get("https://superadmin.nxtwash.com/users")
    page = UsersPage(browser)
    page.wait_for_loaded()
    assert "users" in browser.current_url, \
        f"Expected /users URL, got: {browser.current_url}"


def test_primary_test_user_appears_in_list(users_page):
    """SA-USR-LST-010 — Primary test user (vksauser4) is visible after email filter."""
    users_page.filter_by_email(PRIMARY_USER["email"])
    rows = users_page.driver.find_elements(
        *users_page.get_user_row_locator(PRIMARY_USER["email"])
    )
    assert rows, \
        f"Expected a row for '{PRIMARY_USER['email']}' in the Users list"
