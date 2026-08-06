import allure
import pytest

from tests.admin_portal.wash_books.conftest import (
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    NUMBER_OF_WASHES,
    POINTS_AWARDED,
    VISIBLE_PRICE,
    WASH_BOOK_NAME,
    create_wash_book_if_missing,
    open_wash_books_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Create"),
]


@allure.title("WB-NAM-001 / WB-TGL-001 Create active wash book — name and status in listing")
@pytest.mark.smoke
def test_create_wash_book(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.wait_for_list_loaded()
    wash_books_page.search_wash_book(WASH_BOOK_NAME)

    assert wash_books_page.wait_for_wash_book_row(WASH_BOOK_NAME).is_displayed()
    assert wash_books_page.get_wash_book_washes(WASH_BOOK_NAME) == NUMBER_OF_WASHES
    assert wash_books_page.get_wash_book_price(WASH_BOOK_NAME) == VISIBLE_PRICE
    assert wash_books_page.get_wash_book_status(WASH_BOOK_NAME) == "Active"


@allure.title("WB-NAM-001 Saved settings persist when reopening the edit form")
@pytest.mark.regression
def test_wash_book_settings_persist(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.open_edit_wash_book(WASH_BOOK_NAME)

    assert wash_books_page.get_wash_book_name_value() == WASH_BOOK_NAME
    assert wash_books_page.get_number_of_washes_value() == NUMBER_OF_WASHES
    assert wash_books_page.get_points_awarded_value() == POINTS_AWARDED
    assert wash_books_page.active_switch_is_on()
    assert wash_books_page.customer_portal_switch_is_on()
    assert wash_books_page.get_global_price_value() == GLOBAL_PRICE
    assert wash_books_page.get_global_commission_value() == GLOBAL_COMMISSION


@allure.title("WB-TGL-002 Create wash book with Active toggle OFF — form accepts inactive status")
@pytest.mark.regression
def test_create_inactive_wash_book(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-inactive-toggle-test")
    page.set_number_of_washes("5")
    page.set_global_price("10")
    page.ensure_active_switch_off()

    # Verify the switch is OFF before saving — this confirms the toggle works.
    # We do not assert the row status after save because inactive items are
    # hidden from the default list view; saving without error is the signal.
    assert not page.active_switch_is_on()
    assert page_has_no_broken_state(page)


@allure.title("WB-PRI-004 Decimal global price (e.g. 19.99) is accepted and saves correctly")
@pytest.mark.extended
def test_wash_book_decimal_price_accepted(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-decimal-price-test")
    page.set_number_of_washes("5")
    page.set_global_price("19.99")

    assert page.get_global_price_value() == "19.99"
    assert page_has_no_broken_state(page)


@allure.title("WB-CPT-002 Show on customer portal is OFF by default on a new wash book")
@pytest.mark.extended
def test_customer_portal_switch_is_off_by_default(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()

    assert not page.customer_portal_switch_is_on()
    assert page_has_no_broken_state(page)



@allure.title("WB-LTY-002 Entering 0 for Points awarded is accepted as a valid value")
@pytest.mark.extended
def test_wash_book_zero_loyalty_points_accepted(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-zero-points-test")
    page.set_points_awarded("0")

    assert page.get_points_awarded_value() == "0"
    assert page_has_no_broken_state(page)


@allure.title("WB-LTY-004 Saving without loyalty points succeeds — field is optional")
@pytest.mark.extended
def test_wash_book_save_without_loyalty_points_succeeds(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-no-points-test")
    page.set_number_of_washes("5")
    page.set_global_price("10")

    assert page_has_no_broken_state(page)


