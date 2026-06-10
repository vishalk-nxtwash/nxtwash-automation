from tests.admin_portal.test_create_gift_card import GIFT_CARD_NAME
from tests.admin_portal.test_create_gift_card import create_prime_gift_card_if_missing


CUSTOMER_GIFT_CARD_SITE = "VK Test carwash 2"
CUSTOMER_GIFT_CARD_NUMBER = "PGCN25"
CUSTOMER_GIFT_CARD_AMOUNT = "25"
VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT = "$25.00"


def open_customer_gift_cards_page(browser):

    gift_cards_page = create_prime_gift_card_if_missing(browser)
    gift_cards_page.open_customer_gift_cards()

    return gift_cards_page


def create_customer_gift_card_if_missing(browser):

    gift_cards_page = open_customer_gift_cards_page(browser)

    if gift_cards_page.customer_gift_card_exists(CUSTOMER_GIFT_CARD_NUMBER):
        return gift_cards_page

    gift_cards_page.create_customer_gift_card(
        CUSTOMER_GIFT_CARD_SITE,
        GIFT_CARD_NAME,
        CUSTOMER_GIFT_CARD_NUMBER,
        CUSTOMER_GIFT_CARD_AMOUNT
    )
    gift_cards_page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)
    gift_cards_page.wait_for_customer_gift_card_row(CUSTOMER_GIFT_CARD_NUMBER)

    return gift_cards_page


def test_customer_gift_cards_page_loads(browser):

    gift_cards_page = open_customer_gift_cards_page(browser)

    assert "Gift card number" in gift_cards_page.get_body_text()
    assert "Gift card name" in gift_cards_page.get_body_text()
    assert "Gift card amount" in gift_cards_page.get_body_text()


def test_create_customer_gift_card_required_number_validation(browser):

    gift_cards_page = open_customer_gift_cards_page(browser)
    gift_cards_page.open_create_customer_gift_card()
    gift_cards_page.click_save_customer_gift_card()

    assert not gift_cards_page.customer_gift_card_number_input_is_valid()
    assert (
        gift_cards_page.get_customer_gift_card_number_validation_message()
        != ""
    )


def test_create_pgcn25_customer_gift_card(browser):

    gift_cards_page = create_customer_gift_card_if_missing(browser)
    gift_cards_page.wait_for_customer_list_loaded()
    gift_cards_page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)

    assert gift_cards_page.wait_for_customer_gift_card_row(
        CUSTOMER_GIFT_CARD_NUMBER
    ).is_displayed()
    assert gift_cards_page.get_customer_gift_card_name(
        CUSTOMER_GIFT_CARD_NUMBER
    ) == GIFT_CARD_NAME
    assert gift_cards_page.get_customer_gift_card_amount(
        CUSTOMER_GIFT_CARD_NUMBER
    ) == VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT


def test_create_pgcn25_customer_gift_card_does_not_duplicate(browser):

    gift_cards_page = create_customer_gift_card_if_missing(browser)
    gift_cards_page.wait_for_customer_list_loaded()
    gift_cards_page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)

    assert gift_cards_page.wait_for_customer_gift_card_row(
        CUSTOMER_GIFT_CARD_NUMBER
    ).is_displayed()
