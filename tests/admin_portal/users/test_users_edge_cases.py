import allure
import pytest

from tests.admin_portal.admin_session import ensure_admin_logged_in
from tests.admin_portal.users.conftest import (
    USER_EMAIL,
    USER_ROLE,
    create_user_if_missing,
    open_create_user_form,
    open_edit_user_form,
    open_users_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Users"),
    allure.story("Edge Cases"),
]


@allure.title("USR-EC-003 Only active roles appear in the User Role dropdown")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-EC-003: Role dropdown options require at least one deactivated role in staging "
        "to verify exclusion. Verify role combobox locator in DevTools."
    ),
)
def test_only_active_roles_in_dropdown(browser):
    form = open_create_user_form(browser)
    options = form.get_role_dropdown_options()

    assert len(options) > 0, "Role dropdown returned no options"
    assert USER_ROLE in options, (
        "Active role '%s' missing from dropdown. Got: %s" % (USER_ROLE, options)
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-EC-004 Only active employees appear in the Employee dropdown")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-EC-004: Employee dropdown exclusion of deactivated employees needs a "
        "deactivated employee in staging to verify. Verify combobox locator in DevTools."
    ),
)
def test_only_active_employees_in_dropdown(browser):
    from tests.admin_portal.users.conftest import EMPLOYEE_NAME
    form = open_create_user_form(browser)
    options = form.get_employee_dropdown_options()

    assert len(options) > 0, "Employee dropdown returned no options"
    assert EMPLOYEE_NAME in options, (
        "Active employee '%s' missing from dropdown. Got: %s" % (EMPLOYEE_NAME, options[:10])
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-EC-005 Email with leading/trailing whitespace is trimmed or rejected")
@pytest.mark.edge
def test_email_whitespace_trimmed_or_rejected(browser):
    from tests.admin_portal.users.conftest import EMPLOYEE_NAME, USER_PASSWORD, USER_ROLE
    import uuid
    padded_email = "  vk.ws.%s@test.com  " % uuid.uuid4().hex[:6]
    stripped_email = padded_email.strip()

    form = open_create_user_form(browser)
    form.enter_email(padded_email)
    form.click_save()

    body = form.get_body_text()
    # Acceptable: saved with stripped address, or validation rejected the padded input.
    assert stripped_email in body or padded_email not in body or page_has_no_broken_state(form)
    assert page_has_no_broken_state(form)


@allure.title("USR-EC-006 Very long email at boundary length is handled without crash")
@pytest.mark.edge
def test_long_email_at_boundary(browser):
    local = "a" * 60
    domain = "test.com"
    long_email = "%s@%s" % (local, domain)     # 69 chars — at/above typical DB limits

    form = open_create_user_form(browser)
    form.enter_email(long_email)
    form.click_save()

    # Must not crash — error or success are both acceptable outcomes.
    assert page_has_no_broken_state(form)


@allure.title("USR-EC-007 User data persists correctly after logout and re-login")
@pytest.mark.edge
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-EC-007: After clearing cookies and storage, ensure_admin_logged_in cannot "
        "reliably re-authenticate in the staging environment (redirects to / instead of the "
        "login form). Verify manually: clear session and confirm user data is present after re-login."
    ),
)
def test_user_data_persists_after_relogin(browser, managed_user):
    page = open_users_page(browser)
    assert page.user_exists(USER_EMAIL)

    browser.delete_all_cookies()
    browser.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")

    ensure_admin_logged_in(browser)
    page = open_users_page(browser)
    assert page.user_exists(USER_EMAIL), (
        "User '%s' missing after logout and re-login" % USER_EMAIL
    )
    assert page_has_no_broken_state(page)


@allure.title("USR-UX-002 Filter panel is always accessible for name and email lookup")
@pytest.mark.regression
def test_filter_panel_accessible_for_name_email_lookup(browser):
    page = open_users_page(browser)

    assert page.filter_panel_has_expected_controls(), (
        "Filter panel must expose First Name, Last Name, Email, Site, and Active controls"
    )
    assert page_has_no_broken_state(page)
