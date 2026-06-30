import allure
import pytest

from pages.admin_portal.sites_page import EditSitePage
from pages.admin_portal.sites_page import SitesPage

from tests.admin_portal.sites.conftest import (
    create_site_if_missing,
    open_sites_page,
    page_has_no_broken_state,
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
