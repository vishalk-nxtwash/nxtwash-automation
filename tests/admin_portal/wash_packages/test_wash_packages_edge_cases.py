from tests.admin_portal.wash_packages.conftest import EXISTING_PACKAGE
from tests.admin_portal.wash_packages.conftest import open_wash_packages_page


def test_wash_package_existing_search_is_repeatable(browser):

    page = open_wash_packages_page(browser)
    page.search_package(EXISTING_PACKAGE)
    page.search_package(EXISTING_PACKAGE)

    assert page.wait_for_package_row(EXISTING_PACKAGE).is_displayed()


def test_wash_package_long_name_does_not_break_form(browser):

    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("VK " + ("P" * 128))

    assert page.get_service_name_value().startswith("VK ")
    assert "Service name" in page.get_body_text()
