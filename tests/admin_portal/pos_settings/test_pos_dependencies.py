import allure
import pytest

from tests.admin_portal.pos_settings.conftest import (
    POS_SITE,
    open_create_pos_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("POS Settings"),
    allure.story("Dependencies"),
]

# POS-DEP-003: Categories reflect Services module — Not Scheduled (Deferred)
# POS-DEP-004: POS Settings permission enforcement — Not Scheduled (Deferred)
# POS-DEP-005: Create POS permission visibility — Not Scheduled (Deferred)


@allure.title("POS-DEP-001 Site dropdown lists entries from Sites & Locations module")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "POS-DEP-001: Site combobox locator uses positional heuristics — "
        "verify exact React Select element in DevTools before removing xfail."
    ),
)
def test_site_dropdown_from_sites_locations(browser):
    # Dependency: Sites & Locations module
    form = open_create_pos_form(browser)
    site_options = form.get_site_options()

    assert len(site_options) > 0, "Site dropdown returned no options"
    assert POS_SITE in site_options, (
        "Expected site '%s' not found. Got: %s" % (POS_SITE, site_options[:10])
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-DEP-002 Lane dropdown lists lanes configured for selected site")
@pytest.mark.regression
def test_lane_dropdown_from_site_lanes(browser):
    # Dependency: Sites & Locations module
    form = open_create_pos_form(browser)
    form.select_site(POS_SITE)
    lane_options = form.get_lane_options()

    assert len(lane_options) > 0, (
        "Lane dropdown returned no options after selecting site '%s'" % POS_SITE
    )
    assert page_has_no_broken_state(form)
