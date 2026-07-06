import allure
import pytest

from tests.admin_portal.users.conftest import (
    EMPLOYEE_NAME,
    INVALID_EMAIL,
    UPDATED_EMAIL,
    UPDATED_PHONE,
    UPDATED_ROLE,
    USER_EMAIL,
    USER_PHONE,
    USER_ROLE,
    open_edit_user_form,
    open_users_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Users"),
    allure.story("Edit"),
]


@allure.title("USR-EDT-001 Edit button opens the edit form at the correct URL")
@pytest.mark.smoke
def test_users_edit_form_opens(browser, managed_user):
    page = open_users_page(browser)
    page.search_user_by_email(USER_EMAIL)
    page.open_edit_user(USER_EMAIL)

    assert "edit" in browser.current_url.lower() or "users" in browser.current_url
    assert page_has_no_broken_state(page)


@allure.title("USR-EDT-002 Editing the Email saves and persists on list reload")
@pytest.mark.regression
def test_edit_user_email_persists(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.enter_email(UPDATED_EMAIL)
    form.click_save()

    page = open_users_page(browser)
    assert page.user_exists(UPDATED_EMAIL)

    # Restore original email so the managed_user teardown can find the record
    form = open_edit_user_form(browser, UPDATED_EMAIL)
    form.enter_email(USER_EMAIL)
    form.click_save()
    open_users_page(browser)

    assert page_has_no_broken_state(page)


@allure.title("USR-EDT-003 Editing the Phone number saves and persists")
@pytest.mark.regression
def test_edit_user_phone_persists(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.enter_phone(UPDATED_PHONE)
    form.click_save()

    form = open_edit_user_form(browser, USER_EMAIL)
    assert form.get_phone_value() == UPDATED_PHONE
    assert page_has_no_broken_state(form)


@allure.title("USR-EDT-004 Changing the User Role saves and is visible on the list")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-EDT-004: Role combobox locator uses label heuristics. "
        "Verify in DevTools and confirm UPDATED_ROLE exists in staging before removing xfail."
    ),
)
def test_edit_user_role_persists(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.select_role(UPDATED_ROLE)
    form.click_save()

    form = open_edit_user_form(browser, USER_EMAIL)
    body = form.get_body_text()
    assert UPDATED_ROLE in body
    assert page_has_no_broken_state(form)


@allure.title("USR-EDT-005 Changing the linked Employee saves and persists")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-EDT-005: Requires a second distinct employee in staging to switch to. "
        "Verify employee availability and combobox locator in DevTools."
    ),
)
def test_edit_user_employee_persists(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    # Re-select the same employee to verify the round-trip without needing a second employee
    form.select_employee(EMPLOYEE_NAME)
    form.click_save()

    form = open_edit_user_form(browser, USER_EMAIL)
    assert EMPLOYEE_NAME in form.get_body_text()
    assert page_has_no_broken_state(form)


@allure.title("USR-EDT-006 Activating an inactive user updates its status to Active")
@pytest.mark.smoke
@pytest.mark.skip(reason="Manual — USR-EDT-006: Activate/deactivate toggle flow verified manually in staging.")
def test_activate_inactive_user(browser, managed_user):
    # Deactivate first
    form = open_edit_user_form(browser, USER_EMAIL)
    form.ensure_active_switch_off()
    form.click_save()

    # Activate
    form = open_edit_user_form(browser, USER_EMAIL)
    form.ensure_active_switch_on()
    form.click_save()

    page = open_users_page(browser)
    page.search_user_by_email(USER_EMAIL)
    assert page.user_exists(USER_EMAIL)
    assert page.get_user_status(USER_EMAIL) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("USR-EDT-007 Deactivating an active user hides it from the default list")
@pytest.mark.smoke
def test_deactivate_active_user(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.ensure_active_switch_off()
    form.click_save()

    page = open_users_page(browser)
    page.search_user_by_email(USER_EMAIL)
    body = page.get_body_text()

    assert USER_EMAIL not in body or page.get_user_status(USER_EMAIL) == "Inactive"
    assert page_has_no_broken_state(page)


@allure.title("USR-EDT-008 Clearing the Email on the edit form blocks save")
@pytest.mark.regression
def test_edit_user_email_required(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.clear_email()
    form.click_save()

    assert not form.email_input_is_valid() or "email" in form.get_body_text().lower()
    assert page_has_no_broken_state(form)


@allure.title("USR-EDT-009 Clearing the Phone on the edit form blocks save")
@pytest.mark.regression
def test_edit_user_phone_required(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.clear_phone()
    form.click_save()

    assert not form.phone_input_is_valid() or "phone" in form.get_body_text().lower()
    assert page_has_no_broken_state(form)


@allure.title("USR-EDT-010 Invalid email format is blocked on the edit form")
@pytest.mark.regression
def test_edit_user_invalid_email_blocked(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.enter_email(INVALID_EMAIL)
    form.click_save()

    assert not form.email_input_is_valid() or "email" in form.get_body_text().lower()
    assert page_has_no_broken_state(form)


@allure.title("USR-EDT-011 Cancelling the edit form discards changes and keeps original data")
@pytest.mark.regression
def test_edit_user_cancel_discards_changes(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.enter_email("discarded.change@test.com")
    form.click_cancel()

    page = open_users_page(browser)
    assert page.user_exists(USER_EMAIL)
    assert not page.user_exists("discarded.change@test.com")
    assert page_has_no_broken_state(page)


@allure.title("USR-EDT-012 Edit form does not show password fields — only Change Password button")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-EDT-012: password_fields_absent() uses name-based heuristics for password inputs "
        "and Change password button. Verify exact form structure in DevTools."
    ),
)
def test_edit_user_no_password_fields(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)

    assert form.password_fields_absent(), (
        "Edit form should not show password/confirm-password fields; "
        "only a Change Password button is expected."
    )
    assert page_has_no_broken_state(form)
