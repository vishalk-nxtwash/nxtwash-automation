from pages.admin_portal.gift_cards_page import GiftCardsPage
from tests.admin_portal.admin_session import open_admin_path


GIFT_CARD_NAME = "VK AGC1"
GIFT_CARD_AMOUNT = "25"
VISIBLE_GIFT_CARD_AMOUNT = "$25.00"
LANDING_PAGE_CODE = "VKAGC1"
UPDATED_LANDING_PAGE_CODE = "VKAGC1-EDIT"
ASSIGNMENT_LOCATIONS = [
    "VK AL11",
    "VK Test Wash 01",
]
CUSTOMER_GIFT_CARD_SITE = "VK Test carwash 2"
CUSTOMER_GIFT_CARD_NUMBER = "VKAGC1001"
CUSTOMER_GIFT_CARD_AMOUNT = "25"
VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT = "$25.00"
MISSING_GIFT_CARD = "gift-card-does-not-exist-automation"
MISSING_CUSTOMER_GIFT_CARD = "customer-gift-card-does-not-exist-automation"
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def open_gift_cards_page(browser):

    open_admin_path(browser, "/services/giftCards")

    page = GiftCardsPage(browser)
    page.wait_for_list_loaded()

    return page


def create_gift_card_if_missing(browser, update_existing=False):

    page = open_gift_cards_page(browser)

    if page.gift_card_exists(GIFT_CARD_NAME):
        if update_existing:
            page = open_gift_cards_page(browser)
            page.update_gift_card_settings(
                GIFT_CARD_NAME,
                GIFT_CARD_AMOUNT,
                LANDING_PAGE_CODE,
                ASSIGNMENT_LOCATIONS
            )

        page = open_gift_cards_page(browser)
        page.search_gift_card(GIFT_CARD_NAME)
        page.wait_for_gift_card_row(GIFT_CARD_NAME)
        return page

    page.create_gift_card(
        GIFT_CARD_NAME,
        GIFT_CARD_AMOUNT,
        LANDING_PAGE_CODE,
        ASSIGNMENT_LOCATIONS
    )
    page.search_gift_card(GIFT_CARD_NAME)
    page.wait_for_gift_card_row(GIFT_CARD_NAME)

    return page


def open_customer_gift_cards_page(browser):

    page = create_gift_card_if_missing(browser)
    page.open_customer_gift_cards()

    return page


def create_customer_gift_card_if_missing(browser):

    page = open_customer_gift_cards_page(browser)

    if page.customer_gift_card_exists(CUSTOMER_GIFT_CARD_NUMBER):
        return page

    page.create_customer_gift_card(
        CUSTOMER_GIFT_CARD_SITE,
        GIFT_CARD_NAME,
        CUSTOMER_GIFT_CARD_NUMBER,
        CUSTOMER_GIFT_CARD_AMOUNT
    )
    page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)
    page.wait_for_customer_gift_card_row(CUSTOMER_GIFT_CARD_NUMBER)

    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)
