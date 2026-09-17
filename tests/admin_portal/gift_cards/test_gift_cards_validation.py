import allure
import pytest

from tests.admin_portal.gift_cards.conftest import ASSIGNMENT_LOCATIONS
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_NUMBER
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_SITE
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import LANDING_PAGE_CODE
from tests.admin_portal.gift_cards.conftest import create_customer_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import create_gift_card_if_missing
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


@allure.title("GC-VAL-005 Duplicate gift card name is blocked on save")
@pytest.mark.regression
@pytest.mark.validation
def test_duplicate_gift_card_name_blocked(browser):

    create_gift_card_if_missing(browser)
    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name(GIFT_CARD_NAME)
    page.enter_gift_card_amount(GIFT_CARD_AMOUNT)
    page.enter_landing_page_code(LANDING_PAGE_CODE)
    page.assign_location(ASSIGNMENT_LOCATIONS[0])
    page.ensure_switch_on(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()

    # Form must stay open (save rejected) or show an error
    assert "Save gift card" in page.get_body_text()


@allure.title("GC-VAL-006 Expiration date in the past is rejected")
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.skip(
    reason="GC-VAL-006: expiration date input locator not yet mapped in the page object."
)
def test_past_expiration_date_rejected(browser):
    pass


@allure.title("CGC-VAL-004 Customer search requires at least 2 characters")
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.skip(
    reason=(
        "CGC-VAL-004: the customer-search field inside the CGC create form is not "
        "mapped in the page object. Implement once the locator is confirmed."
    )
)
def test_customer_search_requires_two_chars(browser):
    pass


@allure.title("CGC-VAL-005 Duplicate customer gift card number is blocked on save")
@pytest.mark.regression
@pytest.mark.validation
def test_duplicate_customer_gift_card_number_blocked(browser):

    create_customer_gift_card_if_missing(browser)
    page = open_customer_gift_cards_page(browser)
    page.open_create_customer_gift_card()
    page.select_customer_gift_card_site(CUSTOMER_GIFT_CARD_SITE)
    page.select_customer_gift_card_template(GIFT_CARD_NAME)
    page.enter_customer_gift_card_number(CUSTOMER_GIFT_CARD_NUMBER)
    page.enter_customer_gift_card_amount(CUSTOMER_GIFT_CARD_AMOUNT)
    page.click_save_customer_gift_card()

    # Form must stay open if the duplicate is rejected
    assert "Save customer gift card" in page.get_body_text()
