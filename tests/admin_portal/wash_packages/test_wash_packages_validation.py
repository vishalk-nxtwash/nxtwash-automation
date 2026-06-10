from tests.admin_portal.wash_packages.conftest import open_wash_packages_page
from tests.admin_portal.wash_packages.conftest import page_has_no_broken_state


def test_wash_package_required_service_name_validation(browser):

    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.click_save_package()

    assert not page.service_name_input_is_valid()
    assert page.get_service_name_validation_message() != ""


def test_wash_package_invalid_numeric_values_do_not_break_form(browser):

    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("VK invalid package")
    page.set_loyalty_points("-1", "abc")
    page.set_global_price("-10")
    page.set_global_commission("abc")

    assert page_has_no_broken_state(page)
