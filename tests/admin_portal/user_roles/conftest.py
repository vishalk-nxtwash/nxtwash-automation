import uuid

import pytest

from pages.admin_portal.user_roles_page import AdminUserRoleFormPage, AdminUserRolesPage
from tests.admin_portal.admin_session import ensure_admin_logged_in, open_admin_path


# ── Test data constants  (values managed in test_data/user_roles.json) ────────

from tests.admin_portal._data import load as _load

_D = _load("user_roles")

ROLE_NAME             = _D["template"]["role_name"]
ROLE_PRIORITY         = _D["template"]["priority"]
UPDATED_ROLE_NAME     = _D["updated"]["role_name"]
UPDATED_ROLE_PRIORITY = _D["updated"]["priority"]
DEFAULT_ROLE_NAME     = _D["reference"]["default_role"]
DEFAULT_ROLE_NAMES    = _D["reference"]["predefined_roles"]
ASSIGNMENT_SITE       = _D["reference"]["assignment_site"]

NONEXISTENT_ROLE = _D["search"]["nonexistent"]

BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


# ── Internal helpers ──────────────────────────────────────────────────────────

def _clear_filter_storage(browser):
    """Remove userRoles entry from the persisted Redux filter state."""
    try:
        browser.execute_script("""
            try {
                var root = JSON.parse(localStorage.getItem('persist:root') || '{}');
                var tfr = JSON.parse(root.tableFilterReducer || '{}');
                var tf = tfr.tableFilters || {};
                delete tf.userRoles;
                tfr.tableFilters = tf;
                root.tableFilterReducer = JSON.stringify(tfr);
                localStorage.setItem('persist:root', JSON.stringify(root));
            } catch(e) {}
        """)
    except Exception:
        pass


def _recover_session(browser):
    """Clear auth state and re-login to escape the staging post-create broken state.

    Staging's create-role endpoint sometimes leaves the server session in an error
    state.  A full cookie + storage reset followed by a fresh login gets a clean
    session so subsequent navigations work normally.
    """
    browser.delete_all_cookies()
    try:
        browser.execute_script(
            "try{window.localStorage.clear();window.sessionStorage.clear();}catch(e){}"
        )
    except Exception:
        pass
    ensure_admin_logged_in(browser)


# ── Navigation helpers ────────────────────────────────────────────────────────

def open_user_roles_page(browser):
    _clear_filter_storage(browser)
    open_admin_path(browser, "/users/userRoles")
    page = AdminUserRolesPage(browser)
    try:
        # Use a shorter frame timeout on the first attempt so recovery triggers
        # quickly when staging is in a broken state after a create-form submission.
        page.wait_for_loaded(frame_timeout=60)
    except Exception:
        # Staging sometimes enters a broken state (LIST_FRAME never loads) after
        # the create-role form is submitted.  A full session reset fixes it.
        _recover_session(browser)
        _clear_filter_storage(browser)
        open_admin_path(browser, "/users/userRoles")
        page = AdminUserRolesPage(browser)
        page.wait_for_loaded()
    page.clear_active_filters()
    return page


def open_create_role_form(browser):
    page = open_user_roles_page(browser)
    page.click_add_role()
    form = AdminUserRoleFormPage(browser)
    form.wait_for_create_loaded()
    return form


def open_edit_role_form(browser, role_name):
    page = open_user_roles_page(browser)
    page.open_edit_role(role_name)
    form = AdminUserRoleFormPage(browser)
    form.wait_for_edit_loaded()
    return form


def page_has_no_broken_state(page):
    body = page.get_body_text()
    return not any(text in body for text in BROKEN_STATE_TEXTS)


# ── Role upsert helper ────────────────────────────────────────────────────────

def create_role_if_missing(browser, role_name=ROLE_NAME, priority=ROLE_PRIORITY):
    # Fast path: role visible in active list — return immediately without any save.
    try:
        page = open_user_roles_page(browser)
        if page.role_exists(role_name) and page.get_role_status(role_name) == "Active":
            return page
    except Exception:
        pass

    # Role absent or hidden by active filter — try the edit form (searches inactive too).
    try:
        form = open_edit_role_form(browser, role_name)
        needs_save = (
            not form.active_switch_is_on()
            or str(form.get_priority_value()) != str(priority)
        )
        if not needs_save:
            # Already correct — cancel without triggering the create endpoint.
            form.click_cancel()
            return open_user_roles_page(browser)
        form.enter_priority(priority)
        form.ensure_active_switch_on()
        form.click_save()
        # open_user_roles_page has recovery for the broken state that edit saves can cause.
        return open_user_roles_page(browser)
    except Exception:
        pass

    # Role truly doesn't exist — create it.
    # The create endpoint sometimes breaks staging; open_user_roles_page recovers.
    form = open_create_role_form(browser)
    form.enter_role_name(role_name)
    form.enter_priority(priority)
    form.ensure_active_switch_on()
    form.click_save()
    return open_user_roles_page(browser)


def make_unique_role_name():
    return "VK UR tmp %s" % uuid.uuid4().hex[:6]


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def managed_role(browser):
    """Ensure ROLE_NAME exists with baseline settings before the test; restore after."""
    page = create_role_if_missing(browser)
    yield page
    create_role_if_missing(browser)
