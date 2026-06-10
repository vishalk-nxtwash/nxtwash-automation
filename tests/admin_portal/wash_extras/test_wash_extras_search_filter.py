from tests.admin_portal.wash_extras.conftest import EXISTING_EXTRA
from tests.admin_portal.wash_extras.conftest import MISSING_EXTRA
from tests.admin_portal.wash_extras.conftest import open_wash_extras_page
from tests.admin_portal.wash_extras.conftest import page_has_no_broken_state


def test_wash_extras_existing_search(browser):

    page = open_wash_extras_page(browser)
    page.search_extra(EXISTING_EXTRA)

    assert page.wait_for_extra_row(EXISTING_EXTRA).is_displayed()


def test_wash_extras_missing_search(browser):

    page = open_wash_extras_page(browser)
    page.search_extra(MISSING_EXTRA)

    assert MISSING_EXTRA not in page.get_body_text()


def test_wash_extras_search_payloads_do_not_break_grid(browser):

    page = open_wash_extras_page(browser)
    page.search_extra("<script>alert(1)</script>")

    assert page_has_no_broken_state(page)
