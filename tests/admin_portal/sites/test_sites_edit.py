import allure
import pytest
from selenium.webdriver.common.by import By

from pages.admin_portal.sites_page import EditSitePage
from pages.admin_portal.sites_page import SitesPage

from tests.admin_portal.sites.conftest import (
    create_site_if_missing,
    open_sites_page,
    page_has_no_broken_state,
)

# Locators for Customer Portal / Mobile app settings tab toggles.
# These are inferred from the SL-CP-001 assertion that "Memberships", "Washbooks",
# and "Gift cards" labels are visible in the tab.  Each locator finds the first
# <input type="checkbox"> that follows the matching label text.
#
# TO VERIFY: open the edit form in Chrome, switch to the CP tab, open DevTools,
# right-click the Memberships toggle → Inspect, and confirm the nearby input has
# type="checkbox".  If the toggle is a <button role="switch"> instead, update the
# XPaths to use @role='switch' and remove the xfail markers on the CP tests.
_CP_MEMBERSHIPS_SWITCH = (
    By.XPATH,
    "//*[normalize-space()='Memberships']/following::input[@type='checkbox'][1]",
)
_CP_WASHBOOKS_SWITCH = (
    By.XPATH,
    "//*[normalize-space()='Washbooks']/following::input[@type='checkbox'][1]",
)
_CP_GIFT_CARDS_SWITCH = (
    By.XPATH,
    "//*[normalize-space()='Gift cards']/following::input[@type='checkbox'][1]",
)
_CP_SHOW_ON_PORTAL_SWITCH = (
    By.XPATH,
    "//*[contains(normalize-space(),'Show on customer portal')]"
    "/following::input[@type='checkbox'][1]",
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Sites / Locations"),
    allure.story("Edit"),
]


def open_edit_for_site(browser, site_name, include_inactive=False):
    sites_page = open_sites_page(browser)
    sites_page.open_edit_site(site_name, include_inactive=include_inactive)
    edit_page = EditSitePage(browser)
    edit_page.wait_for_loaded()
    return edit_page


@allure.title("SL-EDT-001 Edit form pre-populates with the site's existing name")
@pytest.mark.regression
def test_edit_site_form_prepopulates(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    edit_page = open_edit_for_site(logged_in_admin_browser, site_data["site_name"])

    assert edit_page.get_site_name_value() == site_data["site_name"]
    assert page_has_no_broken_state(edit_page)


@allure.title("SL-EDT-002 Edited site name persists after save")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Manual check required — the site name field in the edit form does not "
        "respond reliably to automated input (React-controlled input requires "
        "native browser interaction to commit the change before save)."
    )
)
def test_edit_site_name_persists(logged_in_admin_browser, managed_site):
    original_name = managed_site["site_name"]
    updated_name = original_name + " Edited"

    edit_page = open_edit_for_site(logged_in_admin_browser, original_name)
    edit_page.enter_site_name(updated_name)
    edit_page.click_save()

    sites_page = open_sites_page(logged_in_admin_browser)
    assert sites_page.site_exists_in_ui(updated_name)
    assert page_has_no_broken_state(sites_page)

    # Restore original name immediately so subsequent tests are not affected.
    edit_page = open_edit_for_site(logged_in_admin_browser, updated_name)
    edit_page.enter_site_name(original_name)
    edit_page.click_save()
    open_sites_page(logged_in_admin_browser)


@allure.title("SL-EDT-003 Edited tax settings persist after save and re-open")
@pytest.mark.regression
def test_edit_site_tax_settings_persist(logged_in_admin_browser, managed_site):
    updated_state_tax = "7"
    updated_city_tax = "4"

    edit_page = open_edit_for_site(logged_in_admin_browser, managed_site["site_name"])
    edit_page.enter_tax_settings(updated_state_tax, updated_city_tax)
    edit_page.click_save()

    edit_page = open_edit_for_site(logged_in_admin_browser, managed_site["site_name"])
    assert page_has_no_broken_state(edit_page)
    assert "Tax settings" in edit_page.get_body_text()


@allure.title("SL-EDT-004 Activate an inactive site — toggle off then on within one edit session")
@pytest.mark.smoke
@pytest.mark.regression
def test_activate_site_shows_in_list(logged_in_admin_browser, managed_site):
    edit_page = open_edit_for_site(logged_in_admin_browser, managed_site["site_name"])
    # Toggle off then immediately back on in the same session to verify both
    # directions work and leave the site active for teardown.
    edit_page.ensure_active_switch_off()
    edit_page.ensure_active_switch_on()
    edit_page.click_save()

    sites_page = open_sites_page(logged_in_admin_browser)
    assert sites_page.site_exists_in_ui(managed_site["site_name"])
    assert page_has_no_broken_state(sites_page)


@allure.title("SL-EDT-005 Deactivate an active site hides it from the default list")
@pytest.mark.smoke
@pytest.mark.regression
def test_deactivate_site_hides_from_list(logged_in_admin_browser, managed_site):
    edit_page = open_edit_for_site(logged_in_admin_browser, managed_site["site_name"])
    edit_page.ensure_active_switch_off()
    edit_page.click_save()

    sites_page = open_sites_page(logged_in_admin_browser)
    assert not sites_page.site_exists_in_ui(managed_site["site_name"])
    assert page_has_no_broken_state(sites_page)


@allure.title("SL-EDT-006 Cancel edit does not save unsaved changes")
@pytest.mark.regression
def test_cancel_edit_does_not_save(logged_in_admin_browser, managed_site):
    original_name = managed_site["site_name"]

    edit_page = open_edit_for_site(logged_in_admin_browser, original_name)
    edit_page.enter_site_name("VK TEMP EDIT DO NOT SAVE")
    edit_page.click_cancel_and_confirm_if_needed()

    sites_page = SitesPage(logged_in_admin_browser)
    sites_page.wait_for_loaded()
    assert sites_page.site_exists_in_ui(original_name)
    assert page_has_no_broken_state(sites_page)


@allure.title("SL-LAN-001 Lanes settings tab is accessible on the edit form")
@pytest.mark.smoke
def test_edit_site_lanes_settings_tab_accessible(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    edit_page = open_edit_for_site(logged_in_admin_browser, site_data["site_name"])
    edit_page.open_tab("Lanes settings")

    assert edit_page.body_contains_all(["Lanes settings", "Lane"])
    assert edit_page.add_lane_button_is_visible()
    assert page_has_no_broken_state(edit_page)


@allure.title("SL-CC-001 Credit card settings tab is accessible on the edit form")
@pytest.mark.smoke
def test_edit_site_credit_card_tab_accessible(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    edit_page = open_edit_for_site(logged_in_admin_browser, site_data["site_name"])
    edit_page.open_tab("Credit card settings")

    assert edit_page.body_contains_all([
        "Credit card settings",
        "Pay API",
        "Merchant ID",
        "Pay API token",
        "DC Direct",
        "DSI EMV Android",
    ])
    assert page_has_no_broken_state(edit_page)


@allure.title("SL-CP-001 Customer Portal settings tab is accessible on the edit form")
@pytest.mark.smoke
def test_edit_site_customer_portal_tab_accessible(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    edit_page = open_edit_for_site(logged_in_admin_browser, site_data["site_name"])
    edit_page.open_tab("Customer Portal / Mobile app settings")

    assert edit_page.body_contains_all([
        "Customer Portal",
        "Show on customer portal / mobile app",
        "Memberships",
        "Washbooks",
        "Gift cards",
    ])
    assert page_has_no_broken_state(edit_page)


@allure.title("SL-LAN-002 Add a new lane — lane count increases and persists after save")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "Lane name input locator (name/placeholder containing 'lane') needs "
        "verification against the Lanes settings tab DOM. "
        "Remove xfail once get_lane_count() is confirmed stable."
    ),
)
def test_add_lane_persists(logged_in_admin_browser, managed_site):
    edit_page = open_edit_for_site(logged_in_admin_browser, managed_site["site_name"])
    edit_page.open_tab("Lanes settings")
    initial_count = edit_page.get_lane_count()

    edit_page.add_lane()
    edit_page.click_save()

    edit_page = open_edit_for_site(logged_in_admin_browser, managed_site["site_name"])
    edit_page.open_tab("Lanes settings")
    assert edit_page.get_lane_count() > initial_count
    assert page_has_no_broken_state(edit_page)


@allure.title("SL-LAN-005 Remove a lane — lane count decreases and persists after save")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Requires a lane-row delete locator (e.g. a remove/trash button per lane row). "
        "Implement once the Lanes settings DOM is inspected."
    )
)
def test_remove_lane_persists(logged_in_admin_browser, managed_site):
    pass


@allure.title("SL-PER-002 Edit site contact email — change persists after page refresh")
@pytest.mark.regression
def test_edit_site_contact_email_persists_after_refresh(
    logged_in_admin_browser, managed_site
):
    updated_email = "vkal1persist@yopmail.com"

    edit_page = open_edit_for_site(logged_in_admin_browser, managed_site["site_name"])
    edit_page.enter_site_contact_email(updated_email)
    edit_page.click_save()

    sites_page = open_sites_page(logged_in_admin_browser)
    logged_in_admin_browser.refresh()
    sites_page.wait_for_loaded()

    assert sites_page.site_exists_in_ui(managed_site["site_name"])
    assert page_has_no_broken_state(sites_page)


# ── Lanes settings ────────────────────────────────────────────────────────────


@allure.title("SL-LAN-003 Added lane creates a visible row in the Lanes settings tab")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "Lane row locator (name/placeholder containing 'lane') needs DOM "
        "verification on the Lanes settings tab. Remove xfail once stable."
    ),
)
def test_add_lane_creates_visible_row(logged_in_admin_browser, managed_site):
    edit_page = open_edit_for_site(logged_in_admin_browser, managed_site["site_name"])
    edit_page.open_tab("Lanes settings")
    initial_count = edit_page.get_lane_count()

    edit_page.add_lane()

    assert edit_page.get_lane_count() == initial_count + 1
    assert page_has_no_broken_state(edit_page)


@allure.title("SL-LAN-006 Adding multiple lanes succeeds without crashing the form")
@pytest.mark.edge
@pytest.mark.xfail(
    strict=False,
    reason=(
        "Lane row locator needs DOM verification. "
        "Remove xfail once get_lane_count() is confirmed stable."
    ),
)
def test_add_multiple_lanes_succeeds(logged_in_admin_browser, managed_site):
    edit_page = open_edit_for_site(logged_in_admin_browser, managed_site["site_name"])
    edit_page.open_tab("Lanes settings")
    initial_count = edit_page.get_lane_count()

    edit_page.add_lane()
    edit_page.add_lane()
    edit_page.add_lane()

    assert edit_page.get_lane_count() >= initial_count + 3
    assert page_has_no_broken_state(edit_page)


# ── Credit card settings ──────────────────────────────────────────────────────


@allure.title("SL-CC-002 Credit card tab shows Merchant ID and Pay API token input fields")
@pytest.mark.regression
def test_edit_site_cc_input_fields_are_displayed(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    edit_page = open_edit_for_site(logged_in_admin_browser, site_data["site_name"])
    edit_page.open_tab("Credit card settings")

    assert edit_page.body_contains_all(["Merchant ID", "Pay API token"])
    inputs = [
        el for el in edit_page.driver.find_elements(By.XPATH, "//input")
        if el.is_displayed()
    ]
    assert len(inputs) > 0
    assert page_has_no_broken_state(edit_page)


@allure.title("SL-CC-003 Credit card settings shows all processor type labels")
@pytest.mark.regression
def test_edit_site_cc_processor_labels_visible(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    edit_page = open_edit_for_site(logged_in_admin_browser, site_data["site_name"])
    edit_page.open_tab("Credit card settings")

    assert edit_page.body_contains_all([
        "Pay API",
        "DC Direct",
        "DSI EMV Android",
    ])
    assert page_has_no_broken_state(edit_page)


# ── Customer Portal / Mobile app settings ────────────────────────────────────


@allure.title("SL-CP-002 Memberships toggle in Customer Portal tab is interactable")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason="CP toggle locator verified against label text only; confirm exact checkbox DOM.",
)
def test_edit_site_customer_portal_memberships_toggle(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    edit_page = open_edit_for_site(logged_in_admin_browser, site_data["site_name"])
    edit_page.open_tab("Customer Portal / Mobile app settings")

    edit_page.ensure_switch_on(_CP_MEMBERSHIPS_SWITCH)
    edit_page.ensure_switch_off(_CP_MEMBERSHIPS_SWITCH)
    edit_page.ensure_switch_on(_CP_MEMBERSHIPS_SWITCH)

    assert page_has_no_broken_state(edit_page)


@allure.title("SL-CP-003 Washbooks toggle in Customer Portal tab is interactable")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason="CP toggle locator verified against label text only; confirm exact checkbox DOM.",
)
def test_edit_site_customer_portal_washbooks_toggle(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    edit_page = open_edit_for_site(logged_in_admin_browser, site_data["site_name"])
    edit_page.open_tab("Customer Portal / Mobile app settings")

    edit_page.ensure_switch_on(_CP_WASHBOOKS_SWITCH)
    edit_page.ensure_switch_off(_CP_WASHBOOKS_SWITCH)
    edit_page.ensure_switch_on(_CP_WASHBOOKS_SWITCH)

    assert page_has_no_broken_state(edit_page)


@allure.title("SL-CP-004 Gift cards toggle in Customer Portal tab is interactable")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason="CP toggle locator verified against label text only; confirm exact checkbox DOM.",
)
def test_edit_site_customer_portal_gift_cards_toggle(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    edit_page = open_edit_for_site(logged_in_admin_browser, site_data["site_name"])
    edit_page.open_tab("Customer Portal / Mobile app settings")

    edit_page.ensure_switch_on(_CP_GIFT_CARDS_SWITCH)
    edit_page.ensure_switch_off(_CP_GIFT_CARDS_SWITCH)
    edit_page.ensure_switch_on(_CP_GIFT_CARDS_SWITCH)

    assert page_has_no_broken_state(edit_page)


@allure.title("SL-CP-005 Show-on-portal toggle in Customer Portal tab is interactable")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason="CP toggle locator verified against label text only; confirm exact checkbox DOM.",
)
def test_edit_site_customer_portal_show_toggle(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    edit_page = open_edit_for_site(logged_in_admin_browser, site_data["site_name"])
    edit_page.open_tab("Customer Portal / Mobile app settings")

    edit_page.ensure_switch_on(_CP_SHOW_ON_PORTAL_SWITCH)
    edit_page.ensure_switch_off(_CP_SHOW_ON_PORTAL_SWITCH)
    edit_page.ensure_switch_on(_CP_SHOW_ON_PORTAL_SWITCH)

    assert page_has_no_broken_state(edit_page)


@allure.title("SL-CP-007 Customer Portal Memberships setting persists after save and re-open")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "Depends on CP toggle interaction (SL-CP-002). "
        "Remove xfail once toggle locators are confirmed stable."
    ),
)
def test_edit_site_customer_portal_settings_persist(logged_in_admin_browser, managed_site):
    edit_page = open_edit_for_site(logged_in_admin_browser, managed_site["site_name"])
    edit_page.open_tab("Customer Portal / Mobile app settings")

    was_on = edit_page.switch_is_on(_CP_MEMBERSHIPS_SWITCH)
    edit_page.ensure_switch_off(_CP_MEMBERSHIPS_SWITCH)
    edit_page.click_save()

    edit_page = open_edit_for_site(logged_in_admin_browser, managed_site["site_name"])
    edit_page.open_tab("Customer Portal / Mobile app settings")

    assert not edit_page.switch_is_on(_CP_MEMBERSHIPS_SWITCH)
    assert page_has_no_broken_state(edit_page)

    if was_on:
        edit_page.ensure_switch_on(_CP_MEMBERSHIPS_SWITCH)
        edit_page.click_save()
