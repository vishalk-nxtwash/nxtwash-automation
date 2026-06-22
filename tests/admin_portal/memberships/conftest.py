from pages.admin_portal.memberships_page import MembershipsPage
from tests.admin_portal._managed import managed_name
from tests.admin_portal._managed import managed_resource
from tests.admin_portal.admin_session import open_admin_path


EXISTING_MEMBERSHIP = "Plus membership"
MISSING_MEMBERSHIP = "membership-does-not-exist-automation"
MEMBERSHIP_NAME = "VK MA2"
RECURRING_MEMBERSHIP_NAME = "VK MR1"
UPDATED_MEMBERSHIP_NAME = "VK MA2 updated"
GLOBAL_PRICE = "15"
GLOBAL_COMMISSION = "2"
FIRST_LOCATION_PRICE = "20"
FIRST_LOCATION_COMMISSION = "3"
PREPAID_MONTHS = "1"
REDEEM_AS_SERVICE = "VK detail wash"
VISIBLE_PRICE = "$15.00"

# Known filter data (a membership assigned to a specific site on staging).
FILTER_SITE_QUERY = "carwash"
FILTER_SITE_LABEL = "VK Test carwash 2"
SITE_MEMBERSHIP = "VK MA1"


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
        memberships_page.click_save_membership()
        memberships_page.wait_for_list_loaded()
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
        memberships_page.click_save_membership()
        memberships_page.wait_for_list_loaded()
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
BASELINE_POINTS = "0"


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
    memberships_page.open_edit_membership(MANAGED_MEMBERSHIP)
    memberships_page.fill_membership_form(
        MANAGED_MEMBERSHIP,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        FIRST_LOCATION_PRICE,
        FIRST_LOCATION_COMMISSION,
        PREPAID_MONTHS
    )
    memberships_page.open_membership_settings()
    memberships_page.set_points_awarded(BASELINE_POINTS)
    memberships_page.set_barcode("")
    memberships_page.clear_applicable_discounts()
    memberships_page.open_membership_settings()
    memberships_page.click_save_membership()
    memberships_page.wait_for_list_loaded()

    return memberships_page


managed_membership = managed_resource(reset_managed_membership)
