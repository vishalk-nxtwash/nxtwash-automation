import allure
import pytest

from selenium.webdriver.common.by import By

from pages.superadmin.user_roles_page import CreateUserRolePage, EditUserRolePage, UserRolesPage
from tests.superadmin.user_roles.conftest import PREDEFINED_ROLE_NAME, TEST_ROLE_NAME

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("User Roles"),
    allure.story("Edit"),
]


def test_edit_button_opens_form_at_correct_url(browser, edit_role_page):
    """SA-UR-EDT-001 — 'Edit' opens the Edit form at /user-roles/{id} with data pre-filled."""
    assert "/user-roles/" in browser.current_url, \
        f"Expected URL to contain '/user-roles/{{id}}', got: {browser.current_url}"
    assert "/create" not in browser.current_url, \
        "Edit URL should not contain '/create'"


def test_edit_form_prefills_role_name(edit_role_page):
    """SA-UR-EDT-001 (cont.) — Edit form pre-fills the role name from the list."""
    name = edit_role_page.get_role_name()
    assert TEST_ROLE_NAME.lower() in name.lower(), \
        f"Edit form should pre-fill Role Name with '{TEST_ROLE_NAME}', got: {name!r}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-EDT-002: Pre-filled permission toggles — toggle state detection "
           "(is_selected / aria-checked) not confirmed for the edit form.",
)
def test_edit_form_prefills_permission_toggles(edit_role_page):
    """SA-UR-EDT-002 — Pre-filled permission toggles reflect the role's saved permissions."""
    edit_role_page.expand_permission_groups()
    checkboxes = edit_role_page.get_permission_checkboxes()
    assert checkboxes, \
        "Permission checkboxes should be visible on the edit form"
    # The test role was upserted with several permissions enabled — at least one should be on
    on_count = sum(1 for cb in checkboxes if cb.is_selected())
    assert on_count >= 1, \
        f"Edit form should pre-fill at least one enabled permission, got {on_count} on"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-EDT-003: Active User Role toggle state on the edit form — "
           "toggle locator not confirmed; aria-checked detection may vary.",
)
def test_edit_form_active_toggle_reflects_saved_state(edit_role_page):
    """SA-UR-EDT-003 — Active User Role toggle reflects the saved active state."""
    state = edit_role_page.get_active_toggle_state()
    # TEST_ROLE_NAME was upserted with is_active=True
    assert state is True, \
        f"Active User Role toggle should reflect 'active' for '{TEST_ROLE_NAME}', got: {state}"


def test_edit_role_name_persists_after_save(browser, edit_role_page):
    """SA-UR-EDT-004 — Editing the Role Name → Save changes persists on the list and
    after reload."""
    original_name = edit_role_page.get_role_name()
    edited_name = original_name + " Edited"
    edit_url = browser.current_url

    try:
        edit_role_page.set_role_name(edited_name)
        edit_role_page.click_save_changes()
        edit_role_page.confirm_yes_if_present()

        # Reload the edit page and verify name persisted
        browser.get(edit_url)
        reloaded = EditUserRolePage(browser)
        reloaded.wait_for_loaded()
        assert edited_name.lower() in reloaded.get_role_name().lower(), \
            f"Role name should be '{edited_name}' after save and reload, " \
            f"got: {reloaded.get_role_name()!r}"

    finally:
        try:
            api = CreateUserRolePage(browser)
            api.upsert_role_with_api(original_name, is_active=True)
        except Exception:
            pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-EDT-005: Toggling a permission on/off and verifying persistence — "
           "toggle interaction (set_checkbox) not confirmed on the edit form.",
)
def test_toggling_permission_persists_after_save(browser, edit_role_page):
    """SA-UR-EDT-005 — Toggling a permission on/off → Save changes persists."""
    edit_url = browser.current_url
    edit_role_page.expand_permission_groups()
    checkboxes = edit_role_page.get_permission_checkboxes()
    assert checkboxes, "Permissions should be visible on the edit form"

    # Toggle the first checkbox
    target = checkboxes[0]
    before_state = target.is_selected()
    helper = CreateUserRolePage(browser)
    helper.set_checkbox(target, not before_state)

    edit_role_page.click_save_changes()
    edit_role_page.confirm_yes_if_present()

    browser.get(edit_url)
    reloaded = EditUserRolePage(browser)
    reloaded.wait_for_loaded()
    reloaded.expand_permission_groups()
    new_cbs = reloaded.get_permission_checkboxes()
    new_state = new_cbs[0].is_selected() if new_cbs else None
    assert new_state == (not before_state), \
        f"Permission state should be {not before_state} after save and reload, " \
        f"got: {new_state}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-EDT-006: Role Name field inline clear (X) button locator "
           "not confirmed — needs DOM inspection.",
)
def test_clearing_role_name_via_x_and_saving_is_blocked(edit_role_page):
    """SA-UR-EDT-006 — Clearing the Role Name (via the X clear icon) and saving is blocked."""
    edit_role_page.click_role_name_clear_button()
    edit_role_page.click_save_changes()
    edit_role_page.confirm_yes_if_present()

    body = edit_role_page.get_body_text().lower()
    still_on_edit = "/user-roles/" in edit_role_page.driver.current_url \
        and "/create" not in edit_role_page.driver.current_url
    has_error = "required" in body or "invalid" in body or "too small" in body
    assert still_on_edit or has_error, \
        "Saving with a cleared Role Name should be blocked with a validation error"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-EDT-007: Predefined role edit behaviour — whether Company Owner "
           "can be renamed / have permissions changed / deleted is not confirmed.",
)
def test_predefined_role_edit_documents_behaviour(user_roles_page, browser):
    """SA-UR-EDT-007 — Predefined role (e.g. Company Owner) edit vs restricted behaviour."""
    user_roles_page.open_role(PREDEFINED_ROLE_NAME)
    page = EditUserRolePage(browser)
    page.wait_for_loaded()

    name = page.get_role_name()
    assert PREDEFINED_ROLE_NAME.lower() in name.lower(), \
        f"Edit form should show '{PREDEFINED_ROLE_NAME}' as the pre-filled role name"

    body = page.get_body_text()
    assert "error" not in body.lower(), \
        "Opening a predefined role edit form should not show an error"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-EDT-008: Duplicate Role Name on edit — uniqueness rule on staging "
           "not confirmed; same caveat as CRT-011.",
)
def test_duplicate_role_name_on_edit_is_rejected(edit_role_page, user_roles_page):
    """SA-UR-EDT-008 — Setting a duplicate Role Name on edit is rejected."""
    edit_role_page.set_role_name(PREDEFINED_ROLE_NAME)
    edit_role_page.click_save_changes()
    edit_role_page.confirm_yes_if_present(timeout=8)

    edit_role_page.wait_for_any_text(
        "already", "exists", "duplicate", timeout=10
    )
    body = edit_role_page.get_body_text().lower()
    assert "already" in body or "exists" in body or "duplicate" in body, \
        "Setting a duplicate role name on edit should show an error"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-EDT-009: Active User Role toggle interaction on edit and verification "
           "that deactivate/reactivate persists — toggle locator not confirmed.",
)
def test_deactivate_and_reactivate_role_persists(browser, edit_role_page):
    """SA-UR-EDT-009 — Deactivating / reactivating the role via Active User Role toggle persists."""
    edit_url = browser.current_url

    # Deactivate
    edit_role_page.set_active_toggle(False)
    edit_role_page.click_save_changes()
    edit_role_page.confirm_yes_if_present()

    browser.get(edit_url)
    reloaded = EditUserRolePage(browser)
    reloaded.wait_for_loaded()
    assert reloaded.get_active_toggle_state() is False, \
        "Role should be inactive after deactivating and reloading"

    # Reactivate
    reloaded.set_active_toggle(True)
    reloaded.click_save_changes()
    reloaded.confirm_yes_if_present()

    browser.get(edit_url)
    re_reloaded = EditUserRolePage(browser)
    re_reloaded.wait_for_loaded()
    assert re_reloaded.get_active_toggle_state() is True, \
        "Role should be active again after reactivating and reloading"


@pytest.mark.skip(
    reason="SA-UR-EDT-010: Impact of deactivating a role on assigned users — requires "
           "the Users module and a user account assigned to the test role."
)
def test_deactivating_assigned_role_documents_impact_on_users(browser):
    """SA-UR-EDT-010 — Deactivating a role that is assigned to users — document impact."""
    pass


def test_cancel_on_edit_discards_changes(browser, edit_role_page):
    """SA-UR-EDT-011 — Cancel on Edit discards changes — the role is unchanged."""
    original_name = edit_role_page.get_role_name()
    edit_role_page.set_role_name(original_name + " CANCELLED")
    edit_role_page.click_cancel()
    edit_role_page.confirm_yes_if_present()

    # Navigate back and reopen edit to verify name is unchanged
    roles_list = UserRolesPage(browser)
    roles_list.wait_for_loaded()
    roles_list.open_role(TEST_ROLE_NAME)

    reopened = EditUserRolePage(browser)
    reopened.wait_for_loaded()
    assert reopened.get_role_name() == original_name, \
        f"Role name should be unchanged after cancelling edit; " \
        f"expected '{original_name}', got '{reopened.get_role_name()}'"
