from tests.admin_portal.discounts.conftest import (
    DISCOUNT_AMOUNT,
    DISCOUNT_NAME,
    START_VALUE,
    create_discount_if_missing,
)


def test_create_amount_discount(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.wait_for_list_loaded()
    discounts_page.search_discount(DISCOUNT_NAME)

    assert discounts_page.wait_for_discount_row(DISCOUNT_NAME).is_displayed()
    assert discounts_page.get_discount_status(DISCOUNT_NAME) == "Active"


def test_discount_settings_persist(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.open_edit_discount(DISCOUNT_NAME)

    assert discounts_page.get_discount_name_value() == DISCOUNT_NAME
    assert discounts_page.amount_discount_type_is_selected()
    assert discounts_page.get_discount_amount_value() == DISCOUNT_AMOUNT
    assert discounts_page.get_discount_start_value() == START_VALUE
    assert discounts_page.active_switch_is_on()
