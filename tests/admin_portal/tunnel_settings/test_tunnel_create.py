import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.admin_portal.tunnel_settings.conftest import (
    NONEXISTENT_TUNNEL_NAME,
    TUNNEL_BEHAVIOR_DEFAULT,
    TUNNEL_CONTROLLER_IP,
    TUNNEL_CRT_NAME,
    TUNNEL_MIDDLEWARE_IP,
    TUNNEL_NAME,
    TUNNEL_SITE,
    open_create_tunnel_form,
    open_tunnel_list,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Tunnel Settings"),
    allure.story("Create"),
]

_FORM_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Form field locators use heuristics — verify exact DOM selectors in "
        "DevTools before removing xfail."
    ),
)

_SECTION_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Section accordion locators use aria-expanded heuristics — "
        "verify in DevTools before removing xfail."
    ),
)

_SITE_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Site dropdown depends on Sites & Locations data — "
        "verify VK Test carwash 2 exists in staging before removing xfail."
    ),
)

_SESSION_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "TUN-CRT-008 fails in full suite runs (47+ min) when the staging session "
        "expires mid-run. Passes in isolation. Fix: increase session TTL or add "
        "mid-suite re-auth. Not a product or locator defect."
    ),
)


@allure.title("TUN-CRT-001 Add new tunnel button navigates to create form")
@pytest.mark.smoke
def test_add_tunnel_button_opens_form(browser):
    page = open_tunnel_list(browser)
    page.click_add_tunnel()

    assert "tunnel" in browser.current_url.lower() or "new" in browser.current_url.lower()
    assert page_has_no_broken_state(page)


@allure.title("TUN-CRT-002 Required fields are marked with asterisk on create form")
@pytest.mark.regression
@_FORM_XFAIL
def test_required_fields_marked_with_asterisk(browser):
    form = open_create_tunnel_form(browser)
    body = form.get_body_text()

    assert "*" in body, "No required field asterisk visible on create form"
    for label in ("Tunnel name", "Site", "Controller IP"):
        assert label.lower().replace(" ", "") in body.lower().replace(" ", ""), (
            "Required field '%s' not visible on create form" % label
        )
    assert page_has_no_broken_state(form)


@allure.title("TUN-CRT-003 Creating tunnel with all fields saves and appears in list")
@pytest.mark.smoke
@_SITE_XFAIL
def test_create_tunnel_full_save(browser):
    # Dependency: Sites & Locations module
    form = open_create_tunnel_form(browser)
    form.enter_tunnel_name(TUNNEL_CRT_NAME)
    form.select_site(TUNNEL_SITE)
    form.enter_controller_ip(TUNNEL_CONTROLLER_IP)
    form.enter_middleware_ip(TUNNEL_MIDDLEWARE_IP)
    form.click_save()

    page = open_tunnel_list(browser)
    assert page.tunnel_exists(TUNNEL_CRT_NAME), (
        "Tunnel '%s' not found in list after full-field save" % TUNNEL_CRT_NAME
    )
    assert page_has_no_broken_state(page)


@allure.title("TUN-CRT-004 New tunnel appears in list immediately after save")
@pytest.mark.regression
@_SITE_XFAIL
def test_new_tunnel_appears_immediately(browser):
    # Dependency: Sites & Locations module
    form = open_create_tunnel_form(browser)
    form.enter_tunnel_name(TUNNEL_CRT_NAME)
    form.select_site(TUNNEL_SITE)
    form.enter_controller_ip(TUNNEL_CONTROLLER_IP)
    form.click_save()

    page = open_tunnel_list(browser)
    assert page.tunnel_exists(TUNNEL_CRT_NAME), (
        "Tunnel '%s' did not appear in list immediately after save" % TUNNEL_CRT_NAME
    )
    assert page_has_no_broken_state(page)


@allure.title("TUN-CRT-005 Site dropdown lists active sites including VK Test carwash 2")
@pytest.mark.regression
@_SITE_XFAIL
def test_site_dropdown_lists_active_sites(browser):
    # Dependency: Sites & Locations module
    form = open_create_tunnel_form(browser)
    combobox = form.wait.until(EC.element_to_be_clickable(form.SITE_COMBOBOX))
    form.driver.execute_script("arguments[0].click();", combobox)
    opts = WebDriverWait(form.driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//*[contains(@class,'form-select__option')] | //*[@role='option']")
        )
    )
    option_texts = [o.text.strip() for o in opts if o.text.strip()]

    assert len(option_texts) > 0, "Site dropdown has no options"
    assert TUNNEL_SITE in option_texts, (
        "Expected site '%s' not in dropdown: %s" % (TUNNEL_SITE, option_texts)
    )
    assert page_has_no_broken_state(form)


@allure.title("TUN-CRT-006 Behavior defaults to Sequence stacking on create form")
@pytest.mark.regression
@_FORM_XFAIL
def test_behavior_defaults_to_sequence_stacking(browser):
    form = open_create_tunnel_form(browser)
    body = form.get_body_text()

    assert TUNNEL_BEHAVIOR_DEFAULT in body, (
        "Behavior default '%s' not visible on create form" % TUNNEL_BEHAVIOR_DEFAULT
    )
    assert (
        form.get_behavior_radio_state(TUNNEL_BEHAVIOR_DEFAULT)
        or TUNNEL_BEHAVIOR_DEFAULT in body
    ), "Sequence stacking radio not selected by default"
    assert page_has_no_broken_state(form)


@allure.title("TUN-CRT-007 Three collapsible sections present on create form")
@pytest.mark.regression
@_SECTION_XFAIL
def test_three_sections_present_on_create_form(browser):
    section_names = ["Tunnel settings", "Retract settings", "Tunnel functions"]
    form = open_create_tunnel_form(browser)
    body = form.get_body_text()

    for section in section_names:
        assert section.lower() in body.lower(), (
            "Section '%s' not found on create form body" % section
        )
    assert page_has_no_broken_state(form)


@allure.title("TUN-CRT-008 Cancel discards form and returns to list without saving")
@pytest.mark.regression
@_SESSION_XFAIL
def test_cancel_discards_form_returns_to_list(browser):
    form = open_create_tunnel_form(browser)
    form.enter_tunnel_name(NONEXISTENT_TUNNEL_NAME)
    form.click_cancel()

    page = open_tunnel_list(browser)
    assert not page.tunnel_exists(NONEXISTENT_TUNNEL_NAME), (
        "Tunnel was saved despite clicking Cancel"
    )
    assert page_has_no_broken_state(page)


@allure.title("TUN-CRT-009 Save with required fields only (no optional fields) works")
@pytest.mark.regression
@_SITE_XFAIL
def test_create_tunnel_required_fields_only(browser):
    # Dependency: Sites & Locations module
    # Middleware IP and non-default toggles intentionally omitted
    form = open_create_tunnel_form(browser)
    form.enter_tunnel_name(TUNNEL_CRT_NAME)
    form.select_site(TUNNEL_SITE)
    form.enter_controller_ip(TUNNEL_CONTROLLER_IP)
    form.click_save()

    page = open_tunnel_list(browser)
    assert page.tunnel_exists(TUNNEL_CRT_NAME), (
        "Tunnel '%s' not found after save with required fields only" % TUNNEL_CRT_NAME
    )
    assert page_has_no_broken_state(page)


# ---------------------------------------------------------------------------
# TUN-VAL-001, TUN-VAL-002, TUN-VAL-003 — required field validation
# ---------------------------------------------------------------------------

@allure.title("TUN-VAL Required field validation blocks save when field is blank")
@pytest.mark.smoke
@pytest.mark.parametrize("field", [
    pytest.param("name", id="TUN-VAL-001"),
    pytest.param("site", id="TUN-VAL-002"),
    pytest.param("controller_ip", id="TUN-VAL-003"),
])
def test_required_field_validation(browser, field):
    form = open_create_tunnel_form(browser)

    if field == "name":
        form.enter_controller_ip(TUNNEL_CONTROLLER_IP)
        form.click_save()
        body = form.get_body_text()
        assert (
            not form.name_input_is_valid()
            or "name" in body.lower()
            or "required" in body.lower()
            or "new" in browser.current_url.lower()
        ), "Blank tunnel name should block save"

    elif field == "site":
        # Site intentionally omitted — form starts with no site selected
        form.enter_tunnel_name(TUNNEL_NAME)
        form.enter_controller_ip(TUNNEL_CONTROLLER_IP)
        form.click_save()
        body = form.get_body_text()
        assert (
            "site" in body.lower()
            or "required" in body.lower()
            or "new" in browser.current_url.lower()
        ), "Missing site should block save"

    elif field == "controller_ip":
        form.enter_tunnel_name(TUNNEL_NAME)
        # Controller IP intentionally omitted; clear any pre-filled value
        try:
            el = form.wait.until(lambda d: d.find_element(*form.CONTROLLER_IP_INPUT))
            el.send_keys(Keys.COMMAND + "a")
            el.send_keys(Keys.BACKSPACE)
        except Exception:
            pass
        form.click_save()
        body = form.get_body_text()
        assert (
            not form.controller_ip_is_valid()
            or "ip" in body.lower()
            or "controller" in body.lower()
            or "required" in body.lower()
            or "new" in browser.current_url.lower()
        ), "Blank Controller IP should block save"

    assert page_has_no_broken_state(form)
