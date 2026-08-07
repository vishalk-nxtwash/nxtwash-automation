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
from tests.admin_portal.memberships.conftest import managed_membership  # noqa: F401
from tests.admin_portal.memberships.conftest import open_memberships_page


LOG = logging.getLogger(__name__)
POINTS_AWARDED = "5"
APPLICABLE_DISCOUNT = "Plus discount"
MEMBERSHIP_DESCRIPTION = "VK automation test description"

# Managed-fixture tests run reset_managed_membership in setup AND teardown;
# each pass takes ~5 min, so the default 180s is not enough.
pytestmark = pytest.mark.timeout(900)


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
@pytest.mark.timeout(300)
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
    page.save_and_return_to_list()

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
    page.save_and_return_to_list()

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
    page.save_and_return_to_list()

    page.open_edit_membership(MANAGED_MEMBERSHIP)

    assert page.get_barcode_value() == barcode


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Membership Settings")
@allure.title("MB-TGL-004 Hide membership from customer portal")
@pytest.mark.regression
@pytest.mark.skip(reason="MB-TGL-004: managed_membership filter state leak — confirm same root cause as MB-EDT-009 on first run; deferred")
def test_edit_managed_membership_customer_portal_toggle_off(managed_membership):

    page = managed_membership
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.ensure_customer_portal_switch_off()
    page.save_and_return_to_list()

    page.open_edit_membership(MANAGED_MEMBERSHIP)

    assert not page.customer_portal_switch_is_on()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Membership Settings")
@allure.title("MB-TGL-003 Show membership on customer portal persists after save")
@pytest.mark.regression
def test_edit_managed_membership_customer_portal_toggle_on(managed_membership):

    page = managed_membership
    # Baseline is portal ON; turn it OFF first so the ON→save→verify cycle is real
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.ensure_customer_portal_switch_off()
    page.save_and_return_to_list()

    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.ensure_customer_portal_switch_on()
    page.save_and_return_to_list()

    page.open_edit_membership(MANAGED_MEMBERSHIP)

    assert page.customer_portal_switch_is_on()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Location Assignment")
@allure.title("MB-SIT-002/MB-EDT-006 Assign multiple membership locations")
@pytest.mark.regression
@pytest.mark.skip(reason="MB-SIT-002: managed_membership gw0/gw1 race causes filter state leak — 'No records available'; deferred until fixture serialised")
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
    page.save_and_return_to_list()

    page.open_edit_membership(MANAGED_MEMBERSHIP)

    assert page.location_is_assigned_by_index(0)
    assert page.location_is_assigned_by_index(1)
    assert page.get_location_price_by_index(1) == GLOBAL_PRICE
    assert page.get_location_commission_by_index(1) == GLOBAL_COMMISSION


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Discount Settings")
@allure.title("MB-DIS-001 Assign applicable discount persists after save")
@pytest.mark.regression
def test_applicable_discount_persists(managed_membership):

    page = managed_membership
    LOG.info("Assigning discount %s to %s", APPLICABLE_DISCOUNT, MANAGED_MEMBERSHIP)
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.select_applicable_discount(APPLICABLE_DISCOUNT)
    page.save_and_return_to_list()

    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.open_discount_settings()

    assert page.discount_is_selected(APPLICABLE_DISCOUNT)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Discount Settings")
@allure.title("MB-DIS-003 Remove applicable discount persists after save")
@pytest.mark.regression
def test_remove_applicable_discount_persists(managed_membership):

    page = managed_membership
    LOG.info(
        "Assigning then removing discount %s from %s",
        APPLICABLE_DISCOUNT,
        MANAGED_MEMBERSHIP
    )
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.select_applicable_discount(APPLICABLE_DISCOUNT)
    page.save_and_return_to_list()

    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.deselect_applicable_discount(APPLICABLE_DISCOUNT)
    page.save_and_return_to_list()

    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.open_discount_settings()

    assert not page.discount_is_selected(APPLICABLE_DISCOUNT)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Membership Settings")
@allure.title("MB-LMT-001 Limit membership toggle persists after save")
@pytest.mark.regression
def test_limit_membership_toggle_persists(managed_membership):
    """Limit membership switch survives a save. Cleans itself up in finally."""
    page = managed_membership
    LOG.info("Enabling Limit Membership toggle for %s", MANAGED_MEMBERSHIP)
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.ensure_limit_membership_switch_on()
    page.set_redemption_limits()
    page.save_and_return_to_list()

    try:
        page.open_edit_membership(MANAGED_MEMBERSHIP)
        assert page.limit_membership_switch_is_on()
    finally:
        # Still on the edit form opened above; no need to re-open.
        page.ensure_switch_off(page.LIMIT_MEMBERSHIP_SWITCH)
        page.save_and_return_to_list()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Membership Settings")
@allure.title("MB-DESC-001 Membership description saves and persists")
@pytest.mark.regression
def test_membership_description_saves(managed_membership):
    """Description field survives a save. Clears itself in finally."""
    page = managed_membership
    LOG.info(
        "Setting description '%s' on %s", MEMBERSHIP_DESCRIPTION, MANAGED_MEMBERSHIP
    )
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.set_membership_description(MEMBERSHIP_DESCRIPTION)
    page.save_and_return_to_list()

    try:
        page.open_edit_membership(MANAGED_MEMBERSHIP)
        assert page.get_membership_description_value() == MEMBERSHIP_DESCRIPTION
    finally:
        page.open_edit_membership(MANAGED_MEMBERSHIP)
        page.set_membership_description("")
        page.save_and_return_to_list()
