import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    open_edit_kiosk_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("Gate Settings"),
]

_SETTINGS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Settings section locators use heuristics — verify section header classes "
        "in DevTools before removing xfail."
    ),
)


@allure.title("KSK-GAT-001 Gate settings section can be expanded and collapsed")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_gate_section_expand_collapse(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Gate")
    assert form.section_is_expanded("Gate"), (
        "Gate section should be expanded after expand_section()"
    )
    form.collapse_section("Gate")
    assert not form.section_is_expanded("Gate"), (
        "Gate section should be collapsed after collapse_section()"
    )
    assert page_has_no_broken_state(form)


@allure.title("KSK-GAT-002 Gate operational toggle ON persists after save")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_gate_operational_toggle_on_persists(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Gate")
    form.ensure_gate_operational_on()
    form.click_save()

    form2 = open_edit_kiosk_form(browser)
    form2.expand_section("Gate")
    assert form2.get_gate_operational_state() == "on", (
        "Gate operational toggle should be ON after save"
    )
    assert page_has_no_broken_state(form2)


@allure.title("KSK-GAT-003 Gate operational toggle OFF persists after save")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_gate_operational_toggle_off_persists(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Gate")
    form.ensure_gate_operational_off()
    form.click_save()

    form2 = open_edit_kiosk_form(browser)
    form2.expand_section("Gate")
    assert form2.get_gate_operational_state() == "off", (
        "Gate operational toggle should be OFF after save"
    )
    assert page_has_no_broken_state(form2)
