from pages.admin_portal.login_page import AdminLoginPage
from pages.admin_portal.sidebar import AdminSidebar
from pages.admin_portal.wash_books_page import WashBooksPage


EXISTING_WASH_BOOK = "Basic washbook"
MISSING_WASH_BOOK = "wash-book-does-not-exist-automation"
WASH_BOOK_NAME = "VK AWB2"
NUMBER_OF_WASHES = "15"
POINTS_AWARDED = "5"
GLOBAL_PRICE = "55"
GLOBAL_COMMISSION = "5"
VISIBLE_PRICE = "$55.00"


def open_wash_books_page(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()
    login_page.login()
    login_page.wait_for_overview()

    sidebar = AdminSidebar(browser)
    sidebar.open_wash_books()

    wash_books_page = WashBooksPage(browser)
    wash_books_page.wait_for_list_loaded()

    return wash_books_page


def create_wash_book_if_missing(browser, wash_book_name=WASH_BOOK_NAME):

    wash_books_page = open_wash_books_page(browser)

    if wash_books_page.wash_book_exists(wash_book_name):
        return wash_books_page

    wash_books_page.create_wash_book(
        wash_book_name,
        NUMBER_OF_WASHES,
        POINTS_AWARDED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION
    )
    wash_books_page.search_wash_book(wash_book_name)
    wash_books_page.wait_for_wash_book_row(wash_book_name)

    return wash_books_page


def test_wash_books_page_loads(browser):

    wash_books_page = open_wash_books_page(browser)

    assert "Wash book name" in wash_books_page.get_body_text()
    assert "Washes number" in wash_books_page.get_body_text()
    assert "Price" in wash_books_page.get_body_text()
    assert "Status" in wash_books_page.get_body_text()


def test_wash_books_existing_search(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book(EXISTING_WASH_BOOK)

    assert wash_books_page.wait_for_wash_book_row(
        EXISTING_WASH_BOOK
    ).is_displayed()


def test_wash_books_missing_search(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book(MISSING_WASH_BOOK)

    assert MISSING_WASH_BOOK not in wash_books_page.get_body_text()


def test_wash_books_filter_panel_shows_controls(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.open_filter_panel()

    assert "Select site" in wash_books_page.get_body_text()
    assert "Apply filters" in wash_books_page.get_body_text()
    assert "Reset all" in wash_books_page.get_body_text()


def test_wash_books_download_button_is_available(browser):

    wash_books_page = open_wash_books_page(browser)

    assert wash_books_page.download_button_is_clickable()


def test_create_wash_book_required_name_validation(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.open_create_wash_book()
    wash_books_page.click_save_wash_book()

    assert not wash_books_page.wash_book_name_input_is_valid()
    assert wash_books_page.get_wash_book_name_validation_message() != ""


def test_create_vk_awb2_wash_book(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.wait_for_list_loaded()
    wash_books_page.search_wash_book(WASH_BOOK_NAME)

    assert wash_books_page.wait_for_wash_book_row(WASH_BOOK_NAME).is_displayed()
    assert wash_books_page.get_wash_book_washes(WASH_BOOK_NAME) == NUMBER_OF_WASHES
    assert wash_books_page.get_wash_book_price(WASH_BOOK_NAME) == VISIBLE_PRICE
    assert wash_books_page.get_wash_book_status(WASH_BOOK_NAME) == "Active"


def test_create_vk_awb2_does_not_duplicate_existing_wash_book(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.wait_for_list_loaded()
    wash_books_page.search_wash_book(WASH_BOOK_NAME)

    assert wash_books_page.wait_for_wash_book_row(WASH_BOOK_NAME).is_displayed()
    assert wash_books_page.get_wash_book_washes(WASH_BOOK_NAME) == NUMBER_OF_WASHES
    assert wash_books_page.get_wash_book_price(WASH_BOOK_NAME) == VISIBLE_PRICE
    assert wash_books_page.get_wash_book_status(WASH_BOOK_NAME) == "Active"


def test_vk_awb2_wash_book_settings_persist(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.open_edit_wash_book(WASH_BOOK_NAME)

    assert wash_books_page.get_wash_book_name_value() == WASH_BOOK_NAME
    assert wash_books_page.get_number_of_washes_value() == NUMBER_OF_WASHES
    assert wash_books_page.get_points_awarded_value() == POINTS_AWARDED
    assert wash_books_page.active_switch_is_on()
    assert wash_books_page.customer_portal_switch_is_on()
    assert wash_books_page.get_global_price_value() == GLOBAL_PRICE
    assert wash_books_page.get_global_commission_value() == GLOBAL_COMMISSION
