import allure
import pytest

from tests.admin_portal.service_categories.conftest import create_category_if_missing
from tests.admin_portal.service_categories.conftest import create_inactive_category_if_missing
from tests.admin_portal.service_categories.conftest import open_service_categories_page
from tests.admin_portal.service_categories.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Filter"),
]


@allure.title("SC-RG-003 Filter by active shows only active records")
@pytest.mark.regression
def test_filter_active_categories_shows_active(browser):

    page = create_category_if_missing(browser)

    page.open_filter_panel()
    page.set_active_category_filter(True)
    page.apply_filters()

    statuses = page.get_visible_category_statuses()
    assert statuses, "Expected at least one active category after applying active filter"
    assert all(s == "Active" for s in statuses), (
        "Expected only Active records after applying active filter, got: %s" % statuses
    )
    assert page_has_no_broken_state(page)


@allure.title("SC-RG-004 Filter by inactive shows only inactive records")
@pytest.mark.regression
def test_filter_inactive_categories_shows_inactive(browser):

    create_inactive_category_if_missing(browser)
    page = open_service_categories_page(browser)

    page.open_filter_panel()
    page.set_active_category_filter(False)
    page.apply_filters()

    statuses = page.get_visible_category_statuses()
    assert statuses, "Expected at least one inactive category after applying inactive filter"
    assert all(s == "Inactive" for s in statuses), (
        "Expected only Inactive records after applying inactive filter, got: %s" % statuses
    )
    assert page_has_no_broken_state(page)


@allure.title("SC-RG-005 Export button is clickable on the list")
@pytest.mark.regression
def test_export_button_is_clickable(browser):

    page = open_service_categories_page(browser)

    assert page.download_button_is_clickable()
    assert page_has_no_broken_state(page)


@allure.title("SC-RG-007 Resetting active filter restores full grid")
@pytest.mark.regression
def test_reset_active_filter_restores_full_grid(browser):

    page = create_category_if_missing(browser)
    baseline_count = len(page.get_visible_category_names())

    page.open_filter_panel()
    page.set_active_category_filter(True)
    page.apply_filters()
    filtered_count = len(page.get_visible_category_names())

    page._reset_to_default_view()

    restored_count = len(page.get_visible_category_names())
    assert restored_count >= filtered_count, (
        "Expected full grid count (%d) to be at least the filtered count (%d) "
        "after resetting the active filter" % (restored_count, filtered_count)
    )
    assert page_has_no_broken_state(page)
