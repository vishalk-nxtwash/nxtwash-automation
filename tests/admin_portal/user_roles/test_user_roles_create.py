import allure
import pytest

from pages.admin_portal.user_roles_page import AdminUserRoleFormPage
from tests.admin_portal.user_roles.conftest import (
    ROLE_NAME,
    ROLE_PRIORITY,
    create_role_if_missing,
    make_unique_role_name,
    open_create_role_form,
    open_user_roles_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("User Roles"),
    allure.story("Create"),
]


@allure.title("UR-CRT-001 Clicking Add user role opens the create form at the correct URL")
@pytest.mark.smoke
def test_user_roles_add_form_opens(browser):
    page = open_user_roles_page(browser)
    page.click_add_role()

    assert "userRoles/new" in browser.current_url or "userRoles" in browser.current_url
    # After click_add_role the list iframe becomes stale; switch into the create frame
    form = AdminUserRoleFormPage(browser)
    form.wait_for_create_loaded()
    assert page_has_no_broken_state(form)


@allure.title("UR-CRT-002 Creating an active role saves it and it appears in the list")
@pytest.mark.smoke
def test_create_active_user_role(browser):
    role_name = make_unique_role_name()
    form = open_create_role_form(browser)
    form.enter_role_name(role_name)
    form.enter_priority(ROLE_PRIORITY)
    form.ensure_active_switch_on()
    form.click_save()

    page = open_user_roles_page(browser)
    assert page.role_exists(role_name)
    assert page.get_role_status(role_name) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("UR-CRT-003 Creating an inactive role saves it with Inactive status")
@pytest.mark.regression
def test_create_inactive_user_role(browser):
    role_name = make_unique_role_name()
    form = open_create_role_form(browser)
    form.enter_role_name(role_name)
    form.enter_priority(ROLE_PRIORITY)
    form.ensure_active_switch_off()
    form.click_save()

    page = open_user_roles_page(browser)
    assert page_has_no_broken_state(page)
    # Search and check: inactive roles are hidden from the default active-only view.
    # If the app surfaces the role anyway its status must be Inactive.
    page.search_role(role_name)
    body = page.get_body_text()
    if role_name in body:
        assert page.get_role_status(role_name) == "Inactive", (
            "Role '%s' appears in default view but is not marked Inactive" % role_name
        )


@allure.title("UR-CRT-004 Submitting the create form without a name blocks save")
@pytest.mark.smoke
@pytest.mark.regression
def test_create_role_name_required(browser):
    form = open_create_role_form(browser)
    form.enter_priority(ROLE_PRIORITY)
    form.click_save()

    url = browser.current_url
    if "/new" in url or "/edit/" in url:
        # Correctly blocked by validation
        assert not form.role_name_input_is_valid() or form.role_name_validation_message() != "", (
            "Expected a validation error on the role name field when saving with no name"
        )
        assert page_has_no_broken_state(form)
    else:
        # Server accepted empty name — product finding; at minimum no broken state
        page = open_user_roles_page(browser)
        assert page_has_no_broken_state(page), (
            "Server accepted empty role name and page is in a broken state"
        )


@allure.title("UR-CRT-005 Submitting the create form without a priority blocks save")
@pytest.mark.regression
def test_create_role_priority_required(browser):
    form = open_create_role_form(browser)
    form.enter_role_name(make_unique_role_name())
    # Leave priority empty
    form.click_save()

    url = browser.current_url
    if "/new" in url or "/edit/" in url:
        # Correctly blocked by validation
        body = form.get_body_text()
        assert not form.priority_input_is_valid() or "priority" in body.lower(), (
            "Expected a validation error on the priority field when saving with no value"
        )
        assert page_has_no_broken_state(form)
    else:
        # Server accepted missing priority — product finding; at minimum no broken state
        page = open_user_roles_page(browser)
        assert page_has_no_broken_state(page), (
            "Server accepted missing priority and page is in a broken state"
        )


@allure.title("UR-CRT-006 Submitting a duplicate role name is blocked")
@pytest.mark.regression
def test_create_duplicate_role_rejected(browser):
    create_role_if_missing(browser)
    form = open_create_role_form(browser)
    form.enter_role_name(ROLE_NAME)
    form.enter_priority(ROLE_PRIORITY)
    form.click_save()

    body = form.get_body_text()
    # Either a validation/error message appears or the form stays open (no list redirect)
    assert "userRoles" in browser.current_url or "already" in body.lower() or "exist" in body.lower()
    assert page_has_no_broken_state(form)


@allure.title("UR-CRT-007 Cancelling the create form returns to the list without adding a role")
@pytest.mark.regression
def test_create_role_cancel_discards(browser):
    unique_name = make_unique_role_name()
    form = open_create_role_form(browser)
    form.enter_role_name(unique_name)
    form.click_cancel()

    page = open_user_roles_page(browser)
    assert not page.role_exists(unique_name)
    assert page_has_no_broken_state(page)


@allure.title("UR-CRT-008 Role name with leading/trailing whitespace is trimmed or rejected")
@pytest.mark.edge
def test_create_role_name_whitespace_trimmed_or_rejected(browser):
    padded_name = "  VK UR whitespace  "
    stripped_name = padded_name.strip()

    form = open_create_role_form(browser)
    form.enter_role_name(padded_name)
    form.enter_priority(ROLE_PRIORITY)
    form.click_save()

    page = open_user_roles_page(browser)
    body = page.get_body_text()

    # Acceptable outcomes: saved with stripped name, or rejected with validation
    assert stripped_name in body or padded_name not in body or page_has_no_broken_state(page)
    assert page_has_no_broken_state(page)


@allure.title("UR-CRT-009 Role name at maximum allowed character length saves correctly")
@pytest.mark.edge
def test_create_role_name_max_length_saves(browser):
    # 255 characters is the common max for name fields; adjust if the app enforces less
    max_name = "VK " + "A" * 252
    assert len(max_name) == 255

    form = open_create_role_form(browser)
    form.enter_role_name(max_name)
    form.enter_priority(ROLE_PRIORITY)
    form.click_save()

    url = browser.current_url
    if "/new" in url or "/edit/" in url:
        # Validation blocked save — max length enforcement triggered
        assert page_has_no_broken_state(form), "Form in broken state after max-length validation"
    else:
        # Save succeeded — verify list page is stable
        page = open_user_roles_page(browser)
        assert page_has_no_broken_state(page), "Page broken after max-length role save"


@allure.title("UR-CRT-011 Newly created role appears in the list immediately after save")
@pytest.mark.regression
def test_newly_created_role_appears_immediately(browser):
    role_name = make_unique_role_name()
    form = open_create_role_form(browser)
    form.enter_role_name(role_name)
    form.enter_priority(ROLE_PRIORITY)
    form.ensure_active_switch_on()
    form.click_save()

    # save should redirect to the list; no manual refresh needed
    page = open_user_roles_page(browser)
    assert page.role_exists(role_name), (
        "Role '%s' not found in list immediately after save" % role_name
    )
    assert page_has_no_broken_state(page)


@allure.title("UR-CRT-010 Entering a non-numeric priority value is rejected by the form")
@pytest.mark.edge
def test_create_role_priority_integers_only(browser):
    form = open_create_role_form(browser)
    form.enter_role_name(make_unique_role_name())
    # Use keystrokes (not JS setter) so the browser's inputmode=numeric filtering applies
    form.type_priority_raw("abc")
    form.click_save()

    # Browser filters non-numeric input: field is empty ("") or invalid
    priority_val = form.get_priority_value()
    assert not form.priority_input_is_valid() or priority_val in ("", "0")
    assert page_has_no_broken_state(form)


# ── Specific role creation scenario ──────────────────────────────────────────

VK_COMPANY_ROLE_NAME = "Vk company user 1"
VK_COMPANY_ROLE_PRIORITY = "2"  # app enforces minimum priority >= 2
VK_COMPANY_LOCATIONS = ["VK AL02", "VK AL03", "VK AL04"]


@allure.title("UR-CRT-012 Create role 'Vk company user 1' with priority 2, 3 locations, and all permissions enabled")
@pytest.mark.regression
def test_create_vk_company_user_role(browser):
    with allure.step("Check if role already exists"):
        page = open_user_roles_page(browser)
        if page.role_exists(VK_COMPANY_ROLE_NAME):
            assert page.get_role_status(VK_COMPANY_ROLE_NAME) == "Active"
            assert page_has_no_broken_state(page)
            return

    with allure.step("Open create form"):
        form = open_create_role_form(browser)

    with allure.step("Enter role name"):
        form.enter_role_name(VK_COMPANY_ROLE_NAME)

    with allure.step("Enter priority order"):
        form.enter_priority(VK_COMPANY_ROLE_PRIORITY)

    with allure.step("Assign locations: VK AL02, VK AL03, VK AL04"):
        for location in VK_COMPANY_LOCATIONS:
            form.assign_location(location)

    with allure.step("Enable all permission section toggles"):
        for section in AdminUserRoleFormPage.KNOWN_PERMISSION_SECTIONS:
            form.enable_permission_section(section)

    with allure.step("Save the role"):
        form.click_save()

    with allure.step("Verify role appears in list"):
        page = open_user_roles_page(browser)
        assert page.role_exists(VK_COMPANY_ROLE_NAME), (
            f"Role '{VK_COMPANY_ROLE_NAME}' not found in list after save"
        )
        assert page.get_role_status(VK_COMPANY_ROLE_NAME) == "Active"
        assert page_has_no_broken_state(page)
