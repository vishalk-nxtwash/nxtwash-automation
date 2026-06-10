from tests.admin_portal.test_wash_extras import open_wash_extras_page


WASH_EXTRA_NAME = "VK EWA2"
GLOBAL_PRICE = "15"
GLOBAL_COMMISSION = "2"
DISCOUNT_NAME = "Plus discount"
VISIBLE_PRICE = "$15.00"


def create_wash_extra_if_missing(browser, extra_name=WASH_EXTRA_NAME):

    wash_extras_page = open_wash_extras_page(browser)

    if wash_extras_page.extra_exists(extra_name):
        return wash_extras_page

    wash_extras_page.create_extra(
        extra_name,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        DISCOUNT_NAME
    )
    wash_extras_page.search_extra(extra_name)
    wash_extras_page.wait_for_extra_row(extra_name)

    return wash_extras_page


def test_create_wash_extra_required_service_name_validation(browser):

    wash_extras_page = open_wash_extras_page(browser)
    wash_extras_page.open_create_extra()
    wash_extras_page.click_save_extra()

    assert not wash_extras_page.service_name_input_is_valid()
    assert wash_extras_page.get_service_name_validation_message() != ""


def test_create_vk_ewa2_active_wash_extra(browser):

    wash_extras_page = create_wash_extra_if_missing(browser)
    wash_extras_page.wait_for_list_loaded()
    wash_extras_page.search_extra(WASH_EXTRA_NAME)

    assert wash_extras_page.wait_for_extra_row(WASH_EXTRA_NAME).is_displayed()
    assert wash_extras_page.get_extra_price(WASH_EXTRA_NAME) == VISIBLE_PRICE
    assert wash_extras_page.get_extra_status(WASH_EXTRA_NAME) == "Active"


def test_create_vk_ewa2_does_not_duplicate_existing_wash_extra(browser):

    wash_extras_page = create_wash_extra_if_missing(browser)
    wash_extras_page.wait_for_list_loaded()
    wash_extras_page.search_extra(WASH_EXTRA_NAME)

    assert wash_extras_page.wait_for_extra_row(WASH_EXTRA_NAME).is_displayed()
    assert wash_extras_page.get_extra_price(WASH_EXTRA_NAME) == VISIBLE_PRICE
    assert wash_extras_page.get_extra_status(WASH_EXTRA_NAME) == "Active"


def test_vk_ewa2_discount_selection_persists(browser):

    wash_extras_page = create_wash_extra_if_missing(browser)
    wash_extras_page.open_edit_extra(WASH_EXTRA_NAME)
    wash_extras_page.open_discount_settings()

    assert wash_extras_page.discount_is_selected(DISCOUNT_NAME)


def test_vk_ewa2_all_locations_are_assigned(browser):

    wash_extras_page = create_wash_extra_if_missing(browser)
    wash_extras_page.open_edit_extra(WASH_EXTRA_NAME)

    assert wash_extras_page.all_locations_are_assigned_with_price_and_commission(
        GLOBAL_PRICE,
        GLOBAL_COMMISSION
    )
