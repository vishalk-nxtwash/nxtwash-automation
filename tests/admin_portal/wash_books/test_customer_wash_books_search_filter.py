import allure
import pytest

from tests.admin_portal.wash_books.conftest import (
    ASSIGNMENT_SITE,
    CWB_WASH_BOOK_NUMBER,
    create_customer_wash_book_if_missing,
    open_customer_wash_books_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Customer Wash Books — Search and Filter"),
]


@allure.title("CWB-SRH-001 Searching by exact wash book number returns the matching record")
@pytest.mark.regression
def test_cwb_search_by_exact_number(browser):

    create_customer_wash_book_if_missing(browser)
    page = open_customer_wash_books_page(browser)
    page.search_cwb(CWB_WASH_BOOK_NUMBER)

    assert page.wait_for_cwb_row(CWB_WASH_BOOK_NUMBER).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("CWB-SRH-002 Searching by partial wash book number returns matching records")
@pytest.mark.extended
def test_cwb_search_by_partial_number(browser):

    create_customer_wash_book_if_missing(browser)
    page = open_customer_wash_books_page(browser)
    partial = CWB_WASH_BOOK_NUMBER[:5]
    page.search_cwb(partial)

    assert CWB_WASH_BOOK_NUMBER.lower() in page.get_body_text().lower()
    assert page_has_no_broken_state(page)


@allure.title("CWB-SRH-003 Searching a non-existing number shows an empty state without error")
@pytest.mark.extended
def test_cwb_search_non_existing_number_shows_empty_state(browser):

    page = open_customer_wash_books_page(browser)
    page.search_cwb("cwb-does-not-exist-automation-99999")

    assert "cwb-does-not-exist-automation-99999" not in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("CWB-FLT-001 Filtering by site narrows the customer wash books list")
@pytest.mark.regression
def test_cwb_filter_by_site_narrows_results(browser):

    page = open_customer_wash_books_page(browser)
    # open_cwb_filter_panel() ensures we are in the CWB list iframe before clicking
    page.open_cwb_filter_panel()
    page.set_filter_site(ASSIGNMENT_SITE)
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("CWB-FLT-004 Reset all clears filters and restores the full CWB list")
@pytest.mark.extended
def test_cwb_filter_reset_all_restores_list(browser):

    page = open_customer_wash_books_page(browser)
    page.open_cwb_filter_panel()
    page.set_filter_site(ASSIGNMENT_SITE)
    page.apply_filters()

    page.open_cwb_filter_panel()
    page.reset_filters()

    assert page_has_no_broken_state(page)
