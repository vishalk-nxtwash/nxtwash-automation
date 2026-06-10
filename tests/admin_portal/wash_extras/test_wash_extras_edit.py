from tests.admin_portal.wash_extras.conftest import FIRST_LOCATION_PRICE
from tests.admin_portal.wash_extras.conftest import SECOND_LOCATION_PRICE
from tests.admin_portal.wash_extras.conftest import UPDATED_DISCOUNT_NAME
from tests.admin_portal.wash_extras.conftest import UPDATED_WASH_EXTRA_NAME
from tests.admin_portal.wash_extras.conftest import update_wash_extra_if_needed


def test_edit_wash_extra_updates_name_prices_and_discount(browser):

    page = update_wash_extra_if_needed(browser)
    page.search_extra(UPDATED_WASH_EXTRA_NAME)

    assert page.wait_for_extra_row(UPDATED_WASH_EXTRA_NAME).is_displayed()


def test_edit_wash_extra_values_persist(browser):

    page = update_wash_extra_if_needed(browser)
    page.open_edit_extra(UPDATED_WASH_EXTRA_NAME)

    assert page.get_service_name_value() == UPDATED_WASH_EXTRA_NAME
    assert page.get_location_price_by_index(0) == FIRST_LOCATION_PRICE
    assert page.get_location_price_by_index(1) == SECOND_LOCATION_PRICE

    page.open_discount_settings()

    assert page.discount_is_selected(UPDATED_DISCOUNT_NAME)
