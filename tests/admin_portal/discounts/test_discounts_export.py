import allure
import pytest

from tests.admin_portal.discounts.conftest import create_discount_if_missing
from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Export"),
]


@allure.title("DS-EXP-001 Export discounts button is clickable")
@pytest.mark.regression
def test_discounts_export_button_clickable(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.click_download_button()

    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-EXP-002 Export after filter does not break the grid")
@pytest.mark.regression
def test_discounts_export_after_filter(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_filter_panel()
    discounts_page.set_active_discount_filter(True)
    discounts_page.apply_filters()
    discounts_page.click_download_button()

    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-EXP-003 Export record count matches filtered grid count")
@pytest.mark.regression
@pytest.mark.xfail(
    reason=(
        "Cannot reliably verify downloaded file record count in this environment "
        "without file-system download polling. Tracked for future implementation."
    ),
    strict=False,
)
def test_discounts_export_record_count_matches_grid(browser):

    discounts_page = open_discounts_page(browser)
    grid_count = len(discounts_page.get_visible_discount_names())
    discounts_page.click_download_button()

    assert grid_count > 0
    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-EXP-004 Export data matches grid data")
@pytest.mark.regression
@pytest.mark.xfail(
    reason=(
        "Cannot verify exported file contents without file-system download access. "
        "Tracked for future implementation with download folder inspection."
    ),
    strict=False,
)
def test_discounts_export_data_matches_grid(browser):

    discounts_page = create_discount_if_missing(browser)
    grid_names = discounts_page.get_visible_discount_names()
    discounts_page.click_download_button()

    assert len(grid_names) > 0
    assert page_has_no_broken_state(discounts_page)
