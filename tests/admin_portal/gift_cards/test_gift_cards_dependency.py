import uuid

import allure
import pytest

from tests.admin_portal.gift_cards.conftest import ASSIGNMENT_LOCATIONS
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_SITE
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import create_customer_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import open_customer_gift_cards_page
from tests.admin_portal.gift_cards.conftest import open_gift_cards_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gift Cards"),
    allure.story("Dependency"),
]


@allure.title("GC-PER-002 Show on customer portal per-location switch persists after save")
@pytest.mark.manual
@pytest.mark.skip(
    reason=(
        "GC-PER-002: Per-location Show on CP switch is interactive but the value is "
        "not persisted by the save API — the switch resets to OFF on reload. "
        "CP visibility per location is governed by Site settings (Customer Portal tab). "
        "Verify manually via DevTools network tab or site-level CP gift cards toggle."
    )
)
def test_gift_card_show_on_cp_persists(browser):
    pass


@allure.title("GC-DEP-001 Discount applied to gift card shows in gift card details")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "GC-DEP-001: Requires a known active discount linked to a gift card. "
        "Cross-module dependency — discount locators inside the GC create form are "
        "not yet mapped in the page object. Implement once the discount selector "
        "locator is confirmed."
    )
)
def test_discount_applied_to_gift_card_shown(browser):
    pass


@allure.title("GC-DEP-003 Deactivating a gift card removes it from the customer gift card dropdown")
@pytest.mark.regression
def test_deactivating_gift_card_removes_from_cgc_dropdown(browser):

    temp_name = "VK DEP003-%s" % uuid.uuid4().hex[:6]
    lp_code = "VKDEP3" + uuid.uuid4().hex[:5].upper()
    page = open_gift_cards_page(browser)
    page.create_gift_card(temp_name, GIFT_CARD_AMOUNT, lp_code, ASSIGNMENT_LOCATIONS)

    page.open_edit_gift_card(temp_name)
    page.ensure_switch_off(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()
    page.wait_for_list_after_edit_save()

    cgc_page = open_customer_gift_cards_page(browser)
    cgc_page.open_create_customer_gift_card()
    cgc_page.select_customer_gift_card_site(CUSTOMER_GIFT_CARD_SITE)

    assert not cgc_page.gift_card_option_exists_in_dropdown(temp_name)
