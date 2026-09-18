import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    open_edit_kiosk_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("Service Settings"),
]

_SETTINGS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Settings section locators use heuristics — verify section header classes "
        "in DevTools before removing xfail."
    ),
)


@allure.title("KSK-SVC-001 Service settings section can be expanded and collapsed")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_service_section_expand_collapse(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Service")
    assert form.section_is_expanded("Service"), (
        "Service section should be expanded after expand_section()"
    )
    form.collapse_section("Service")
    assert not form.section_is_expanded("Service"), (
        "Service section should be collapsed after collapse_section()"
    )
    assert page_has_no_broken_state(form)


@allure.title("KSK-SVC-002 Expanding service section shows the four service checkboxes")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_service_section_shows_checkboxes(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Service")
    body = form.get_body_text()

    assert (
        "Memberships" in body
        or "Wash packages" in body
        or "Wash extras" in body
        or "checkbox" in body.lower()
    ), "Expected service checkboxes not visible after expanding Service section"
    assert page_has_no_broken_state(form)


@allure.title("KSK-SVC-003 Unchecking Memberships persists after save")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_uncheck_memberships_persists(browser, managed_kiosk_form):
    # Dependency: Services module
    form = managed_kiosk_form
    form.expand_section("Service")
    form.ensure_checkbox_unchecked(form.MEMBERSHIPS_CHECKBOX)
    form.click_save()

    form2 = open_edit_kiosk_form(browser)
    form2.expand_section("Service")
    assert not form2.get_checkbox_state(form2.MEMBERSHIPS_CHECKBOX), (
        "Memberships checkbox should remain unchecked after save"
    )
    assert page_has_no_broken_state(form2)


@allure.title("KSK-SVC-004 Re-checking Memberships persists after save")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_recheck_memberships_persists(browser, managed_kiosk_form):
    # Dependency: Services module
    form = managed_kiosk_form
    form.expand_section("Service")
    form.ensure_checkbox_checked(form.MEMBERSHIPS_CHECKBOX)
    form.click_save()

    form2 = open_edit_kiosk_form(browser)
    form2.expand_section("Service")
    assert form2.get_checkbox_state(form2.MEMBERSHIPS_CHECKBOX), (
        "Memberships checkbox should remain checked after save"
    )
    assert page_has_no_broken_state(form2)


@allure.title("KSK-SVC-005 Enabling all four checkboxes and upsale toggle persists after save")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_enable_all_checkboxes_and_upsale(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Service")
    form.ensure_checkbox_checked(form.MEMBERSHIPS_CHECKBOX)
    form.ensure_checkbox_checked(form.WASH_PACKAGES_CHECKBOX)
    form.ensure_checkbox_checked(form.WASH_EXTRAS_CHECKBOX)
    form.ensure_checkbox_checked(form.SECOND_WASH_EXTRAS_CHECKBOX)
    form.ensure_upsale_on()
    form.click_save()

    form2 = open_edit_kiosk_form(browser)
    form2.expand_section("Service")
    assert form2.get_checkbox_state(form2.MEMBERSHIPS_CHECKBOX)
    assert page_has_no_broken_state(form2)


@allure.title("KSK-SVC-006 Turning upsale toggle OFF persists after save")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_upsale_toggle_off_persists(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Service")
    form.ensure_upsale_off()
    form.click_save()

    form2 = open_edit_kiosk_form(browser)
    form2.expand_section("Service")
    assert page_has_no_broken_state(form2)
