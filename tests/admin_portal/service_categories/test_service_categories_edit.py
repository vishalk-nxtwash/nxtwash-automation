from tests.admin_portal.service_categories.conftest import CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import UPDATED_CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import create_category_if_missing


def test_edit_service_category_name_and_restore(browser):

    page = create_category_if_missing(browser)

    try:
        page.update_category_name(CATEGORY_NAME, UPDATED_CATEGORY_NAME)
        page.search_category(UPDATED_CATEGORY_NAME)

        assert page.wait_for_category_row(UPDATED_CATEGORY_NAME).is_displayed()

    finally:
        page.wait_for_list_loaded()
        if page.category_exists(UPDATED_CATEGORY_NAME):
            page.update_category_name(UPDATED_CATEGORY_NAME, CATEGORY_NAME)
