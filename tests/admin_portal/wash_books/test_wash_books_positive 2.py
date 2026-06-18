from tests.admin_portal.wash_books.conftest import (
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    NUMBER_OF_WASHES,
    POINTS_AWARDED,
    VISIBLE_PRICE,
    WASH_BOOK_NAME,
    create_wash_book_if_missing,
)


def test_create_wash_book(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.wait_for_list_loaded()
    wash_books_page.search_wash_book(WASH_BOOK_NAME)

    assert wash_books_page.wait_for_wash_book_row(WASH_BOOK_NAME).is_displayed()
    assert wash_books_page.get_wash_book_washes(WASH_BOOK_NAME) == NUMBER_OF_WASHES
    assert wash_books_page.get_wash_book_price(WASH_BOOK_NAME) == VISIBLE_PRICE
    assert wash_books_page.get_wash_book_status(WASH_BOOK_NAME) == "Active"


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

    for row_index in range(2):
        assert wash_books_page.location_is_assigned_by_index(row_index)
        assert wash_books_page.get_location_price_by_index(row_index) == GLOBAL_PRICE
        assert (
            wash_books_page.get_location_commission_by_index(row_index)
            == GLOBAL_COMMISSION
        )
