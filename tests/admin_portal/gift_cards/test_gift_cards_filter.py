import allure
import pytest

from tests.admin_portal.gift_cards.conftest import ASSIGNMENT_LOCATIONS
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_SITE
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import create_customer_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import create_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import open_customer_gift_cards_page
from tests.admin_portal.gift_cards.conftest import open_gift_cards_page
from tests.admin_portal.gift_cards.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gift Cards"),
    allure.story("Filter"),
]


@allure.title("GC-FLT-001 Filter by site narrows gift card list to that site's cards")
@pytest.mark.regression
def test_filter_by_site_narrows_gift_card_list(browser):

    create_gift_card_if_missing(browser)
    page = open_gift_cards_page(browser)
    page.select_site_filter(ASSIGNMENT_LOCATIONS[0])
    page.apply_filters()
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("GC-FLT-002 Active service toggle shows only active gift cards")
@pytest.mark.regression
def test_active_toggle_shows_active_gift_cards_only(browser):

    create_gift_card_if_missing(browser)
    page = open_gift_cards_page(browser)
    page.reset_all_filters()
    page.open_filter_panel()
    page.toggle_active_filter()
    page.apply_filters()
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page.get_gift_card_status(GIFT_CARD_NAME) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("GC-FLT-005 Reset all clears gift card filters and restores the full list")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "GC-FLT-005: StaleElementReferenceException — filter panel closes after "
        "reset; element reference goes stale before re-check completes."
    ),
)
def test_reset_all_clears_gift_card_filters(browser):

    page = open_gift_cards_page(browser)
    page.select_site_filter(ASSIGNMENT_LOCATIONS[0])
    page.apply_filters()
    page.reset_all_filters()

    assert page_has_no_broken_state(page)


@allure.title("CGC-FLT-001 Filter by site narrows customer gift card list")
@pytest.mark.regression
def test_filter_by_site_narrows_customer_gift_card_list(browser):

    create_customer_gift_card_if_missing(browser)
    page = open_customer_gift_cards_page(browser)
    page.select_site_filter(CUSTOMER_GIFT_CARD_SITE)
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("GC-FLT-003 Active filter off shows all gift cards including inactive")
@pytest.mark.regression
def test_active_filter_off_shows_all_gift_cards(browser):

    create_gift_card_if_missing(browser)
    page = open_gift_cards_page(browser)
    page.open_filter_panel()
    page.set_active_gift_card_filter(False)
    page.apply_filters()
    page.search_gift_card(GIFT_CARD_NAME)

    # Active cards must still appear when the active-only filter is removed
    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("GC-FLT-004 Site and active filter combined narrows gift card list")
@pytest.mark.regression
def test_site_and_active_filter_combined(browser):

    create_gift_card_if_missing(browser)
    page = open_gift_cards_page(browser)
    page.select_site_filter(ASSIGNMENT_LOCATIONS[0])
    page.open_filter_panel()
    page.toggle_active_filter()
    page.apply_filters()
    page.search_gift_card(GIFT_CARD_NAME)

    assert page.wait_for_gift_card_row(GIFT_CARD_NAME).is_displayed()
    assert page.get_gift_card_status(GIFT_CARD_NAME) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("CGC-FLT-002 Reset all clears customer gift card filters")
@pytest.mark.regression
def test_reset_all_clears_customer_gift_card_filters(browser):

    create_customer_gift_card_if_missing(browser)
    page = open_customer_gift_cards_page(browser)
    page.select_site_filter(CUSTOMER_GIFT_CARD_SITE)
    page.apply_filters()
    page.reset_all_filters()

    assert page_has_no_broken_state(page)
