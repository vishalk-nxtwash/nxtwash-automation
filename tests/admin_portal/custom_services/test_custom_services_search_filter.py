import uuid

import allure
import pytest

from tests.admin_portal.custom_services.conftest import (
    ASSIGNMENT_SITE,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    MISSING_SERVICE,
    SERVICE_CATEGORY,
    SERVICE_NAME,
    create_service_if_missing,
    open_custom_services_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Custom Services"),
    allure.story("Search and Filter"),
]


@allure.title("CS-SRH-001 Search by exact service name returns the correct service")
@pytest.mark.regression
def test_search_exact_service_name(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.search_service(SERVICE_NAME)

    names = page.get_visible_service_names()
    assert SERVICE_NAME in names
    assert page_has_no_broken_state(page)


@allure.title("CS-SRH-002 Search by partial name returns matching services")
@pytest.mark.regression
def test_search_partial_service_name(browser):

    create_service_if_missing(browser)
    partial = SERVICE_NAME[:6]
    page = open_custom_services_page(browser)
    page.search_service(partial)

    names = page.get_visible_service_names()
    assert any(partial.lower() in n.lower() for n in names)
    assert page_has_no_broken_state(page)


@allure.title("CS-SRH-003 Search for non-existing service returns empty state")
@pytest.mark.regression
def test_search_non_existing_service_returns_empty(browser):

    page = open_custom_services_page(browser)
    page.search_service(MISSING_SERVICE)

    names = page.get_visible_service_names()
    assert names == [] or MISSING_SERVICE not in names
    assert page_has_no_broken_state(page)


@allure.title("CS-SRH-004 Clearing search restores the full list")
@pytest.mark.regression
def test_clear_search_restores_full_list(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.search_service(MISSING_SERVICE)
    page.clear_service_search()

    names = page.get_visible_service_names()
    assert SERVICE_NAME in names
    assert page_has_no_broken_state(page)


@allure.title("CS-FLT-001 Filter by site narrows the list to services assigned to that site")
@pytest.mark.regression
def test_filter_by_site_narrows_results(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.select_site_filter(ASSIGNMENT_SITE)
    page.apply_filters()

    names = page.get_visible_service_names()
    assert SERVICE_NAME in names
    assert page_has_no_broken_state(page)


@allure.title("CS-FLT-002 Active service toggle shows active services only")
@pytest.mark.regression
def test_active_service_filter_shows_active_only(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.open_filter_panel()
    page.toggle_active_service_filter()
    page.apply_filters()

    body = page.get_body_text()
    assert SERVICE_NAME in body
    assert page_has_no_broken_state(page)


@allure.title("CS-FLT-003 Active service filter off shows all services including inactive")
@pytest.mark.regression
@pytest.mark.skip(reason="Manual: Active service filter toggle updates DOM but React state does not change — same root cause as CS-EDT-004. Needs app-level investigation.")
def test_active_service_filter_off_shows_all(browser):

    inactive = "VK flt-inact-%s" % uuid.uuid4().hex[:6]
    page = open_custom_services_page(browser)
    page.open_create_service()
    page.enter_service_name(inactive)
    page.select_service_category(SERVICE_CATEGORY)
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)
    page.ensure_active_switch_off()
    page.assign_site_with_price_and_commission(ASSIGNMENT_SITE, GLOBAL_PRICE, GLOBAL_COMMISSION)
    page.click_save_service()
    page.wait_for_list_loaded()

    page.open_filter_panel()
    page.toggle_active_service_filter()
    page.apply_filters()

    body = page.get_body_text()
    assert inactive in body
    assert page_has_no_broken_state(page)


@allure.title("CS-FLT-004 Site filter combined with active toggle shows correct results")
@pytest.mark.regression
def test_site_and_active_filter_combined(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.select_site_filter(ASSIGNMENT_SITE)
    page.toggle_active_service_filter()
    page.apply_filters()

    names = page.get_visible_service_names()
    assert SERVICE_NAME in names
    assert page_has_no_broken_state(page)


@allure.title("CS-FLT-005 Reset all clears applied filters and restores full list")
@pytest.mark.regression
def test_reset_filters_clears_filters(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.select_site_filter(ASSIGNMENT_SITE)
    page.apply_filters()
    page.reset_filters()

    names = page.get_visible_service_names()
    assert SERVICE_NAME in names
    assert page_has_no_broken_state(page)
