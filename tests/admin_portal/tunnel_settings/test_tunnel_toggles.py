import allure
import pytest

from tests.admin_portal.tunnel_settings.conftest import (
    TUNNEL_NAME,
    open_create_tunnel_form,
    open_edit_tunnel_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Tunnel Settings"),
    allure.story("Toggles"),
]

_TOGGLE_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Toggle locators use label-proximity XPath and role='switch' heuristics — "
        "verify aria-checked attribute and label adjacency in DevTools before removing xfail."
    ),
)

_TOGGLES = [
    ("Auto send",                       False, "TUN-TGL-001"),
    ("MOXA auto send",                  False, "TUN-TGL-002"),
    ("Skip prompt on send car",         False, "TUN-TGL-003"),
    ("Show car count",                  False, "TUN-TGL-004"),
    ("Prompt RFID entry",               False, "TUN-TGL-005"),
    ("Automatic Car Selection",         False, "TUN-TGL-006"),
    ("Skip retract confirmation dialog",False, "TUN-TGL-007"),
    ("Active tunnel configuration",     True,  "TUN-TGL-008"),
]

_TOGGLE_LABELS = [label for label, _, _ in _TOGGLES]
_TOGGLE_TC_IDS = [tc_id for _, _, tc_id in _TOGGLES]
_TOGGLE_DEFAULTS = [(label, default) for label, default, _ in _TOGGLES]


# ---------------------------------------------------------------------------
# TUN-TGL-009 — default states on /new form (no fixture dependency)
# ---------------------------------------------------------------------------

@allure.title("TUN-TGL-009 Toggle defaults on create form")
@pytest.mark.regression
@_TOGGLE_XFAIL
@pytest.mark.parametrize("toggle_label,expected_on", [
    pytest.param(label, default, id=label.replace(" ", "-"))
    for label, default in _TOGGLE_DEFAULTS
])
def test_toggle_defaults_on_create_form(browser, toggle_label, expected_on):
    form = open_create_tunnel_form(browser)
    actual = form.get_toggle_state(toggle_label)

    assert actual == expected_on, (
        "Toggle '%s' default: expected %s, got %s" % (toggle_label, expected_on, actual)
    )
    assert page_has_no_broken_state(form)


# ---------------------------------------------------------------------------
# TUN-TGL-001..008 — each toggle saves and persists both ON and OFF
# ---------------------------------------------------------------------------

@allure.title("TUN-TGL Toggle saves and persists ON and OFF states")
@pytest.mark.regression
@_TOGGLE_XFAIL
@pytest.mark.parametrize("toggle_label", [
    pytest.param(label, id=tc_id)
    for label, _, tc_id in _TOGGLES
])
def test_toggle_saves_and_persists(browser, managed_tunnel_form, toggle_label):
    form = managed_tunnel_form

    for state in (True, False):
        form.set_toggle(toggle_label, state)
        form.click_save()

        form2 = open_edit_tunnel_form(browser, TUNNEL_NAME)
        actual = form2.get_toggle_state(toggle_label)
        assert actual == state, (
            "Toggle '%s' not persisted as %s after save" % (toggle_label, state)
        )
        assert page_has_no_broken_state(form2)

        # Re-open edit form for the next iteration
        if state is True:
            form = open_edit_tunnel_form(browser, TUNNEL_NAME)


# ---------------------------------------------------------------------------
# TUN-TGL-010 — all toggle states are reflected correctly on re-open
# ---------------------------------------------------------------------------

@allure.title("TUN-TGL-010 All toggle states are reflected on form re-open")
@pytest.mark.regression
@_TOGGLE_XFAIL
def test_toggle_states_reflected_on_reopen(browser, managed_tunnel_form):
    form = managed_tunnel_form

    # Set a known pattern: alternate ON/OFF across the 8 toggles
    expected_states = {}
    for i, (label, _, _) in enumerate(_TOGGLES):
        desired = (i % 2 == 0)
        form.set_toggle(label, desired)
        expected_states[label] = desired

    form.click_save()

    form2 = open_edit_tunnel_form(browser, TUNNEL_NAME)
    for label, expected in expected_states.items():
        actual = form2.get_toggle_state(label)
        assert actual == expected, (
            "Toggle '%s' re-open state mismatch: expected %s, got %s"
            % (label, expected, actual)
        )
    assert page_has_no_broken_state(form2)
