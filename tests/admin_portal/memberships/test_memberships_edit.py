import logging
import uuid

import allure
import pytest

from tests.admin_portal.memberships.conftest import MEMBERSHIP_NAME
from tests.admin_portal.memberships.conftest import FIRST_LOCATION_COMMISSION
from tests.admin_portal.memberships.conftest import FIRST_LOCATION_PRICE
from tests.admin_portal.memberships.conftest import GLOBAL_COMMISSION
from tests.admin_portal.memberships.conftest import GLOBAL_PRICE
from tests.admin_portal.memberships.conftest import MANAGED_MEMBERSHIP
from tests.admin_portal.memberships.conftest import create_membership_if_missing
from tests.admin_portal.memberships.conftest import open_memberships_page


LOG = logging.getLogger(__name__)
POINTS_AWARDED = "5"
APPLICABLE_DISCOUNT = "Plus discount"


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MB-EDT-005/MB-EDT-008 Edit loyalty points and discount")
@pytest.mark.regression
def test_edit_membership_loyalty_points_and_discount(browser):

    LOG.info("Editing membership loyalty points and discount: %s", MEMBERSHIP_NAME)
    memberships_page = create_membership_if_missing(browser)
    memberships_page.update_loyalty_points_and_discount(
        MEMBERSHIP_NAME,
        POINTS_AWARDED,
        APPLICABLE_DISCOUNT
    )

    memberships_page.open_edit_membership(MEMBERSHIP_NAME)

    assert memberships_page.get_points_awarded_value() == POINTS_AWARDED

    memberships_page.open_discount_settings()

    assert memberships_page.discount_is_selected(APPLICABLE_DISCOUNT)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MB-EDT-001 Verify Edit Membership functionality")
@pytest.mark.regression
def test_edit_membership_name_and_restore(browser):

    LOG.info(
        "Editing membership name from %s and restoring it",
        MEMBERSHIP_NAME,
    )
    updated_membership_name = "%s edit %s" % (
        MEMBERSHIP_NAME,
        uuid.uuid4().hex[:6]
    )
    memberships_page = create_membership_if_missing(browser)

    try:
        memberships_page.update_membership_name(
            MEMBERSHIP_NAME,
            updated_membership_name
        )
        memberships_page.search_membership(updated_membership_name)

        assert memberships_page.wait_for_membership_row(
            updated_membership_name
        ).is_displayed()
        assert updated_membership_name in memberships_page.get_body_text()

        memberships_page.open_edit_membership(updated_membership_name)

        assert memberships_page.get_membership_name_value() == updated_membership_name

    finally:
        memberships_page = open_memberships_page(browser)
        if memberships_page.membership_exists(updated_membership_name):
            memberships_page.update_membership_name(
                updated_membership_name,
                MEMBERSHIP_NAME
            )


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Membership Settings")
@allure.title("MB-TYP-003 Edit membership type")
@pytest.mark.regression
def test_edit_managed_membership_type(managed_membership):

    page = managed_membership
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.select_recurring_membership_type()
    page.click_save_membership()
    page.wait_for_list_loaded()

    page.open_edit_membership(MANAGED_MEMBERSHIP)

    assert page.recurring_membership_type_is_selected()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Membership Settings")
@allure.title("MB-EDT-003/MB-EDT-004 Edit global price and commission")
@pytest.mark.regression
def test_edit_managed_membership_global_price_and_commission(managed_membership):

    page = managed_membership
    updated_price = "25"
    updated_commission = "4"

    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.set_global_price(updated_price)
    page.set_global_commission(updated_commission)
    page.click_save_membership()
    page.wait_for_list_loaded()

    page.open_edit_membership(MANAGED_MEMBERSHIP)

    assert page.get_global_price_value() == updated_price
    assert page.get_global_commission_value() == updated_commission


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Membership Settings")
@allure.title("MB-BAR-001/MB-BAR-002 Membership barcode can be added and cleared")
@pytest.mark.regression
def test_edit_managed_membership_barcode_persists(managed_membership):

    page = managed_membership
    barcode = "AUTO-MB-BAR-001"

    page.open_edit_membership(MANAGED_MEMBERSHIP)
    assert page.get_barcode_value() == ""

    page.set_barcode(barcode)
    page.click_save_membership()
    page.wait_for_list_loaded()

    page.open_edit_membership(MANAGED_MEMBERSHIP)

    assert page.get_barcode_value() == barcode


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Membership Settings")
@allure.title("MB-TGL-004 Hide membership from customer portal")
@pytest.mark.regression
def test_edit_managed_membership_customer_portal_toggle_off(managed_membership):

    page = managed_membership
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.ensure_customer_portal_switch_off()
    page.click_save_membership()
    page.wait_for_list_loaded()

    page.open_edit_membership(MANAGED_MEMBERSHIP)

    assert not page.customer_portal_switch_is_on()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Location Assignment")
@allure.title("MB-SIT-002/MB-EDT-006 Assign multiple membership locations")
@pytest.mark.regression
def test_edit_managed_membership_assigns_multiple_locations(managed_membership):

    page = managed_membership
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.assign_location_by_index_with_price_and_commission(
        0,
        FIRST_LOCATION_PRICE,
        FIRST_LOCATION_COMMISSION
    )
    page.assign_location_by_index_with_price_and_commission(
        1,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION
    )
    page.set_location_price_and_commission_by_index(1, GLOBAL_PRICE, GLOBAL_COMMISSION)
    page.click_save_membership()
    page.wait_for_list_loaded()

    page.open_edit_membership(MANAGED_MEMBERSHIP)

    assert page.location_is_assigned_by_index(0)
    assert page.location_is_assigned_by_index(1)
    assert page.get_location_price_by_index(1) == GLOBAL_PRICE
    assert page.get_location_commission_by_index(1) == GLOBAL_COMMISSION
