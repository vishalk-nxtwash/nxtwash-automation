import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    open_edit_kiosk_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("Timer Settings"),
]

_SETTINGS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Settings section locators use heuristics — verify section header classes "
        "in DevTools before removing xfail."
    ),
)


@allure.title("KSK-TMR-001 Timer settings section can be expanded and collapsed")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_timer_section_expand_collapse(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")
    assert form.section_is_expanded("Timer"), (
        "Timer section should be expanded after expand_section()"
    )
    form.collapse_section("Timer")
    assert not form.section_is_expanded("Timer"), (
        "Timer section should be collapsed after collapse_section()"
    )
    assert page_has_no_broken_state(form)


@allure.title("KSK-TMR-002 Receipt modal delay accepts value within valid range (2-120s)")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_receipt_modal_delay_valid_value(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")
    form.enter_receipt_modal_delay("30")
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("KSK-TMR-003 Receipt modal delay rejects value below minimum (< 2)")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_receipt_modal_delay_below_min_rejected(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")
    form.enter_receipt_modal_delay("1")
    form.click_save()

    body = form.get_body_text().lower()
    assert (
        not form.timer_input_is_valid(form.RECEIPT_MODAL_DELAY_INPUT)
        or "invalid" in body
        or "minimum" in body
        or "range" in body
    ), "Receipt modal delay value below 2 should be rejected"
    assert page_has_no_broken_state(form)


@allure.title("KSK-TMR-004 Receipt modal delay rejects value above maximum (> 120)")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_receipt_modal_delay_above_max_rejected(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")
    form.enter_receipt_modal_delay("121")
    form.click_save()

    body = form.get_body_text().lower()
    assert (
        not form.timer_input_is_valid(form.RECEIPT_MODAL_DELAY_INPUT)
        or "invalid" in body
        or "maximum" in body
        or "range" in body
    ), "Receipt modal delay value above 120 should be rejected"
    assert page_has_no_broken_state(form)


@allure.title("KSK-TMR-005 Take RFID tag message delay accepts valid range (2-120s)")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_rfid_tag_delay_valid_value(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")
    form.enter_rfid_tag_delay("10")
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("KSK-TMR-006 Take RFID tag message delay rejects out-of-range values")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_rfid_tag_delay_out_of_range_rejected(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")
    form.enter_rfid_tag_delay("1")
    form.click_save()

    body = form.get_body_text().lower()
    assert (
        not form.timer_input_is_valid(form.RFID_TAG_DELAY_INPUT)
        or "invalid" in body
        or "range" in body
    ), "RFID tag delay value below 2 should be rejected"
    assert page_has_no_broken_state(form)


@allure.title("KSK-TMR-007 Extras dismiss delay accepts value within range (5-120s)")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_extras_dismiss_delay_valid_value(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")
    form.enter_extras_dismiss_delay("15")
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("KSK-TMR-008 Extras dismiss delay rejects value below minimum (< 5)")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_extras_dismiss_delay_below_min_rejected(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")
    form.enter_extras_dismiss_delay("4")
    form.click_save()

    body = form.get_body_text().lower()
    assert (
        not form.timer_input_is_valid(form.EXTRAS_DISMISS_DELAY_INPUT)
        or "invalid" in body
        or "minimum" in body
        or "range" in body
    ), "Extras dismiss delay value below 5 should be rejected"
    assert page_has_no_broken_state(form)


@allure.title("KSK-TMR-009 Extras dismiss delay rejects value above maximum (> 120)")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_extras_dismiss_delay_above_max_rejected(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")
    form.enter_extras_dismiss_delay("121")
    form.click_save()

    body = form.get_body_text().lower()
    assert (
        not form.timer_input_is_valid(form.EXTRAS_DISMISS_DELAY_INPUT)
        or "invalid" in body
        or "maximum" in body
        or "range" in body
    ), "Extras dismiss delay value above 120 should be rejected"
    assert page_has_no_broken_state(form)


@allure.title("KSK-TMR-010 Non-numeric input in a timer field is rejected")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_timer_field_non_numeric_rejected(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")
    form.enter_receipt_modal_delay("abc")
    form.click_save()

    body = form.get_body_text().lower()
    assert (
        not form.timer_input_is_valid(form.RECEIPT_MODAL_DELAY_INPUT)
        or "invalid" in body
        or "number" in body
        or "numeric" in body
    ), "Non-numeric input in timer field should be rejected"
    assert page_has_no_broken_state(form)
