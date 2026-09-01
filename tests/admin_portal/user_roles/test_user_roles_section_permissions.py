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

# Each tuple: (section_name, sheet_tc_ids)
# Services covers UR-PRM-009/010/011 (categories + memberships/packages + gift-cards etc.)
# Customers covers UR-PRM-012/013 (customer/car settings + membership/payment)
_SECTION_CASES = [
    ("Sites",             "UR-PRM-008"),
    ("Services",          "UR-PRM-009/010/011"),
    ("Gift Cards",        "UR-PRM-011b"),
    ("Customers",         "UR-PRM-012/013"),
    ("Users",             "UR-PRM-014"),
    ("Employees",         "UR-PRM-015"),
    ("User Roles",        "UR-PRM-016"),
    ("Kiosk Settings",    "UR-PRM-017"),
    ("Kiosk App",         "UR-PRM-018"),
    ("POS Settings",      "UR-PRM-019"),
    ("POS App",           "UR-PRM-020"),
    ("Tunnel Settings",   "UR-PRM-021"),
    ("Gas Pump Settings", "UR-PRM-022"),
    ("Reports",           "UR-PRM-023"),
]

@pytest.mark.parametrize(
    "section,tc_ids",
    _SECTION_CASES,
    ids=[s.replace(" ", "_") for s, _ in _SECTION_CASES],
)
@pytest.mark.regression
def test_section_permissions_persist_after_save(browser, managed_role, section, tc_ids):
    allure.dynamic.title(
        "%s — all sub-permissions persist after save (%s)" % (section, tc_ids)
    )

    # Enable all sub-permissions for the section
    form = open_edit_role_form(browser, ROLE_NAME)
    form.expand_permission_section(section)
    form.enable_permission_section(section)

    children_before = form.all_section_children_on(section)
    assert children_before, (
        "Not all children enabled before save in section '%s'" % section
    )

    form.click_save()

    # Reopen and verify the state persisted
    form = open_edit_role_form(browser, ROLE_NAME)
    form.expand_permission_section(section)

    assert form.all_section_children_on(section), (
        "Permissions not persisted for section '%s' (%s)" % (section, tc_ids)
    )
    assert page_has_no_broken_state(form)
