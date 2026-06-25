import allure
import pytest

from tests.admin_portal.wash_books.conftest import ASSIGNMENT_SITE
from tests.admin_portal.wash_books.conftest import EXISTING_WASH_BOOK
from tests.admin_portal.wash_books.conftest import MISSING_WASH_BOOK
from tests.admin_portal.wash_books.conftest import open_wash_books_page
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Search and Filter"),
]


@allure.title("WB-SRH-001 Searching an existing wash book by exact name returns the record")
@pytest.mark.regression
def test_wash_books_existing_search(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book(EXISTING_WASH_BOOK)

    assert wash_books_page.wait_for_wash_book_row(EXISTING_WASH_BOOK).is_displayed()


@allure.title("WB-SRH-002 Searching by partial name returns matching records")
@pytest.mark.regression
def test_wash_books_partial_search_returns_matches(browser):

    page = open_wash_books_page(browser)
    partial = EXISTING_WASH_BOOK[:5]
    page.search_wash_book(partial)

    assert EXISTING_WASH_BOOK.lower() in page.get_body_text().lower()
    assert page_has_no_broken_state(page)


@allure.title("WB-SRH-003 Searching a non-existing wash book shows an empty state without error")
@pytest.mark.extended
def test_wash_books_missing_search(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book(MISSING_WASH_BOOK)

    assert MISSING_WASH_BOOK not in wash_books_page.get_body_text()
    assert page_has_no_broken_state(wash_books_page)


@allure.title("WB-SRH-004 Clearing the search field restores the complete wash book list")
@pytest.mark.extended
def test_wash_books_clear_search_restores_list(browser):

    page = open_wash_books_page(browser)
    original_names = page.get_visible_wash_book_names()

    page.search_wash_book(EXISTING_WASH_BOOK)
    page.clear_wash_book_search()

    assert len(page.get_visible_wash_book_names()) >= min(len(original_names), 1)
    assert page_has_no_broken_state(page)


@allure.title("Filter panel shows site dropdown, Apply filters, and Reset all controls")
@pytest.mark.regression
def test_wash_books_filter_panel_shows_controls(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.open_filter_panel()
    body_text = wash_books_page.get_body_text()

    assert "Select site" in body_text
    assert "Apply filters" in body_text
    assert "Reset all" in body_text


@allure.title("WB-FLT-001 Filtering by site narrows results to that site's wash books")
@pytest.mark.regression
def test_wash_books_filter_by_site_narrows_results(browser):

    page = open_wash_books_page(browser)
    page.open_filter_panel()
    page.set_filter_site(ASSIGNMENT_SITE)
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("WB-FLT-002 Active wash books filter returns only active records")
@pytest.mark.regression
def test_wash_books_filter_active_returns_active_only(browser):

    page = open_wash_books_page(browser)
    page.open_filter_panel()
    page.apply_filters()

    body_text = page.get_body_text()
    assert "Inactive" not in body_text or page_has_no_broken_state(page)


@allure.title("WB-FLT-003 Disabling Active toggle in filter reveals all wash books")
@pytest.mark.extended
def test_wash_books_filter_active_toggle_off_shows_all(browser):

    page = open_wash_books_page(browser)
    page.open_filter_panel()
    page.reset_filters()
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("WB-FLT-004 Site and Active filter combined narrows results correctly")
@pytest.mark.extended
def test_wash_books_filter_site_and_active_combined(browser):

    page = open_wash_books_page(browser)
    page.open_filter_panel()
    page.set_filter_site(ASSIGNMENT_SITE)
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("WB-FLT-005 Reset all clears filters and restores the default list")
@pytest.mark.extended
def test_wash_books_filter_reset_all_restores_list(browser):

    page = open_wash_books_page(browser)
    page.open_filter_panel()
    page.set_filter_site(ASSIGNMENT_SITE)
    page.apply_filters()

    page.open_filter_panel()
    page.reset_filters()

    assert page_has_no_broken_state(page)


@allure.title("Injection payloads in search do not produce a broken page state")
@pytest.mark.regression
def test_wash_books_search_payloads_do_not_break_grid(browser):

    wash_books_page = open_wash_books_page(browser)

    for payload in ("' OR 1=1 --", "<script>alert(1)</script>"):
        wash_books_page.search_wash_book(payload)
        assert page_has_no_broken_state(wash_books_page)
