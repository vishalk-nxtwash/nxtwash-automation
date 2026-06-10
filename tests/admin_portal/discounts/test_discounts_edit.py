from tests.admin_portal.discounts.conftest import (
    DISCOUNT_AMOUNT,
    DISCOUNT_NAME,
    REQUESTED_SERVICE_CATEGORY,
    SERVICE_CATEGORY,
    START_DAY,
    START_TIME,
    create_discount_if_missing,
)


def test_edit_discount_reapplies_expected_settings(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.update_discount(
        DISCOUNT_NAME,
        REQUESTED_SERVICE_CATEGORY,
        DISCOUNT_AMOUNT,
        START_DAY,
        START_TIME,
        SERVICE_CATEGORY
    )

    discounts_page.open_edit_discount(DISCOUNT_NAME)

    assert discounts_page.get_discount_name_value() == DISCOUNT_NAME
    assert discounts_page.amount_discount_type_is_selected()
    assert discounts_page.get_discount_amount_value() == DISCOUNT_AMOUNT
    assert discounts_page.active_switch_is_on()
