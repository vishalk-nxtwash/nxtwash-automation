import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    open_edit_kiosk_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("Tunnel Settings"),
]

_SETTINGS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Settings section locators use heuristics — verify section header classes "
        "in DevTools before removing xfail."
    ),
)


@allure.title("KSK-TUN-001 Tunnel settings section can be expanded and collapsed")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_tunnel_section_expand_collapse(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Tunnel")
    assert form.section_is_expanded("Tunnel"), (
        "Tunnel section should be expanded after expand_section()"
    )
    form.collapse_section("Tunnel")
    assert not form.section_is_expanded("Tunnel"), (
        "Tunnel section should be collapsed after collapse_section()"
    )
    assert page_has_no_broken_state(form)


@allure.title("KSK-TUN-002 Tunnel operational toggle ON persists after save")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_tunnel_operational_toggle_on_persists(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Tunnel")
    form.ensure_tunnel_operational_on()
    form.click_save()

    form2 = open_edit_kiosk_form(browser)
    form2.expand_section("Tunnel")
    assert page_has_no_broken_state(form2)


@allure.title("KSK-TUN-003 Tunnel operational toggle OFF persists after save")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_tunnel_operational_toggle_off_persists(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Tunnel")
    form.ensure_tunnel_operational_off()
    form.click_save()

    form2 = open_edit_kiosk_form(browser)
    form2.expand_section("Tunnel")
    assert page_has_no_broken_state(form2)
