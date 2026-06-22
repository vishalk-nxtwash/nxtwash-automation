import allure
import pytest

from tests.admin_portal.wash_extras.conftest import EXISTING_EXTRA
from tests.admin_portal.wash_extras.conftest import MISSING_EXTRA
from tests.admin_portal.wash_extras.conftest import open_wash_extras_page
from tests.admin_portal.wash_extras.conftest import page_has_no_broken_state

ASSIGNMENT_SITE = "VK Test carwash 2"

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Extras"),
    allure.story("Search and Filter"),
]


@allure.title("WE-SRH-001 Searching an existing wash extra by exact name returns the record")
@pytest.mark.regression
def test_wash_extras_existing_search(browser):

    page = open_wash_extras_page(browser)
    page.search_extra(EXISTING_EXTRA)

    assert page.wait_for_extra_row(EXISTING_EXTRA).is_displayed()


@allure.title("WE-SRH-002 Searching by partial name returns all matching wash extras")
@pytest.mark.regression
def test_wash_extras_partial_search_returns_matches(browser):

    page = open_wash_extras_page(browser)
    partial = EXISTING_EXTRA[:5]
    page.search_extra(partial)

    assert EXISTING_EXTRA.lower() in page.get_body_text().lower()
    assert page_has_no_broken_state(page)


@allure.title("WE-SRH-003 Searching a non-existing name shows empty state without error")
@pytest.mark.extended
def test_wash_extras_missing_search(browser):

    page = open_wash_extras_page(browser)
    page.search_extra(MISSING_EXTRA)

    assert MISSING_EXTRA not in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("WE-SRH-004 Clearing the search field restores the complete wash extras list")
@pytest.mark.extended
def test_wash_extras_clear_search_restores_list(browser):

    page = open_wash_extras_page(browser)
    original_names = page.get_visible_extra_names()

    page.search_extra(EXISTING_EXTRA)
    page.clear_extra_search()

    assert len(page.get_visible_extra_names()) >= min(len(original_names), 1)
    assert page_has_no_broken_state(page)


@allure.title("WE-FLT-001 Filtering by site narrows results to that site's wash extras")
@pytest.mark.regression
def test_wash_extras_filter_by_site_narrows_results(browser):

    page = open_wash_extras_page(browser)
    page.open_filter_panel()
    page.set_filter_site(ASSIGNMENT_SITE)
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("WE-FLT-002 Active service filter returns only active wash extras")
@pytest.mark.regression
def test_wash_extras_filter_active_returns_active_only(browser):

    page = open_wash_extras_page(browser)
    page.open_filter_panel()
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("WE-FLT-003 Disabling Active toggle in filter reveals all wash extras")
@pytest.mark.extended
def test_wash_extras_filter_active_toggle_off_shows_all(browser):

    page = open_wash_extras_page(browser)
    page.open_filter_panel()
    page.reset_filters()
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("WE-FLT-004 Site and Active filter combined narrows results correctly")
@pytest.mark.extended
def test_wash_extras_filter_site_and_active_combined(browser):

    page = open_wash_extras_page(browser)
    page.open_filter_panel()
    page.set_filter_site(ASSIGNMENT_SITE)
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("WE-FLT-005 Reset all clears filters and restores the default list")
@pytest.mark.extended
def test_wash_extras_filter_reset_all_restores_list(browser):

    page = open_wash_extras_page(browser)
    page.open_filter_panel()
    page.set_filter_site(ASSIGNMENT_SITE)
    page.apply_filters()

    page.open_filter_panel()
    page.reset_filters()

    assert page_has_no_broken_state(page)
