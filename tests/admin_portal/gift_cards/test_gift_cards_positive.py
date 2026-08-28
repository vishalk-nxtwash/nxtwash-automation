import uuid

import allure
import pytest

from tests.admin_portal.gift_cards.conftest import ASSIGNMENT_LOCATIONS
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_NUMBER
from tests.admin_portal.gift_cards.conftest import CUSTOMER_GIFT_CARD_SITE
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import GIFT_CARD_NAME
from tests.admin_portal.gift_cards.conftest import LANDING_PAGE_CODE
from tests.admin_portal.gift_cards.conftest import VISIBLE_CUSTOMER_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import VISIBLE_GIFT_CARD_AMOUNT
from tests.admin_portal.gift_cards.conftest import create_customer_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import create_gift_card_if_missing
from tests.admin_portal.gift_cards.conftest import open_customer_gift_cards_page
from tests.admin_portal.gift_cards.conftest import open_gift_cards_page
from tests.admin_portal.gift_cards.conftest import page_has_no_broken_state


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


@allure.title("GC-CRT-002 Create gift card with expiration date")
@pytest.mark.regression
@pytest.mark.skip(
    reason="GC-CRT-002: expiration date input locator not yet mapped in the page object."
)
def test_create_gift_card_with_expiration_date(browser):
    pass


@allure.title("GC-CRT-003 Create gift card with a discount assigned")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "GC-CRT-003: requires a known active discount; cross-module dependency "
        "not yet set up. Wire discount name from discounts conftest and implement."
    )
)
def test_create_gift_card_with_discount(browser):
    pass


@allure.title("GC-CRT-004 Create gift card with a landing page code persists")
@pytest.mark.regression
def test_create_gift_card_with_landing_page_code(browser):

    temp_name = "VK CRT004-%s" % uuid.uuid4().hex[:6]
    lp_code = "VKCRT004-%s" % uuid.uuid4().hex[:5].upper()
    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name(temp_name)
    page.enter_gift_card_amount(GIFT_CARD_AMOUNT)
    page.enter_landing_page_code(lp_code)
    page.assign_location(ASSIGNMENT_LOCATIONS[0])
    page.ensure_switch_on(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()
    page.wait_for_list_after_edit_save()
    page.open_edit_gift_card(temp_name)

    assert page.get_landing_page_code_value() == lp_code


@allure.title("GC-CRT-005 Create gift card with Open price enabled")
@pytest.mark.regression
def test_create_gift_card_with_open_price(browser):

    temp_name = "VK CRT005-%s" % uuid.uuid4().hex[:6]
    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name(temp_name)
    page.enter_gift_card_amount(GIFT_CARD_AMOUNT)
    page.enter_landing_page_code(LANDING_PAGE_CODE)
    page.assign_location(ASSIGNMENT_LOCATIONS[0])
    page.ensure_switch_on(page.OPEN_PRICE_SWITCH)
    page.ensure_switch_on(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()
    page.wait_for_list_after_edit_save()
    page.open_edit_gift_card(temp_name)

    assert page.switch_is_on(page.OPEN_PRICE_SWITCH)


@allure.title("GC-CRT-006 Create gift card with Wash card enabled")
@pytest.mark.regression
def test_create_gift_card_with_wash_card(browser):

    temp_name = "VK CRT006-%s" % uuid.uuid4().hex[:6]
    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name(temp_name)
    page.enter_gift_card_amount(GIFT_CARD_AMOUNT)
    page.enter_landing_page_code(LANDING_PAGE_CODE)
    page.assign_location(ASSIGNMENT_LOCATIONS[0])
    page.ensure_switch_on(page.WASH_CARD_SWITCH)
    page.ensure_switch_on(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()
    page.wait_for_list_after_edit_save()
    page.open_edit_gift_card(temp_name)

    assert page.switch_is_on(page.WASH_CARD_SWITCH)


@allure.title("GC-CRT-007 Create gift card with Show on customer portal enabled")
@pytest.mark.regression
def test_create_gift_card_with_show_on_portal(browser):

    temp_name = "VK CRT007-%s" % uuid.uuid4().hex[:6]
    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name(temp_name)
    page.enter_gift_card_amount(GIFT_CARD_AMOUNT)
    page.enter_landing_page_code(LANDING_PAGE_CODE)
    page.assign_location(ASSIGNMENT_LOCATIONS[0])
    page.ensure_switch_on(page.SHOW_ON_CUSTOMER_PORTAL_SWITCH)
    page.ensure_switch_on(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()
    page.wait_for_list_after_edit_save()
    page.open_edit_gift_card(temp_name)

    assert page.switch_is_on(page.SHOW_ON_CUSTOMER_PORTAL_SWITCH)


@allure.title("GC-CRT-009 Assign gift card to a single site")
@pytest.mark.regression
def test_create_gift_card_assigned_to_single_site(browser):

    temp_name = "VK CRT009-%s" % uuid.uuid4().hex[:6]
    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name(temp_name)
    page.enter_gift_card_amount(GIFT_CARD_AMOUNT)
    page.enter_landing_page_code(LANDING_PAGE_CODE)
    page.assign_location(ASSIGNMENT_LOCATIONS[0])
    page.ensure_switch_on(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()
    page.wait_for_list_after_edit_save()
    page.open_edit_gift_card(temp_name)

    assert page.location_is_assigned(ASSIGNMENT_LOCATIONS[0])


@allure.title("GC-CRT-010 Assign gift card to multiple sites")
@pytest.mark.regression
def test_create_gift_card_assigned_to_multiple_sites(browser):

    temp_name = "VK CRT010-%s" % uuid.uuid4().hex[:6]
    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name(temp_name)
    page.enter_gift_card_amount(GIFT_CARD_AMOUNT)
    page.enter_landing_page_code(LANDING_PAGE_CODE)
    for loc in ASSIGNMENT_LOCATIONS[:2]:
        page.assign_location(loc)
    page.ensure_switch_on(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()
    page.wait_for_list_after_edit_save()
    page.open_edit_gift_card(temp_name)

    assert page.location_is_assigned(ASSIGNMENT_LOCATIONS[0])
    assert page.location_is_assigned(ASSIGNMENT_LOCATIONS[1])


@allure.title("GC-CRT-011 Enable Show on CP per site on a new gift card")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "GC-CRT-011: per-location Show on CP is not persisted by the server — "
        "the switch resets to OFF on reload. Remove xfail once the API is fixed."
    ),
)
def test_create_gift_card_with_show_on_cp_per_site(browser):

    temp_name = "VK CRT011-%s" % uuid.uuid4().hex[:6]
    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.enter_gift_card_name(temp_name)
    page.enter_gift_card_amount(GIFT_CARD_AMOUNT)
    page.enter_landing_page_code(LANDING_PAGE_CODE)
    page.assign_location(ASSIGNMENT_LOCATIONS[0])
    page.ensure_switch_on(page.SHOW_ON_CUSTOMER_PORTAL_SWITCH)
    page.enable_location_show_on_cp(ASSIGNMENT_LOCATIONS[0])
    page.ensure_switch_on(page.ACTIVE_SERVICE_SWITCH)
    page.click_save_gift_card()
    page.wait_for_list_after_edit_save()
    page.open_edit_gift_card(temp_name)

    assert page.location_show_on_cp_is_on(ASSIGNMENT_LOCATIONS[0])


@allure.title("GC-CRT-012 Cancel out of Add new gift card returns to list")
@pytest.mark.regression
def test_cancel_add_gift_card_returns_to_list(browser):

    page = open_gift_cards_page(browser)
    page.open_create_gift_card()
    page.click_cancel()
    page.wait_for_list_loaded()

    assert page.add_gift_card_button_is_clickable()
    assert page_has_no_broken_state(page)


@allure.title("CGC-CRT-002 Select gift card dropdown lists available gift cards")
@pytest.mark.regression
def test_cgc_create_form_gift_card_dropdown_lists_cards(browser):

    create_gift_card_if_missing(browser)
    page = open_customer_gift_cards_page(browser)
    page.open_create_customer_gift_card()
    page.select_customer_gift_card_site(CUSTOMER_GIFT_CARD_SITE)

    assert page.gift_card_option_exists_in_dropdown(GIFT_CARD_NAME)


@allure.title("CGC-CRT-003 Filter by site narrows gift card dropdown in CGC form")
@pytest.mark.regression
def test_cgc_site_selection_populates_gift_card_dropdown(browser):

    create_gift_card_if_missing(browser)
    page = open_customer_gift_cards_page(browser)
    page.open_create_customer_gift_card()
    page.select_customer_gift_card_site(CUSTOMER_GIFT_CARD_SITE)

    # GIFT_CARD_NAME is assigned to CUSTOMER_GIFT_CARD_SITE — must appear in dropdown
    assert page.gift_card_option_exists_in_dropdown(GIFT_CARD_NAME)


@allure.title("CGC-CRT-007 Create inactive customer gift card is not visible by default")
@pytest.mark.regression
def test_create_inactive_customer_gift_card(browser):

    page = open_customer_gift_cards_page(browser)
    page.open_create_customer_gift_card()
    page.select_customer_gift_card_site(CUSTOMER_GIFT_CARD_SITE)
    page.select_customer_gift_card_template(GIFT_CARD_NAME)
    inactive_number = "VKCGCINACT-%s" % uuid.uuid4().hex[:6].upper()
    page.enter_customer_gift_card_number(inactive_number)
    page.enter_customer_gift_card_amount(CUSTOMER_GIFT_CARD_AMOUNT)
    page.ensure_switch_off(page.ACTIVE_CUSTOMER_GIFT_CARD_SWITCH)
    page.click_save_customer_gift_card()
    page.wait_for_customer_list_loaded()
    page.search_customer_gift_card(inactive_number)

    assert inactive_number not in page.get_body_text()


@allure.title("CGC-CRT-008 Cancel out of Add customer gift card returns to list")
@pytest.mark.regression
def test_cancel_add_customer_gift_card_returns_to_list(browser):

    page = open_customer_gift_cards_page(browser)
    page.open_create_customer_gift_card()
    page.click_cancel()
    page.wait_for_customer_list_loaded()

    assert page.add_customer_gift_card_button_is_clickable()
    assert page_has_no_broken_state(page)
