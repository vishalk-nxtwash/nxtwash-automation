import allure
import pytest

from tests.admin_portal.gift_cards.conftest import open_gift_cards_page
from tests.admin_portal.gift_cards.conftest import open_customer_gift_cards_page
from tests.admin_portal.gift_cards.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gift Cards"),
    allure.story("UI"),
]


@allure.title("GC-LST-001 Gift cards page loads with primary controls")
@pytest.mark.sanity
@pytest.mark.prod_smoke
def test_gift_cards_page_loads(browser):

    page = open_gift_cards_page(browser)
    body_text = page.get_body_text()

    assert "Gift card name" in body_text
    assert "Gift card amount" in body_text
    assert "Status" in body_text
    assert page_has_no_broken_state(page)


@allure.title("GC-LST-001 Gift cards primary action buttons are available")
@pytest.mark.sanity
def test_gift_cards_primary_actions_are_available(browser):

    page = open_gift_cards_page(browser)

    assert page.download_button_is_clickable()
    assert page.search_input_is_visible()
    assert page.filter_button_is_clickable()
    assert page.add_gift_card_button_is_clickable()
    assert "+ Add new gift card" in page.get_body_text()
    assert "Customer gift cards" in page.get_body_text()


@allure.title("CGC-LST-001 Customer gift cards tab loads with correct controls")
@pytest.mark.sanity
def test_customer_gift_cards_tab_loads(browser):

    page = open_customer_gift_cards_page(browser)
    body_text = page.get_body_text()

    assert "Customer gift cards" in body_text
    assert "Gift card number" in body_text
    assert page.customer_search_input_is_visible()
    assert page.add_customer_gift_card_button_is_clickable()
    assert page_has_no_broken_state(page)


@allure.title("GC-LST-002 Gift cards tab shows correct columns")
@pytest.mark.regression
def test_gift_cards_list_shows_correct_columns(browser):

    page = open_gift_cards_page(browser)
    body_text = page.get_body_text()

    assert "Gift card name" in body_text
    assert "Gift card amount" in body_text
    assert "Status" in body_text
    assert page_has_no_broken_state(page)


@allure.title("GC-LST-003 Pagination and results-per-page control are visible")
@pytest.mark.regression
def test_gift_cards_list_has_pagination(browser):

    page = open_gift_cards_page(browser)

    assert "Results per page" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("CGC-LST-002 Pagination and results-per-page control visible in customer tab")
@pytest.mark.regression
def test_customer_gift_cards_list_has_pagination(browser):

    page = open_customer_gift_cards_page(browser)

    assert "Results per page" in page.get_body_text()
    assert page_has_no_broken_state(page)
