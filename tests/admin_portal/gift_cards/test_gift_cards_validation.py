from tests.admin_portal.gift_cards.conftest import open_gift_cards_page
from tests.admin_portal.gift_cards.conftest import open_customer_gift_cards_page


def test_create_gift_card_requires_name(browser):

    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.click_save_gift_card()

    assert not page.gift_card_name_input_is_valid()
    assert page.get_gift_card_name_validation_message() != ""


def test_create_customer_gift_card_requires_number(browser):

    page = open_customer_gift_cards_page(browser)
    page.open_create_customer_gift_card()
    page.click_save_customer_gift_card()

    assert not page.customer_gift_card_number_input_is_valid()
    assert page.get_customer_gift_card_number_validation_message() != ""
