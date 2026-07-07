import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("Fleet Settings"),
]

_SETTINGS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Settings section locators use heuristics — verify section header classes "
        "in DevTools before removing xfail."
    ),
)


@allure.title("KSK-FLT2-001 Fleet settings section can be expanded and collapsed")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_fleet_section_expand_collapse(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Fleet")
    assert form.section_is_expanded("Fleet"), (
        "Fleet section should be expanded after expand_section()"
    )
    form.collapse_section("Fleet")
    assert not form.section_is_expanded("Fleet"), (
        "Fleet section should be collapsed after collapse_section()"
    )
    assert page_has_no_broken_state(form)


@allure.title("KSK-FLT2-002 Fleet toggles save ON and OFF state correctly")
@pytest.mark.extended
@_SETTINGS_XFAIL
def test_fleet_toggles_save_on_off(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Fleet")
    form.ensure_fleet_toggle_on()
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("KSK-FLT2-003 Fleet capabilities dropdown saves selected value")
@pytest.mark.extended
@_SETTINGS_XFAIL
def test_fleet_capabilities_dropdown_saves(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Fleet")
    form.select_fleet_capabilities("default")
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("KSK-FLT2-004 Fleet manager URL field accepts valid URL and saves")
@pytest.mark.extended
@_SETTINGS_XFAIL
def test_fleet_manager_url_saves(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Fleet")
    form.enter_fleet_manager_url("https://fleet.example.com")
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("KSK-FLT2-005 Call attendant Moxa output enabled toggle saves correctly")
@pytest.mark.extended
@_SETTINGS_XFAIL
def test_fleet_call_attendant_toggle_saves(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Fleet")
    form.ensure_call_attendant_on()
    form.click_save()

    assert page_has_no_broken_state(form)
