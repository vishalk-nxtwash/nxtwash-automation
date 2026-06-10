from tests.admin_portal.wash_packages.conftest import EXISTING_PACKAGE
from tests.admin_portal.wash_packages.conftest import open_wash_packages_page


def test_existing_wash_package_is_visible(browser):

    page = open_wash_packages_page(browser)
    page.search_package(EXISTING_PACKAGE)

    assert page.wait_for_package_row(EXISTING_PACKAGE).is_displayed()
    assert page.get_package_status(EXISTING_PACKAGE) == "Active"


def test_wash_package_edit_form_loads_existing_settings(browser):

    page = open_wash_packages_page(browser)
    page.open_edit_package(EXISTING_PACKAGE)

    assert page.get_service_name_value() == EXISTING_PACKAGE
    assert page.active_switch_is_on()
