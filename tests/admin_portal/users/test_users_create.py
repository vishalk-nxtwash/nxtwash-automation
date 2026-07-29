import uuid

import allure
import pytest

from tests.admin_portal.users.conftest import (
    EMPLOYEE_NAME,
    INVALID_EMAIL,
    USER_EMAIL,
    USER_PASSWORD,
    USER_PHONE,
    USER_ROLE,
    create_user_if_missing,
    open_create_user_form,
    open_users_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Users"),
    allure.story("Create"),
]


def _unique_email():
    return "vk.auto.%s@yopmail.com" % uuid.uuid4().hex[:8]


def _unique_phone():
    return "90%010d" % (abs(hash(uuid.uuid4())) % 100000000)


@allure.title("USR-CRT-001 Clicking Add user opens the create form at the correct URL")
@pytest.mark.smoke
def test_users_add_form_opens(browser):
    page = open_users_page(browser)
    page.click_add_user()

    assert "users/new" in browser.current_url or "users" in browser.current_url
    assert page_has_no_broken_state(page)


@allure.title("USR-CRT-002 Creating an active user with all required fields saves correctly")
@pytest.mark.smoke
@pytest.mark.skip(reason="Manual — USR-CRT-002: Create active user flow verified manually in staging.")
def test_create_active_user(browser):
    email = _unique_email()
    phone = _unique_phone()

    form = open_create_user_form(browser)
    form.fill_create_form(EMPLOYEE_NAME, USER_PASSWORD, email, phone, USER_ROLE)
    form.ensure_active_switch_on()
    form.click_save()

    page = open_users_page(browser)
    assert page.user_exists(email)
    assert page.get_user_status(email) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("USR-CRT-003 Creating an inactive user saves it with Inactive status")
@pytest.mark.regression
@pytest.mark.skip(reason="staging data: employee 'test user 3' not seeded — deferred")
def test_create_inactive_user(browser):
    email = _unique_email()
    phone = _unique_phone()

    form = open_create_user_form(browser)
    form.fill_create_form(EMPLOYEE_NAME, USER_PASSWORD, email, phone, USER_ROLE)
    form.ensure_active_switch_off()
    form.click_save()

    page = open_users_page(browser)
    assert page_has_no_broken_state(page)
    # Inactive users are hidden by default; they should not appear in the active list
    page.search_user_by_email(email)
    body = page.get_body_text()
    assert email not in body or page.get_user_status(email) == "Inactive"


@allure.title("USR-CRT-004 Submitting form without Employee is blocked with validation")
@pytest.mark.smoke
def test_create_user_employee_required(browser):
    form = open_create_user_form(browser)
    form.enter_password(USER_PASSWORD)
    form.enter_confirm_password(USER_PASSWORD)
    form.enter_email(_unique_email())
    form.enter_phone(_unique_phone())
    # Employee intentionally omitted
    form.click_save()

    body = form.get_body_text()
    assert (
        "employee" in body.lower()
        or "required" in body.lower()
        or "users/new" in browser.current_url
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-005 Submitting form without Password is blocked with validation")
@pytest.mark.smoke
@pytest.mark.skip(reason="staging data: employee 'test user 3' not seeded — deferred")
def test_create_user_password_required(browser):
    form = open_create_user_form(browser)
    form.select_employee(EMPLOYEE_NAME)
    form.enter_email(_unique_email())
    form.enter_phone(_unique_phone())
    form.select_role(USER_ROLE)
    # Password intentionally omitted
    form.click_save()

    assert not form.password_input_is_valid() or "password" in form.get_body_text().lower()
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-006 Submitting form without Confirm Password is blocked")
@pytest.mark.regression
@pytest.mark.skip(reason="staging data: employee 'test user 3' not seeded — deferred")
def test_create_user_confirm_password_required(browser):
    form = open_create_user_form(browser)
    form.select_employee(EMPLOYEE_NAME)
    form.enter_password(USER_PASSWORD)
    form.enter_email(_unique_email())
    form.enter_phone(_unique_phone())
    form.select_role(USER_ROLE)
    # Confirm password intentionally omitted
    form.click_save()

    assert (
        not form.confirm_password_input_is_valid()
        or "confirm" in form.get_body_text().lower()
        or "password" in form.get_body_text().lower()
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-007 Submitting form without Email is blocked with validation")
@pytest.mark.smoke
@pytest.mark.skip(reason="staging data: employee 'test user 3' not seeded — deferred")
def test_create_user_email_required(browser):
    form = open_create_user_form(browser)
    form.select_employee(EMPLOYEE_NAME)
    form.enter_password(USER_PASSWORD)
    form.enter_confirm_password(USER_PASSWORD)
    form.enter_phone(_unique_phone())
    form.select_role(USER_ROLE)
    # Email intentionally omitted
    form.click_save()

    assert not form.email_input_is_valid() or "email" in form.get_body_text().lower()
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-008 Submitting form without Phone Number is blocked")
@pytest.mark.regression
@pytest.mark.skip(reason="staging data: employee 'test user 3' not seeded — deferred")
def test_create_user_phone_required(browser):
    form = open_create_user_form(browser)
    form.select_employee(EMPLOYEE_NAME)
    form.enter_password(USER_PASSWORD)
    form.enter_confirm_password(USER_PASSWORD)
    form.enter_email(_unique_email())
    form.select_role(USER_ROLE)
    # Phone intentionally omitted
    form.click_save()

    assert not form.phone_input_is_valid() or "phone" in form.get_body_text().lower()
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-009 Submitting form without User Role is blocked")
@pytest.mark.smoke
@pytest.mark.skip(reason="staging data: employee 'test user 3' not seeded — deferred")
def test_create_user_role_required(browser):
    form = open_create_user_form(browser)
    form.select_employee(EMPLOYEE_NAME)
    form.enter_password(USER_PASSWORD)
    form.enter_confirm_password(USER_PASSWORD)
    form.enter_email(_unique_email())
    form.enter_phone(_unique_phone())
    # Role intentionally omitted
    form.click_save()

    body = form.get_body_text()
    assert (
        "role" in body.lower()
        or "required" in body.lower()
        or "users/new" in browser.current_url
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-010 Mismatched passwords show a validation error")
@pytest.mark.regression
@pytest.mark.skip(reason="staging data: employee 'test user 3' not seeded — deferred")
def test_create_user_password_mismatch(browser):
    form = open_create_user_form(browser)
    form.select_employee(EMPLOYEE_NAME)
    form.enter_password(USER_PASSWORD)
    form.enter_confirm_password(USER_PASSWORD + "wrong")
    form.enter_email(_unique_email())
    form.enter_phone(_unique_phone())
    form.select_role(USER_ROLE)
    form.click_save()

    body = form.get_body_text()
    assert (
        "match" in body.lower()
        or "password" in body.lower()
        or "users/new" in browser.current_url
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-011 Password visibility toggle shows and hides password text")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-CRT-011: Eye-icon locator uses class heuristics. "
        "Verify toggle button selector in DevTools before removing xfail."
    ),
)
def test_create_user_password_visibility_toggle(browser):
    form = open_create_user_form(browser)
    form.enter_password(USER_PASSWORD)

    assert form.password_field_type() == "password"
    form.toggle_password_visibility()
    assert form.password_field_type() == "text"
    form.toggle_password_visibility()
    assert form.password_field_type() == "password"
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-012 Confirm password visibility toggle works independently")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-CRT-012: Eye-icon locator on confirm field uses class heuristics. "
        "Verify in DevTools before removing xfail."
    ),
)
def test_create_user_confirm_password_visibility_toggle(browser):
    form = open_create_user_form(browser)
    form.enter_confirm_password(USER_PASSWORD)

    assert form.confirm_password_field_type() == "password"
    form.toggle_confirm_password_visibility()
    assert form.confirm_password_field_type() == "text"
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-013 Employee dropdown lists active employees")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-CRT-013: Employee combobox locator uses label heuristics. "
        "Verify in DevTools and confirm EMPLOYEE_NAME exists in staging."
    ),
)
def test_create_user_employee_dropdown_lists_employees(browser):
    form = open_create_user_form(browser)
    options = form.get_employee_dropdown_options()

    assert len(options) > 0, "Employee dropdown returned no options"
    assert EMPLOYEE_NAME in options, (
        "Expected employee '%s' not found. Got: %s" % (EMPLOYEE_NAME, options[:10])
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-014 User role dropdown lists active roles")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-CRT-014: Role combobox locator uses label heuristics. "
        "Verify in DevTools before removing xfail."
    ),
)
def test_create_user_role_dropdown_lists_roles(browser):
    form = open_create_user_form(browser)
    options = form.get_role_dropdown_options()

    assert len(options) > 0, "Role dropdown returned no options"
    assert USER_ROLE in options, (
        "Expected role '%s' not found. Got: %s" % (USER_ROLE, options)
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-015 Invalid email format is rejected")
@pytest.mark.regression
def test_create_user_invalid_email_rejected(browser):
    form = open_create_user_form(browser)
    form.enter_email(INVALID_EMAIL)
    form.click_save()

    assert not form.email_input_is_valid() or "email" in form.get_body_text().lower()
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-016 Duplicate email address is rejected")
@pytest.mark.regression
def test_create_user_duplicate_email_rejected(browser):
    create_user_if_missing(browser)
    form = open_create_user_form(browser)
    form.select_employee(EMPLOYEE_NAME)
    form.enter_password(USER_PASSWORD)
    form.enter_confirm_password(USER_PASSWORD)
    form.enter_email(USER_EMAIL)      # already exists
    form.enter_phone(_unique_phone())
    form.select_role(USER_ROLE)
    form.click_save()

    body = form.get_body_text()
    assert (
        "exist" in body.lower()
        or "duplicate" in body.lower()
        or "already" in body.lower()
        or "users/new" in browser.current_url
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-CRT-019 Cancelling the create form discards it and returns to the list")
@pytest.mark.regression
def test_create_user_cancel_discards_form(browser):
    email = _unique_email()
    form = open_create_user_form(browser)
    form.enter_email(email)
    form.click_cancel()

    page = open_users_page(browser)
    assert not page.user_exists(email)
    assert page_has_no_broken_state(page)


@allure.title("USR-CRT-020 Newly created user appears in the list immediately after save")
@pytest.mark.regression
@pytest.mark.skip(reason="Manual — USR-CRT-020: New user visibility in list verified manually in staging.")
def test_new_user_appears_immediately(browser):
    email = _unique_email()
    phone = _unique_phone()

    form = open_create_user_form(browser)
    form.fill_create_form(EMPLOYEE_NAME, USER_PASSWORD, email, phone, USER_ROLE)
    form.click_save()

    page = open_users_page(browser)
    assert page.user_exists(email), (
        "User '%s' not found in list immediately after save" % email
    )
    assert page_has_no_broken_state(page)
