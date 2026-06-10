from pages.admin_portal.discounts_page import DiscountsPage
from pages.admin_portal.login_page import AdminLoginPage
from pages.admin_portal.sidebar import AdminSidebar


EXISTING_DISCOUNT = "Basic Discount"
MISSING_DISCOUNT = "discount-does-not-exist-automation"
DISCOUNT_NAME = "VK AD02"
REQUESTED_SERVICE_CATEGORY = "VK wash 01"
SERVICE_CATEGORY = "VK wash01"
DISCOUNT_AMOUNT = "5"
START_DAY = "9"
START_TIME = "10:00 AM"
START_VALUE = "June 9, 2026 10:00 AM"


def open_discounts_page(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()
    login_page.login()
    login_page.wait_for_overview()

    sidebar = AdminSidebar(browser)
    sidebar.open_discounts()

    discounts_page = DiscountsPage(browser)
    discounts_page.wait_for_list_loaded()

    return discounts_page


def create_discount_if_missing(browser, discount_name=DISCOUNT_NAME):

    discounts_page = open_discounts_page(browser)

    if discounts_page.discount_exists(discount_name):
        discounts_page.search_discount(discount_name)
        discounts_page.wait_for_discount_row(discount_name)
        return discounts_page

    discounts_page.create_discount(
        discount_name,
        REQUESTED_SERVICE_CATEGORY,
        DISCOUNT_AMOUNT,
        START_DAY,
        START_TIME,
        SERVICE_CATEGORY
    )
    discounts_page.search_discount(discount_name)
    discounts_page.wait_for_discount_row(discount_name)

    return discounts_page


def test_discounts_page_loads(browser):

    discounts_page = open_discounts_page(browser)

    assert discounts_page.wait_for_discount_row(EXISTING_DISCOUNT).is_displayed()
    assert "Discount name" in discounts_page.get_body_text()
    assert "Status" in discounts_page.get_body_text()


def test_discounts_missing_discount_search(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.search_discount(MISSING_DISCOUNT)

    assert MISSING_DISCOUNT not in discounts_page.get_body_text()


def test_discounts_filter_panel_shows_controls(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_filter_panel()
    body_text = discounts_page.get_body_text()

    assert "Select site" in body_text
    assert "Active discount" in body_text
    assert "Apply filters" in body_text
    assert "Reset all" in body_text


def test_discounts_download_button_is_available(browser):

    discounts_page = open_discounts_page(browser)

    assert discounts_page.download_button_is_clickable()


def test_create_discount_required_name_validation(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.click_save_discount()

    assert not discounts_page.discount_name_input_is_valid()
    assert discounts_page.get_discount_name_validation_message() != ""


def test_create_vk_ad02_amount_discount(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.wait_for_list_loaded()
    discounts_page.search_discount(DISCOUNT_NAME)

    assert discounts_page.wait_for_discount_row(DISCOUNT_NAME).is_displayed()
    assert discounts_page.get_discount_status(DISCOUNT_NAME) == "Active"


def test_create_vk_ad02_does_not_duplicate_existing_discount(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.wait_for_list_loaded()
    discounts_page.search_discount(DISCOUNT_NAME)

    assert discounts_page.wait_for_discount_row(DISCOUNT_NAME).is_displayed()
    assert discounts_page.get_discount_status(DISCOUNT_NAME) == "Active"


def test_vk_ad02_discount_settings_persist(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.open_edit_discount(DISCOUNT_NAME)

    assert discounts_page.get_discount_name_value() == DISCOUNT_NAME
    assert discounts_page.amount_discount_type_is_selected()
    assert discounts_page.get_discount_amount_value() == DISCOUNT_AMOUNT
    assert discounts_page.get_discount_start_value() == START_VALUE
    assert discounts_page.active_switch_is_on()
