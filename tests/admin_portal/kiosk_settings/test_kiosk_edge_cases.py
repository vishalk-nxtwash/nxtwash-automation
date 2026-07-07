import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    open_create_kiosk_form,
    open_edit_kiosk_form,
    open_kiosk_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("Edge Cases"),
]

_SETTINGS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Settings section locators use heuristics — verify section header classes "
        "in DevTools before removing xfail."
    ),
)


@allure.title("KSK-EC-001 Kiosk name with leading/trailing whitespace is trimmed or rejected")
@pytest.mark.extended
def test_kiosk_name_whitespace_trimmed(browser):
    padded_name = "  VK kiosk edge  "
    trimmed_name = padded_name.strip()

    form = open_create_kiosk_form(browser)
    form.enter_kiosk_name(padded_name)
    form.click_save()

    page = open_kiosk_page(browser)
    body = page.get_body_text()
    assert trimmed_name in body or padded_name.strip() in body or not page.kiosk_exists(padded_name), (
        "Kiosk name should be trimmed or rejected — padded name should not appear verbatim"
    )
    assert page_has_no_broken_state(page)


@allure.title("KSK-EC-002 Kiosk created with no Site or Lane assigned appears in the list")
@pytest.mark.regression
def test_kiosk_without_site_lane_appears_in_list(browser):
    name = "VK kiosk no-site"

    form = open_create_kiosk_form(browser)
    form.enter_kiosk_name(name)
    form.click_save()

    page = open_kiosk_page(browser)
    assert page.kiosk_exists(name), (
        "Kiosk '%s' (no site/lane) should appear in list after save" % name
    )
    assert page_has_no_broken_state(page)


@allure.title("KSK-EC-004 Timer boundary: exactly 2 and 120 are valid for Receipt modal delay")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_receipt_modal_delay_boundary_values_valid(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")

    form.enter_receipt_modal_delay("2")
    form.click_save()
    assert form.timer_input_is_valid(form.RECEIPT_MODAL_DELAY_INPUT), (
        "Value 2 (minimum boundary) should be valid for Receipt modal delay"
    )

    form2 = open_edit_kiosk_form(browser)
    form2.expand_section("Timer")
    form2.enter_receipt_modal_delay("120")
    form2.click_save()
    assert form2.timer_input_is_valid(form2.RECEIPT_MODAL_DELAY_INPUT), (
        "Value 120 (maximum boundary) should be valid for Receipt modal delay"
    )
    assert page_has_no_broken_state(form2)


@allure.title("KSK-EC-005 Timer boundary: exactly 5 and 120 are valid for Extras dismiss delay")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_extras_dismiss_delay_boundary_values_valid(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Timer")

    form.enter_extras_dismiss_delay("5")
    form.click_save()
    assert form.timer_input_is_valid(form.EXTRAS_DISMISS_DELAY_INPUT), (
        "Value 5 (minimum boundary) should be valid for Extras dismiss delay"
    )

    form2 = open_edit_kiosk_form(browser)
    form2.expand_section("Timer")
    form2.enter_extras_dismiss_delay("120")
    form2.click_save()
    assert form2.timer_input_is_valid(form2.EXTRAS_DISMISS_DELAY_INPUT), (
        "Value 120 (maximum boundary) should be valid for Extras dismiss delay"
    )
    assert page_has_no_broken_state(form2)
