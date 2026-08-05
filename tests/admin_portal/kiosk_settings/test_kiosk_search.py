import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    KSK_NAME,
    NONEXISTENT_KSK_NAME,
    create_kiosk_if_missing,
    open_kiosk_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("Search"),
]


@allure.title("KSK-SRH-001 Search by exact kiosk name returns the matching kiosk")
@pytest.mark.regression
@pytest.mark.skip(reason="CI-SKIP KSK-SRH-001: managed_kiosk fixture fails in headless CI — kiosk create flow times out. Fix: same as WP-FRM-001.")
def test_search_by_exact_name(browser, managed_kiosk):
    page = open_kiosk_page(browser)
    page.search_kiosk(KSK_NAME)
    body = page.get_body_text()

    assert KSK_NAME in body, (
        "Kiosk '%s' not found after exact name search" % KSK_NAME
    )
    assert page_has_no_broken_state(page)


@allure.title("KSK-SRH-002 Search by partial kiosk name returns matching results")
@pytest.mark.regression
@pytest.mark.skip(reason="CI-SKIP KSK-SRH-002: managed_kiosk fixture fails in headless CI — kiosk create flow times out. Fix: same as WP-FRM-001.")
def test_search_by_partial_name(browser, managed_kiosk):
    partial = KSK_NAME[:5]
    page = open_kiosk_page(browser)
    page.search_kiosk(partial)
    body = page.get_body_text()

    assert partial.lower() in body.lower() or KSK_NAME in body, (
        "No kiosks found for partial name search '%s'" % partial
    )
    assert page_has_no_broken_state(page)


@allure.title("KSK-SRH-003 Searching a non-existent name shows an empty state or zero rows")
@pytest.mark.extended
def test_search_nonexistent_name(browser):
    page = open_kiosk_page(browser)
    page.search_kiosk(NONEXISTENT_KSK_NAME)
    body = page.get_body_text()

    assert (
        NONEXISTENT_KSK_NAME not in body
        or "no record" in body.lower()
        or "no data" in body.lower()
        or page.get_visible_row_count() == 0
    ), "Non-existent kiosk name should yield empty state or zero rows"
    assert page_has_no_broken_state(page)


@allure.title("KSK-SRH-004 Clearing the search field restores the full kiosk list")
@pytest.mark.extended
@pytest.mark.skip(reason="CI-SKIP KSK-SRH-004: managed_kiosk fixture fails in headless CI — kiosk create flow times out. Fix: same as WP-FRM-001.")
def test_clear_search_restores_list(browser, managed_kiosk):
    page = open_kiosk_page(browser)
    page.search_kiosk(KSK_NAME)
    count_filtered = page.get_visible_row_count()

    page.clear_search()
    count_full = page.get_visible_row_count()

    assert count_full >= count_filtered, (
        "Row count after clearing search (%d) should be >= filtered count (%d)"
        % (count_full, count_filtered)
    )
    assert page_has_no_broken_state(page)
