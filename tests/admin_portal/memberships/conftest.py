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


# Prefix of leftover per-run memberships that any create-flow helper below may
# adopt in place of creating a fresh one (see _adopt_leftover_membership).
ADOPTABLE_PREFIX = "VK decimal"


def _needs_baseline_resave(memberships_page):
    """True if the open edit form's global price/commission differ from baseline.

    create_membership_if_missing()/create_recurring_membership_if_missing()
    run on every test using them, every run — re-saving the form unconditionally
    (as before) pays a full fill+save+redirect cycle even on the overwhelming
    majority of runs where the record already matches. This check lets callers
    skip straight back to the list instead.
    """
    return (
        memberships_page.get_global_price_value() != GLOBAL_PRICE
        or memberships_page.get_global_commission_value() != GLOBAL_COMMISSION
    )

def open_memberships_page(browser):

    open_admin_path(browser, "/services/memberships")

    memberships_page = MembershipsPage(browser)
    memberships_page.wait_for_list_loaded()
    memberships_page.clear_active_filters()

    return memberships_page


def _adopt_leftover_membership(browser, membership_name, fill_fn, attempts=3):
    """Rename a leftover "VK decimal ..." membership into ``membership_name``.

    Creating a membership is broken on staging (Save sends no request at all
    — BUG 7, docs/bug_reports.md) but EDITING works, so every create-flow
    helper in this file adopts a leftover uniquely-named test membership
    (created by earlier runs, never cleaned up — product has no delete)
    instead of calling create_membership()/create_recurring_membership().

    ``fill_fn`` is one of MembershipsPage.fill_membership_form /
    fill_recurring_membership_form, called as ``fill_fn(membership_name, ...)``
    on the opened edit page to both rename and fill it.

    Returns the list-page MembershipsPage on success, or None if no leftover
    was found (caller falls back to the normal create call, in case BUG 7
    ever gets fixed).

    Wrapped in a bounded outer retry: multiple xdist workers can each pick
    the SAME leftover record — the first ``adoptable`` match of their own
    fresh search — and race to rename it to their own different target
    name; nothing locks this across workers. A lost race surfaces either as
    an exception opening/editing a record another worker already renamed
    out from under us, or as the post-rename verification below never
    finding our target name. Either way, re-searching from scratch for the
    retry picks whatever's left — the record we raced over no longer
    matches ADOPTABLE_PREFIX once someone else has renamed it — so
    retrying the whole attempt, not just the verification, recovers
    cleanly instead of failing on what was just bad luck.
    """
    import time as _time

    last_error = None
    for _ in range(attempts):
        memberships_page = open_memberships_page(browser)
        memberships_page.search_membership(ADOPTABLE_PREFIX)
        adoptable = [
            line for line in memberships_page.get_body_text().split("\n")
            if line.startswith(ADOPTABLE_PREFIX)
        ]
        if not adoptable:
            return None

        try:
            memberships_page = open_memberships_page(browser)
            memberships_page.open_edit_membership(adoptable[0])
            fill_fn(memberships_page, membership_name)
            memberships_page.save_and_return_to_list()
        except Exception as error:  # noqa: BLE001 — likely lost a race, retry fresh
            last_error = error
            continue

        # Search lags behind a rename (the search index updates later), and a
        # missed lookup here would make the next run adopt a second leftover.
        # Confirm on the unfiltered list instead, retrying for up to ~60 s.
        for _ in range(6):
            memberships_page = open_memberships_page(browser)
            if membership_name in memberships_page.get_body_text():
                return memberships_page
            _time.sleep(10)
        last_error = AssertionError(
            "Adopted membership '%s' not visible on the list after rename" % membership_name
        )

    raise last_error


def create_membership_if_missing(browser, membership_name=MEMBERSHIP_NAME):
    from selenium.common.exceptions import TimeoutException

    memberships_page = open_memberships_page(browser)

    if memberships_page.membership_exists(membership_name):
        memberships_page = open_memberships_page(browser)
        memberships_page.open_edit_membership(membership_name)
        if _needs_baseline_resave(memberships_page):
            memberships_page.fill_membership_form(
                membership_name,
                GLOBAL_PRICE,
                GLOBAL_COMMISSION,
                FIRST_LOCATION_PRICE,
                FIRST_LOCATION_COMMISSION
            )
            memberships_page.save_and_return_to_list()
        else:
            memberships_page = open_memberships_page(browser)
        memberships_page.clear_active_filters()
        return memberships_page

    # Not in active list — check inactive before trying to create (staging may
    # have deactivated it; creating a duplicate name would fail silently).
    # Use a short 10s wait so we don't burn 60s when the record simply doesn't exist.
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

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
        memberships_page.open_edit_membership(membership_name)
        if _needs_baseline_resave(memberships_page):
            memberships_page.fill_membership_form(
                membership_name,
                GLOBAL_PRICE,
                GLOBAL_COMMISSION,
                FIRST_LOCATION_PRICE,
                FIRST_LOCATION_COMMISSION
            )
            memberships_page.save_and_return_to_list()
        else:
            memberships_page = open_memberships_page(browser)
        memberships_page.clear_active_filters()
        return memberships_page

    def _fill(page, name):
        page.fill_membership_form(
            name,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION,
            FIRST_LOCATION_PRICE,
            FIRST_LOCATION_COMMISSION
        )

    adopted = _adopt_leftover_membership(browser, membership_name, _fill)
    if adopted is not None:
        return adopted

    try:
        memberships_page.create_membership(
            membership_name,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION,
            FIRST_LOCATION_PRICE,
            FIRST_LOCATION_COMMISSION
        )
    except Exception:
        # No locking across xdist workers — another worker can create this
        # exact membership between the checks above and this call (same
        # race already fixed for customers/service_categories). If it
        # exists now, adopt it instead of failing the test.
        memberships_page = open_memberships_page(browser)
        if memberships_page.membership_exists(membership_name):
            memberships_page = open_memberships_page(browser)
            memberships_page.search_membership(membership_name)
            memberships_page.wait_for_membership_row(membership_name)
            return memberships_page
        raise
    # Fresh navigation clears the inactive-filter chip left by _show_inactive_memberships().
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
        memberships_page = open_memberships_page(browser)
        memberships_page.open_edit_membership(membership_name)
        if _needs_baseline_resave(memberships_page):
            memberships_page.fill_recurring_membership_form(
                membership_name,
                GLOBAL_PRICE,
                GLOBAL_COMMISSION,
                FIRST_LOCATION_PRICE,
                FIRST_LOCATION_COMMISSION
            )
            memberships_page.save_and_return_to_list()
        else:
            memberships_page = open_memberships_page(browser)
        memberships_page.clear_active_filters()
        return memberships_page

    # Not in active list — check inactive before trying to create.
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

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
        memberships_page.open_edit_membership(membership_name)
        if _needs_baseline_resave(memberships_page):
            memberships_page.fill_recurring_membership_form(
                membership_name,
                GLOBAL_PRICE,
                GLOBAL_COMMISSION,
                FIRST_LOCATION_PRICE,
                FIRST_LOCATION_COMMISSION
            )
            memberships_page.save_and_return_to_list()
        else:
            memberships_page = open_memberships_page(browser)
        memberships_page.clear_active_filters()
        return memberships_page

    def _fill_recurring(page, name):
        page.fill_recurring_membership_form(
            name,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION,
            FIRST_LOCATION_PRICE,
            FIRST_LOCATION_COMMISSION
        )

    adopted = _adopt_leftover_membership(browser, membership_name, _fill_recurring)
    if adopted is not None:
        return adopted

    try:
        memberships_page.create_recurring_membership(
            membership_name,
            GLOBAL_PRICE,
            GLOBAL_COMMISSION,
            FIRST_LOCATION_PRICE,
            FIRST_LOCATION_COMMISSION
        )
    except Exception:
        # Same race as create_membership_if_missing's create_membership()
        # call above — adopt it if another worker got there first.
        memberships_page = open_memberships_page(browser)
        if memberships_page.membership_exists(membership_name):
            memberships_page = open_memberships_page(browser)
            memberships_page.search_membership(membership_name)
            memberships_page.wait_for_membership_row(membership_name)
            return memberships_page
        raise
    # Fresh navigation clears the inactive-filter chip left by _show_inactive_memberships().
    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(membership_name)
    memberships_page.wait_for_membership_row(membership_name)

    return memberships_page


# --- Managed (self-cleaning) membership ------------------------------------
# A dedicated record reset to baseline before and after each test that mutates
# it. Memberships cannot be deleted in the product, so teardown resets mutable
# fields instead of deleting. See tests/admin_portal/_managed.py.

MANAGED_MEMBERSHIP = managed_name("Membership")
# Second, independent managed record — splits the managed_membership test
# group across two xdist workers instead of forcing all of them onto one
# (see reset_managed_membership's membership_name parameter). Tests on
# MANAGED_MEMBERSHIP and tests on MANAGED_MEMBERSHIP_2 never touch the same
# record, so they can run fully in parallel with each other.
MANAGED_MEMBERSHIP_2 = managed_name("Membership 2")
# The server silently rejects changes to pointsAwarded for this membership
# (likely because it has active subscribers).  The field always reads back
# as "5" regardless of what is submitted, so the baseline matches that value.
BASELINE_POINTS = "5"


def _managed_membership_matches_baseline(memberships_page):
    """True if every field reset_managed_membership() would touch is already
    at baseline, on the currently-open edit form for MANAGED_MEMBERSHIP.

    reset_managed_membership() runs twice per managed_membership test (setup
    and teardown), and the fill+save cycle it guards is the single most
    expensive thing in the module. Skipping it is only safe if every field it
    would otherwise reset already matches — so this checks each one
    individually rather than assuming "looks fine" from a subset. Anything
    not covered here (should a new mutating test add a field) falls back to
    the full reset by design: this function must return False, not raise, on
    anything it isn't sure about.
    """
    if memberships_page.get_global_price_value() != GLOBAL_PRICE:
        return False
    if memberships_page.get_global_commission_value() != GLOBAL_COMMISSION:
        return False
    if memberships_page.get_barcode_value():
        return False
    if memberships_page.get_points_awarded_value() != BASELINE_POINTS:
        return False
    if not memberships_page.prepaid_membership_type_is_selected():
        return False
    if memberships_page.get_prepaid_months_value() != PREPAID_MONTHS:
        return False
    if not memberships_page.active_switch_is_on():
        return False
    if not memberships_page.customer_portal_switch_is_on():
        return False
    if memberships_page.limit_membership_switch_is_on():
        return False

    first_location_name = memberships_page.get_location_name_by_index(0)
    if memberships_page.get_location_price(first_location_name) != FIRST_LOCATION_PRICE:
        return False
    if memberships_page.get_location_commission(first_location_name) != FIRST_LOCATION_COMMISSION:
        return False

    if memberships_page.has_applicable_discounts():
        return False

    return True


def reset_managed_membership(browser, membership_name=MANAGED_MEMBERSHIP):
    """Ensure the managed membership exists and reset its mutable fields.

    membership_name defaults to the original single shared record
    (MANAGED_MEMBERSHIP) but accepts any managed-record name — see
    MANAGED_MEMBERSHIP_2 — so the same reset logic serves multiple
    independent records. Splitting the 17 managed_membership tests across
    two records lets them run on two xdist workers instead of one long
    serialized queue (they still can't share a record — see
    feedback_ci_managed_fixture_parallel_race — but two independent records
    race nothing).
    """
    from selenium.common.exceptions import TimeoutException

    memberships_page = open_memberships_page(browser)

    # Check existence without calling membership_exists() (which re-triggers
    # wait_for_list_loaded, costing ~100 s on slow staging).  We are already
    # inside the list frame after open_memberships_page().
    memberships_page.search_membership(membership_name)
    try:
        memberships_page.wait_for_membership_row(membership_name)
        membership_found = True
    except TimeoutException:
        membership_found = False

    if not membership_found:
        # Not in active view — check inactive filter before creating.
        memberships_page._show_inactive_memberships()
        memberships_page.search_membership(membership_name)
        try:
            memberships_page.wait_for_membership_row(membership_name)
            membership_found = True
        except TimeoutException:
            membership_found = False

    if not membership_found:
        def _fill(page, name):
            page.fill_membership_form(
                name,
                GLOBAL_PRICE,
                GLOBAL_COMMISSION,
                FIRST_LOCATION_PRICE,
                FIRST_LOCATION_COMMISSION,
            )

        adopted = _adopt_leftover_membership(browser, membership_name, _fill)
        if adopted is not None:
            # Adoption already renamed + filled it to baseline via _fill above.
            return adopted

        try:
            memberships_page.create_membership(
                membership_name,
                GLOBAL_PRICE,
                GLOBAL_COMMISSION,
                FIRST_LOCATION_PRICE,
                FIRST_LOCATION_COMMISSION,
            )
        except Exception:
            # MANAGED_MEMBERSHIP / MANAGED_MEMBERSHIP_2 are split into two
            # independent records specifically so managed-membership tests
            # never race each other — this path is only reachable by
            # construction if something outside that pair claims the same
            # name, which doesn't happen today. Kept consistent with the
            # same adopt-on-race handling used everywhere else anyway.
            memberships_page = open_memberships_page(browser)
            if memberships_page.membership_exists(membership_name):
                memberships_page = open_memberships_page(browser)
                memberships_page.clear_active_filters()
                return memberships_page
            raise
        # create_membership() saves and returns to list — membership is at
        # baseline from fill_membership_form(), so reset is complete.
        memberships_page.clear_active_filters()
        return memberships_page

    # Open edit directly from the current list state, skipping the extra
    # wait_for_list_loaded() call that open_edit_membership() would trigger.
    # This saves ~100 s per reset on slow staging.
    memberships_page.open_edit_membership_if_visible(membership_name)

    if _managed_membership_matches_baseline(memberships_page):
        # Nothing to reset — skip the fill+save cycle entirely (this runs
        # twice per managed_membership test, setup and teardown, and the
        # save-and-redirect wait is the single most expensive step in the
        # module). Re-navigate to the list fresh rather than relying on
        # whatever tab the baseline check left active.
        memberships_page = open_memberships_page(browser)
        memberships_page.clear_active_filters()
        return memberships_page

    # Reset all mutable fields touched by tests back to a known baseline.
    # clear_applicable_discounts() navigates to the Discount tab, so do all
    # Discount tab work before navigating to Settings — that way the Settings
    # tab is the LAST active tab when save is called, keeping any field edits
    # made there in React Hook Form's live state.
    memberships_page.fill_membership_form(
        membership_name,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        FIRST_LOCATION_PRICE,
        FIRST_LOCATION_COMMISSION,
        PREPAID_MONTHS
    )
    memberships_page.clear_applicable_discounts()
    memberships_page.open_membership_settings()
    memberships_page.set_barcode("")
    # Explicitly restore points_awarded — do not rely on the server "always"
    # reverting it to baseline. That assumption broke: the field was found
    # persistently blank on staging even with no other job touching the
    # record, because nothing here ever wrote a real value back to it once
    # it went blank (memberships cannot be deleted, so a bad value sticks
    # forever otherwise).
    memberships_page.set_points_awarded(BASELINE_POINTS)
    memberships_page.save_and_return_to_list()
    # Clear any residual filters (e.g. inactive-only from _show_inactive_memberships)
    # so the next test sees a clean default list view.
    memberships_page.clear_active_filters()

    return memberships_page


managed_membership = managed_resource(reset_managed_membership)
managed_membership_2 = managed_resource(
    lambda browser: reset_managed_membership(browser, MANAGED_MEMBERSHIP_2)
)
