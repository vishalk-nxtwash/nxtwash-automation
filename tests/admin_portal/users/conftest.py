import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.users_page import AdminUserFormPage, AdminUsersPage
from tests.admin_portal.admin_session import open_admin_path


# ── Test data constants  (values managed in test_data/users.json) ─────────────

from tests.admin_portal._data import load as _load

_D = _load("users")

USER_EMAIL      = _D["template"]["email"]
USER_PHONE      = _D["template"]["phone"]
USER_PASSWORD   = _D["template"]["password"]
EMPLOYEE_NAME   = _D["template"]["employee_name"]
USER_ROLE       = _D["template"]["role"]
USER_FIRST_NAME = _D["template"]["first_name"]
USER_LAST_NAME  = _D["template"]["last_name"]
EMPLOYEE_CODE   = _D["template"]["employee_code"]

UPDATED_EMAIL   = _D["updated"]["email"]
UPDATED_PHONE   = _D["updated"]["phone"]
UPDATED_ROLE    = _D["updated"]["role"]

ASSIGNMENT_SITE   = _D["template"]["assignment_site"]
NONEXISTENT_PHONE = _D["invalid"]["phone"]
INVALID_EMAIL     = _D["invalid"]["email"]

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
    # Open a fresh list page — active-only filter is ON by default after navigation.
    page = open_users_page(browser)

    # Build a combined filter: active=OFF + email match, so we find the user
    # regardless of whether a prior test left them inactive.
    page.open_filter_panel()
    switch = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located(AdminUsersPage.ACTIVE_FILTER_SWITCH)
    )
    if switch.get_attribute("aria-checked") == "true":
        try:
            switch.click()
        except Exception:  # noqa: BLE001
            browser.execute_script("arguments[0].click();", switch)
    page._enter_filter_field(AdminUsersPage.FILTER_EMAIL, email)
    page.apply_filters()
    # Grid now shows 0 or 1 rows: users (active or inactive) matching the email.

    try:
        page.wait_for_user_row(email)
        visible_links = [
            lnk for lnk in page.driver.find_elements(*AdminUsersPage._EDIT_LINK)
            if lnk.is_displayed()
        ]
        if not visible_links:
            raise TimeoutException("No edit links visible for: %s" % email)
        page.driver.execute_script("arguments[0].click();", visible_links[0])
        page.driver.switch_to.default_content()

        form = AdminUserFormPage(browser)
        form.wait_for_edit_loaded()
        form.enter_email(email)
        form.enter_phone(phone)
        form.select_role(role)
        form.ensure_active_switch_on()
        form.click_save()
        return open_users_page(browser)
    except Exception:  # noqa: BLE001
        pass  # user not found — fall through to create

    # User does not exist — create it.
    page = open_users_page(browser)
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
    try:
        create_user_if_missing(browser)
    except Exception as exc:  # noqa: BLE001
        import logging
        logging.getLogger("nxtwash").warning(
            "managed_user teardown could not restore user baseline: %s", exc
        )
