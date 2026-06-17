from tests.admin_portal.wash_extras.conftest import MISSING_EXTRA
from tests.admin_portal.wash_extras.conftest import open_wash_extras_page
from tests.admin_portal.wash_extras.conftest import page_has_no_broken_state


def test_missing_wash_extra_is_not_returned(browser):

    page = open_wash_extras_page(browser)
    page.search_extra(MISSING_EXTRA)

    assert MISSING_EXTRA not in page.get_body_text()


def test_wash_extras_special_character_search_stays_usable(browser):

    page = open_wash_extras_page(browser)
    page.search_extra("' OR 1=1 --")

    assert page_has_no_broken_state(page)
