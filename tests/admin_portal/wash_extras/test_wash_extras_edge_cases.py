from tests.admin_portal.wash_extras.conftest import WASH_EXTRA_NAME
from tests.admin_portal.wash_extras.conftest import create_wash_extra_if_missing


def test_wash_extra_create_is_idempotent(browser):

    page = create_wash_extra_if_missing(browser)
    page.search_extra(WASH_EXTRA_NAME)

    assert page.wait_for_extra_row(WASH_EXTRA_NAME).is_displayed()


def test_wash_extra_long_name_does_not_break_form(browser):

    page = create_wash_extra_if_missing(browser)
    page.open_create_extra()
    page.enter_service_name("VK " + ("E" * 128))

    assert page.get_service_name_value().startswith("VK ")
    assert "Service name" in page.get_body_text()
