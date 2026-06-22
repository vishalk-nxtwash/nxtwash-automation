import allure
import pytest

from tests.admin_portal.sites.conftest import MISSING_SITE
from tests.admin_portal.sites.conftest import create_site_if_missing
from tests.admin_portal.sites.conftest import open_create_site_page
from tests.admin_portal.sites.conftest import open_sites_page
from tests.admin_portal.sites.conftest import page_has_no_broken_state


@allure.epic("Admin Portal")
@allure.feature("Sites / Locations")
@allure.story("UI and List")
@allure.title("SITE-UI and SITE-LIST list shell coverage")
@pytest.mark.sanity
def test_sites_locations_list_shell_and_records(logged_in_admin_browser):
    sites_page = open_sites_page(logged_in_admin_browser)

    assert "Sites/Locations" in sites_page.get_body_text()
    assert sites_page.download_button_is_clickable()
    assert sites_page.filter_button_is_clickable()
    assert sites_page.add_site_button_is_clickable()
    assert sites_page.table_headers_are_visible()
    assert sites_page.visible_row_count() > 0
    assert sites_page.edit_actions_are_visible_for_rows()
    assert sites_page.pagination_is_visible()
    assert sites_page.page_size_selector_is_visible()
    assert page_has_no_broken_state(sites_page)


@allure.epic("Admin Portal")
@allure.feature("Sites / Locations")
@allure.story("Filters")
@allure.title("SITE-FILTER drawer open, close, active switch, apply, reset")
@pytest.mark.regression
def test_sites_filter_drawer_controls(logged_in_admin_browser):
    sites_page = open_sites_page(logged_in_admin_browser)

    sites_page.open_filters()
    body_text = sites_page.get_body_text()

    assert "Filter by" in body_text
    assert "Site name" in body_text
    assert sites_page.active_site_filter_is_visible()
    assert "Apply filters" in body_text
    assert "Reset filters" in body_text

    sites_page.close_filters()
    assert "Apply filters" not in sites_page.get_body_text()


@allure.epic("Admin Portal")
@allure.feature("Sites / Locations")
@allure.story("Filters")
@allure.title("SITE-FILTER existing, partial, missing, and reset")
@pytest.mark.regression
def test_sites_filter_existing_partial_missing_and_reset(logged_in_admin_browser):
    site_data = create_site_if_missing(logged_in_admin_browser)
    sites_page = open_sites_page(logged_in_admin_browser)

    assert sites_page.site_exists_in_ui(site_data["site_name"])

    partial_site_name = site_data["site_name"][:-1]
    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.filter_by_site_name(partial_site_name)
    assert site_data["site_name"] in sites_page.get_body_text()

    sites_page = open_sites_page(logged_in_admin_browser)
    sites_page.filter_by_site_name(MISSING_SITE)
    assert MISSING_SITE not in sites_page.get_body_text()

    sites_page.reset_filters()
    assert sites_page.get_site_count_from_title() is not None


@allure.epic("Admin Portal")
@allure.feature("Sites / Locations")
@allure.story("Create General Settings")
@allure.title("SITE-CREATE general settings sections and default controls")
@pytest.mark.sanity
def test_create_site_general_settings_sections(logged_in_admin_browser):
    create_page = open_create_site_page(logged_in_admin_browser)

    assert create_page.body_contains_all(
        [
            "General settings",
            "Basic information",
            "Site name",
            "Site code",
            "Pay week start day",
            "Address information",
            "Street address",
            "ZIP code",
            "State",
            "City",
            "Time zone",
            "Tax settings",
            "Site contact info",
        ]
    )
    assert create_page.active_site_switch_is_on()


@allure.epic("Admin Portal")
@allure.feature("Sites / Locations")
@allure.story("Create Lanes")
@allure.title("SITE-LANE settings tab UI coverage")
@pytest.mark.regression
def test_create_site_lanes_settings_ui(logged_in_admin_browser):
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.open_tab("Lanes settings")

    assert create_page.body_contains_all(["Lanes settings", "Lane"])
    assert create_page.add_lane_button_is_visible()


@allure.epic("Admin Portal")
@allure.feature("Sites / Locations")
@allure.story("Create Credit Card")
@allure.title("SITE-CC settings tab UI coverage")
@pytest.mark.regression
def test_create_site_credit_card_settings_ui(logged_in_admin_browser):
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.open_tab("Credit card settings")

    assert create_page.body_contains_all(
        [
            "Credit card settings",
            "Pay API",
            "Merchant ID",
            "Pay API token",
            "DC Direct",
            "DSI EMV Android",
        ]
    )


@allure.epic("Admin Portal")
@allure.feature("Sites / Locations")
@allure.story("Create Customer Portal")
@allure.title("SITE-PORTAL settings tab UI coverage")
@pytest.mark.regression
def test_create_site_customer_portal_settings_ui(logged_in_admin_browser):
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.open_tab("Customer Portal / Mobile app settings")

    assert create_page.body_contains_all(
        [
            "Customer Portal",
            "Show on customer portal / mobile app",
            "Memberships",
            "Washbooks",
            "Gift cards",
            "Allow membership cancellation",
            "Resignup current date extension",
            "Next payment same as other vehicle",
            "Omit special character",
            "Prefix characters",
            "Suffix characters",
            "Enable free wash",
            "Facebook",
            "Instagram",
            "YouTube",
            "X (Twitter)",
            "TikTok",
        ]
    )


@allure.epic("Admin Portal")
@allure.feature("Sites / Locations")
@allure.story("Negative")
@allure.title("SITE-NEG-006 rapid save clicks are guarded")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="No stable created-record uniqueness assertion exists for rapid multi-save yet.",
    strict=False,
)
def test_create_site_rapid_save_clicks_do_not_duplicate(logged_in_admin_browser):
    create_page = open_create_site_page(logged_in_admin_browser)

    create_page.click_save_new()
    create_page.click_save_new()

    raise AssertionError(
        "Rapid multi-save uniqueness validation needs a stable created-record "
        "count assertion before it can be marked covered."
    )


@allure.epic("Admin Portal")
@allure.feature("Sites / Locations")
@allure.story("Negative")
@allure.title("SITE-NEG-008 network interruption during save")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Framework has no network interception helper for Sites save requests.",
    strict=False,
)
def test_create_site_network_interruption_during_save(logged_in_admin_browser):
    create_page = open_create_site_page(logged_in_admin_browser)

    assert "create" in logged_in_admin_browser.current_url
    assert page_has_no_broken_state(create_page)
    raise AssertionError(
        "Network interruption coverage needs a reusable network interception "
        "helper before it can be marked covered."
    )
