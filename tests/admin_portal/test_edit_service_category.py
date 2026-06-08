from tests.admin_portal.test_create_service_category import CATEGORY_NAME
from tests.admin_portal.test_create_service_category import create_category_if_missing


UPDATED_CATEGORY_NAME = "VK wash01 edited"


def test_open_edit_service_category(browser):

    service_categories_page = create_category_if_missing(browser)
    service_categories_page.open_edit_category(CATEGORY_NAME)

    assert CATEGORY_NAME in service_categories_page.get_body_text()
    assert service_categories_page.active_switch_is_on()


def test_cancel_edit_service_category_does_not_change_category(browser):

    service_categories_page = create_category_if_missing(browser)
    service_categories_page.open_edit_category(CATEGORY_NAME)
    service_categories_page.enter_category_name(UPDATED_CATEGORY_NAME)
    service_categories_page.click_cancel()
    service_categories_page.wait_for_list_loaded()
    service_categories_page.search_category(CATEGORY_NAME)

    assert service_categories_page.wait_for_category_row(
        CATEGORY_NAME
    ).is_displayed()


def test_update_service_category_name_and_restore(browser):

    service_categories_page = create_category_if_missing(browser)

    try:
        service_categories_page.update_category_name(
            CATEGORY_NAME,
            UPDATED_CATEGORY_NAME
        )
        service_categories_page.search_category(UPDATED_CATEGORY_NAME)

        assert service_categories_page.wait_for_category_row(
            UPDATED_CATEGORY_NAME
        ).is_displayed()
        assert service_categories_page.get_category_status(
            UPDATED_CATEGORY_NAME
        ) == "Active"

    finally:
        service_categories_page.wait_for_list_loaded()

        if service_categories_page.category_exists(UPDATED_CATEGORY_NAME):
            service_categories_page.update_category_name(
                UPDATED_CATEGORY_NAME,
                CATEGORY_NAME
            )

        service_categories_page.wait_for_list_loaded()
        service_categories_page.search_category(CATEGORY_NAME)
        service_categories_page.wait_for_category_row(CATEGORY_NAME)
