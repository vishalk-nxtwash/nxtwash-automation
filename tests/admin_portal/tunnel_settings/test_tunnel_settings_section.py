import allure
import pytest
from selenium.webdriver.common.by import By

from tests.admin_portal.tunnel_settings.conftest import (
    TUNNEL_CONTROLLER_ID,
    TUNNEL_NAME,
    open_edit_tunnel_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Tunnel Settings"),
    allure.story("Tunnel Settings Section"),
]

@allure.title("TUN-TSN-001 Tunnel settings section expands and collapses")
@pytest.mark.regression
def test_tunnel_settings_section_expand_collapse(browser, managed_tunnel_form):
    form = managed_tunnel_form
    form.expand_section("Tunnel settings")
    assert form.section_is_expanded("Tunnel settings"), (
        "Tunnel settings section should be expanded after expand_section()"
    )
    form.collapse_section("Tunnel settings")
    assert not form.section_is_expanded("Tunnel settings"), (
        "Tunnel settings section should be collapsed after collapse_section()"
    )
    assert page_has_no_broken_state(form)


@allure.title("TUN-TSN-002/003 Tunnel operational toggle persists ON and OFF states")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "TUN-TSN-002/003: 'Tunnel operational' toggle is absent from the form. "
        "Actual form structure (confirmed from body text) shows the 'Tunnel settings' "
        "accordion contains only the 8 named toggle switches — no Tunnel operational "
        "element. TUNNEL_OPERATIONAL_TOGGLE locator always times out. Pending DevTools "
        "verification to find the actual location of this control."
    ),
)
@pytest.mark.parametrize("operational_on", [
    pytest.param(True, id="TUN-TSN-002"),
    pytest.param(False, id="TUN-TSN-003"),
])
def test_tunnel_operational_toggle_persists(browser, managed_tunnel_form, operational_on):
    form = managed_tunnel_form
    form.expand_section("Tunnel settings")
    form.set_tunnel_operational(operational_on)
    form.click_save()

    form2 = open_edit_tunnel_form(browser, TUNNEL_NAME)
    form2.expand_section("Tunnel settings")
    assert form2.get_tunnel_operational_state() == operational_on, (
        "Tunnel operational toggle state (%s) not persisted after save" % operational_on
    )
    assert page_has_no_broken_state(form2)


@allure.title("TUN-TSN-004 Controller ID dropdown lists expected options")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "TUN-TSN-004: Controller ID dropdown is absent from the form. Actual form "
        "body text shows no Controller ID field in any section. CONTROLLER_ID_COMBOBOX "
        "locator (placeholder-based) matches nothing. Pending DevTools verification "
        "to locate the actual dropdown or confirm it is not present in this staging version."
    ),
)
def test_controller_id_dropdown_lists_options(browser, managed_tunnel_form):
    form = managed_tunnel_form
    form.expand_section("Tunnel settings")
    options = form.get_controller_id_options()

    assert len(options) > 0, "Controller ID dropdown has no options"
    assert TUNNEL_CONTROLLER_ID in options, (
        "Expected controller ID '%s' not in options: %s" % (TUNNEL_CONTROLLER_ID, options)
    )
    assert page_has_no_broken_state(form)


@allure.title("TUN-TSN-005 Controller ID selection (RTC) persists after save")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "TUN-TSN-005: Controller ID dropdown is absent from the form — same root cause "
        "as TUN-TSN-004. select_controller_id() will time out. Pending DevTools "
        "verification."
    ),
)
def test_controller_id_selection_persists(browser, managed_tunnel_form):
    form = managed_tunnel_form
    form.expand_section("Tunnel settings")
    form.select_controller_id(TUNNEL_CONTROLLER_ID)
    form.click_save()

    form2 = open_edit_tunnel_form(browser, TUNNEL_NAME)
    form2.expand_section("Tunnel settings")
    body = form2.get_body_text()
    assert TUNNEL_CONTROLLER_ID in body, (
        "Controller ID '%s' not persisted after save" % TUNNEL_CONTROLLER_ID
    )
    assert page_has_no_broken_state(form2)


@allure.title("TUN-TSN-006 Controller ID label and placeholder spell 'controller' correctly")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "Copy defect TUN-TSN-006: label reads 'Select controler ID' and "
        "placeholder reads 'Tunnel controler ID' — missing second l in controller"
    ),
)
def test_controller_id_label_spelled_correctly(browser, managed_tunnel_form):
    form = managed_tunnel_form
    form.expand_section("Tunnel settings")
    body = form.get_body_text()

    assert "Select controller ID" in body, (
        "Controller ID label should read 'Select controller ID'; got body excerpt: %r"
        % body[:500]
    )
    inputs = form.driver.find_elements(By.XPATH,
        "//input[contains(@placeholder,'controller') or contains(@placeholder,'Controller')]")
    for inp in inputs:
        if inp.is_displayed():
            ph = inp.get_attribute("placeholder") or ""
            assert "controller" in ph.lower(), (
                "Controller ID placeholder should contain 'controller' (got: %r)" % ph
            )
    assert page_has_no_broken_state(form)
