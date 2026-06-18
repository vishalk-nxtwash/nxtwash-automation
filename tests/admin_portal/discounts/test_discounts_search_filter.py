import allure
import pytest

from tests.admin_portal.discounts.conftest import DISCOUNT_AMOUNT
from tests.admin_portal.discounts.conftest import DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import EXISTING_DISCOUNT
from tests.admin_portal.discounts.conftest import MANAGED_DISCOUNT
from tests.admin_portal.discounts.conftest import create_discount_if_missing
from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
]


@allure.story("Search")
@allure.title("DS-SRH-001 Search exact discount")
@pytest.mark.regression
def test_discounts_existing_search(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.search_discount(EXISTING_DISCOUNT)

    assert discounts_page.wait_for_discount_row(EXISTING_DISCOUNT).is_displayed()


@allure.story("Search")
@allure.title("DS-SRH-002 Partial search returns matching results")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_discounts_partial_search(browser):
    discounts_page = create_discount_if_missing(browser)
    discounts_page.search_discount(DISCOUNT_NAME[:4])

    assert discounts_page.wait_for_discount_row(DISCOUNT_NAME).is_displayed()


@allure.story("Filter")
@allure.title("DS-FLT-001 Filter by active shows only active discounts")
@pytest.mark.regression
@pytest.mark.visual
def test_discounts_filter_active_shows_only_active(browser, screenshot):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_filter_panel()
    screenshot("discount filter panel")

    body_text = discounts_page.get_body_text()
    assert "Select site" in body_text
    assert "Active discount" in body_text
    assert "Apply filters" in body_text
    assert "Reset all" in body_text

    discounts_page.set_active_discount_filter(True)
    discounts_page.apply_filters()
    screenshot("active-filtered grid")

    statuses = discounts_page.get_visible_discount_statuses()
    assert statuses, "expected at least one discount after filtering"
    assert all(status == "Active" for status in statuses), statuses
    assert page_has_no_broken_state(discounts_page)

@allure.story("Filter")
@allure.title("DS-FLT-002 Filter by site")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_discounts_filter_by_site(browser):
    discounts_page = open_discounts_page(browser)
    discounts_page.open_filter_panel()
    site = discounts_page.select_filter_site("VK")
    if site is None:
        pytest.skip("No site matching 'VK' found in filter dropdown")
    discounts_page.apply_filters()
    assert page_has_no_broken_state(discounts_page)


@allure.story("Search")
@allure.title("DS-SRH-006 Search payloads do not break grid")
@pytest.mark.regression
def test_discounts_search_payloads_do_not_break_grid(browser):

    discounts_page = open_discounts_page(browser)

    for payload in ("' OR 1=1 --", "<script>alert(1)</script>"):
        discounts_page.search_discount(payload)
        assert page_has_no_broken_state(discounts_page)


@allure.story("Search")
@allure.title("DS-SRH-003 Search inactive discount returns it")
@pytest.mark.regression
def test_discounts_search_inactive_discount(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_filter_panel()
    discounts_page.set_active_discount_filter(False)
    discounts_page.apply_filters()
    inactive_names = discounts_page.get_visible_discount_names()

    if not inactive_names:
        pytest.skip("No inactive discounts available in current data set")

    target = inactive_names[0]
    discounts_page.search_discount(target)

    assert discounts_page.wait_for_discount_row(target).is_displayed()


@allure.story("Search")
@allure.title("DS-SRH-004 Search returns updated discount name after edit")
@pytest.mark.regression
def test_discounts_search_finds_updated_name(managed_discount):

    page = managed_discount
    new_name = MANAGED_DISCOUNT + " SRCH"

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.enter_discount_name(new_name)
    page.click_save_discount()
    page.wait_for_list_loaded()
    page.search_discount(new_name)

    assert page.wait_for_discount_row(new_name).is_displayed()

    page.open_edit_discount(new_name)
    page.enter_discount_name(MANAGED_DISCOUNT)
    page.click_save_discount()
    page.wait_for_list_loaded()


@allure.story("Filter")
@allure.title("DS-FLT-003 Filter active + site")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_discounts_filter_active_and_site(browser):
    discounts_page = open_discounts_page(browser)
    discounts_page.open_filter_panel()
    discounts_page.set_active_discount_filter(True)
    site = discounts_page.select_filter_site("VK")
    if site is None:
        pytest.skip("No site matching 'VK' found in filter dropdown")
    discounts_page.apply_filters()
    statuses = discounts_page.get_visible_discount_statuses()
    assert all(s == "Active" for s in statuses)


@allure.story("Filter")
@allure.title("DS-FLT-004 Filter inactive + site")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_discounts_filter_inactive_and_site(browser):
    discounts_page = open_discounts_page(browser)
    discounts_page.open_filter_panel()
    discounts_page.set_active_discount_filter(False)
    site = discounts_page.select_filter_site("VK")
    if site is None:
        pytest.skip("No site matching 'VK' found in filter dropdown")
    discounts_page.apply_filters()
    statuses = discounts_page.get_visible_discount_statuses()
    assert all(s == "Inactive" for s in statuses)


@allure.story("Filter")
@allure.title("DS-FLT-005 Clear filters restores full grid")
@pytest.mark.regression
def test_discounts_clear_filters_restores_grid(browser):

    discounts_page = create_discount_if_missing(browser)
    all_names = discounts_page.get_visible_discount_names()

    discounts_page.open_filter_panel()
    discounts_page.set_active_discount_filter(True)
    discounts_page.apply_filters()
    filtered_names = discounts_page.get_visible_discount_names()

    discounts_page.reset_filters()
    discounts_page.wait_for_list_loaded()
    restored_names = discounts_page.get_visible_discount_names()

    assert len(restored_names) >= len(filtered_names)
    assert page_has_no_broken_state(discounts_page)


@allure.story("Filter")
@allure.title("DS-FLT-006 Search and filter together narrows results")
@pytest.mark.regression
def test_discounts_search_and_filter_together(browser):

    discounts_page = create_discount_if_missing(browser)

    discounts_page.open_filter_panel()
    discounts_page.set_active_discount_filter(True)
    discounts_page.apply_filters()

    discounts_page.search_discount(DISCOUNT_NAME)

    assert discounts_page.wait_for_discount_row(DISCOUNT_NAME).is_displayed()
    assert page_has_no_broken_state(discounts_page)
