from tests.admin_portal.wash_extras.conftest import open_wash_extras_page
from tests.admin_portal.wash_extras.conftest import page_has_no_broken_state


def test_wash_extra_required_service_name_validation(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.click_save_extra()

    assert not page.service_name_input_is_valid()
    assert page.get_service_name_validation_message() != ""


def test_wash_extra_invalid_numeric_values_do_not_break_form(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK invalid extra")
    page.set_global_price("-10")
    page.set_global_commission("abc")

    assert page_has_no_broken_state(page)
