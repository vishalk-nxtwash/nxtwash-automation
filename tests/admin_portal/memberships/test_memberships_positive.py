from tests.admin_portal.memberships.conftest import (
    FIRST_LOCATION_COMMISSION,
    FIRST_LOCATION_PRICE,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    MEMBERSHIP_NAME,
    PREPAID_MONTHS,
    REDEEM_AS_SERVICE,
    VISIBLE_PRICE,
    create_membership_if_missing,
)


def test_create_prepaid_membership(browser):

    memberships_page = create_membership_if_missing(browser)
    memberships_page.wait_for_list_loaded()
    memberships_page.search_membership(MEMBERSHIP_NAME)

    assert memberships_page.wait_for_membership_row(MEMBERSHIP_NAME).is_displayed()
    assert memberships_page.get_membership_type(MEMBERSHIP_NAME) == "Prepaid"
    assert memberships_page.get_membership_price(MEMBERSHIP_NAME) == VISIBLE_PRICE
    assert memberships_page.get_membership_status(MEMBERSHIP_NAME) == "Active"


def test_membership_settings_persist(browser):

    memberships_page = create_membership_if_missing(browser)
    memberships_page.open_edit_membership(MEMBERSHIP_NAME)

    assert memberships_page.get_membership_name_value() == MEMBERSHIP_NAME
    assert memberships_page.prepaid_membership_type_is_selected()
    assert memberships_page.get_prepaid_months_value() == PREPAID_MONTHS
    assert memberships_page.active_switch_is_on()
    assert memberships_page.customer_portal_switch_is_on()
    assert memberships_page.get_global_price_value() == GLOBAL_PRICE
    assert memberships_page.get_global_commission_value() == GLOBAL_COMMISSION
    assert memberships_page.location_is_assigned_by_index(0)
    assert memberships_page.get_location_price_by_index(0) == FIRST_LOCATION_PRICE
    assert (
        memberships_page.get_location_commission_by_index(0)
        == FIRST_LOCATION_COMMISSION
    )

    memberships_page.open_redemption_settings()

    assert memberships_page.redemption_location_is_assigned_by_index(0)
    assert REDEEM_AS_SERVICE.lower() in memberships_page.get_body_text().lower()
