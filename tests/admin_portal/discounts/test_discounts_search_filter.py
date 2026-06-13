import allure
import pytest

from tests.admin_portal.discounts.conftest import DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import EXISTING_DISCOUNT
from tests.admin_portal.discounts.conftest import MISSING_DISCOUNT
from tests.admin_portal.discounts.conftest import create_discount_if_missing
from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
]


@allure.story("Search")
@allure.title("DIS-SRCH-001 Search exact discount")
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
@allure.title("DIS-SRCH-003 Partial search requires product support")
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
@allure.title("DIS-FLT-001 Discounts filter panel shows controls")
@pytest.mark.regression
def test_discounts_filter_panel_shows_controls(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_filter_panel()
    body_text = discounts_page.get_body_text()

    assert "Select site" in body_text
    assert "Active discount" in body_text
    assert "Apply filters" in body_text
    assert "Reset all" in body_text


@allure.story("Search")
@allure.title("DIS-SRCH-005 Search payloads do not break grid")
@pytest.mark.regression
def test_discounts_search_payloads_do_not_break_grid(browser):

    discounts_page = open_discounts_page(browser)

    for payload in ("' OR 1=1 --", "<script>alert(1)</script>"):
        discounts_page.search_discount(payload)
        assert page_has_no_broken_state(discounts_page)
