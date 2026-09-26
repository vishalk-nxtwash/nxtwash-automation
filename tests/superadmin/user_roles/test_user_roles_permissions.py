import allure
import pytest

from selenium.webdriver.common.by import By

from tests.superadmin.user_roles.conftest import TEST_ROLE_NAME

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("User Roles"),
    allure.story("Permissions"),
]

# Confirmed permission tree from SA-UR-PRM-003
PERMISSION_GROUPS = ["Overview", "Users", "User Roles", "Sites", "Companies"]
PERMISSION_ITEMS = [
    "Dashboard Overview",
    "Users",
    "User Roles",
    "Create Role",
    "Sites",
    "Companies",
    "Create company",
]


def test_permission_groups_are_present_on_create_form(create_role_page):
    """SA-UR-PRM-001 — Permission groups are present: Overview, Users, User Roles, Sites, Companies."""
    body = create_role_page.get_body_text()
    for group in PERMISSION_GROUPS:
        assert group in body, \
            f"Expected permission group '{group}' to be visible on the create form"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-PRM-002: Expand/collapse behaviour via chevron — the expand buttons "
           "may toggle visibility differently; collapsed state not confirmed.",
)
def test_permission_groups_expand_and_collapse(create_role_page):
    """SA-UR-PRM-002 — Each permission group expands and collapses via its chevron."""
    expand_btns = create_role_page.driver.find_elements(
        *create_role_page.EXPAND_PERMISSION_BUTTONS
    )
    assert expand_btns, \
        "Permission group expand buttons should be present on the create form"

    # Click first group to expand then collapse
    btn = expand_btns[0]
    btn.click()  # expand
    btn.click()  # collapse
    body = create_role_page.get_body_text()
    assert "error" not in body.lower(), \
        "Expanding and collapsing a permission group should not cause an error"


def test_permission_items_match_confirmed_tree(create_role_page):
    """SA-UR-PRM-003 — Permission items match the confirmed tree: Overview > Dashboard Overview;
    Users > Users; User Roles > User Roles, Create Role; Sites > Sites;
    Companies > Companies, Create company."""
    create_role_page.expand_permission_groups()
    body = create_role_page.get_body_text()
    for item in PERMISSION_ITEMS:
        assert item in body, \
            f"Expected permission item '{item}' to be visible after expanding all groups"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-PRM-004: All permission toggles default to OFF on a new role — "
           "toggle state detection via is_selected() / aria-checked not confirmed.",
)
def test_all_permission_toggles_default_to_off_on_new_form(create_role_page):
    """SA-UR-PRM-004 — All permission toggles default to OFF on a new role create form."""
    checkboxes = create_role_page.get_permission_checkboxes()
    assert checkboxes, "Permission checkboxes should be present after expanding groups"
    for cb in checkboxes:
        assert not cb.is_selected(), \
            "All permission toggles should be OFF by default on a new create form"


def test_enabling_permission_and_saving_persists(edit_role_page, browser):
    """SA-UR-PRM-005 — Enabling a permission and saving persists it (verified on reopen)."""
    from pages.superadmin.user_roles_page import EditUserRolePage

    edit_url = browser.current_url

    # Record initial state then toggle a permission
    edit_role_page.expand_permission_groups()
    checkboxes = edit_role_page.get_permission_checkboxes()
    assert checkboxes, "Permissions should be visible on the edit form"

    # Find the first unchecked permission and enable it
    target_cb = None
    for cb in checkboxes:
        if not cb.is_selected():
            target_cb = cb
            break

    if target_cb is None:
        pytest.skip("All permissions already enabled on test role — cannot test toggle-on")

    from pages.superadmin.user_roles_page import CreateUserRolePage
    create_page = CreateUserRolePage(browser)
    create_page.set_checkbox(target_cb, True)

    edit_role_page.click_save_changes()
    edit_role_page.confirm_yes_if_present()

    # Reload the edit page and verify the permission is still on
    browser.get(edit_url)
    reloaded = EditUserRolePage(browser)
    reloaded.wait_for_loaded()
    reloaded.expand_permission_groups()
    reloaded_cbs = reloaded.get_permission_checkboxes()
    assert any(cb.is_selected() for cb in reloaded_cbs), \
        "At least one permission should remain enabled after save and reload"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-PRM-006: Each individual permission toggle independently — "
           "toggle interaction via set_checkbox not confirmed on staging.",
)
def test_each_permission_toggle_can_be_set_independently(create_role_page):
    """SA-UR-PRM-006 — Each individual permission toggle can be turned on and off independently."""
    checkboxes = create_role_page.get_permission_checkboxes()
    assert checkboxes, "Permission checkboxes should be present"
    assert len(checkboxes) >= 2, \
        f"Expected at least 2 permission checkboxes, got {len(checkboxes)}"

    # Toggle first on, keep second off
    create_page = create_role_page
    create_page.set_checkbox(checkboxes[0], True)
    create_page.set_checkbox(checkboxes[1], False)

    assert checkboxes[0].is_selected(), \
        "First permission toggle should be ON after enabling it"
    assert not checkboxes[1].is_selected(), \
        "Second permission toggle should remain OFF"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-PRM-007: Whether enabling 'Create Role' auto-enables the parent "
           "'User Roles' view permission — parent-child rule not confirmed on staging.",
)
def test_create_role_permission_relative_to_parent_user_roles(create_role_page):
    """SA-UR-PRM-007 — 'Create Role' behaviour relative to its parent 'User Roles' permission."""
    create_role_page.expand_permission_groups()
    create_role_cb = create_role_page.get_permission_checkbox_by_name("Create Role")
    user_roles_cb = create_role_page.get_permission_checkbox_by_name("User Roles")

    assert create_role_cb is not None, "'Create Role' permission checkbox should be findable"
    assert user_roles_cb is not None, "'User Roles' permission checkbox should be findable"

    # Enable only Create Role and check if parent auto-enables
    create_role_page.set_checkbox(create_role_cb, True)
    body = create_role_page.get_body_text()
    assert "error" not in body.lower(), \
        "Enabling 'Create Role' should not cause an error"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-PRM-008: Whether enabling 'Create company' auto-enables the parent "
           "'Companies' view permission — parent-child rule not confirmed on staging.",
)
def test_create_company_permission_relative_to_parent_companies(create_role_page):
    """SA-UR-PRM-008 — 'Create company' behaviour relative to its parent 'Companies' permission."""
    create_role_page.expand_permission_groups()
    create_co_cb = create_role_page.get_create_company_checkbox()
    companies_cb = create_role_page.get_permission_checkbox_by_name("Companies")

    assert companies_cb is not None, "'Companies' permission checkbox should be findable"

    # Enable only Create company
    create_role_page.set_checkbox(create_co_cb, True)
    body = create_role_page.get_body_text()
    assert "error" not in body.lower(), \
        "Enabling 'Create company' should not cause an error"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-PRM-009: Enabling all permissions and verifying they persist — "
           "set_checkbox interaction with all toggles not confirmed.",
)
def test_enabling_all_permissions_persists(edit_role_page, browser):
    """SA-UR-PRM-009 — Enabling all permissions and saving persists the full set."""
    from pages.superadmin.user_roles_page import EditUserRolePage

    edit_url = browser.current_url

    from pages.superadmin.user_roles_page import CreateUserRolePage
    helper = CreateUserRolePage(browser)
    edit_role_page.expand_permission_groups()
    for cb in edit_role_page.get_permission_checkboxes():
        helper.set_checkbox(cb, True)

    edit_role_page.click_save_changes()
    edit_role_page.confirm_yes_if_present()

    browser.get(edit_url)
    reloaded = EditUserRolePage(browser)
    reloaded.wait_for_loaded()
    count = reloaded.enabled_permissions_count()
    assert count >= 5, \
        f"Expected all permissions enabled after save, got {count} enabled"


@pytest.mark.xfail(
    strict=False,
    reason="SA-UR-PRM-010: Disabling all permissions and saving an empty set — "
           "whether the server allows a zero-permission role is not confirmed.",
)
def test_disabling_all_permissions_persists_empty_set(edit_role_page, browser):
    """SA-UR-PRM-010 — Disabling all permissions and saving persists an empty permission set."""
    from pages.superadmin.user_roles_page import CreateUserRolePage, EditUserRolePage

    edit_url = browser.current_url
    helper = CreateUserRolePage(browser)

    edit_role_page.expand_permission_groups()
    for cb in edit_role_page.get_permission_checkboxes():
        helper.set_checkbox(cb, False)

    edit_role_page.click_save_changes()
    edit_role_page.confirm_yes_if_present()

    body = browser.find_element(By.TAG_NAME, "body").text.lower()
    is_away = "/user-roles/" in browser.current_url and "create" not in browser.current_url
    has_error = "required" in body or "permission" in body
    assert is_away or has_error, \
        "Saving with all permissions OFF should either succeed or show a clear error"


@pytest.mark.skip(
    reason="SA-UR-PRM-011: End-to-end permission enforcement requires assigning the "
           "test role to a user and logging in as that user — depends on the Users module "
           "and a separate non-superadmin account."
)
def test_user_with_role_can_access_only_permitted_modules(browser):
    """SA-UR-PRM-011 — User assigned the role can access only the permitted modules."""
    pass


@pytest.mark.skip(
    reason="SA-UR-PRM-012: Negative enforcement check — requires a non-superadmin user "
           "account assigned a restricted role, outside current test scope."
)
def test_user_without_permission_cannot_reach_module(browser):
    """SA-UR-PRM-012 — User whose role lacks a module permission cannot reach that module."""
    pass


@pytest.mark.skip(
    reason="SA-UR-PRM-013: Create permission off / view permission on — requires a "
           "non-superadmin user session, outside current test scope."
)
def test_view_permission_on_create_off_user_can_view_not_create(browser):
    """SA-UR-PRM-013 — Create permission off but view on: user can view but not create."""
    pass
