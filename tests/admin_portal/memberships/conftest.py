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

    open_admin_path(browser, "/services/memberships")

    memberships_page = MembershipsPage(browser)
    memberships_page.wait_for_list_loaded()
    memberships_page.clear_active_filters()

    return memberships_page


def create_membership_if_missing(browser, membership_name=MEMBERSHIP_NAME):

    memberships_page = open_memberships_page(browser)

    if memberships_page.membership_exists(membership_name):
        memberships_page = open_memberships_page(browser)
        memberships_page.open_edit_membership(membership_name)
        memberships_page.fill_membership_form(
            membership_name,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION,
            FIRST_LOCATION_PRICE,
            FIRST_LOCATION_COMMISSION
        )
        memberships_page.save_and_return_to_list()
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


def create_recurring_membership_if_missing(
    browser,
    membership_name=RECURRING_MEMBERSHIP_NAME
):

    memberships_page = open_memberships_page(browser)

    if memberships_page.membership_exists(membership_name):
        memberships_page = open_memberships_page(browser)
        memberships_page.open_edit_membership(membership_name)
        memberships_page.fill_recurring_membership_form(
            membership_name,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION,
            FIRST_LOCATION_PRICE,
            FIRST_LOCATION_COMMISSION
        )
        memberships_page.save_and_return_to_list()
        return memberships_page

    memberships_page.create_recurring_membership(
        membership_name,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        FIRST_LOCATION_PRICE,
        FIRST_LOCATION_COMMISSION
    )
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
    memberships_page = open_memberships_page(browser)

    if not memberships_page.membership_exists(MANAGED_MEMBERSHIP):
        memberships_page.create_membership(
            MANAGED_MEMBERSHIP,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION,
            FIRST_LOCATION_PRICE,
            FIRST_LOCATION_COMMISSION
        )

    # Reset all mutable fields touched by tests back to a known baseline.
    # clear_applicable_discounts() navigates to the Discount tab, so do all
    # Discount tab work before navigating to Settings — that way the Settings
    # tab is the LAST active tab when save is called, keeping any field edits
    # made there in React Hook Form's live state.
    memberships_page.open_edit_membership(MANAGED_MEMBERSHIP)
    memberships_page.fill_membership_form(
        MANAGED_MEMBERSHIP,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        FIRST_LOCATION_PRICE,
        FIRST_LOCATION_COMMISSION,
        PREPAID_MONTHS
    )
    memberships_page.clear_applicable_discounts()
    memberships_page.open_membership_settings()
    memberships_page.set_barcode("")
    memberships_page.save_and_return_to_list()

    return memberships_page


managed_membership = managed_resource(reset_managed_membership)
