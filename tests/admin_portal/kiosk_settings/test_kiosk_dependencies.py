import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    KSK_LANE,
    KSK_SITE,
    open_create_kiosk_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("Dependencies"),
]


@allure.title("KSK-DEP-001 Site dropdown lists sites from Sites & Locations module")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "KSK-DEP-001: Site dropdown options depend on Sites & Locations module data — "
        "verify KSK_SITE exists in staging before removing xfail."
    ),
)
def test_site_dropdown_lists_sites(browser):
    # Dependency: Sites & Locations module
    form = open_create_kiosk_form(browser)
    options = form.get_site_options()

    assert len(options) > 0, "Site dropdown returned no options"
    assert KSK_SITE in options, (
        "Expected site '%s' not found in dropdown. Got: %s" % (KSK_SITE, options[:10])
    )
    assert page_has_no_broken_state(form)


@allure.title("KSK-DEP-002 Lane dropdown lists lanes for the selected site")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "KSK-DEP-002: Lane options depend on selected site in Sites & Locations module — "
        "verify KSK_LANE exists under KSK_SITE in staging before removing xfail."
    ),
)
def test_lane_dropdown_lists_lanes_for_site(browser):
    # Dependency: Sites & Locations module
    form = open_create_kiosk_form(browser)
    form.select_site(KSK_SITE)
    options = form.get_lane_options()

    assert len(options) > 0, (
        "Lane dropdown returned no options after selecting site '%s'" % KSK_SITE
    )
    assert KSK_LANE in options, (
        "Expected lane '%s' not found for site '%s'. Got: %s" % (KSK_LANE, KSK_SITE, options)
    )
    assert page_has_no_broken_state(form)
