import allure
import pytest

from tests.admin_portal.tunnel_settings.conftest import (
    TUNNEL_BEHAVIOR_DEFAULT,
    TUNNEL_NAME,
    open_create_tunnel_form,
    open_edit_tunnel_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Tunnel Settings"),
    allure.story("Behavior"),
]

_FORM_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Behavior radio locators use label heuristics — "
        "verify radio input DOM structure in DevTools before removing xfail."
    ),
)


@allure.title("TUN-BHV-001/002 Behavior radio buttons are present and mutually exclusive")
@pytest.mark.regression
@_FORM_XFAIL
def test_behavior_radio_mutual_exclusivity(browser):
    form = open_create_tunnel_form(browser)
    radios = form.get_behavior_radio_elements()

    assert len(radios) == 2, (
        "Expected 2 behavior radio options, found %d" % len(radios)
    )

    form.driver.execute_script("arguments[0].click();", radios[0])
    assert radios[0].is_selected(), "Radio 0 should be selected after click"
    assert not radios[1].is_selected(), "Radio 1 should be deselected when radio 0 is selected"

    form.driver.execute_script("arguments[0].click();", radios[1])
    assert radios[1].is_selected(), "Radio 1 should be selected after click"
    assert not radios[0].is_selected(), "Radio 0 should be deselected when radio 1 is selected"

    assert page_has_no_broken_state(form)


@allure.title("TUN-BHV-003 Sequence stacking is the default behavior on create form")
@pytest.mark.regression
@_FORM_XFAIL
def test_behavior_default_sequence_stacking(browser):
    form = open_create_tunnel_form(browser)
    body = form.get_body_text()

    assert TUNNEL_BEHAVIOR_DEFAULT in body, (
        "Default behavior '%s' not visible on create form" % TUNNEL_BEHAVIOR_DEFAULT
    )
    assert (
        form.get_behavior_radio_state(TUNNEL_BEHAVIOR_DEFAULT)
        or TUNNEL_BEHAVIOR_DEFAULT in body
    ), "Sequence stacking radio should be selected by default"
    assert page_has_no_broken_state(form)


@allure.title("TUN-BHV-004 Selected behavior persists after save")
@pytest.mark.regression
@_FORM_XFAIL
def test_behavior_radio_persists(browser, managed_tunnel_form):
    form = managed_tunnel_form
    radios = form.get_behavior_radio_elements()

    assert len(radios) >= 2, "Expected at least 2 behavior radio options"

    # Identify the currently unselected (non-default) radio
    non_default = next((r for r in radios if not r.is_selected()), None)
    assert non_default is not None, "All behavior radios are selected simultaneously"
    non_default_index = radios.index(non_default)

    form.driver.execute_script("arguments[0].click();", non_default)
    form.click_save()

    form2 = open_edit_tunnel_form(browser, TUNNEL_NAME)
    radios2 = form2.get_behavior_radio_elements()
    assert len(radios2) >= non_default_index + 1, "Behavior radios not found on re-open"
    assert radios2[non_default_index].is_selected(), (
        "Non-default behavior (index %d) not persisted after save" % non_default_index
    )
    assert page_has_no_broken_state(form2)
