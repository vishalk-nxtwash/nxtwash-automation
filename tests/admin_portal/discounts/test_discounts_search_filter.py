import allure
import pytest

from tests.admin_portal.discounts.conftest import DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import EXISTING_DISCOUNT
from tests.admin_portal.discounts.conftest import MISSING_DISCOUNT
from tests.admin_portal.discounts.conftest import create_discount_if_missing
from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state
from tests.admin_portal._bugs import BUG1
from tests.admin_portal._bugs import BUG2


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
]


@allure.story("Search")
@allure.title("DS-RG-001 Search exact discount")
@pytest.mark.regression
def test_discounts_existing_search(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.search_discount(EXISTING_DISCOUNT)

    assert discounts_page.wait_for_discount_row(EXISTING_DISCOUNT).is_displayed()


@allure.story("Search")
@allure.title("DIS-SRCH-002 Exact search clear restores records")
@pytest.mark.regression
def test_discounts_exact_search_clear_restores_records(browser):
    discounts_page = create_discount_if_missing(browser)
    original_count = len(discounts_page.get_visible_discount_names())

    discounts_page.search_discount(DISCOUNT_NAME)
    assert discounts_page.wait_for_discount_row(DISCOUNT_NAME).is_displayed()

    discounts_page.clear_discount_search()
    discounts_page.wait.until(
        lambda driver: len(discounts_page.get_visible_discount_names())
        >= min(original_count, 1)
    )


@allure.story("Search")
@allure.title("DS-RG-002 Partial search requires product support")
@allure.description(BUG1)
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.xfail(
    reason=(
        "Known product defect (tracked under NXTDEV-2320): partial discount "
        "search returns no records for an existing discount name. strict=True "
        "so this flags as XPASS once the product supports partial matching."
    ),
    strict=True,
)
def test_discounts_partial_search_blocker(browser):
    discounts_page = create_discount_if_missing(browser)
    discounts_page.search_discount(DISCOUNT_NAME[:4])

    assert DISCOUNT_NAME in discounts_page.get_body_text()


@allure.story("Search")
@allure.title("DIS-SRCH-004 Missing discount search returns no matching record")
@pytest.mark.regression
def test_discounts_missing_search(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.search_discount(MISSING_DISCOUNT)

    assert MISSING_DISCOUNT not in discounts_page.get_body_text()
    assert page_has_no_broken_state(discounts_page)


@allure.story("Filter")
@allure.title("DS-RG-003 Filter by active shows only active discounts")
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
@allure.title("DS-RG-004 Filter by site [blocked by product defect]")
@allure.description(BUG2)
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Known product defect (BUG 2): the discount filter 'Select site' "
        "dropdown returns no options, so discounts cannot be filtered by site. "
        "The same control works in the membership filter. "
        "DiscountsPage.select_filter_site() is ready once the dropdown populates."
    )
)
def test_discounts_filter_by_site_blocked_by_defect(browser):
    # Intentionally not executed — documents the blocked DS-RG-004 coverage and
    # surfaces BUG 2 in the Allure report (Categories: Known product defects).
    discounts_page = open_discounts_page(browser)
    discounts_page.open_filter_panel()
    discounts_page.select_filter_site("VK")
    discounts_page.apply_filters()


@allure.story("Search")
@allure.title("DIS-SRCH-005 Search payloads do not break grid")
@pytest.mark.regression
def test_discounts_search_payloads_do_not_break_grid(browser):

    discounts_page = open_discounts_page(browser)

    for payload in ("' OR 1=1 --", "<script>alert(1)</script>"):
        discounts_page.search_discount(payload)
        assert page_has_no_broken_state(discounts_page)
