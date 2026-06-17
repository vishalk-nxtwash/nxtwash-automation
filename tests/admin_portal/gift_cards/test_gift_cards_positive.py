from tests.admin_portal.gift_cards.conftest import ASSIGNMENT_LOCATIONS
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import VISIBLE_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import create_gift_card_if_missing


def test_create_gift_card_with_required_settings(browser):

    page = create_gift_card_if_missing(browser, update_existing=True)
    page.wait_for_list_loaded()
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page.get_gift_card_amount(GIFT_CARD_NAME) == VISIBLE_GIFT_CARD_AMOUNT
    assert page.get_gift_card_status(GIFT_CARD_NAME) == "Active"


def test_created_gift_card_settings_persist(browser):

    page = create_gift_card_if_missing(browser, update_existing=True)
    page.open_edit_gift_card(GIFT_CARD_NAME)

    assert page.get_gift_card_name_value() == GIFT_CARD_NAME
    assert page.main_toggles_are_on()

    for location_name in ASSIGNMENT_LOCATIONS:
        assert page.location_is_assigned(location_name)
