from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.admin_portal.service_categories_page import ServiceCategoriesPage
from tests.admin_portal._managed import managed_name
from tests.admin_portal._managed import managed_resource
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._data import load as _load

_D = _load("service_categories")

CATEGORY_NAME          = _D["reference"]["active_category"]
INACTIVE_CATEGORY_NAME = _D["reference"]["inactive_category"]
MISSING_CATEGORY       = _D["search"]["nonexistent"]
UPDATED_CATEGORY_NAME  = _D["updated"]["category_name"]

BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def open_service_categories_page(browser):

    open_admin_path(browser, "/services/serviceCategories")

    page = ServiceCategoriesPage(browser)
    page.wait_for_list_loaded()

    return page


def create_category_if_missing(browser, category_name=CATEGORY_NAME):
    """Ensure an active category exists and return the page."""
    page = open_service_categories_page(browser)

    if page.category_exists(category_name):
        return page

    page.create_category(category_name)
    page.search_category(category_name)
    page.wait_for_category_row(category_name)

    return page


def create_inactive_category_if_missing(browser, category_name=INACTIVE_CATEGORY_NAME):
    """Ensure an inactive category exists and is actually inactive.

    If the category was accidentally activated by a previous test it is
    deactivated before returning, so callers always get a truly inactive record.
    """
    page = open_service_categories_page(browser)

    if not page.category_exists(category_name):
        page.create_inactive_category(category_name)
        return page

    if page.get_category_status(category_name) != "Inactive":
        page.open_edit_category(category_name)
        page.ensure_active_switch_off()
        page.save_changes_and_return_to_list()

    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


# ------------------------------------------------------------------ Managed

MANAGED_CATEGORY = managed_name("Category")
MANAGED_CATEGORY_EDITED = "%s edited" % MANAGED_CATEGORY


def _consolidate_duplicate_category(page, name):
    """If more than one row is named exactly `name`, rename every extra one
    out of the way, keeping just the first (by id) as canonical.

    Defends against duplicate-creation paths this fixture can't fully
    prevent on its own — confirmed in CI: extra "CI-AUTOTEST Category"
    records sporadically appear by a mechanism not yet root-caused, each
    one permanently blocking any future rename back to the base name
    (no delete UI). Self-heals on every setup/teardown instead of
    requiring every possible creation path to be found and fixed first.

    Resolves every matching row's id up front from the href (not by
    position) before touching anything, then edits each EXTRA id directly
    by URL — never re-queries row order mid-cleanup, which previously
    caused the "keeper" to get caught by a later iteration when the grid
    re-sorted after a rename (confirmed in CI: wiped the canonical record
    to zero).
    """
    import re
    import time

    page.search_category(name)
    rows = page.get_visible_category_rows()
    ids = []
    for row in rows:
        try:
            row_name = row.find_element(
                By.XPATH, ".//*[@data-props-id='categoryName']"
            ).text.strip()
        except Exception:  # noqa: BLE001
            continue
        if row_name != name:
            continue
        try:
            href = row.find_element(
                By.XPATH, ".//*[normalize-space()='Edit']/ancestor::*[self::a or self::button][1]"
            ).get_attribute("href")
        except Exception:  # noqa: BLE001
            continue
        match = re.search(r"/edit/(\d+)", href or "")
        if match and match.group(1) not in ids:
            ids.append(match.group(1))

    if len(ids) <= 1:
        return

    origin = page.driver.execute_script("return window.location.origin")
    for extra_id in ids[1:]:
        page.driver.get("%s/services/serviceCategories/edit/%s" % (origin, extra_id))
        page.wait_for_edit_loaded()
        page.enter_category_name("ZZ-DUP-%s-%d-DO-NOT-USE" % (extra_id, int(time.time() * 1000)))
        page.save_changes_and_return_to_list()
    page.search_category(name)


def reset_managed_category(browser):
    """Ensure the managed category exists at its baseline name and is Active.

    Handles three cases:
    - Renamed by a test   → rename back to baseline
    - Does not exist yet  → create it
    - Deactivated by test → re-activate it
    """
    page = open_service_categories_page(browser)
    _consolidate_duplicate_category(page, MANAGED_CATEGORY)
    _consolidate_duplicate_category(page, MANAGED_CATEGORY_EDITED)

    if page.category_exists(MANAGED_CATEGORY_EDITED):
        if page.category_exists(MANAGED_CATEGORY):
            # Split identity: one id holds the base name, a DIFFERENT id is
            # stuck on "...edited" — not caught by _consolidate_duplicate_category
            # above, which only looks for multiple rows sharing ONE exact
            # name. Confirmed in CI (full-suite run, heavier staging load):
            # the base-name holder is already the canonical survivor, so the
            # "edited" one is the orphan — park it instead of attempting a
            # rename that's guaranteed to collide with "already exists".
            import time as _time
            page.open_edit_category(MANAGED_CATEGORY_EDITED)
            page.enter_category_name(
                "ZZ-ORPHAN-edited-%d-DO-NOT-USE" % int(_time.time() * 1000)
            )
            page.save_changes_and_return_to_list()
        else:
            # Rename back — bypass update_category_name to avoid open_edit_category's
            # own inactive-filter fallback interfering with this reopen; the
            # deterministic save-and-return (waits for the app's own save signal,
            # then re-navigates) survives that regardless.
            try:
                page.open_edit_category(MANAGED_CATEGORY_EDITED)
                page.enter_category_name(MANAGED_CATEGORY)
                page.ensure_active_switch_on()
                page.save_changes_and_return_to_list()
            except RuntimeError:
                # Lost a race against something else that just claimed the
                # base name between the category_exists() check above and
                # this save — park this one as an orphan rather than
                # propagate; the next reset() call sees MANAGED_CATEGORY
                # already satisfied and moves on.
                pass
    elif not page.category_exists(MANAGED_CATEGORY):
        # category_exists()'s 10s probe (bound short deliberately for the
        # read-after-write fallback paths elsewhere) can false-negative on
        # genuine backend lag — confirmed in CI: it fabricated 2 duplicate
        # "CI-AUTOTEST Category" records in a single run this way. Creating
        # one here is unrecoverable staging pollution (no delete UI), so
        # give it one longer, final look before concluding it's really gone.
        page.search_category(MANAGED_CATEGORY)
        try:
            page.wait_for_category_row(MANAGED_CATEGORY, timeout=40)
            return page
        except TimeoutException:
            pass
        page.create_category(MANAGED_CATEGORY)
        page.search_category(MANAGED_CATEGORY)
        page.wait_for_category_row(MANAGED_CATEGORY)
        return page

    # Restore active status if a test deactivated the category. Best-effort:
    # this step depends on the same shared staging record's read-after-write
    # lag that's been the recurring theme in this fixture (confirmed in CI,
    # sometimes 40s+). A paced retry (wait_for_persisted_value) already
    # covers the common case; if it's STILL not resolved after that budget,
    # don't fail setup/teardown over it — this fixture runs again before
    # the very next test and will simply retry this same step then. Letting
    # a flaky read here fail the whole test (or worse, teardown, which
    # xfail can't even mark) is a worse outcome than one test occasionally
    # starting from a not-yet-reactivated record.
    try:
        page.search_category(MANAGED_CATEGORY)
        status = page.wait_for_persisted_value(
            lambda: page.get_category_status(MANAGED_CATEGORY),
            "Active",
            reopen=lambda: page.search_category(MANAGED_CATEGORY),
        )
        if status != "Active":
            page.open_edit_category(MANAGED_CATEGORY)
            page.ensure_active_switch_on()
            page.save_changes_and_return_to_list()
    except TimeoutException:
        pass

    return page


managed_category = managed_resource(reset_managed_category)
