from tests.admin_portal.wash_extras.conftest import GLOBAL_COMMISSION
from tests.admin_portal.wash_extras.conftest import GLOBAL_PRICE
from tests.admin_portal.wash_extras.conftest import VISIBLE_PRICE
from tests.admin_portal.wash_extras.conftest import WASH_EXTRA_NAME
from tests.admin_portal.wash_extras.conftest import create_wash_extra_if_missing


def test_create_wash_extra(browser):

    page = create_wash_extra_if_missing(browser)
    page.search_extra(WASH_EXTRA_NAME)

    assert page.wait_for_extra_row(WASH_EXTRA_NAME).is_displayed()
    assert page.get_extra_price(WASH_EXTRA_NAME) == VISIBLE_PRICE
    assert page.get_extra_status(WASH_EXTRA_NAME) == "Active"


def test_wash_extra_settings_persist(browser):

    page = create_wash_extra_if_missing(browser)
    page.open_edit_extra(WASH_EXTRA_NAME)

    assert page.get_service_name_value() == WASH_EXTRA_NAME
    assert page.get_global_price_value() == GLOBAL_PRICE
    assert page.get_global_commission_value() == GLOBAL_COMMISSION
    assert page.active_switch_is_on()
