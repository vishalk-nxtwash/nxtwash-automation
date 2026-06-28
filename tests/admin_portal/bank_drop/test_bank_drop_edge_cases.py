import allure
import pytest

from tests.admin_portal.bank_drop.conftest import (
    BANK_DROP_NAME,
    BANK_DROP_ORDER,
    LONG_BANK_DROP_NAME,
    XSS_BANK_DROP_NAME,
    create_bank_drop_if_missing,
    open_bank_drop_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Bank Drop"),
    allure.story("Edge Cases"),
]


@allure.title("BD-VAL-004 Negative order value — document browser behaviour")
@pytest.mark.edge
def test_negative_order_documents_behavior(browser):
    """type=number with no min constraint: browser may accept -1. Test documents current behavior."""
    page = open_bank_drop_page(browser)
    page.open_create()
    page.enter_name("VK ABD NEGATIVE ORDER")
    page.enter_order("-1")

    assert page_has_no_broken_state(page)


@allure.title("BD-VAL-005 Zero order value — document browser behaviour")
@pytest.mark.edge
def test_zero_order_documents_behavior(browser):
    """type=number with no min constraint: zero may be accepted. Test documents current behavior."""
    page = open_bank_drop_page(browser)
    page.open_create()
    page.enter_name("VK ABD ZERO ORDER")
    page.enter_order("0")

    assert page_has_no_broken_state(page)


@allure.title("BD-VAL-006 Duplicate bank drop name — document server behaviour")
@pytest.mark.edge
def test_duplicate_name_documents_behavior(browser):
    """App may accept or reject a duplicate name. Test documents that the form stays usable."""
    create_bank_drop_if_missing(browser)
    page = open_bank_drop_page(browser)
    page.open_create()
    page.enter_name(BANK_DROP_NAME)
    page.enter_order("80")
    page.click_save()

    body = page.get_body_text()
    assert "Bank drop name" in body or "saveNewBankDrop" in body or "Save bank drop" in body
    assert page_has_no_broken_state(page)


@allure.title("BD-VAL-007 Duplicate order value — document server behaviour")
@pytest.mark.edge
def test_duplicate_order_documents_behavior(browser):
    """App may accept or reject a duplicate order. Test documents that the form stays usable."""
    create_bank_drop_if_missing(browser)
    page = open_bank_drop_page(browser)
    page.open_create()
    page.enter_name("VK dup-order-%s" % BANK_DROP_ORDER)
    page.enter_order(BANK_DROP_ORDER)
    page.click_save()

    assert page_has_no_broken_state(page)


@allure.title("BD-ORD-002 Changing order value re-sequences the bank drop in the list")
@pytest.mark.edge
@pytest.mark.skip(
    reason=(
        "Manual: the admin list sorts by creation time, not order value; "
        "order sequencing on the customer portal must be verified manually."
    )
)
def test_changing_order_resequences_list(browser):

    create_bank_drop_if_missing(browser)
    page = open_bank_drop_page(browser)
    page.open_edit(BANK_DROP_NAME)
    page.enter_order("1")
    page.click_save()
    page.wait_for_list_loaded()
    orders = page.get_visible_row_orders()

    assert 1 in orders
    assert orders == sorted(orders), "Grid rows are not sorted by order value after re-sequence"

    page.open_edit(BANK_DROP_NAME)
    page.enter_order(BANK_DROP_ORDER)
    page.click_save()
    page.wait_for_list_loaded()


@allure.title("BD-EXP-001 Export download button is visible and clickable")
@pytest.mark.export
def test_download_button_is_visible(browser):

    page = open_bank_drop_page(browser)

    assert page.download_button_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("BD-UI-001 Save button on Add form shows raw i18n key instead of label")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "BD-UI-001: Save button text is the raw i18n key 'saveNewBankDrop' instead of "
        "'Save bank drop'. Remove xfail once the translation is wired up."
    ),
)
def test_save_button_has_human_readable_label(browser):

    page = open_bank_drop_page(browser)
    page.open_create()
    body_text = page.get_body_text()

    assert "Save bank drop" in body_text or "Save new bank drop" in body_text
    assert "saveNewBankDrop" not in body_text


@allure.title("BD-UI-002 Pagination footer shows correct record count when records exist")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "BD-UI-002: Pagination footer displays '0 of 0' even when records are present. "
        "Remove xfail once the count is rendered correctly."
    ),
)
def test_pagination_footer_shows_record_count(browser):

    create_bank_drop_if_missing(browser)
    page = open_bank_drop_page(browser)
    body_text = page.get_body_text()

    assert "0 of 0" not in body_text
    assert page.pagination_controls_are_visible()
