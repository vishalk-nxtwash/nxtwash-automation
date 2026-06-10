from tests.admin_portal.discounts.conftest import EXISTING_DISCOUNT
from tests.admin_portal.discounts.conftest import MISSING_DISCOUNT
from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state


def test_discounts_existing_search(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.search_discount(EXISTING_DISCOUNT)

    assert discounts_page.wait_for_discount_row(EXISTING_DISCOUNT).is_displayed()


def test_discounts_missing_search(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.search_discount(MISSING_DISCOUNT)

    assert MISSING_DISCOUNT not in discounts_page.get_body_text()
    assert page_has_no_broken_state(discounts_page)


def test_discounts_filter_panel_shows_controls(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.open_filter_panel()
    body_text = discounts_page.get_body_text()

    assert "Select site" in body_text
    assert "Active discount" in body_text
    assert "Apply filters" in body_text
    assert "Reset all" in body_text


def test_discounts_search_payloads_do_not_break_grid(browser):

    discounts_page = open_discounts_page(browser)

    for payload in ("' OR 1=1 --", "<script>alert(1)</script>"):
        discounts_page.search_discount(payload)
        assert page_has_no_broken_state(discounts_page)
