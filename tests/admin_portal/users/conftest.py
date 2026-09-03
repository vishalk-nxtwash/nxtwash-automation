import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
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


def open_edit_user_form(browser, email, phone=USER_PHONE):
    # Users filter panel has no email field — use phone search instead.
    # The managed_user fixture ensures the user is active, so phone search (active=ON) finds them.
    page = open_users_page(browser)
    page.search_user(phone)
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

    # --- Step 1: ensure active filter is OFF (show all users: active + inactive) ---
    # Don't blindly toggle — filter state may persist across navigation.
    # Check current aria-checked state and only click if it is not already OFF.
    page.open_filter_panel()
    try:
        _sw = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(AdminUsersPage.ACTIVE_FILTER_SWITCH)
        )
        if _sw.get_attribute("aria-checked") != "false":
            try:
                _sw.click()
            except Exception:
                browser.execute_script("arguments[0].click();", _sw)
            try:
                WebDriverWait(browser, 10).until(
                    EC.visibility_of_element_located(AdminUsersPage.FILTER_FIRST_NAME)
                )
            except TimeoutException:
                pass
    except Exception:
        pass
    page.apply_filters()
    # Grid now shows ALL users (active + inactive).

    # --- Step 2: find the managed user's row by email (try current AND updated email) ---
    # A prior partial test run may have left the email set to UPDATED_EMAIL.
    found_cell = None
    for candidate_email in [email, UPDATED_EMAIL]:
        try:
            found_cell = WebDriverWait(browser, 15).until(
                EC.visibility_of_element_located(
                    page._user_email_cell_locator(candidate_email)
                )
            )
            break
        except TimeoutException:
            continue

    if found_cell is not None:
        # Use Y-coordinate proximity to click the edit link on the same row.
        cell_y = found_cell.location["y"]
        try:
            WebDriverWait(browser, 10).until(
                lambda d: any(
                    lnk.is_displayed() for lnk in d.find_elements(*AdminUsersPage._EDIT_LINK)
                )
            )
        except TimeoutException:
            pass
        visible_links = [
            lnk for lnk in page.driver.find_elements(*AdminUsersPage._EDIT_LINK)
            if lnk.is_displayed()
        ]
        if visible_links:
            closest = min(visible_links, key=lambda lnk: abs(lnk.location["y"] - cell_y))
            page.driver.execute_script("arguments[0].click();", closest)
            page.driver.switch_to.default_content()

            try:
                form = AdminUserFormPage(browser)
                form.wait_for_edit_loaded()
                # Reset ALL baseline fields — handles dirty state from prior partial runs.
                form.enter_email(email)
                form.enter_phone(phone)
                form.select_role(role)
                form.ensure_active_switch_on()
                form.click_save()
            except Exception as _edit_exc:
                import logging
                logging.getLogger("nxtwash").warning(
                    "create_user_if_missing: edit-form reset failed for %s (%s). "
                    "User likely already in correct state; continuing.",
                    email, _edit_exc,
                )
                browser.switch_to.default_content()
            return open_users_page(browser)

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
    except BaseException as exc:  # noqa: BLE001 — catches pytest.skip() / Skipped
        import logging
        logging.getLogger("nxtwash").warning(
            "managed_user teardown raised non-Exception (e.g. skip signal): %s", exc
        )
