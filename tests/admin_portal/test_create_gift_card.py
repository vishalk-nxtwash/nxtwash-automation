from tests.admin_portal.test_gift_cards import open_gift_cards_page


GIFT_CARD_NAME = "Prime Gift card"
GIFT_CARD_AMOUNT = "25"
VISIBLE_GIFT_CARD_AMOUNT = "$25.00"
LANDING_PAGE_CODE = "Prime GC"
ASSIGNMENT_LOCATIONS = [
    "VK Test carwash 2",
    "VK Test Wash 01",
]


def create_prime_gift_card_if_missing(browser, update_existing=False):

    gift_cards_page = open_gift_cards_page(browser)

    if gift_cards_page.gift_card_exists(GIFT_CARD_NAME):
        if update_existing:
            gift_cards_page.update_gift_card_settings(
                GIFT_CARD_NAME,
                GIFT_CARD_AMOUNT,
                LANDING_PAGE_CODE,
                ASSIGNMENT_LOCATIONS
            )

        gift_cards_page.search_gift_card(GIFT_CARD_NAME)
        gift_cards_page.wait_for_gift_card_row(GIFT_CARD_NAME)
        return gift_cards_page

    gift_cards_page.create_gift_card(
        GIFT_CARD_NAME,
        GIFT_CARD_AMOUNT,
        LANDING_PAGE_CODE,
        ASSIGNMENT_LOCATIONS
    )
    gift_cards_page.search_gift_card(GIFT_CARD_NAME)
    gift_cards_page.wait_for_gift_card_row(GIFT_CARD_NAME)

    return gift_cards_page


def test_create_gift_card_required_name_validation(browser):

    gift_cards_page = open_gift_cards_page(browser)
    gift_cards_page.open_create_gift_card()
    gift_cards_page.click_save_gift_card()

    assert not gift_cards_page.gift_card_name_input_is_valid()
    assert gift_cards_page.get_gift_card_name_validation_message() != ""


def test_create_prime_gift_card_with_all_toggles_and_locations(browser):

    gift_cards_page = create_prime_gift_card_if_missing(
        browser,
        update_existing=True
    )
    gift_cards_page.wait_for_list_loaded()
    gift_cards_page.search_gift_card(GIFT_CARD_NAME)

    assert gift_cards_page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert gift_cards_page.get_gift_card_amount(
        GIFT_CARD_NAME
    ) == VISIBLE_GIFT_CARD_AMOUNT
    assert gift_cards_page.get_gift_card_status(GIFT_CARD_NAME) == "Active"

    gift_cards_page.open_edit_gift_card(GIFT_CARD_NAME)

    assert gift_cards_page.get_gift_card_name_value() == GIFT_CARD_NAME
    assert gift_cards_page.main_toggles_are_on()

    for location_name in ASSIGNMENT_LOCATIONS:
        assert gift_cards_page.location_is_assigned(location_name)
        assert gift_cards_page.location_show_on_cp_is_on(location_name)


def test_create_prime_gift_card_does_not_duplicate_existing_card(browser):

    gift_cards_page = create_prime_gift_card_if_missing(browser)
    gift_cards_page.wait_for_list_loaded()
    gift_cards_page.search_gift_card(GIFT_CARD_NAME)

    assert gift_cards_page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert gift_cards_page.get_gift_card_status(GIFT_CARD_NAME) == "Active"
