import logging
import uuid

import allure
import pytest

from tests.admin_portal.memberships.conftest import (
    FIRST_LOCATION_COMMISSION,
    FIRST_LOCATION_PRICE,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    MANAGED_MEMBERSHIP,
    MEMBERSHIP_NAME,
    PREPAID_MONTHS,
    RECURRING_MEMBERSHIP_NAME,
    REDEEM_AS_SERVICE,
    VISIBLE_PRICE,
    create_membership_if_missing,
    create_recurring_membership_if_missing,
    open_memberships_page,
)


LOG = logging.getLogger(__name__)
pytestmark = pytest.mark.timeout(900)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MB-TYP-002 / MB-TGL-001 Verify creation of active Prepaid membership")
@pytest.mark.smoke
def test_create_prepaid_membership(browser):

    LOG.info("Creating/verifying prepaid membership: %s", MEMBERSHIP_NAME)
    memberships_page = create_membership_if_missing(browser)
    memberships_page.wait_for_list_loaded()
    memberships_page.search_membership(MEMBERSHIP_NAME)

    assert memberships_page.wait_for_membership_row(MEMBERSHIP_NAME).is_displayed()
    assert memberships_page.get_membership_type(MEMBERSHIP_NAME) == "Prepaid"
    assert memberships_page.get_membership_price(MEMBERSHIP_NAME) == VISIBLE_PRICE
    assert memberships_page.get_membership_status(MEMBERSHIP_NAME) == "Active"


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MB-TYP-001 Verify creation of Recurring membership")
@pytest.mark.smoke
def test_create_recurring_membership(browser):

    LOG.info(
        "Creating/verifying recurring membership: %s",
        RECURRING_MEMBERSHIP_NAME
    )
    memberships_page = create_recurring_membership_if_missing(browser)
    memberships_page.wait_for_list_loaded()
    memberships_page.search_membership(RECURRING_MEMBERSHIP_NAME)

    assert memberships_page.wait_for_membership_row(
        RECURRING_MEMBERSHIP_NAME
    ).is_displayed()
    assert (
        memberships_page.get_membership_type(RECURRING_MEMBERSHIP_NAME)
        == "Recurring"
    )
    assert (
        memberships_page.get_membership_price(RECURRING_MEMBERSHIP_NAME)
        == VISIBLE_PRICE
    )
    assert (
        memberships_page.get_membership_status(RECURRING_MEMBERSHIP_NAME)
        == "Active"
    )

    memberships_page.open_edit_membership(RECURRING_MEMBERSHIP_NAME)

    assert memberships_page.recurring_membership_type_is_selected()
    assert memberships_page.get_global_price_value() == GLOBAL_PRICE
    assert memberships_page.get_global_commission_value() == GLOBAL_COMMISSION
    assert memberships_page.location_is_assigned_by_index(0)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MEM-CRUD-003/004/005/011/012/013/015/016/018 Persistence")
@pytest.mark.regression
def test_membership_settings_persist(browser):

    LOG.info("Verifying membership settings persist: %s", MEMBERSHIP_NAME)
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


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MB-TGL-002 Verify Active Service toggle blocks default-list visibility")
@pytest.mark.regression
def test_create_inactive_membership(browser):

    membership_name = "VK inactive %s" % uuid.uuid4().hex[:6]
    LOG.info("Creating inactive membership: %s", membership_name)
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.fill_membership_form(
        membership_name,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        FIRST_LOCATION_PRICE,
        FIRST_LOCATION_COMMISSION,
        PREPAID_MONTHS
    )
    memberships_page.open_membership_settings()
    memberships_page.ensure_active_switch_off()
    memberships_page.save_and_return_to_list()
    memberships_page.search_membership(membership_name)

    assert memberships_page.search_input_value() == membership_name
    assert membership_name not in memberships_page.get_body_text()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MEM-CRUD-008 Verify Cancel button on create screen")
@pytest.mark.regression
def test_cancel_create_membership_discards_unsaved_changes(browser):

    membership_name = "VK cancel %s" % uuid.uuid4().hex[:6]
    LOG.info("Validating cancel discards new membership: %s", membership_name)
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.enter_membership_name(membership_name)
    memberships_page.click_cancel()
    memberships_page.search_membership(membership_name)

    assert memberships_page.search_input_value() == membership_name
    assert membership_name not in memberships_page.get_body_text()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MB-EDT-009 Activate membership updates Status in list")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.skip(reason="MB-EDT-009: inactive filter left active after re-activation save — clear_active_filters not called in managed_membership restore; deferred")
@pytest.mark.xdist_group("managed_membership")
def test_activate_membership(managed_membership):

    page = managed_membership
    # Deactivate first so we have something to activate
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.ensure_active_switch_off()
    page.save_and_return_to_list()

    # Re-activate — open_edit_membership uses inactive-filter fallback
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.ensure_active_switch_on()
    page.save_and_return_to_list()

    page.search_membership(MANAGED_MEMBERSHIP)
    assert page.wait_for_membership_row(MANAGED_MEMBERSHIP).is_displayed()
    assert page.get_membership_status(MANAGED_MEMBERSHIP) == "Active"


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MB-EDT-010 Deactivate membership hides it from the default list")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.xdist_group("managed_membership")
@pytest.mark.xfail(
    strict=False,
    reason=(
        "MB-EDT-010: 29 AUTOTEST Membership duplicates exist on staging — deactivating "
        "one does not clear the name from search results while 28 active copies remain. "
        "Remove xfail after staging cleanup."
    ),
)
def test_deactivate_membership(managed_membership):

    page = managed_membership
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.ensure_active_switch_off()
    page.save_and_return_to_list()

    # Inactive memberships are hidden from the default grid — verify the row
    # does not appear after searching for it without any filter applied
    page.search_membership(MANAGED_MEMBERSHIP)
    assert MANAGED_MEMBERSHIP not in page.get_body_text()
