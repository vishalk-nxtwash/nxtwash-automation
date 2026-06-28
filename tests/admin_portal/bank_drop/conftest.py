import pytest

from pages.admin_portal.bank_drop_page import BankDropPage
from tests.admin_portal.admin_session import open_admin_path


BANK_DROP_NAME = "VK ABD01"
BANK_DROP_ORDER = "2"
VISIBLE_BANK_DROP_ORDER = "2"
SECOND_BANK_DROP_NAME = "VK ABD02"
SECOND_BANK_DROP_ORDER = "3"
MISSING_BANK_DROP = "bank-drop-does-not-exist-automation"
LONG_BANK_DROP_NAME = "VK BANK DROP AUTOMATION LONG NAME 0123456789"
XSS_BANK_DROP_NAME = "<script>alert(1)</script>"
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
        return page

    page.create_bank_drop(name, order)
    page.wait_for_bank_drop_row(name)

    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


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
