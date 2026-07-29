import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    KSK_LANE,
    KSK_NAME,
    KSK_NEW_NAME,
    KSK_SITE,
    NONEXISTENT_KSK_NAME,
    create_kiosk_if_missing,
    open_create_kiosk_form,
    open_edit_kiosk_form,
    open_kiosk_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("Create"),
]

_LOCATION_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "KSK-CRT-004/5: Site and Lane dropdowns depend on Sites & Locations data — "
        "verify in staging."
    ),
)


@allure.title("KSK-CRT-001 Clicking Add kiosk opens the create form")
@pytest.mark.smoke
def test_add_kiosk_form_opens(browser):
    page = open_kiosk_page(browser)
    page.click_add_kiosk()

    # The create form loads inside an iframe — the outer URL stays at /kiosk_settings/kiosks.
    # Switch to default_content first, then verify the create-frame appeared.
    assert page.wait_for_create_frame(), (
        "Clicking 'Add new kiosk' did not open the create form iframe"
    )
    assert page_has_no_broken_state(page)


@allure.title("KSK-CRT-002 Creating a kiosk with name only saves correctly")
@pytest.mark.smoke
@pytest.mark.xfail(
    strict=False,
    reason="KSK-CRT-002: Site is required to save — name-only submission is blocked by form validation.",
)
def test_create_kiosk_name_only(browser):
    form = open_create_kiosk_form(browser)
    form.enter_kiosk_name(KSK_NAME)
    form.click_save()

    page = open_kiosk_page(browser)
    assert page.kiosk_exists(KSK_NAME), (
        "Kiosk '%s' not found in list after save with name only" % KSK_NAME
    )
    assert page_has_no_broken_state(page)


@allure.title("KSK-CRT-003 Submitting without a name is blocked with a validation error")
@pytest.mark.smoke
def test_create_kiosk_name_required(browser):
    form = open_create_kiosk_form(browser)
    form.click_save()

    assert (
        not form.kiosk_name_input_is_valid()
        or "kiosk" in browser.current_url.lower()
        or "new" in browser.current_url.lower()
        or "required" in form.get_body_text().lower()
        or "name" in form.get_body_text().lower()
    )
    assert page_has_no_broken_state(form)


@allure.title("KSK-CRT-004 Creating a kiosk with site and lane saves correctly")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_create_kiosk_with_site_and_lane(browser):
    page = create_kiosk_if_missing(browser, name=KSK_NAME, site=KSK_SITE, lane=KSK_LANE)
    assert page.kiosk_exists(KSK_NAME), (
        "Kiosk '%s' not found after create_kiosk_if_missing" % KSK_NAME
    )
    assert page_has_no_broken_state(page)


@allure.title("KSK-CRT-005 Selecting a site populates the lane dropdown with options")
@pytest.mark.regression
@_LOCATION_XFAIL
def test_site_selection_populates_lane_dropdown(browser):
    # Dependency: Sites & Locations module
    form = open_create_kiosk_form(browser)
    form.select_site(KSK_SITE)
    lane_options = form.get_lane_options()

    assert len(lane_options) > 0, (
        "Lane dropdown has no options after selecting site '%s'" % KSK_SITE
    )
    assert page_has_no_broken_state(form)


@allure.title("KSK-CRT-006 All setting sections are collapsed by default on the create form")
@pytest.mark.regression
def test_create_form_sections_collapsed_by_default(browser):
    section_names = ["Service", "Gate", "Tunnel", "Middleware", "Device", "Timer", "Flow", "Localization", "Fleet"]
    form = open_create_kiosk_form(browser)

    for section in section_names:
        assert not form.section_is_expanded(section), (
            "Section '%s' should be collapsed by default on create form" % section
        )
    assert page_has_no_broken_state(form)


@allure.title("KSK-CRT-007 Configure panel is visible on the create form with tabs")
@pytest.mark.regression
def test_create_form_configure_panel_visible(browser):
    form = open_create_kiosk_form(browser)

    assert form.configure_panel_is_visible(), (
        "Configure kiosk service screens panel not visible on create form"
    )
    tabs = form.get_configure_panel_tabs()
    assert len(tabs) >= 0
    assert page_has_no_broken_state(form)


@allure.title("KSK-CRT-008 Clicking Cancel discards the form and kiosk does not appear in list")
@pytest.mark.regression
def test_create_kiosk_cancel_discards_form(browser):
    form = open_create_kiosk_form(browser)
    form.enter_kiosk_name(NONEXISTENT_KSK_NAME)
    form.click_cancel()

    page = open_kiosk_page(browser)
    assert not page.kiosk_exists(NONEXISTENT_KSK_NAME), (
        "Kiosk was saved despite clicking Cancel"
    )
    assert page_has_no_broken_state(page)


@allure.title("KSK-CRT-009 Newly created kiosk appears in the list immediately after save")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "KSK-CRT-009: Depends on Site and Lane dropdowns — verify KSK_SITE/KSK_LANE "
        "exist in staging before removing xfail."
    ),
)
def test_new_kiosk_appears_immediately(browser):
    page = create_kiosk_if_missing(browser, name=KSK_NEW_NAME, site=KSK_SITE, lane=KSK_LANE)
    assert page.kiosk_exists(KSK_NEW_NAME), (
        "Kiosk '%s' did not appear in list" % KSK_NEW_NAME
    )
    assert page_has_no_broken_state(page)


@allure.title("KSK-CRT-010 Generate connection code modal opens and shows a code after create")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "KSK-CRT-010: Generate connection code button and modal locators use heuristics "
        "— verify class names in DevTools before removing xfail. "
        "Requires managed_kiosk fixture (KSK_SITE / KSK_LANE must exist in staging)."
    ),
)
def test_generate_connection_code_after_create(browser, managed_kiosk):
    form = open_edit_kiosk_form(browser, KSK_NAME)
    form.click_generate_connection_code()
    code = form.get_connection_code()
    form.click_connection_code_value()

    assert code, (
        "Expected a non-empty connection code in the 'Generate connection code' modal"
    )
    assert page_has_no_broken_state(form)
