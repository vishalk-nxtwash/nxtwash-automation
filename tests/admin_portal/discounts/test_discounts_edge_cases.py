from tests.admin_portal.discounts.conftest import DISCOUNT_AMOUNT
from tests.admin_portal.discounts.conftest import DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import create_discount_if_missing


def test_discount_create_is_idempotent(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.wait_for_list_loaded()
    discounts_page.search_discount(DISCOUNT_NAME)

    assert discounts_page.wait_for_discount_row(DISCOUNT_NAME).is_displayed()


def test_discount_first_location_settings_persist(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.open_edit_discount(DISCOUNT_NAME)

    assert discounts_page.location_is_assigned_by_index(0)
    assert discounts_page.get_location_discount_value_by_index(0) == DISCOUNT_AMOUNT


def test_discount_long_name_does_not_break_form(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("VK " + ("D" * 128))

    assert discounts_page.get_discount_name_value().startswith("VK ")
    assert "Discount name" in discounts_page.get_body_text()
