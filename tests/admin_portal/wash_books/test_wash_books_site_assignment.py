import allure
import pytest

from tests.admin_portal.wash_books.conftest import (
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    WASH_BOOK_NAME,
    create_wash_book_if_missing,
    open_wash_books_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Site Assignment"),
]


@allure.title("WB-SIT-001 Assigning a single site persists after save")
@pytest.mark.regression
@pytest.mark.xfail(
    reason=(
        "WB-SIT-001: EDIT_FRAME iframe not found on second open_edit_wash_book after "
        "saving with location assignment. Needs DevTools inspection of iframe src."
    ),
    strict=False,
)
def test_assign_single_site_persists(browser):

    page = create_wash_book_if_missing(browser)
    page.open_edit_wash_book(WASH_BOOK_NAME)
    page.assign_location_by_index(0)
    page.click_save_wash_book()
    page.wait_for_list_loaded()

    page.open_edit_wash_book(WASH_BOOK_NAME)
    assert page.location_is_assigned_by_index(0)
    assert page_has_no_broken_state(page)


@allure.title("WB-SIT-002 Assigning multiple sites persists after save")
@pytest.mark.regression
@pytest.mark.skip(
    reason="CI-SKIP WB-SIT-002: Inovua site-assignment grid times out in "
           "headless Chrome. Fix: same as WB-EDT-004 — retry on "
           "StaleElementReferenceException, wait for grid row stability."
)
def test_assign_multiple_sites_persists(browser):

    page = create_wash_book_if_missing(browser)
    page.open_edit_wash_book(WASH_BOOK_NAME)
    page.assign_all_locations()
    page.click_save_wash_book()
    page.wait_for_list_loaded()

    page.open_edit_wash_book(WASH_BOOK_NAME)
    page.wait_for_service_location_rows()
    location_count = len(page.visible_service_location_rows())
    for i in range(location_count):
        assert page.location_is_assigned_by_index(i)
    assert page_has_no_broken_state(page)


@allure.title("WB-SIT-003 Location price override persists after save")
@pytest.mark.regression
def test_location_price_override_persists(browser):

    override_price = "45"
    page = create_wash_book_if_missing(browser)
    page.open_edit_wash_book(WASH_BOOK_NAME)
    page.assign_location_by_index(0)
    page.set_location_price_and_commission_by_index(0, override_price, GLOBAL_COMMISSION)
    page.click_save_wash_book()
    page.wait_for_list_loaded()

    page.open_edit_wash_book(WASH_BOOK_NAME)
    assert page.get_location_price_by_index(0) == override_price
    assert page_has_no_broken_state(page)

    page.set_location_price_and_commission_by_index(0, GLOBAL_PRICE, GLOBAL_COMMISSION)
    page.click_save_wash_book()
    page.wait_for_list_loaded()


@allure.title("WB-SIT-004 Saving a wash book with no site assigned is handled gracefully")
@pytest.mark.smoke
def test_save_wash_book_with_no_site_assigned(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-no-site-test")
    page.set_number_of_washes("5")
    page.set_global_price("10")
    page.click_save_wash_book()

    assert page_has_no_broken_state(page)


@allure.title("WB-SIT-005 Per-site Show on customer portal toggle persists (deferred)")
@pytest.mark.extended
@pytest.mark.skip(
    reason="WB-SIT-005: Per-site Show on customer portal requires Customer Portal "
    "integration to verify visibility. Deferred."
)
def test_per_site_customer_portal_toggle_persists(browser):
    pass


