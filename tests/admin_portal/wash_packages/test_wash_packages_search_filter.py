from tests.admin_portal.wash_packages.conftest import EXISTING_PACKAGE
from tests.admin_portal.wash_packages.conftest import MISSING_PACKAGE
from tests.admin_portal.wash_packages.conftest import open_wash_packages_page
from tests.admin_portal.wash_packages.conftest import page_has_no_broken_state


def test_wash_packages_existing_search(browser):

    page = open_wash_packages_page(browser)
    page.search_package(EXISTING_PACKAGE)

    assert page.wait_for_package_row(EXISTING_PACKAGE).is_displayed()


def test_wash_packages_missing_search(browser):

    page = open_wash_packages_page(browser)
    page.search_package(MISSING_PACKAGE)

    assert MISSING_PACKAGE not in page.get_body_text()


def test_wash_packages_search_payloads_do_not_break_grid(browser):

    page = open_wash_packages_page(browser)
    page.search_package("<script>alert(1)</script>")

    assert page_has_no_broken_state(page)
