from tests.admin_portal.test_memberships import open_memberships_page


MEMBERSHIP_NAME = "VK MA2"
GLOBAL_PRICE = "15"
GLOBAL_COMMISSION = "2"
FIRST_LOCATION_PRICE = "20"
FIRST_LOCATION_COMMISSION = "3"
PREPAID_MONTHS = "1"
REDEEM_AS_SERVICE = "VK detail wash"
VISIBLE_PRICE = "$15.00"


def create_membership_if_missing(browser, membership_name=MEMBERSHIP_NAME):

    memberships_page = open_memberships_page(browser)

    if memberships_page.membership_exists(membership_name):
        return memberships_page

    memberships_page.create_membership(
        membership_name,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        FIRST_LOCATION_PRICE,
        FIRST_LOCATION_COMMISSION
    )
    memberships_page.search_membership(membership_name)
    memberships_page.wait_for_membership_row(membership_name)

    return memberships_page


def test_create_membership_required_name_validation(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.click_save_membership()

    assert not memberships_page.membership_name_input_is_valid()
    assert memberships_page.get_membership_name_validation_message() != ""


def test_create_vk_ma2_prepaid_membership(browser):

    memberships_page = create_membership_if_missing(browser)
    memberships_page.wait_for_list_loaded()
    memberships_page.search_membership(MEMBERSHIP_NAME)

    assert memberships_page.wait_for_membership_row(MEMBERSHIP_NAME).is_displayed()
    assert memberships_page.get_membership_type(MEMBERSHIP_NAME) == "Prepaid"
    assert memberships_page.get_membership_price(MEMBERSHIP_NAME) == VISIBLE_PRICE
    assert memberships_page.get_membership_status(MEMBERSHIP_NAME) == "Active"


def test_create_vk_ma2_does_not_duplicate_existing_membership(browser):

    memberships_page = create_membership_if_missing(browser)
    memberships_page.wait_for_list_loaded()
    memberships_page.search_membership(MEMBERSHIP_NAME)

    assert memberships_page.wait_for_membership_row(MEMBERSHIP_NAME).is_displayed()
    assert memberships_page.get_membership_type(MEMBERSHIP_NAME) == "Prepaid"
    assert memberships_page.get_membership_price(MEMBERSHIP_NAME) == VISIBLE_PRICE
    assert memberships_page.get_membership_status(MEMBERSHIP_NAME) == "Active"


def test_vk_ma2_membership_settings_persist(browser):

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


def test_vk_ma2_only_first_location_is_assigned(browser):

    memberships_page = create_membership_if_missing(browser)
    memberships_page.open_edit_membership(MEMBERSHIP_NAME)

    assert memberships_page.location_is_assigned_by_index(0)
    assert not memberships_page.location_is_assigned_by_index(1)
