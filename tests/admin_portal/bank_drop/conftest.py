import pytest

from pages.admin_portal.bank_drop_page import BankDropPage
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._data import load as _load

_D = _load("bank_drop")

BANK_DROP_NAME              = _D["reference"]["first"]
BANK_DROP_ORDER             = _D["reference"]["first_order"]
VISIBLE_BANK_DROP_ORDER     = _D["reference"]["first_order"]
SECOND_BANK_DROP_NAME       = _D["reference"]["second"]
SECOND_BANK_DROP_ORDER      = _D["reference"]["second_order"]
EDIT_BANK_DROP_NAME         = _D["edit_target"]["name"]
EDIT_BANK_DROP_UPDATED_NAME = _D["edit_target"]["updated_name"]
EDIT_BANK_DROP_ORDER        = _D["edit_target"]["order"]
MISSING_BANK_DROP           = _D["search"]["nonexistent"]
LONG_BANK_DROP_NAME = _D["edge_cases"]["long_name"]
XSS_BANK_DROP_NAME  = _D["edge_cases"]["xss_name"]
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def open_bank_drop_page(browser):

    open_admin_path(browser, "/services/bankDrop")

    page = BankDropPage(browser)
    page.wait_for_list_loaded()

    return page


def create_bank_drop_if_missing(browser, name=BANK_DROP_NAME, order=BANK_DROP_ORDER):

    page = open_bank_drop_page(browser)

    if page.bank_drop_exists(name):
        # Reset mutable fields so tests always start from the expected baseline.
        page.open_edit(name)
        page.enter_order(order)
        page.ensure_active_on()
        page.click_save()
        page.wait_for_list_loaded()
        return page

    saved = page.create_bank_drop(name, order)

    if not saved:
        # Server rejected the save — most likely "already exists" because the
        # item is in the DB but beyond page 1 of the server-side paginated grid
        # (>100 total records) so bank_drop_exists could not find it.
        # Navigate to a clean list state and return; tests that require the row
        # to be visible on page 1 will fail with their own clear TimeoutException.
        return open_bank_drop_page(browser)

    # Save succeeded: navigate fresh so filters reset and the new row is visible.
    page = open_bank_drop_page(browser)
    if not page.bank_drop_exists(name):
        page.wait_for_bank_drop_row(name)  # raises with a clear message if truly absent
    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


def _reset_edit_bank_drop(browser):
    """Guarantee VK EDT002 exists and VK EDT002-upd does not.

    If a previous test run renamed VK EDT002 to VK EDT002-upd and never
    restored it, this renames it back before the next run can touch it.
    """
    page = open_bank_drop_page(browser)
    if page.bank_drop_exists(EDIT_BANK_DROP_UPDATED_NAME):
        page.open_edit(EDIT_BANK_DROP_UPDATED_NAME)
        page.enter_name(EDIT_BANK_DROP_NAME)
        page.click_save()
        page.wait_for_list_loaded()
    return create_bank_drop_if_missing(browser, EDIT_BANK_DROP_NAME, EDIT_BANK_DROP_ORDER)


@pytest.fixture
def managed_edit_bank_drop(browser):
    """Stable fixture for BD-EDT-001: VK EDT002 exists before the test, restored after."""
    page = _reset_edit_bank_drop(browser)
    yield page
    try:
        _reset_edit_bank_drop(browser)
    except Exception:  # noqa: BLE001
        pass


@pytest.fixture
def managed_bank_drop(browser):
    """Ensure BANK_DROP_NAME exists at baseline before and after the test."""
    page = create_bank_drop_if_missing(browser)
    yield page
    # Reset order and active status to baseline so later tests see clean state.
    reset = open_bank_drop_page(browser)
    if reset.bank_drop_exists(BANK_DROP_NAME):
        reset.open_edit(BANK_DROP_NAME)
        reset.enter_order(BANK_DROP_ORDER)
        reset.ensure_active_on()
        reset.click_save()
        reset.wait_for_list_loaded()
