from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import create_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import page_has_no_broken_state


def test_create_gift_card_helper_is_idempotent(browser):

    page = create_gift_card_if_missing(browser)
    page = create_gift_card_if_missing(browser)
    page.wait_for_list_loaded()
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()


def test_gift_cards_page_recovers_after_no_result_search(browser):

    page = create_gift_card_if_missing(browser)
    page.search_gift_card("gift-card-does-not-exist-automation")
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page_has_no_broken_state(page)
