import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    KSK_MIDDLEWARE_IP,
    open_edit_kiosk_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("Middleware Settings"),
]

_SETTINGS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Settings section locators use heuristics — verify section header classes "
        "in DevTools before removing xfail."
    ),
)


@allure.title("KSK-MID-001 Middleware settings section can be expanded and collapsed")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_middleware_section_expand_collapse(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Middleware")
    assert form.section_is_expanded("Middleware"), (
        "Middleware section should be expanded after expand_section()"
    )
    form.collapse_section("Middleware")
    assert not form.section_is_expanded("Middleware"), (
        "Middleware section should be collapsed after collapse_section()"
    )
    assert page_has_no_broken_state(form)


@allure.title("KSK-MID-002 Entering middleware IP and saving completes without error")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_enter_middleware_ip_saves(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Middleware")
    form.enter_middleware_ip(KSK_MIDDLEWARE_IP)
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("KSK-MID-003 Middleware IP persists in body after reopening edit form")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_middleware_ip_persists(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Middleware")
    form.enter_middleware_ip(KSK_MIDDLEWARE_IP)
    form.click_save()

    form2 = open_edit_kiosk_form(browser)
    form2.expand_section("Middleware")
    body = form2.get_body_text()
    assert KSK_MIDDLEWARE_IP in body or form2.get_middleware_ip() == KSK_MIDDLEWARE_IP, (
        "Middleware IP '%s' not persisted after save" % KSK_MIDDLEWARE_IP
    )
    assert page_has_no_broken_state(form2)
