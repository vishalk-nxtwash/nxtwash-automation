import uuid

import allure
import pytest

from tests.admin_portal.gift_cards.conftest import ASSIGNMENT_LOCATIONS
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_NUMBER
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import UPDATED_LANDING_PAGE_CODE
from tests.admin_portal.gift_cards.conftest import VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import create_customer_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import create_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import open_gift_cards_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gift Cards"),
    allure.story("Edit"),
]


@allure.title("GC-EDT-001 Edit gift card name persists after save")
@pytest.mark.regression
def test_edit_gift_card_name(browser):

    original_name = "VK EDT001-%s" % uuid.uuid4().hex[:6]
    updated_name = original_name + "-upd"
    page = open_gift_cards_page(browser)
    page.create_gift_card(original_name, GIFT_CARD_AMOUNT, "VKTEMP", ASSIGNMENT_LOCATIONS)

    page.open_edit_gift_card(original_name)
    page.enter_gift_card_name(updated_name)
    page.click_save_gift_card()

    page = open_gift_cards_page(browser)
    page.search_gift_card(updated_name)

    assert page.wait_for_gift_card_row(updated_name).is_displayed()


@allure.title("GC-EDT-002 Edit gift card amount and landing page code persist after save")
@pytest.mark.regression
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


@allure.title("GC-EDT-006 Activate an inactive gift card updates its status to Active")
@pytest.mark.regression
def test_activate_inactive_gift_card(browser):

    page = create_gift_card_if_missing(browser)
    page.open_edit_gift_card(GIFT_CARD_NAME)
    page.ensure_switch_off(page.ACTIVE_SERVICE_SWITCH)
    page.ensure_switch_on(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()
    page.wait_for_list_loaded()
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page.get_gift_card_status(GIFT_CARD_NAME) == "Active"


@allure.title("GC-EDT-007 Deactivate an active gift card hides it from the default list")
@pytest.mark.regression
def test_deactivate_active_gift_card(browser):

    temp_name = "VK deact-%s" % uuid.uuid4().hex[:6]
    page = open_gift_cards_page(browser)
    page.create_gift_card(temp_name, GIFT_CARD_AMOUNT, "VKTEMP2", ASSIGNMENT_LOCATIONS)
    page.search_gift_card(temp_name)
    assert page.wait_for_gift_card_row(temp_name).is_displayed()

    page.open_edit_gift_card(temp_name)
    page.ensure_switch_off(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()
    page.wait_for_list_loaded()
    page.search_gift_card(temp_name)

    assert temp_name not in page.get_body_text()


@allure.title("CGC-EDT-001 Edit customer gift card amount persists after save")
@pytest.mark.regression
def test_edit_customer_gift_card_amount(browser):

    page = create_customer_gift_card_if_missing(browser)
    new_amount = "30"
    page.open_edit_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)
    page.enter_customer_gift_card_amount(new_amount)
    page.click_save_customer_gift_card()
    page.wait_for_customer_list_loaded()

    page.open_edit_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)
    assert page.get_customer_gift_card_amount_value() == new_amount

    page.enter_customer_gift_card_amount(CUSTOMER_GIFT_CARD_AMOUNT)
    page.click_save_customer_gift_card()
    page.wait_for_customer_list_loaded()


@allure.title("CGC-EDT-003 Toggle active customer gift card keeps it active after save")
@pytest.mark.regression
def test_toggle_active_customer_gift_card(browser):

    page = create_customer_gift_card_if_missing(browser)
    page.open_edit_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)
    page.ensure_switch_off(page.ACTIVE_CUSTOMER_GIFT_CARD_SWITCH)
    page.ensure_switch_on(page.ACTIVE_CUSTOMER_GIFT_CARD_SWITCH)
    page.click_save_customer_gift_card()
    page.wait_for_customer_list_loaded()
    page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)

    assert page.wait_for_customer_gift_card_row(
        CUSTOMER_GIFT_CARD_NUMBER
    ).is_displayed()
    assert (
        page.get_customer_gift_card_amount(CUSTOMER_GIFT_CARD_NUMBER)
        == VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT
    )
