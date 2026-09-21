import allure
import pytest

from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_SITE
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import open_gift_cards_page
from tests.admin_portal.gift_cards.conftest import open_customer_gift_cards_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gift Cards"),
    allure.story("Validation"),
]


@allure.title("GC-VAL-001 Blank gift card name is blocked on save")
@pytest.mark.smoke
@pytest.mark.validation
def test_create_gift_card_requires_name(browser):

    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.click_save_gift_card()

    assert not page.gift_card_name_input_is_valid()
    assert page.get_gift_card_name_validation_message() != ""


@allure.title("GC-VAL-002 Blank gift card amount is blocked on save")
@pytest.mark.smoke
@pytest.mark.validation
def test_create_gift_card_requires_amount(browser):

    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name("VK val-amt-test")
    page.click_save_gift_card()

    assert not page.gift_card_amount_input_is_valid()
    assert page.get_gift_card_amount_validation_message() != ""


@allure.title("GC-VAL-003 Negative gift card amount is rejected by the form")
@pytest.mark.regression
@pytest.mark.validation
def test_negative_gift_card_amount_rejected(browser):

    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name("VK val-neg-amt")
    page.enter_gift_card_amount("-10")
    page.click_save_gift_card()

    assert "Save gift card" in page.get_body_text()


@allure.title("GC-VAL-004 Non-numeric gift card amount is rejected by the form")
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.skip(
    reason=(
        "Manual: Chrome silently drops non-numeric chars from type=number inputs, "
        "leaving the field blank; the legacy iframe then saves/redirects to the outer "
        "SPA /new route, so validity assertions run on the wrong form element."
    )
)
def test_non_numeric_gift_card_amount_rejected(browser):

    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name("VK val-nonnumeric-amt")
    page.enter_gift_card_amount("abc")
    page.click_save_gift_card()

    assert not page.gift_card_amount_input_is_valid()
    assert page.get_gift_card_amount_validation_message() != ""


@allure.title("CGC-VAL-001 Saving without selecting a gift card template is blocked")
@pytest.mark.smoke
@pytest.mark.validation
def test_create_customer_gift_card_requires_gift_card_selection(browser):

    page = open_customer_gift_cards_page(browser)
    page.open_create_customer_gift_card()
    page.select_customer_gift_card_site(CUSTOMER_GIFT_CARD_SITE)
    page.enter_customer_gift_card_number("VKVAL001")
    page.enter_customer_gift_card_amount("10")
    page.click_save_customer_gift_card()

    assert "Save customer gift card" in page.get_body_text()


@allure.title("CGC-VAL-002 Blank customer gift card number is blocked on save")
@pytest.mark.smoke
@pytest.mark.validation
def test_create_customer_gift_card_requires_number(browser):

    page = open_customer_gift_cards_page(browser)
    page.open_create_customer_gift_card()
    page.click_save_customer_gift_card()

    assert not page.customer_gift_card_number_input_is_valid()
    assert page.get_customer_gift_card_number_validation_message() != ""


@allure.title("CGC-VAL-003 Blank customer gift card amount is blocked on save")
@pytest.mark.smoke
@pytest.mark.validation
def test_create_customer_gift_card_requires_amount(browser):

    page = open_customer_gift_cards_page(browser)
    page.open_create_customer_gift_card()
    page.select_customer_gift_card_site(CUSTOMER_GIFT_CARD_SITE)
    page.select_customer_gift_card_template(GIFT_CARD_NAME)
    page.enter_customer_gift_card_number("VKVAL003")
    page.click_save_customer_gift_card()

    assert not page.customer_gift_card_amount_input_is_valid()
    assert page.get_customer_gift_card_amount_validation_message() != ""


@allure.title("CGC-VAL-006 Negative customer gift card amount is rejected by the form")
@pytest.mark.regression
@pytest.mark.validation
def test_negative_customer_gift_card_amount_rejected(browser):

    page = open_customer_gift_cards_page(browser)
    page.open_create_customer_gift_card()
    page.select_customer_gift_card_site(CUSTOMER_GIFT_CARD_SITE)
    page.select_customer_gift_card_template(GIFT_CARD_NAME)
    page.enter_customer_gift_card_number("VKVAL006")
    page.enter_customer_gift_card_amount("-5")
    page.click_save_customer_gift_card()

    assert "Save customer gift card" in page.get_body_text()


@allure.title("CGC-VAL-007 Non-numeric customer gift card amount is rejected by the form")
@pytest.mark.regression
@pytest.mark.validation
def test_non_numeric_customer_gift_card_amount_rejected(browser):

    page = open_customer_gift_cards_page(browser)
    page.open_create_customer_gift_card()
    page.enter_customer_gift_card_amount("xyz")

    assert not page.customer_gift_card_amount_input_is_valid()
