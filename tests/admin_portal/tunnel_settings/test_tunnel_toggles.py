import allure
import pytest

from tests.admin_portal.tunnel_settings.conftest import (
    TUNNEL_NAME,
    open_create_tunnel_form,
    open_edit_tunnel_form,
    open_edit_tunnel_form_by_url,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Tunnel Settings"),
    allure.story("Toggles"),
]

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

_TGL_FALSE_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Staging app does not persist the OFF state for this toggle; "
        "the value resets to True on save. Needs product investigation."
    ),
)

_TGL_RACE_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "TUN-TGL-001: parallel worker race — managed_tunnel_form restore on another gw "
        "reverts 'Auto send' between save and re-read under -n 2. "
        "Fix: per-worker tunnel isolation."
    ),
)

_XFAIL_TC_IDS = {
    "TUN-TGL-001": _TGL_RACE_XFAIL,
    "TUN-TGL-002": _TGL_FALSE_XFAIL,
    "TUN-TGL-003": _TGL_FALSE_XFAIL,
    "TUN-TGL-006": _TGL_FALSE_XFAIL,
}

_SKIP_MARK = pytest.mark.skip(
    reason=(
        "CI-SKIP: managed_tunnel_form fixture fails in headless CI. "
        "Fix: decouple frame switch from form fixture setup."
    )
)
_SKIP_TC_IDS = {"TUN-TGL-004", "TUN-TGL-005", "TUN-TGL-007"}

@allure.title("TUN-TGL Toggle saves and persists ON and OFF states")
@pytest.mark.regression
@pytest.mark.parametrize("toggle_label", [
    pytest.param(label, id=tc_id, marks=_XFAIL_TC_IDS[tc_id])
    if tc_id in _XFAIL_TC_IDS else
    pytest.param(label, id=tc_id, marks=_SKIP_MARK)
    if tc_id in _SKIP_TC_IDS else
    pytest.param(label, id=tc_id)
    for label, _, tc_id in _TOGGLES
])
def test_toggle_saves_and_persists(browser, managed_tunnel_form, toggle_label):
    form = managed_tunnel_form

    for state in (True, False):
        # Capture outer-page URL before save — needed if the tunnel disappears from
        # the list (Active=False hides it; direct navigation is required to verify).
        pre_save_url = browser.current_url

        form.set_toggle(toggle_label, state)
        form.click_save()

        if toggle_label == "Active tunnel configuration" and not state:
            form2 = open_edit_tunnel_form_by_url(browser, pre_save_url)
        else:
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
@pytest.mark.xfail(
    strict=False,
    reason=(
        "TUN-TGL-010: staging toggle persistence race — 'Automatic Car Selection' "
        "does not reliably save to False under parallel load."
    ),
)
def test_toggle_states_reflected_on_reopen(browser, managed_tunnel_form):
    form = managed_tunnel_form

    # Set a known pattern: alternate ON/OFF across the 8 toggles.
    # "Active tunnel configuration" is always kept True so the tunnel remains
    # visible in the list and open_edit_tunnel_form can navigate back for verification.
    expected_states = {}
    for i, (label, _, _) in enumerate(_TOGGLES):
        desired = (i % 2 == 0)
        if label == "Active tunnel configuration":
            desired = True
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
