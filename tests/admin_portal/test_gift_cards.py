from pages.admin_portal.gift_cards_page import GiftCardsPage
from pages.admin_portal.login_page import AdminLoginPage
from pages.admin_portal.sidebar import AdminSidebar


MISSING_GIFT_CARD = "gift-card-does-not-exist-automation"


def open_gift_cards_page(browser):

    login_page = AdminLoginPage(browser)
    login_page.open()
    login_page.wait_for_loaded()
    login_page.login()
    login_page.wait_for_overview()

    sidebar = AdminSidebar(browser)
    sidebar.open_gift_cards()

    gift_cards_page = GiftCardsPage(browser)
    gift_cards_page.wait_for_list_loaded()

    return gift_cards_page


def test_gift_cards_page_loads(browser):

    gift_cards_page = open_gift_cards_page(browser)

    assert "Gift card name" in gift_cards_page.get_body_text()
    assert "Gift card amount" in gift_cards_page.get_body_text()
    assert "Status" in gift_cards_page.get_body_text()


def test_gift_cards_missing_gift_card_search(browser):

    gift_cards_page = open_gift_cards_page(browser)
    gift_cards_page.search_gift_card(MISSING_GIFT_CARD)

    assert MISSING_GIFT_CARD not in gift_cards_page.get_body_text()


def test_gift_cards_download_button_is_available(browser):

    gift_cards_page = open_gift_cards_page(browser)

    assert gift_cards_page.download_button_is_clickable()
