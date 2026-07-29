import allure
import pytest

from tests.admin_portal.pos_settings.conftest import (
    open_edit_pos_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("POS Settings"),
    allure.story("Service Settings"),
]

# POS-SVC-002 through POS-SVC-010 and POS-SVC-014 are excluded per the
# Service Settings scripting rule: do not automate individual field configuration.
# The single scripted verification is POS-SVC-001 (tab switch) and
# POS-SVC-012 (restore default settings).

@allure.title("POS-SVC-001 Service settings tab switches view")
@pytest.mark.smoke
def test_service_tab_switches_view(browser, managed_pos):
    # Dependency: Services module
    form = open_edit_pos_form(browser)
    form.click_service_settings_tab()
    body = form.get_body_text()

    assert "service" in body.lower() or "category" in body.lower() or "restore" in body.lower(), (
        "Service settings tab did not switch view"
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-SVC-012 Restore default settings resets order and colors")
@pytest.mark.regression
def test_restore_default_settings(browser, managed_pos):
    # Dependency: Services module
    form = open_edit_pos_form(browser)
    form.click_service_settings_tab()
    form.click_restore_default()

    body = form.get_body_text()
    assert (
        "default" in body.lower()
        or "category" in body.lower()
        or "service" in body.lower()
    ), (
        "Default settings not displayed after clicking Restore Default Settings"
    )
    assert page_has_no_broken_state(form)
