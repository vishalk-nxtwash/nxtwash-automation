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
    MANAGED_MEMBERSHIP_2,
    MEMBERSHIP_NAME,
    PREPAID_MONTHS,
    RECURRING_MEMBERSHIP_NAME,
    REDEEM_AS_SERVICE,
    VISIBLE_PRICE,
    create_membership_if_missing,
    create_recurring_membership_if_missing,
    managed_membership_2,  # noqa: F401
    open_memberships_page,
)


LOG = logging.getLogger(__name__)
pytestmark = pytest.mark.timeout(900)


@pytest.mark.smoke
@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MB-TYP-002 / MB-TGL-001 Verify creation of active Prepaid membership")
def test_create_prepaid_membership(browser):

    LOG.info("Creating/verifying prepaid membership: %s", MEMBERSHIP_NAME)
    memberships_page = create_membership_if_missing(browser)
    memberships_page.wait_for_list_loaded()
    memberships_page.search_membership(MEMBERSHIP_NAME)

    # create_membership_if_missing() may have just resaved this record's
    # baseline fields — give the search index more room than the method's
    # default (60s) before concluding it's missing. Confirmed in CI: under
    # full-suite concurrent load this failed at ~60s even though the record
    # genuinely existed (passed in 5s when run in isolation, no other load).
    assert memberships_page.wait_for_membership_row(
        MEMBERSHIP_NAME, attempts=8, per_try=15
    ).is_displayed()
    assert memberships_page.get_membership_type(MEMBERSHIP_NAME) == "Prepaid"
    assert memberships_page.get_membership_price(MEMBERSHIP_NAME) == VISIBLE_PRICE
    assert memberships_page.get_membership_status(MEMBERSHIP_NAME) == "Active"


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MB-TYP-001 Verify creation of Recurring membership")
@pytest.mark.xfail(
    strict=False,
    reason=(
        "BUG 8 (docs/bug_reports.md): location-assignment checkbox changes "
        "are not reliably saved, so the created membership can end up with "
        "no location assigned. Reports XPASS once fixed."
    ),
)
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
    assert memberships_page.assigned_location_names()


@pytest.mark.smoke
@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.title("MB-CRT-000 Creating a brand-new membership saves it (BUG 7 canary)")
@pytest.mark.xfail(
    strict=False,
    reason="BUG 7 (docs/bug_reports.md): Save on the Add-membership form sends no "
           "request at all on staging; editing works. Reports XPASS once fixed.",
)
def test_create_new_membership_saves(browser):
    # Uses the adoptable prefix: if create works, the record joins the pool the
    # managed fixture adopts from, instead of becoming dead clutter.
    from tests.admin_portal.memberships.conftest import ADOPTABLE_PREFIX
    name = "%s %s" % (ADOPTABLE_PREFIX, uuid.uuid4().hex[:6])
    memberships_page = open_memberships_page(browser)
    memberships_page.create_membership(
        name, GLOBAL_PRICE, GLOBAL_COMMISSION, FIRST_LOCATION_PRICE, FIRST_LOCATION_COMMISSION
    )
    assert name in open_memberships_page(browser).get_body_text()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MEM-CRUD-003/004/005/011/012/013/015/016/018 Persistence")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "BUG 8 (docs/bug_reports.md): location-assignment checkbox changes "
        "are not reliably saved (both assign and unassign) — stale "
        "locations on MEMBERSHIP_NAME accumulated from earlier runs can't "
        "be cleaned up via the UI, so more than one location can show "
        "assigned. Reports XPASS once fixed."
    ),
)
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
    assigned = memberships_page.assigned_location_names()
    assert len(assigned) == 1
    assert memberships_page.get_location_price(assigned[0]) == FIRST_LOCATION_PRICE
    assert (
        memberships_page.get_location_commission(assigned[0])
        == FIRST_LOCATION_COMMISSION
    )

    memberships_page.open_redemption_settings()

    assert memberships_page.assigned_redemption_location_names()
    assert REDEEM_AS_SERVICE.lower() in memberships_page.get_body_text().lower()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MB-TGL-002 Verify Active Service toggle blocks default-list visibility")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "MB-TGL-002: staging server saves membership as Active regardless of the "
        "Inactive selection on the create form. Same app bug as WP-TGL-002 / POS-CRT-007."
    ),
)
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


@pytest.mark.smoke
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
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "MB-EDT-009: reactivating this managed membership right after "
        "deactivating it does not stick — status reads back Inactive even "
        "after polling (wait_for_persisted_value), ruling out read-after-write "
        "lag. Same server-side lock on this record as the price/commission "
        "and MB-EDT-010 Active-status bugs (likely due to active subscribers)."
    ),
)
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
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "MB-EDT-010: staging server saves membership as Active regardless of the "
        "Inactive toggle on the edit form. Same app bug as WP-TGL-002 / POS-CRT-007."
    ),
)
def test_deactivate_membership(managed_membership_2):

    page = managed_membership_2
    page.open_edit_membership(MANAGED_MEMBERSHIP_2)
    page.ensure_active_switch_off()
    page.save_and_return_to_list()

    # Inactive memberships are hidden from the default grid — verify the row
    # does not appear after searching for it without any filter applied
    page.search_membership(MANAGED_MEMBERSHIP_2)
    assert MANAGED_MEMBERSHIP_2 not in page.get_body_text()
