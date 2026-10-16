import allure
import pytest

from tests.admin_portal.wash_books.conftest import (
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    MANAGED_WASH_BOOK,
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
def test_assign_single_site_persists(managed_wash_book):

    page = managed_wash_book
    page.open_edit_wash_book(MANAGED_WASH_BOOK)
    page.assign_location_by_index(0)
    page.click_save_wash_book()
    page.wait_for_list_loaded()

    page.open_edit_wash_book(MANAGED_WASH_BOOK)
    assert page.location_is_assigned_by_index(0)
    assert page_has_no_broken_state(page)


@allure.title("WB-SIT-002 Assigning multiple sites persists after save")
@pytest.mark.regression
@pytest.mark.skip(
    reason="CI-SKIP WB-SIT-002: Inovua site-assignment grid times out in "
           "headless Chrome. Fix: same as WB-EDT-004 — retry on "
           "StaleElementReferenceException, wait for grid row stability."
)
def test_assign_multiple_sites_persists(managed_wash_book):

    page = managed_wash_book
    page.open_edit_wash_book(MANAGED_WASH_BOOK)
    page.assign_all_locations()
    page.click_save_wash_book()
    page.wait_for_list_loaded()

    page.open_edit_wash_book(MANAGED_WASH_BOOK)
    page.wait_for_service_location_rows()
    location_count = len(page.visible_service_location_rows())
    for i in range(location_count):
        assert page.location_is_assigned_by_index(i)
    assert page_has_no_broken_state(page)


@allure.title("WB-SIT-003 Location price override persists after save")
@pytest.mark.regression
def test_location_price_override_persists(managed_wash_book):

    # managed_wash_book's reset deliberately does not touch location price/
    # commission (see _reset_managed_wash_book) — reset it back here so it
    # doesn't leak into whatever test runs next on this fixture.
    override_price = "45"
    page = managed_wash_book
    page.open_edit_wash_book(MANAGED_WASH_BOOK)
    page.assign_location_by_index(0)
    page.set_location_price_and_commission_by_index(0, override_price, GLOBAL_COMMISSION)
    page.click_save_wash_book()
    page.wait_for_list_loaded()

    page.open_edit_wash_book(MANAGED_WASH_BOOK)
    assert page.get_location_price_by_index(0) == override_price
    assert page_has_no_broken_state(page)

    page.set_location_price_and_commission_by_index(0, GLOBAL_PRICE, GLOBAL_COMMISSION)
    page.click_save_wash_book()
    page.wait_for_list_loaded()


@allure.title("WB-SIT-004 Saving a wash book with no site assigned is handled gracefully")
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


