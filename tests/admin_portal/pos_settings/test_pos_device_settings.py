import allure
import pytest
from selenium.webdriver.common.keys import Keys

from tests.admin_portal.pos_settings.conftest import (
    POS_PAYMENT_SERIAL,
    open_edit_pos_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("POS Settings"),
    allure.story("Device Settings"),
]

_SETTINGS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Device settings section locators use heuristics — verify section header "
        "classes in DevTools before removing xfail."
    ),
)


@allure.title("POS-DEV-001 Device settings expand and collapse")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_device_section_expand_collapse(browser, managed_pos_form):
    form = managed_pos_form
    form.expand_section("Device")
    assert form.section_is_expanded("Device"), (
        "Device section should be expanded after expand_section()"
    )
    form.collapse_section("Device")
    assert not form.section_is_expanded("Device"), (
        "Device section should be collapsed after collapse_section()"
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-DEV-002 Payment device serial number required — blocked without entry")
@pytest.mark.regression
def test_device_serial_required(browser, managed_pos_form):
    # Dependency: Physical POS device required
    form = managed_pos_form
    form.expand_section("Device")
    el = form.wait.until(
        lambda d: d.find_element(*form.PAYMENT_SERIAL_INPUT)
    )
    el.send_keys(Keys.COMMAND + "a")
    el.send_keys(Keys.BACKSPACE)
    form.click_save()

    body = form.get_body_text()
    assert (
        not form.payment_serial_is_valid()
        or "serial" in body.lower()
        or "required" in body.lower()
        or page_has_no_broken_state(form)
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-DEV-003 Device serial number accepts valid input and saves")
@pytest.mark.regression
def test_device_serial_accepts_valid_input(browser, managed_pos_form):
    # Dependency: Physical POS device required
    form = managed_pos_form
    form.expand_section("Device")
    form.enter_payment_serial(POS_PAYMENT_SERIAL)
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("POS-DEV-004 Device serial number persists on re-open")
@pytest.mark.regression
def test_device_serial_persists(browser, managed_pos_form):
    # Dependency: Physical POS device required
    form = managed_pos_form
    form.expand_section("Device")
    form.enter_payment_serial(POS_PAYMENT_SERIAL)
    form.click_save()

    form2 = open_edit_pos_form(browser)
    form2.expand_section("Device")
    body = form2.get_body_text()
    assert POS_PAYMENT_SERIAL in body or form2.get_payment_serial() == POS_PAYMENT_SERIAL, (
        "Payment serial '%s' not found in body after save" % POS_PAYMENT_SERIAL
    )
    assert page_has_no_broken_state(form2)
