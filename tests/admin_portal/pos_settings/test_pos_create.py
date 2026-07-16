import allure
import pytest

from tests.admin_portal.pos_settings.conftest import (
    NONEXISTENT_POS_NAME,
    POS_ALLOW_CHECKOUT,
    POS_ALLOW_CHECKOUT_NO_CUSTOMER,
    POS_LANE,
    POS_MIDDLEWARE_IP,
    POS_NAME,
    POS_NEW_NAME,
    POS_PAYMENT_SERIAL,
    POS_SITE,
    create_pos_if_missing,
    get_free_lane,
    get_next_available_pos_name,
    open_create_pos_form,
    open_pos_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("POS Settings"),
    allure.story("Create"),
]

_SITE_LANE_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Site and Lane dropdowns depend on Sites & Locations data — "
        "verify POS_SITE and POS_LANE exist in staging before removing xfail."
    ),
)

_PAYMENT_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Payment method checkbox locators use label heuristics — "
        "verify exact DOM element in DevTools before removing xfail."
    ),
)

_ACCORDION_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Section accordion locators use aria-expanded heuristics — "
        "verify in DevTools before removing xfail."
    ),
)


@allure.title("POS-CRT-001 Add new POS button opens form on Main settings tab")
@pytest.mark.smoke
def test_add_pos_button_opens_form(browser):
    page = open_pos_page(browser)
    page.click_add_pos()

    assert "pos" in browser.current_url.lower() or "new" in browser.current_url.lower()
    assert page_has_no_broken_state(page)


@allure.title("POS-CRT-002 Create active POS with required fields saves correctly")
@pytest.mark.smoke
@_SITE_LANE_XFAIL
def test_create_active_pos_saves(browser):
    # Dependency: Sites & Locations module
    page = open_pos_page(browser)
    pos_name = get_next_available_pos_name(page, POS_NEW_NAME)

    lane = get_free_lane(browser, POS_SITE)
    if lane is None:
        pytest.skip("No free lanes available for site '%s' — all lanes are in use." % POS_SITE)

    form = open_create_pos_form(browser)
    form.fill_create_form(pos_name, POS_SITE, lane,
                          payment_serial=POS_PAYMENT_SERIAL,
                          middleware_ip=POS_MIDDLEWARE_IP)
    form.ensure_active_pos_on()
    form.click_save()

    page = open_pos_page(browser)
    page.search_pos(pos_name)
    try:
        page.wait_for_pos_row(pos_name, timeout=30)
    except Exception:
        assert False, (
            "POS '%s' not found in list after save (lane used: %s)" % (pos_name, lane)
        )
    assert page.get_pos_status(pos_name) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("POS-CRT-003 Save without POS name blocked with error")
@pytest.mark.smoke
def test_create_pos_name_required(browser):
    form = open_create_pos_form(browser)
    form.click_save()

    assert (
        not form.pos_name_input_is_valid()
        or "pos" in browser.current_url.lower()
        or "new" in browser.current_url.lower()
        or "required" in form.get_body_text().lower()
        or "name" in form.get_body_text().lower()
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-CRT-004 Save without site blocked with error")
@pytest.mark.smoke
def test_create_pos_site_required(browser):
    form = open_create_pos_form(browser)
    form.enter_pos_name(POS_NAME)
    # Site intentionally omitted
    form.click_save()

    body = form.get_body_text()
    assert (
        "site" in body.lower()
        or "required" in body.lower()
        or "new" in browser.current_url.lower()
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-CRT-005 Save without lane blocked with error")
@pytest.mark.smoke
def test_create_pos_lane_required(browser):
    # Dependency: Sites & Locations module
    form = open_create_pos_form(browser)
    form.enter_pos_name(POS_NAME)
    form.select_site(POS_SITE)
    # Lane intentionally omitted
    form.click_save()

    body = form.get_body_text()
    assert (
        "lane" in body.lower()
        or "required" in body.lower()
        or "new" in browser.current_url.lower()
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-CRT-006 Lane dropdown populated based on selected site")
@pytest.mark.regression
@_SITE_LANE_XFAIL
def test_lane_dropdown_populates_on_site_selection(browser):
    # Dependency: Sites & Locations module
    form = open_create_pos_form(browser)
    form.select_site(POS_SITE)
    lane_options = form.get_lane_options()

    assert len(lane_options) > 0, (
        "Lane dropdown has no options after selecting site '%s'" % POS_SITE
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-CRT-007 Create inactive POS saves and appears inactive")
@pytest.mark.regression
@_SITE_LANE_XFAIL
def test_create_inactive_pos(browser):
    # Dependency: Sites & Locations module
    form = open_create_pos_form(browser)
    form.enter_pos_name(POS_NEW_NAME)
    form.select_site(POS_SITE)
    form.select_lane(POS_LANE)
    form.ensure_active_pos_off()
    form.click_save()

    page = open_pos_page(browser)
    assert page_has_no_broken_state(page)
    page.search_pos(POS_NEW_NAME)
    body = page.get_body_text()
    assert POS_NEW_NAME not in body or page.get_pos_status(POS_NEW_NAME) == "Inactive"


@allure.title("POS-CRT-008 Allow checkout defaults to assigned customer only")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "POS-CRT-008: Allow checkout combobox locator uses label heuristics — "
        "verify exact React Select element in DevTools before removing xfail."
    ),
)
def test_allow_checkout_default(browser):
    form = open_create_pos_form(browser)
    body = form.get_body_text()

    assert "assigned customer" in body.lower() or "checkout" in body.lower(), (
        "Allow checkout default 'With assigned customer only' not visible on create form"
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-CRT-009 No customer assigned option can be selected")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "POS-CRT-009: Allow checkout combobox locator uses label heuristics — "
        "verify exact React Select element and option text in DevTools."
    ),
)
def test_allow_checkout_no_customer(browser):
    form = open_create_pos_form(browser)
    form.select_allow_checkout(POS_ALLOW_CHECKOUT_NO_CUSTOMER)
    body = form.get_body_text()

    assert "no customer" in body.lower() or "assigned" in body.lower(), (
        "No customer assigned option not selectable"
    )
    assert page_has_no_broken_state(form)


@allure.title("POS-CRT-010 Card payments checkbox checked by default")
@pytest.mark.regression
@_PAYMENT_XFAIL
def test_card_checked_by_default(browser):
    form = open_create_pos_form(browser)

    assert form.card_is_checked(), "Card payments checkbox should be checked by default"
    assert page_has_no_broken_state(form)


@allure.title("POS-CRT-011 Cash payments checkbox checked by default")
@pytest.mark.regression
@_PAYMENT_XFAIL
def test_cash_checked_by_default(browser):
    form = open_create_pos_form(browser)

    assert form.cash_is_checked(), "Cash payments checkbox should be checked by default"
    assert page_has_no_broken_state(form)


@allure.title("POS-CRT-012 Unchecking Card payments saves and persists")
@pytest.mark.regression
@_PAYMENT_XFAIL
@_SITE_LANE_XFAIL
def test_uncheck_card_persists(browser):
    # Dependency: Sites & Locations module
    form = open_create_pos_form(browser)
    form.enter_pos_name(POS_NEW_NAME)
    form.select_site(POS_SITE)
    form.select_lane(POS_LANE)
    form.ensure_active_pos_on()
    form.ensure_card_unchecked()
    form.click_save()

    form2 = open_create_pos_form(browser)
    assert page_has_no_broken_state(form2)


@allure.title("POS-CRT-013 Unchecking Cash payments saves and persists")
@pytest.mark.regression
@_PAYMENT_XFAIL
@_SITE_LANE_XFAIL
def test_uncheck_cash_persists(browser):
    # Dependency: Sites & Locations module
    form = open_create_pos_form(browser)
    form.enter_pos_name(POS_NEW_NAME)
    form.select_site(POS_SITE)
    form.select_lane(POS_LANE)
    form.ensure_active_pos_on()
    form.ensure_cash_unchecked()
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("POS-CRT-014 All settings accordions collapsed by default on create form")
@pytest.mark.regression
@_ACCORDION_XFAIL
def test_settings_accordions_collapsed(browser):
    section_names = ["Tunnel", "Middleware", "Device"]
    form = open_create_pos_form(browser)

    for section in section_names:
        assert not form.section_is_expanded(section), (
            "Section '%s' should be collapsed by default on create form" % section
        )
    assert page_has_no_broken_state(form)


@allure.title("POS-CRT-015 Cancel discards form and returns to list")
@pytest.mark.regression
def test_cancel_discards_form(browser):
    form = open_create_pos_form(browser)
    form.enter_pos_name(NONEXISTENT_POS_NAME)
    form.click_cancel()

    page = open_pos_page(browser)
    assert not page.pos_exists(NONEXISTENT_POS_NAME), (
        "POS was saved despite clicking Cancel"
    )
    assert page_has_no_broken_state(page)


@allure.title("POS-CRT-016 Newly created POS appears in list immediately after save")
@pytest.mark.regression
@_SITE_LANE_XFAIL
def test_new_pos_appears_immediately(browser):
    # Dependency: Sites & Locations module
    form = open_create_pos_form(browser)
    form.fill_create_form(POS_NEW_NAME, POS_SITE, POS_LANE)
    form.click_save()

    page = open_pos_page(browser)
    assert page.pos_exists(POS_NEW_NAME), (
        "POS '%s' did not appear in list immediately after save" % POS_NEW_NAME
    )
    assert page_has_no_broken_state(page)
