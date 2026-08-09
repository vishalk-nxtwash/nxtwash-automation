from pages.admin_portal.memberships_page import MembershipsPage
from tests.admin_portal._managed import managed_name
from tests.admin_portal._managed import managed_resource
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._data import load as _load

_D = _load("memberships")

EXISTING_MEMBERSHIP        = _D["reference"]["existing_membership"]
MISSING_MEMBERSHIP         = _D["search"]["nonexistent"]
MEMBERSHIP_NAME            = _D["reference"]["existing_membership"]
RECURRING_MEMBERSHIP_NAME  = _D["reference"]["recurring_membership"]
UPDATED_MEMBERSHIP_NAME    = _D["updated"]["membership_name"]
GLOBAL_PRICE               = _D["template"]["global_price"]
GLOBAL_COMMISSION          = _D["template"]["global_commission"]
FIRST_LOCATION_PRICE       = _D["template"]["first_location_price"]
FIRST_LOCATION_COMMISSION  = _D["template"]["first_location_commission"]
PREPAID_MONTHS             = _D["template"]["prepaid_months"]
REDEEM_AS_SERVICE          = _D["reference"]["redeem_as_service"]
VISIBLE_PRICE              = _D["template"]["visible_price"]
FILTER_SITE_QUERY          = _D["reference"]["filter_site_query"]
FILTER_SITE_LABEL          = _D["reference"]["filter_site_label"]
SITE_MEMBERSHIP            = _D["reference"]["site_membership"]


BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


def open_memberships_page(browser):
    # Reset Redux Persist memberships filter BEFORE navigation so the page
    # loads with the default filter state (isActive:true).  The UI-based
    # clear_active_filters() handles the in-memory Redux state; this reset
    # is the belt-and-suspenders for the localStorage rehydration path.
    try:
        browser.execute_script("""
            try {
                var root = JSON.parse(localStorage.getItem('persist:root') || '{}');
                var tfr = JSON.parse(root.tableFilterReducer || '{}');
                var tf = tfr.tableFilters || {};
                tf.memberships = {
                    type: 0,
                    isActive: true,
                    membershipName: ''
                };
                tfr.tableFilters = tf;
                root.tableFilterReducer = JSON.stringify(tfr);
                localStorage.setItem('persist:root', JSON.stringify(root));
            } catch(e) {}
        """)
    except Exception:
        pass

    open_admin_path(browser, "/services/memberships")

    memberships_page = MembershipsPage(browser)
    memberships_page.wait_for_list_loaded()
    memberships_page.clear_active_filters()

    return memberships_page


def create_membership_if_missing(browser, membership_name=MEMBERSHIP_NAME):
    from selenium.common.exceptions import TimeoutException

    memberships_page = open_memberships_page(browser)

    if memberships_page.membership_exists(membership_name):
        memberships_page.open_edit_membership_if_visible(membership_name)
        memberships_page.ensure_active_switch_on()
        memberships_page.ensure_customer_portal_switch_on()
        memberships_page.save_and_return_to_list()
        memberships_page.clear_active_filters()
        return memberships_page

    # Not in active list — check inactive before trying to create (staging may
    # have deactivated it; creating a duplicate name would fail silently).
    # Fresh navigation resets the DOM state after membership_exists() timed out
    # so that _show_inactive_memberships() and search_membership() work cleanly.
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    memberships_page = open_memberships_page(browser)
    inactive_found = False
    try:
        memberships_page._show_inactive_memberships()
        memberships_page.search_membership(membership_name)
        locator = memberships_page.get_membership_row_locator(membership_name)
        try:
            WebDriverWait(memberships_page.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            inactive_found = True
        except TimeoutException:
            inactive_found = False

        if inactive_found:
            memberships_page.open_edit_membership_if_visible(membership_name)
            memberships_page.ensure_active_switch_on()
            memberships_page.ensure_customer_portal_switch_on()
            memberships_page.save_and_return_to_list()
    finally:
        memberships_page.clear_active_filters()

    if inactive_found:
        return memberships_page

    memberships_page.create_membership(
        membership_name,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        FIRST_LOCATION_PRICE,
        FIRST_LOCATION_COMMISSION
    )
    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(membership_name)
    memberships_page.wait_for_membership_row(membership_name)

    return memberships_page


def create_recurring_membership_if_missing(
    browser,
    membership_name=RECURRING_MEMBERSHIP_NAME
):
    from selenium.common.exceptions import TimeoutException

    memberships_page = open_memberships_page(browser)

    if memberships_page.membership_exists(membership_name):
        memberships_page.open_edit_membership_if_visible(membership_name)
        memberships_page.ensure_active_switch_on()
        memberships_page.ensure_customer_portal_switch_on()
        memberships_page.save_and_return_to_list()
        memberships_page.clear_active_filters()
        return memberships_page

    # Not in active list — check inactive before trying to create.
    # Fresh navigation resets DOM state after membership_exists() timed out.
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    memberships_page = open_memberships_page(browser)
    inactive_found = False
    try:
        memberships_page._show_inactive_memberships()
        memberships_page.search_membership(membership_name)
        locator = memberships_page.get_membership_row_locator(membership_name)
        try:
            WebDriverWait(memberships_page.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            inactive_found = True
        except TimeoutException:
            inactive_found = False

        if inactive_found:
            memberships_page.open_edit_membership_if_visible(membership_name)
            memberships_page.ensure_active_switch_on()
            memberships_page.ensure_customer_portal_switch_on()
            memberships_page.save_and_return_to_list()
    finally:
        memberships_page.clear_active_filters()

    if inactive_found:
        return memberships_page

    memberships_page.create_recurring_membership(
        membership_name,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        FIRST_LOCATION_PRICE,
        FIRST_LOCATION_COMMISSION
    )
    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(membership_name)
    memberships_page.wait_for_membership_row(membership_name)

    return memberships_page


# --- Managed (self-cleaning) membership ------------------------------------
# A dedicated record reset to baseline before and after each test that mutates
# it. Memberships cannot be deleted in the product, so teardown resets mutable
# fields instead of deleting. See tests/admin_portal/_managed.py.

MANAGED_MEMBERSHIP = managed_name("Membership")
# The server silently rejects changes to pointsAwarded for this membership
# (likely because it has active subscribers).  The field always reads back
# as "5" regardless of what is submitted, so the baseline matches that value.
BASELINE_POINTS = "5"


def reset_managed_membership(browser):
    """Ensure the managed membership exists and reset its mutable fields."""
    from selenium.common.exceptions import TimeoutException

    memberships_page = open_memberships_page(browser)

    # Check existence without calling membership_exists() (which re-triggers
    # wait_for_list_loaded, costing ~100 s on slow staging).  We are already
    # inside the list frame after open_memberships_page().
    memberships_page.search_membership(MANAGED_MEMBERSHIP)
    try:
        memberships_page.wait_for_membership_row(MANAGED_MEMBERSHIP)
        membership_found = True
    except TimeoutException:
        membership_found = False

    if not membership_found:
        # Not in active view — check inactive filter before creating.
        # Fresh navigation resets DOM state after wait_for_membership_row timed out.
        memberships_page = open_memberships_page(browser)
        try:
            memberships_page._show_inactive_memberships()
            memberships_page.search_membership(MANAGED_MEMBERSHIP)
            try:
                memberships_page.wait_for_membership_row(MANAGED_MEMBERSHIP)
                membership_found = True
            except TimeoutException:
                membership_found = False
        finally:
            if not membership_found:
                memberships_page.clear_active_filters()

    if not membership_found:
        memberships_page.create_membership(
            MANAGED_MEMBERSHIP,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION,
            FIRST_LOCATION_PRICE,
            FIRST_LOCATION_COMMISSION,
        )
        # create_membership() navigates into CREATE_FRAME; fresh navigation
        # restores LIST_FRAME before clear_active_filters() runs.
        memberships_page = open_memberships_page(browser)
        memberships_page.clear_active_filters()
        return memberships_page

    # Open edit directly from the current list state, skipping the extra
    # wait_for_list_loaded() call that open_edit_membership() would trigger.
    # try/finally guarantees clear_active_filters() runs even if the edit
    # or save raises (e.g. when open_edit_membership_if_visible internally
    # calls _show_inactive_memberships and an exception fires before save).
    try:
        memberships_page.open_edit_membership_if_visible(MANAGED_MEMBERSHIP)

        # Reset only the fields that tests actually mutate.  Skipping fill_membership_form()
        # (location grid ops) and clear_applicable_discounts() (Discount tab navigation)
        # saves ~4-6 min per fixture cycle on slow staging — the root cause of the 90 min
        # CI job timeout.
        memberships_page.ensure_active_switch_on()
        memberships_page.ensure_customer_portal_switch_on()
        memberships_page.set_global_price(GLOBAL_PRICE)
        memberships_page.set_global_commission(GLOBAL_COMMISSION)
        memberships_page.open_membership_settings()
        memberships_page.set_barcode("")
        memberships_page.save_and_return_to_list()
    finally:
        # Clear any residual filters (e.g. inactive-only from _show_inactive_memberships)
        # so the next test sees a clean default list view.
        memberships_page.clear_active_filters()

    return memberships_page


managed_membership = managed_resource(reset_managed_membership)
