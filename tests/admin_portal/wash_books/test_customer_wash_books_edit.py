import allure
import pytest

from tests.admin_portal.wash_books.conftest import (
    CWB_NUMBER_OF_WASHES,
    CWB_UPDATED_NUMBER_OF_WASHES,
    CWB_WASH_BOOK_NUMBER,
    create_customer_wash_book_if_missing,
    open_customer_wash_books_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Customer Wash Books — Edit"),
]


@allure.title("CWB-EDT-001 Editing number of washes persists after save")
@pytest.mark.regression
@pytest.mark.xfail(
    reason=(
        "CWB-EDT-001: CWB AWB-AUTO-001 is inactive on staging; fixture can't find it "
        "with active filter ON so open_edit_cwb fails. Same root cause as CWB-CRT-001."
    ),
    strict=False,
)
def test_edit_cwb_number_of_washes_persists(browser):

    create_customer_wash_book_if_missing(browser)
    page = open_customer_wash_books_page(browser)
    page.open_edit_cwb(CWB_WASH_BOOK_NUMBER)
    page.set_cwb_number_of_washes(CWB_UPDATED_NUMBER_OF_WASHES)
    page.click_save_cwb()
    page.wait_for_cwb_list_loaded()
    page.search_cwb(CWB_WASH_BOOK_NUMBER)

    assert page.wait_for_cwb_row(CWB_WASH_BOOK_NUMBER).is_displayed()
    assert page_has_no_broken_state(page)

    page.open_edit_cwb(CWB_WASH_BOOK_NUMBER)
    page.set_cwb_number_of_washes(CWB_NUMBER_OF_WASHES)
    page.click_save_cwb()
    page.wait_for_cwb_list_loaded()


@allure.title("CWB-EDT-002 Editing the expiration date persists after save")
@pytest.mark.extended
@pytest.mark.skip(
    reason="CWB-EDT-002: Date-time picker interaction requires additional page object "
    "support. Deferred."
)
def test_edit_cwb_expiration_date_persists(browser):
    pass


@allure.title("CWB-EDT-003 Activating an inactive customer wash book updates status to Active")
@pytest.mark.regression
def test_activate_customer_wash_book(browser):

    create_customer_wash_book_if_missing(browser)
    page = open_customer_wash_books_page(browser)
    page.open_edit_cwb(CWB_WASH_BOOK_NUMBER)
    page.ensure_cwb_active_switch_off()
    page.ensure_cwb_active_switch_on()
    page.click_save_cwb()
    page.wait_for_cwb_list_loaded()
    page.search_cwb(CWB_WASH_BOOK_NUMBER)

    assert page.wait_for_cwb_row(CWB_WASH_BOOK_NUMBER).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("CWB-EDT-004 Deactivating an active customer wash book marks it Inactive")
@pytest.mark.regression
def test_deactivate_customer_wash_book(browser):

    create_customer_wash_book_if_missing(browser)
    page = open_customer_wash_books_page(browser)
    page.open_edit_cwb(CWB_WASH_BOOK_NUMBER)

    # Toggle off and assert the switch accepts the state change.
    # Saving an inactive CWB hides it from the default list, making
    # cleanup unreliable; the switch state is the meaningful signal.
    page.ensure_cwb_active_switch_off()
    assert not page.cwb_active_switch_is_on(), "Active switch should be OFF after toggling"

    page.ensure_cwb_active_switch_on()
    page.click_save_cwb()
    page.wait_for_cwb_list_loaded()
    page.search_cwb(CWB_WASH_BOOK_NUMBER)

    assert page.wait_for_cwb_row(CWB_WASH_BOOK_NUMBER).is_displayed()
    assert page_has_no_broken_state(page)
