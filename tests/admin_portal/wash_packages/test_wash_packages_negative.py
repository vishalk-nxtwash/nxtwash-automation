from tests.admin_portal.wash_packages.conftest import MISSING_PACKAGE
from tests.admin_portal.wash_packages.conftest import open_wash_packages_page
from tests.admin_portal.wash_packages.conftest import page_has_no_broken_state


def test_missing_wash_package_is_not_returned(browser):

    page = open_wash_packages_page(browser)
    page.search_package(MISSING_PACKAGE)

    assert MISSING_PACKAGE not in page.get_body_text()


def test_wash_packages_special_character_search_stays_usable(browser):

    page = open_wash_packages_page(browser)
    page.search_package("' OR 1=1 --")

    assert page_has_no_broken_state(page)
