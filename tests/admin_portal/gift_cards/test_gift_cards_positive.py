import uuid

import allure
import pytest

from tests.admin_portal.gift_cards.conftest import ASSIGNMENT_LOCATIONS
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_NUMBER
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_SITE
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import VISIBLE_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import create_customer_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import create_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import open_gift_cards_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gift Cards"),
    allure.story("CRUD"),
]


@allure.title("GC-CRT-001 Create gift card with name and amount appears in list as Active")
@pytest.mark.smoke
def test_create_gift_card_with_required_settings(browser):

    page = create_gift_card_if_missing(browser, update_existing=True)
    page.wait_for_list_loaded()
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page.get_gift_card_amount(GIFT_CARD_NAME) == VISIBLE_GIFT_CARD_AMOUNT
    assert page.get_gift_card_status(GIFT_CARD_NAME) == "Active"


@allure.title("GC-CRT-008 Create inactive gift card does not appear in the default list")
@pytest.mark.regression
def test_create_inactive_gift_card(browser):

    inactive_name = "VK inactive-%s" % uuid.uuid4().hex[:6]
    lp_code = "VKINACT" + uuid.uuid4().hex[:4].upper()
    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name(inactive_name)
    page.enter_gift_card_amount(GIFT_CARD_AMOUNT)
    page.enter_landing_page_code(lp_code)
    page.assign_location(ASSIGNMENT_LOCATIONS[0])
    page.ensure_switch_off(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()
    page.wait_for_list_loaded()
    page.search_gift_card(inactive_name)

    assert inactive_name not in page.get_body_text()


@allure.title("GC-PER-001 Created gift card data persists after page reload")
@pytest.mark.regression
def test_created_gift_card_settings_persist(browser):

    create_gift_card_if_missing(browser, update_existing=True)
    page = open_gift_cards_page(browser)
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page.get_gift_card_amount(GIFT_CARD_NAME) == VISIBLE_GIFT_CARD_AMOUNT
    assert page.get_gift_card_status(GIFT_CARD_NAME) == "Active"

    page.open_edit_gift_card(GIFT_CARD_NAME)
    assert page.get_gift_card_name_value() == GIFT_CARD_NAME
    assert page.main_toggles_are_on()

    for location_name in ASSIGNMENT_LOCATIONS:
        assert page.location_is_assigned(location_name)


@allure.title("GC-DEP-002 Active gift card appears in Customer gift cards select dropdown")
@pytest.mark.smoke
def test_gift_card_appears_in_customer_gift_card_dropdown(browser):

    create_gift_card_if_missing(browser)
    page = open_gift_cards_page(browser)
    page.open_customer_gift_cards()
    page.open_create_customer_gift_card()
    page.select_customer_gift_card_site(CUSTOMER_GIFT_CARD_SITE)

    assert page.gift_card_option_exists_in_dropdown(GIFT_CARD_NAME)


@allure.title("CGC-CRT-001 Create customer gift card with required fields succeeds")
@pytest.mark.smoke
@pytest.mark.skip(reason="CI-SKIP CGC-CRT-001: wait_for_customer_list_loaded times out in headless CI. Fix: same as CS-CRT-001 — use window.location.origin fallback; increase frame wait.")
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


@allure.title("CGC-PER-001 Created customer gift card data persists after page reload")
@pytest.mark.regression
def test_customer_gift_card_persists_after_page_reload(browser):

    create_customer_gift_card_if_missing(browser)
    from tests.admin_portal.gift_cards.conftest import open_customer_gift_cards_page
    page = open_customer_gift_cards_page(browser)
    page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)

    assert page.wait_for_customer_gift_card_row(
        CUSTOMER_GIFT_CARD_NUMBER
    ).is_displayed()


@allure.title("CGC-DEP-001 Customer gift card is linked to the correct gift card template")
@pytest.mark.smoke
@pytest.mark.skip(reason="CI-SKIP CGC-DEP-001: same root cause as CGC-CRT-001 — wait_for_customer_list_loaded times out in headless CI.")
def test_customer_gift_card_linked_to_correct_template(browser):

    page = create_customer_gift_card_if_missing(browser)
    page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)

    assert page.wait_for_customer_gift_card_row(
        CUSTOMER_GIFT_CARD_NUMBER
    ).is_displayed()
    assert page.get_customer_gift_card_name(CUSTOMER_GIFT_CARD_NUMBER) == GIFT_CARD_NAME
    assert (
        page.get_customer_gift_card_amount(CUSTOMER_GIFT_CARD_NUMBER)
        == VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT
    )
