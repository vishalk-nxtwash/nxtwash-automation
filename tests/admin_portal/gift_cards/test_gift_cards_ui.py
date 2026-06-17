from tests.admin_portal.gift_cards.conftest import open_gift_cards_page
from tests.admin_portal.gift_cards.conftest import page_has_no_broken_state


def test_gift_cards_page_loads(browser):

    page = open_gift_cards_page(browser)
    body_text = page.get_body_text()

    assert "Gift card name" in body_text
    assert "Gift card amount" in body_text
    assert "Status" in body_text
    assert page_has_no_broken_state(page)


def test_gift_cards_primary_actions_are_available(browser):

    page = open_gift_cards_page(browser)

    assert page.download_button_is_clickable()
    assert "+ Add new gift card" in page.get_body_text()
    assert "Customer gift cards" in page.get_body_text()
