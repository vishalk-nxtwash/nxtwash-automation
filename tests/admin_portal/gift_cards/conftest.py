from pages.admin_portal.gift_cards_page import GiftCardsPage
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._managed import managed_name, managed_resource
from tests.admin_portal._data import load as _load

_D = _load("gift_cards")

GIFT_CARD_NAME                    = _D["reference"]["gift_card_name"]
GIFT_CARD_AMOUNT                  = _D["template"]["amount"]
VISIBLE_GIFT_CARD_AMOUNT          = _D["template"]["visible_amount"]
LANDING_PAGE_CODE                 = _D["template"]["landing_page_code"]
UPDATED_LANDING_PAGE_CODE         = _D["updated"]["landing_page_code"]
ASSIGNMENT_LOCATIONS              = _D["reference"]["assignment_locations"]
CUSTOMER_GIFT_CARD_SITE           = _D["customer_gift_card"]["site"]
CUSTOMER_GIFT_CARD_NUMBER         = _D["customer_gift_card"]["number"]
CUSTOMER_GIFT_CARD_AMOUNT         = _D["customer_gift_card"]["amount"]
VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT = _D["customer_gift_card"]["visible_amount"]
MISSING_GIFT_CARD                 = _D["search"]["nonexistent"]
MISSING_CUSTOMER_GIFT_CARD        = _D["search"]["nonexistent_customer"]
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
    page = open_gift_cards_page(browser)
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
        page = open_customer_gift_cards_page(browser)
        page.open_edit_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)
        page.enter_customer_gift_card_amount(CUSTOMER_GIFT_CARD_AMOUNT)
        page.ensure_active_customer_gift_card_on()
        page.click_save_customer_gift_card()
        page.wait_for_customer_list_loaded()
        page = open_customer_gift_cards_page(browser)
        page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)
        page.wait_for_customer_gift_card_row(CUSTOMER_GIFT_CARD_NUMBER)
        return page

    page.create_customer_gift_card(
        CUSTOMER_GIFT_CARD_SITE,
        GIFT_CARD_NAME,
        CUSTOMER_GIFT_CARD_NUMBER,
        CUSTOMER_GIFT_CARD_AMOUNT
    )
    page = open_customer_gift_cards_page(browser)
    page.search_customer_gift_card(CUSTOMER_GIFT_CARD_NUMBER)
    page.wait_for_customer_gift_card_row(CUSTOMER_GIFT_CARD_NUMBER)

    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


MANAGED_GIFT_CARD = managed_name("Gift Card")


def _reset_managed_gift_card(browser):
    page = open_gift_cards_page(browser)
    if page.gift_card_exists(MANAGED_GIFT_CARD):
        page.update_gift_card_settings(
            MANAGED_GIFT_CARD,
            GIFT_CARD_AMOUNT,
            LANDING_PAGE_CODE,
            ASSIGNMENT_LOCATIONS,
        )
        return open_gift_cards_page(browser)
    page.create_gift_card(
        MANAGED_GIFT_CARD,
        GIFT_CARD_AMOUNT,
        LANDING_PAGE_CODE,
        ASSIGNMENT_LOCATIONS,
    )
    return open_gift_cards_page(browser)


managed_gift_card = managed_resource(_reset_managed_gift_card)
