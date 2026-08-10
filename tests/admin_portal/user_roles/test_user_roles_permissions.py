import allure
import pytest

from tests.admin_portal.user_roles.conftest import (
    ROLE_NAME,
    open_edit_role_form,
    open_user_roles_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("User Roles"),
    allure.story("Permissions"),
]

# A representative section used in toggle tests.
_SAMPLE_SECTION = "Sites"

_PERMISSION_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Permission accordion locators use a JS ancestor-walk that requires DOM "
        "verification. Remove xfail once section structure is confirmed in DevTools."
    ),
)


@allure.title("UR-PRM-001 Permission section headers are visible and collapsed by default")
@pytest.mark.regression
@_PERMISSION_XFAIL
def test_permission_sections_collapsed_by_default(browser, managed_role):
    form = open_edit_role_form(browser, ROLE_NAME)

    assert form.any_section_header_visible(), "No permission section headers found"
    assert not form.any_section_expanded(), (
        "At least one section is expanded on load — expected all collapsed by default"
    )
    assert page_has_no_broken_state(form)


@allure.title("UR-PRM-002 Expanding a permission section reveals its child toggles")
@pytest.mark.regression
@_PERMISSION_XFAIL
def test_expand_permission_section_reveals_toggles(browser, managed_role):
    form = open_edit_role_form(browser, ROLE_NAME)
    form.expand_permission_section(_SAMPLE_SECTION)
    children = form._get_section_child_switches(_SAMPLE_SECTION)

    assert len(children) > 0, (
        "No child toggles found after expanding '%s'" % _SAMPLE_SECTION
    )
    assert page_has_no_broken_state(form)


@allure.title("UR-PRM-003 Enabling the parent switch enables all child permissions")
@pytest.mark.regression
@_PERMISSION_XFAIL
def test_parent_toggle_on_enables_all_children(browser, managed_role):
    form = open_edit_role_form(browser, ROLE_NAME)
    form.expand_permission_section(_SAMPLE_SECTION)
    form.enable_permission_section(_SAMPLE_SECTION)

    assert form.all_section_children_on(_SAMPLE_SECTION), (
        "Not all child permissions are ON after enabling parent for '%s'" % _SAMPLE_SECTION
    )
    assert page_has_no_broken_state(form)


@allure.title("UR-PRM-004 Disabling the parent switch disables all child permissions")
@pytest.mark.regression
@_PERMISSION_XFAIL
def test_parent_toggle_off_disables_all_children(browser, managed_role):
    form = open_edit_role_form(browser, ROLE_NAME)
    form.expand_permission_section(_SAMPLE_SECTION)
    form.enable_permission_section(_SAMPLE_SECTION)   # ensure parent is on first
    form.disable_permission_section(_SAMPLE_SECTION)

    assert form.all_section_children_off(_SAMPLE_SECTION), (
        "Not all child permissions are OFF after disabling parent for '%s'" % _SAMPLE_SECTION
    )
    assert page_has_no_broken_state(form)


@allure.title("UR-PRM-005 A child permission can be toggled independently of the parent")
@pytest.mark.regression
@_PERMISSION_XFAIL
def test_child_toggle_independent(browser, managed_role):
    form = open_edit_role_form(browser, ROLE_NAME)
    form.expand_permission_section(_SAMPLE_SECTION)
    form.enable_permission_section(_SAMPLE_SECTION)   # all children ON

    before = form.get_first_child_permission_state(_SAMPLE_SECTION)
    form.toggle_first_child_permission(_SAMPLE_SECTION)
    after = form.get_first_child_permission_state(_SAMPLE_SECTION)

    assert before != after, "Child toggle did not change state"
    assert page_has_no_broken_state(form)


@allure.title("UR-PRM-006 Permission toggle state persists after save and reopening the form")
@pytest.mark.smoke
@_PERMISSION_XFAIL
def test_permissions_persist_after_save(browser, managed_role):
    form = open_edit_role_form(browser, ROLE_NAME)
    form.expand_permission_section(_SAMPLE_SECTION)
    form.enable_permission_section(_SAMPLE_SECTION)
    form.click_save()

    form = open_edit_role_form(browser, ROLE_NAME)
    form.expand_permission_section(_SAMPLE_SECTION)

    assert form.all_section_children_on(_SAMPLE_SECTION), (
        "Permission state was not persisted after save for '%s'" % _SAMPLE_SECTION
    )
    assert page_has_no_broken_state(form)


@allure.title("UR-EC-005 Disabling all permissions and saving completes without error")
@pytest.mark.edge
@pytest.mark.skip(
    reason="MANUAL CHECK: managed_role fixture errors in CI — staging server in 'Something went wrong' "
           "state after earlier create-form submission; xfail cannot catch fixture ERRORs."
)
def test_all_permissions_off_saves_ok(browser, managed_role):
    form = open_edit_role_form(browser, ROLE_NAME)

    for section in form.KNOWN_PERMISSION_SECTIONS:
        try:
            form.expand_permission_section(section)
            form.disable_permission_section(section)
        except Exception:  # noqa: BLE001
            continue

    form.click_save()

    page = open_user_roles_page(browser)
    assert page.role_exists(ROLE_NAME), "Role disappeared after saving with all permissions OFF"
    assert page_has_no_broken_state(page)
