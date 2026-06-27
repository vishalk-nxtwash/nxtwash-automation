import allure
import pytest

from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import create_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gift Cards"),
    allure.story("Edge Cases"),
]


@allure.title("GC-EDGE create_gift_card_if_missing helper is idempotent")
@pytest.mark.regression
def test_create_gift_card_helper_is_idempotent(browser):

    page = create_gift_card_if_missing(browser)
    page = create_gift_card_if_missing(browser)
    page.wait_for_list_loaded()
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()


@allure.title("GC-SRH-004 Clear search after no-result query restores the gift card list")
@pytest.mark.regression
def test_gift_cards_page_recovers_after_no_result_search(browser):

    page = create_gift_card_if_missing(browser)
    page.search_gift_card("gift-card-does-not-exist-automation")
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page_has_no_broken_state(page)
