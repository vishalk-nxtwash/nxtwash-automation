import allure
import pytest

from tests.admin_portal.customers.conftest import (
    CUSTOMER_FIRST,
    CUSTOMER_LAST,
    CUSTOMER_SITE,
    create_customer_if_missing,
    open_customers_page,
    page_has_no_broken_state,
)


_MEMBERSHIPS_SKIP = "Requires Memberships module fixtures and cross-module setup. Deferred."
_GIFT_CARDS_SKIP = "Requires Gift Cards module with a customer selector fixture. Deferred."
_POS_SKIP = "Requires POS tunnel integration and RFID-linked car. Deferred."

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Customers"),
    allure.story("Dependency"),
]


@allure.title("CUST-DEP-001 Customer appears in the Customer Gift Cards select-customer dropdown")
@pytest.mark.smoke
@pytest.mark.skip(reason=_GIFT_CARDS_SKIP)
def test_customer_appears_in_gift_cards_dropdown(browser):
    pass


@allure.title("CUST-DEP-002 Customer membership status reflects the Memberships module")
@pytest.mark.regression
@pytest.mark.skip(reason=_MEMBERSHIPS_SKIP)
def test_customer_membership_status_reflects_memberships_module(browser):
    pass


@allure.title("CUST-DEP-003 Customer site assignment matches the Sites/Locations module")
@pytest.mark.regression
def test_customer_site_assignment_matches_sites_module(browser):
    create_customer_if_missing(browser)
    page = open_customers_page(browser)
    page.open_filter_panel()
    page.filter_by_first_name(CUSTOMER_FIRST)
    page.filter_by_last_name(CUSTOMER_LAST)
    page.apply_filters()
    page.open_edit_customer_from_row(CUSTOMER_LAST)

    # The site shown in the edit form should match what was set in conftest.
    # Compare case-insensitively — the system may normalise "Vk AL01" to "VK AL01".
    body = page.get_body_text()
    assert CUSTOMER_SITE.upper() in body.upper()
    assert page_has_no_broken_state(page)


@allure.title("CUST-DEP-004 Car RFID links to POS tunnel entry")
@pytest.mark.regression
@pytest.mark.skip(reason=_POS_SKIP)
def test_car_rfid_links_to_pos_tunnel_entry(browser):
    pass
