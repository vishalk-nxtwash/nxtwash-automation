import allure
import pytest

from tests.admin_portal.users.conftest import (
    ASSIGNMENT_SITE,
    EMPLOYEE_NAME,
    USER_ROLE,
    open_create_user_form,
    open_users_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Users"),
    allure.story("Dependencies"),
]


@allure.title("USR-DEP-002 A newly created role appears in the User Role dropdown immediately")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-DEP-002: Requires a freshly created role to verify cross-module propagation. "
        "Role combobox locator also needs DevTools verification. "
        "Activate once USER_ROLES module is confirmed stable."
    ),
)
def test_new_role_appears_in_users_dropdown(browser):
    # This test documents that USER_ROLE (seeded in User Roles module) surfaces here.
    # For full cross-module propagation testing, create a role in User Roles, then
    # open this form and verify the new role name appears — that step requires
    # the user_roles conftest and is deferred to an integration test suite.
    form = open_create_user_form(browser)
    options = form.get_role_dropdown_options()

    assert USER_ROLE in options, (
        "Role '%s' created in User Roles module not found in Users dropdown. Got: %s"
        % (USER_ROLE, options)
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-DEP-004 Employee dropdown in Add user matches active employees in Employees module")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-DEP-004: Employee combobox locator uses label heuristics. "
        "Verify combobox selector in DevTools and ensure EMPLOYEE_NAME exists in staging."
    ),
)
def test_employee_dropdown_reflects_employees_module(browser):
    form = open_create_user_form(browser)
    options = form.get_employee_dropdown_options()

    assert len(options) > 0, (
        "Employee dropdown is empty — active employees from the Employees module "
        "should appear here"
    )
    assert EMPLOYEE_NAME in options, (
        "Employee '%s' missing from dropdown. Got: %s" % (EMPLOYEE_NAME, options[:10])
    )
    assert page_has_no_broken_state(form)


@allure.title("USR-DEP-008 Site filter dropdown matches sites configured in Sites & Locations")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "USR-DEP-008: Site option locator //*[@role='option'] may capture options from "
        "other open dropdowns. Verify after confirming the site filter panel structure."
    ),
)
def test_filter_sites_match_sites_and_locations_module(browser):
    page = open_users_page(browser)
    options = page.get_site_filter_options()

    assert len(options) > 0, "Site filter dropdown returned no options"
    assert ASSIGNMENT_SITE in options, (
        "Expected site '%s' from Sites & Locations not found in filter. Got: %s"
        % (ASSIGNMENT_SITE, options)
    )
    assert page_has_no_broken_state(page)
