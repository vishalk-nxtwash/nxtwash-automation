from tests.admin_portal.gift_cards.conftest import MISSING_GIFT_CARD
from tests.admin_portal.gift_cards.conftest import open_gift_cards_page


def test_gift_cards_missing_gift_card_search_returns_no_match(browser):

    page = open_gift_cards_page(browser)
    page.search_gift_card(MISSING_GIFT_CARD)

    assert MISSING_GIFT_CARD not in page.get_body_text()


def test_gift_cards_search_accepts_partial_text_without_breaking_grid(browser):

    page = open_gift_cards_page(browser)
    page.search_gift_card("Gift")

    assert "Gift card name" in page.get_body_text()
