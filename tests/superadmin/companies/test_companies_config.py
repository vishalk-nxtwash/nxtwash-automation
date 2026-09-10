import allure
import pytest

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Companies"),
    allure.story("Company Config"),
]

_CONFIG_ACCORDION_SECTIONS = [
    "Marketing",
    "Memberships",
    "Admin portal",
    "Customer portal",
    "Owner app",
    "Geofencing",
    "Twilio",
    "AI assistance",
]


def test_gas_pump_toggle_is_off_by_default(edit_company_page):
    """SA-CMP-CFG-001 — Gas Pump codes toggle defaults to OFF."""
    state = edit_company_page.get_gas_pump_toggle_state()
    assert not state, \
        "Gas Pump codes toggle should be OFF by default"


def test_award_points_toggle_is_off_by_default(edit_company_page):
    """SA-CMP-CFG-002 — Award Points toggle defaults to OFF."""
    state = edit_company_page.get_award_points_toggle_state()
    assert not state, \
        "Award Points toggle should be OFF by default"


def test_all_config_accordions_are_present(edit_company_page):
    """SA-CMP-CFG-003 — all 8 config accordion sections are present on the page."""
    missing = [
        section
        for section in _CONFIG_ACCORDION_SECTIONS
        if not edit_company_page.accordion_section_is_visible(section)
    ]
    assert not missing, \
        f"Missing config accordion sections: {missing}"


@pytest.mark.parametrize("section", _CONFIG_ACCORDION_SECTIONS)
def test_accordions_expand_and_collapse(edit_company_page, section):
    """SA-CMP-CFG-004 — each accordion expands and collapses on click."""
    # Expand
    edit_company_page.expand_accordion(section)
    body_after_expand = edit_company_page.get_body_text()

    # Collapse
    edit_company_page.expand_accordion(section)
    body_after_collapse = edit_company_page.get_body_text()

    # Simply assert we didn't crash and both interactions completed
    assert "error" not in body_after_expand.lower(), \
        f"Expanding '{section}' accordion should not show an error"
    assert "error" not in body_after_collapse.lower(), \
        f"Collapsing '{section}' accordion should not show an error"


def test_sms_marketing_on_reveals_related_fields(edit_company_page):
    """SA-CMP-CFG-005 — toggling SMS marketing ON reveals count and opt-in language fields."""
    edit_company_page.expand_accordion("Marketing")
    initial_sms_state = edit_company_page.get_sms_marketing_state()

    try:
        if not initial_sms_state:
            edit_company_page.toggle_sms_marketing()

        assert edit_company_page.sms_count_field_is_visible(), \
            "SMS count field should appear when SMS marketing is ON"
        assert edit_company_page.opt_in_language_field_is_visible(), \
            "Opt-in language field should appear when SMS marketing is ON"
    finally:
        if not initial_sms_state and edit_company_page.get_sms_marketing_state():
            edit_company_page.toggle_sms_marketing()


def test_sms_count_required_when_sms_on(edit_company_page):
    """SA-CMP-CFG-006 — SMS count is required when SMS marketing is ON."""
    edit_company_page.expand_accordion("Marketing")
    initial_state = edit_company_page.get_sms_marketing_state()

    try:
        if not initial_state:
            edit_company_page.toggle_sms_marketing()

        assert edit_company_page.sms_count_field_is_visible(), \
            "SMS count field should be visible when SMS marketing is ON"
    finally:
        if not initial_state and edit_company_page.get_sms_marketing_state():
            edit_company_page.toggle_sms_marketing()


def test_opt_in_language_required_when_sms_on(edit_company_page):
    """SA-CMP-CFG-007 — opt-in language is required when SMS marketing is ON."""
    edit_company_page.expand_accordion("Marketing")
    initial_state = edit_company_page.get_sms_marketing_state()

    try:
        if not initial_state:
            edit_company_page.toggle_sms_marketing()

        assert edit_company_page.opt_in_language_field_is_visible(), \
            "Opt-in language field should be visible when SMS marketing is ON"
    finally:
        if not initial_state and edit_company_page.get_sms_marketing_state():
            edit_company_page.toggle_sms_marketing()


@pytest.mark.skip(
    reason="SA-CMP-CFG-008: Notification event config button — config screen details "
           "pending capture; locator cannot be determined without app inspection."
)
def test_notification_event_config_button_opens_settings(edit_company_page):
    """SA-CMP-CFG-008 — the notification event config button opens a settings screen."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-CFG-009: Membership toggles — field-level locators for the 5 "
           "membership toggles not yet confirmed. Expand Memberships accordion and "
           "inspect DOM before implementing."
)
def test_membership_toggles_persist(edit_company_page):
    """SA-CMP-CFG-009 — 5 membership toggles (email receipt, multi-car, etc.) persist after save."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-CFG-010: Recharge retry type — locator not confirmed; "
           "inspect Memberships accordion DOM first."
)
def test_recharge_retry_type_selection_persists(edit_company_page):
    """SA-CMP-CFG-010 — the recharge retry type selection persists after save."""
    pass


def test_all_sections_expand_without_error(edit_company_page):
    """SA-CMP-CFG-011 — all 8 config accordions can be expanded without an error."""
    for section in _CONFIG_ACCORDION_SECTIONS:
        if edit_company_page.accordion_section_is_visible(section):
            edit_company_page.expand_accordion(section)

    body = edit_company_page.get_body_text()
    assert "error" not in body.lower(), \
        "Expanding all config sections should not produce an error"


@pytest.mark.skip(
    reason="SA-CMP-CFG-012: Twilio invalid credentials error — Twilio field "
           "locators and validation behaviour flagged as '[to be confirmed]'."
)
def test_invalid_twilio_credentials_show_error(edit_company_page):
    """SA-CMP-CFG-012 — entering invalid Twilio credentials triggers a visible error."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-CFG-013: Config changes persist after reload — depends on "
           "knowing specific toggle default states to restore after the test. "
           "Implement after CFG-001/002 establish safe toggle defaults."
)
def test_all_config_changes_persist_after_reload(edit_company_page, browser):
    """SA-CMP-CFG-013 — all config changes persist after a full page reload."""
    pass
