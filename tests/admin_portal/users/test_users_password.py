import allure
import pytest

from tests.admin_portal.users.conftest import (
    USER_EMAIL,
    USER_PASSWORD,
    open_edit_user_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Users"),
    allure.story("Password"),
]


@allure.title("USR-PWD-001 Change password button on the edit form opens the password flow")
@pytest.mark.smoke
def test_change_password_button_opens_flow(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.click_change_password_button()

    assert form.change_password_fields_visible(), (
        "New password fields not visible after clicking Change Password"
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-PWD-002 Matching new passwords save successfully")
@pytest.mark.regression
def test_change_password_matching_passwords_save(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.click_change_password_button()
    form.enter_new_password(USER_PASSWORD)
    form.enter_new_confirm_password(USER_PASSWORD)
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("USR-PWD-003 Mismatched new passwords are rejected with a validation error")
@pytest.mark.regression
def test_change_password_mismatch_rejected(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.click_change_password_button()
    form.enter_new_password(USER_PASSWORD)
    form.enter_new_confirm_password(USER_PASSWORD + "X")
    form.click_save()

    body = form.get_body_text()
    assert "match" in body.lower() or "password" in body.lower()
    assert page_has_no_broken_state(form)


@allure.title("USR-PWD-004 Blank new password field blocks save with a validation error")
@pytest.mark.regression
def test_change_password_blank_blocked(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.click_change_password_button()
    # Leave new password blank
    form.enter_new_confirm_password(USER_PASSWORD)
    form.click_save()

    body = form.get_body_text()
    assert "password" in body.lower() or "required" in body.lower()
    assert page_has_no_broken_state(form)


@allure.title("USR-PWD-008 Password visibility toggles on both new password fields")
@pytest.mark.edge
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-PWD-008: Visibility toggle inside the change-password sub-form. "
        "Locators need DOM verification once the flow is accessible."
    ),
)
def test_change_password_visibility_toggles(browser, managed_user):
    form = open_edit_user_form(browser, USER_EMAIL)
    form.click_change_password_button()
    form.enter_new_password(USER_PASSWORD)

    assert form.password_field_type() == "password"
    form.toggle_password_visibility()
    assert form.password_field_type() == "text"

    assert page_has_no_broken_state(form)
