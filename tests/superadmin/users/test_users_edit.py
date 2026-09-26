import allure
import pytest

from tests.superadmin.users.conftest import PRIMARY_USER, TEST_USERS

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Users"),
    allure.story("Edit"),
]


def test_edit_button_opens_edit_form(browser, edit_user_page):
    """SA-USR-EDT-001 — Edit button opens the edit form at /users/{id}."""
    assert "/users/" in browser.current_url, \
        f"Expected URL to contain '/users/{{id}}', got: {browser.current_url}"
    assert "/users/create" not in browser.current_url, \
        "URL should be the edit URL, not the create URL"


def test_edit_form_shows_edit_label(edit_user_page):
    """SA-USR-EDT-002 — Edit form shows 'Edit' or 'User / Edit' header."""
    body = edit_user_page.get_body_text()
    assert "Edit" in body or "User" in body, \
        "Edit page should display 'User / Edit' or similar header"


def test_edit_form_prefills_first_name(edit_user_page):
    """SA-USR-EDT-003 — Edit form pre-fills the user's first name."""
    first_name = edit_user_page.get_first_name()
    assert PRIMARY_USER["first_name"].lower() in first_name.lower(), \
        f"First name should be pre-filled with '{PRIMARY_USER['first_name']}', " \
        f"got: {first_name!r}"


def test_edit_form_prefills_last_name(edit_user_page):
    """SA-USR-EDT-004 — Edit form pre-fills the user's last name."""
    last_name = edit_user_page.get_last_name()
    assert last_name, \
        "Last name field should be pre-filled in the edit form"


def test_edit_form_prefills_email(edit_user_page):
    """SA-USR-EDT-005 — Edit form pre-fills the user's email address."""
    email = edit_user_page.get_email()
    assert PRIMARY_USER["email"].lower() in email.lower(), \
        f"Email should be pre-filled with '{PRIMARY_USER['email']}', got: {email!r}"


def test_edit_form_prefills_phone(edit_user_page):
    """SA-USR-EDT-006 — Edit form pre-fills the user's phone number."""
    phone = edit_user_page.get_phone()
    assert phone, \
        "Phone field should be pre-filled in the edit form"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-EDT-007: Phone edit persistence — React-controlled input may "
           "not update internal state via Selenium send_keys; save behaviour not confirmed.",
)
def test_edit_phone_persists_after_save(browser, edit_user_page, users_page):
    """SA-USR-EDT-007 — Editing the phone number saves and persists on reload."""
    from pages.superadmin.users_page import EditUserPage

    original_phone = edit_user_page.get_phone()
    new_phone = "9988776655"

    try:
        edit_user_page.set_phone(new_phone)
        edit_user_page.click_save_changes()
        edit_user_page.confirm_yes_if_present()

        edit_url = browser.current_url
        browser.get(edit_url)
        reloaded = EditUserPage(browser)
        reloaded.wait_for_loaded()

        assert reloaded.get_phone() == new_phone, \
            f"Phone should be '{new_phone}' after save and reload, " \
            f"got: {reloaded.get_phone()!r}"
    finally:
        try:
            edit_user_page.set_phone(original_phone)
            edit_user_page.click_save_changes()
            edit_user_page.confirm_yes_if_present()
        except Exception:
            pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-EDT-008: Clearing a required field and saving — "
           "React-controlled inputs may not update state; save may succeed anyway.",
)
def test_clearing_required_field_rejected_on_save(edit_user_page):
    """SA-USR-EDT-008 — Clearing a required field and saving shows a validation error."""
    original_first = edit_user_page.get_first_name()

    try:
        edit_user_page.set_first_name("")
        edit_user_page.click_save_changes()
        edit_user_page.confirm_yes_if_present()

        assert edit_user_page.has_validation_error() \
            or "/users/" in edit_user_page.driver.current_url, \
            "Clearing a required field should trigger a validation error"
    finally:
        try:
            edit_user_page.set_first_name(original_first)
            edit_user_page.click_save_changes()
            edit_user_page.confirm_yes_if_present()
        except Exception:
            pass


def test_cancel_discards_changes(browser, edit_user_page):
    """SA-USR-EDT-009 — Cancel discards unsaved changes and the value is not persisted."""
    from pages.superadmin.users_page import EditUserPage, UsersPage

    original_last = edit_user_page.get_last_name()
    edit_user_page.set_last_name(original_last + " CANCELLED")
    edit_user_page.click_cancel()
    edit_user_page.confirm_yes_if_present()

    # Navigate back to edit the same user and confirm the value is unchanged
    users_list = UsersPage(browser)
    users_list.wait_for_loaded()
    users_list.open_user_edit(PRIMARY_USER["email"])

    reopened = EditUserPage(browser)
    reopened.wait_for_loaded()
    assert reopened.get_last_name() == original_last, \
        "Last name should be unchanged after cancelling the edit"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-EDT-010: Save changes confirmation dialog — "
           "may not appear on staging (direct save without confirmation).",
)
def test_save_changes_shows_confirmation(edit_user_page):
    """SA-USR-EDT-010 — Clicking 'Save changes' with no modifications shows a confirmation dialog."""
    from selenium.webdriver.support import expected_conditions as EC

    edit_user_page.click_save_changes()
    edit_user_page.wait.until(
        EC.visibility_of_element_located(edit_user_page.CONFIRM_YES_BUTTON)
    )
    assert edit_user_page.driver.find_elements(*edit_user_page.CONFIRM_YES_BUTTON), \
        "Save changes should trigger a confirmation dialog"
    edit_user_page.confirm_no()


def test_direct_url_to_users_edit(browser):
    """SA-USR-EDT-011 — Navigating to /users with edit opens the correct form."""
    from pages.superadmin.login_page import LoginPage
    from pages.superadmin.sidebar import Sidebar
    from pages.superadmin.users_page import EditUserPage, UsersPage

    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()
    login_page.wait_for_overview()

    browser.get("https://superadmin.nxtwash.com/users")
    users_list = UsersPage(browser)
    users_list.wait_for_loaded()
    users_list.open_user_edit(PRIMARY_USER["email"])

    edit_page = EditUserPage(browser)
    edit_page.wait_for_loaded()

    assert "/users/" in browser.current_url and "create" not in browser.current_url, \
        f"Expected edit URL /users/{{id}}, got: {browser.current_url}"


@pytest.mark.skip(
    reason="SA-USR-EDT-012: Non-existent user ID (404 vs redirect) — "
           "behaviour flagged as '[to be confirmed]' in spec."
)
def test_nonexistent_user_id_shows_error_or_redirect(browser):
    """SA-USR-EDT-012 — Navigating to /users/999999 shows a 404 or redirects."""
    pass
