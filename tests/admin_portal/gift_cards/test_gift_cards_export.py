import allure
import pytest

from tests.admin_portal.gift_cards.conftest import create_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import create_customer_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import open_customer_gift_cards_page
from tests.admin_portal.gift_cards.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gift Cards"),
    allure.story("Export"),
]


@allure.title("GC-EXP-001 Export button triggers download without breaking the page")
@pytest.mark.regression
def test_gift_card_export_triggers_download(browser):

    create_gift_card_if_missing(browser)
    page = create_gift_card_if_missing(browser)
    page.click_download_button()

    assert page_has_no_broken_state(page)


@allure.title("CGC-EXP-001 Export button on customer gift cards tab triggers download")
@pytest.mark.regression
def test_customer_gift_card_export_triggers_download(browser):

    create_customer_gift_card_if_missing(browser)
    page = open_customer_gift_cards_page(browser)
    page.click_download_button()

    assert page_has_no_broken_state(page)
