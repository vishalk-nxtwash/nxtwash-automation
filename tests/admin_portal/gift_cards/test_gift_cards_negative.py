import allure
import pytest

from tests.admin_portal.gift_cards.conftest import MISSING_CUSTOMER_GIFT_CARD
from tests.admin_portal.gift_cards.conftest import MISSING_GIFT_CARD
from tests.admin_portal.gift_cards.conftest import open_customer_gift_cards_page
from tests.admin_portal.gift_cards.conftest import open_gift_cards_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gift Cards"),
    allure.story("Search"),
]


@allure.title("GC-SRH-003 Search non-existing gift card name returns empty state")
@pytest.mark.regression
def test_opening_missing_gift_card_does_not_show_edit_form(browser):

    page = open_gift_cards_page(browser)
    page.search_gift_card(MISSING_GIFT_CARD)

    assert MISSING_GIFT_CARD not in page.get_body_text()
    assert "Save gift card" not in page.get_body_text()


@allure.title("CGC-SRH-003 Search non-existing customer gift card number returns empty state")
@pytest.mark.regression
def test_missing_customer_gift_card_search_does_not_show_match(browser):

    page = open_customer_gift_cards_page(browser)
    page.search_customer_gift_card(MISSING_CUSTOMER_GIFT_CARD)

    assert MISSING_CUSTOMER_GIFT_CARD not in page.get_body_text()
