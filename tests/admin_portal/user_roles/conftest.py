import uuid

import pytest

from pages.admin_portal.user_roles_page import AdminUserRoleFormPage, AdminUserRolesPage
from tests.admin_portal.admin_session import open_admin_path


# ── Test data constants ───────────────────────────────────────────────────────

ROLE_NAME = "VK UR01"
ROLE_PRIORITY = "5"
UPDATED_ROLE_NAME = "VK UR01 edited"
UPDATED_ROLE_PRIORITY = "8"

# A default role expected to exist in every environment after initial seeding.
DEFAULT_ROLE_NAME = "Admin Portal User"

# Site used for location-assignment tests — must exist in staging.
ASSIGNMENT_SITE = "VK AL11"

NONEXISTENT_ROLE = "role-does-not-exist-automation"

BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


# ── Navigation helpers ────────────────────────────────────────────────────────

def open_user_roles_page(browser):
    open_admin_path(browser, "/users/userRoles")
    page = AdminUserRolesPage(browser)
    page.wait_for_loaded()
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
    # Try to open via edit (searches active + inactive lists via open_edit_role fallback).
    # Only create when the role truly doesn't exist in either list.
    try:
        form = open_edit_role_form(browser, role_name)
        form.enter_role_name(role_name)
        form.enter_priority(priority)
        form.ensure_active_switch_on()
        form.click_save()
        return open_user_roles_page(browser)
    except Exception:
        pass

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
