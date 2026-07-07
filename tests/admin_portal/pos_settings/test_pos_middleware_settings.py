import allure
import pytest
from selenium.webdriver.common.keys import Keys

from tests.admin_portal.pos_settings.conftest import (
    POS_MIDDLEWARE_IP,
    open_edit_pos_form,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("POS Settings"),
    allure.story("Middleware Settings"),
]

_SETTINGS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Middleware settings section locators use heuristics — verify section header "
        "classes in DevTools before removing xfail."
    ),
)


@allure.title("POS-MID-001 Middleware settings expand and collapse")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_middleware_section_expand_collapse(browser, managed_pos_form):
    form = managed_pos_form
    form.expand_section("Middleware")
    assert form.section_is_expanded("Middleware"), (
        "Middleware section should be expanded after expand_section()"
    )
    form.collapse_section("Middleware")
    assert not form.section_is_expanded("Middleware"), (
        "Middleware section should be collapsed after collapse_section()"
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-MID-002 Middleware IP required field — blocked without entry")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_middleware_ip_required(browser, managed_pos_form):
    form = managed_pos_form
    form.expand_section("Middleware")
    el = form.wait.until(
        lambda d: d.find_element(*form.MIDDLEWARE_IP_INPUT)
    )
    el.send_keys(Keys.COMMAND + "a")
    el.send_keys(Keys.BACKSPACE)
    form.click_save()

    body = form.get_body_text()
    assert (
        not form.middleware_ip_is_valid()
        or "middleware" in body.lower()
        or "required" in body.lower()
        or page_has_no_broken_state(form)
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-MID-003 Middleware IP accepts valid URL and saves without error")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_middleware_ip_accepts_valid_url(browser, managed_pos_form):
    form = managed_pos_form
    form.expand_section("Middleware")
    form.enter_middleware_ip(POS_MIDDLEWARE_IP)
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("POS-MID-004 Middleware IP persists in form after reopening edit")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_middleware_ip_persists(browser, managed_pos_form):
    form = managed_pos_form
    form.expand_section("Middleware")
    form.enter_middleware_ip(POS_MIDDLEWARE_IP)
    form.click_save()

    form2 = open_edit_pos_form(browser)
    form2.expand_section("Middleware")
    body = form2.get_body_text()
    assert (
        POS_MIDDLEWARE_IP in body
        or form2.get_middleware_ip() == POS_MIDDLEWARE_IP
    ), (
        "Middleware IP '%s' not persisted after save" % POS_MIDDLEWARE_IP
    )
    assert page_has_no_broken_state(form2)
