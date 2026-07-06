import pytest

from pages.admin_portal.users_page import AdminUserFormPage, AdminUsersPage
from tests.admin_portal.admin_session import open_admin_path


# ── Test data constants ───────────────────────────────────────────────────────

# Core managed user used by fixtures. All values must exist / be creatable in staging.
USER_EMAIL = "vkuser02@yopmail.com"
USER_PHONE = "1234567890"
USER_PASSWORD = "test"
# EMPLOYEE_NAME must match an active employee in the staging Employees module.
EMPLOYEE_NAME = "test user 2"
# USER_ROLE must be an active role visible in the User Role dropdown.
USER_ROLE = "VK UR01"

# First / last name come from the linked employee record (used in filter tests).
USER_FIRST_NAME = "test"
USER_LAST_NAME = "user 2"
EMPLOYEE_CODE = "1234"

UPDATED_EMAIL = "vkuser02.edited@yopmail.com"
UPDATED_PHONE = "1234567891"
UPDATED_ROLE = "VK UR01"

ASSIGNMENT_SITE = "VK AL11"
NONEXISTENT_PHONE = "0000000000"
INVALID_EMAIL = "not-an-email"

BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


# ── Navigation helpers ────────────────────────────────────────────────────────

def open_users_page(browser):
    open_admin_path(browser, "/users/users")
    page = AdminUsersPage(browser)
    page.wait_for_loaded()
    return page


def open_create_user_form(browser):
    page = open_users_page(browser)
    page.click_add_user()
    form = AdminUserFormPage(browser)
    form.wait_for_create_loaded()
    return form


def open_edit_user_form(browser, email):
    page = open_users_page(browser)
    page.search_user_by_email(email)   # narrows grid to this user
    page.open_edit_user(email)
    form = AdminUserFormPage(browser)
    form.wait_for_edit_loaded()
    return form


def page_has_no_broken_state(page):
    body = page.get_body_text()
    return not any(text in body for text in BROKEN_STATE_TEXTS)


# ── User upsert helper ────────────────────────────────────────────────────────

def create_user_if_missing(
    browser,
    email=USER_EMAIL,
    phone=USER_PHONE,
    password=USER_PASSWORD,
    employee_name=EMPLOYEE_NAME,
    role=USER_ROLE,
):
    page = open_users_page(browser)

    if page.user_exists(email):
        # User is active — reset to known baseline via edit
        form = open_edit_user_form(browser, email)
        form.enter_email(email)
        form.enter_phone(phone)
        form.select_role(role)
        form.ensure_active_switch_on()
        form.click_save()
        return open_users_page(browser)

    # User truly doesn't exist (or is inactive) — create it.
    form = open_create_user_form(browser)
    try:
        form.fill_create_form(employee_name, password, email, phone, role)
    except Exception as exc:  # noqa: BLE001
        raise pytest.skip(
            "Could not create test user — EMPLOYEE_NAME '%s' may not exist in staging. "
            "Verify the Employees module. Original error: %s" % (employee_name, exc)
        ) from exc
    form.click_save()
    return open_users_page(browser)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def managed_user(browser):
    """Ensure USER_EMAIL user exists at baseline before the test; restore after."""
    page = create_user_if_missing(browser)
    yield page
    create_user_if_missing(browser)
