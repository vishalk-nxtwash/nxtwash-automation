import allure
import pytest

from tests.admin_portal.user_roles.conftest import (
    ASSIGNMENT_SITE,
    ROLE_NAME,
    open_edit_role_form,
    open_user_roles_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("User Roles"),
    allure.story("Locations"),
]


@allure.title("UR-LOC-001 Assigning a single location persists after save")
@pytest.mark.regression
def test_assign_single_location_persists(browser, managed_role):
    form = open_edit_role_form(browser, ROLE_NAME)
    form.assign_location(ASSIGNMENT_SITE)
    form.click_save()

    form = open_edit_role_form(browser, ROLE_NAME)
    assert form.location_is_checked(ASSIGNMENT_SITE)
    assert page_has_no_broken_state(form)


@allure.title("UR-LOC-002 Assigning multiple locations all persist after save")
@pytest.mark.regression
def test_assign_multiple_locations_persist(browser, managed_role):
    form = open_edit_role_form(browser, ROLE_NAME)

    all_locations = form.get_location_names()
    if len(all_locations) < 2:
        pytest.skip(
            "Need at least 2 configured locations to test multi-location assignment, "
            "found: %s" % all_locations
        )

    site_a, site_b = all_locations[0], all_locations[1]
    form.assign_location(site_a)
    form.assign_location(site_b)
    form.click_save()

    form = open_edit_role_form(browser, ROLE_NAME)
    assert form.location_is_checked(site_a), (
        "Location '%s' not checked after save" % site_a
    )
    assert form.location_is_checked(site_b), (
        "Location '%s' not checked after save" % site_b
    )
    assert page_has_no_broken_state(form)


@allure.title("UR-LOC-004 Location list in the form includes all configured sites")
@pytest.mark.edge
def test_location_list_includes_configured_sites(browser, managed_role):
    form = open_edit_role_form(browser, ROLE_NAME)
    location_names = form.get_location_names()

    assert len(location_names) > 0, "No location entries found in the form"
    assert ASSIGNMENT_SITE in location_names, (
        "Expected site '%s' not found in location list. Got: %s" % (ASSIGNMENT_SITE, location_names)
    )
    assert page_has_no_broken_state(form)


@allure.title("UR-LOC-003 Removing an assigned location persists after save")
@pytest.mark.regression
def test_remove_location_persists(browser, managed_role):
    # Assign first
    form = open_edit_role_form(browser, ROLE_NAME)
    form.assign_location(ASSIGNMENT_SITE)
    form.click_save()

    # Remove
    form = open_edit_role_form(browser, ROLE_NAME)
    form.remove_location(ASSIGNMENT_SITE)
    form.click_save()

    form = open_edit_role_form(browser, ROLE_NAME)
    assert not form.location_is_checked(ASSIGNMENT_SITE)
    assert page_has_no_broken_state(form)
