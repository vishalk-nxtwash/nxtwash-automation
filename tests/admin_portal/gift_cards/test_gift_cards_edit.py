from tests.admin_portal.gift_cards.conftest import ASSIGNMENT_LOCATIONS
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_NUMBER
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import UPDATED_LANDING_PAGE_CODE
from tests.admin_portal.gift_cards.conftest import VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import create_customer_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import create_gift_card_if_missing


def test_edit_gift_card_updates_settings_without_duplicate(browser):

    page = create_gift_card_if_missing(browser)
    page.update_gift_card_settings(
        GIFT_CARD_NAME,
        GIFT_CARD_AMOUNT,
        UPDATED_LANDING_PAGE_CODE,
        ASSIGNMENT_LOCATIONS
    )
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page.get_gift_card_status(GIFT_CARD_NAME) == "Active"


def test_create_customer_gift_card_from_template(browser):

    page = create_customer_gift_card_if_missing(browser)
    page.wait_for_customer_list_loaded()
    page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)

    assert page.wait_for_customer_gift_card_row(
        CUSTOMER_GIFT_CARD_NUMBER
    ).is_displayed()
    assert page.get_customer_gift_card_name(CUSTOMER_GIFT_CARD_NUMBER) == GIFT_CARD_NAME
    assert (
        page.get_customer_gift_card_amount(CUSTOMER_GIFT_CARD_NUMBER)
        == VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT
    )
    assert CUSTOMER_GIFT_CARD_AMOUNT in VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT
