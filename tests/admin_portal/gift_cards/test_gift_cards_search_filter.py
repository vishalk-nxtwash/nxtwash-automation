import allure
import pytest

from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_NUMBER
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import create_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import create_customer_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import open_customer_gift_cards_page
from tests.admin_portal.gift_cards.conftest import open_gift_cards_page
from tests.admin_portal.gift_cards.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gift Cards"),
    allure.story("Search"),
]


@allure.title("GC-SRH-001 Search exact gift card name returns the correct record")
@pytest.mark.regression
def test_search_exact_gift_card_name_returns_match(browser):

    page = create_gift_card_if_missing(browser)
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("GC-SRH-002 Partial gift card name search returns matching records")
@pytest.mark.regression
def test_gift_cards_search_accepts_partial_text_without_breaking_grid(browser):

    page = open_gift_cards_page(browser)
    page.search_gift_card("Gift")

    assert "Gift card name" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("CGC-SRH-001 Search exact customer gift card number returns the correct record")
@pytest.mark.regression
def test_customer_gift_card_search_exact_number_returns_match(browser):

    page = create_customer_gift_card_if_missing(browser)
    page = open_customer_gift_cards_page(browser)
    page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)

    assert page.wait_for_customer_gift_card_row(CUSTOMER_GIFT_CARD_NUMBER).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("CGC-SRH-002 Partial customer gift card number search returns matching records")
@pytest.mark.extended
def test_customer_gift_card_search_partial_number(browser):

    page = create_customer_gift_card_if_missing(browser)
    page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER[:4])

    assert CUSTOMER_GIFT_CARD_NUMBER in page.get_body_text()
    assert page_has_no_broken_state(page)
