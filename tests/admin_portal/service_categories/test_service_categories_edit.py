import allure
import pytest

from tests.admin_portal.service_categories.conftest import MANAGED_CATEGORY
from tests.admin_portal.service_categories.conftest import UPDATED_CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import managed_category  # noqa: F401


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("CRUD"),
]


@allure.title("SC-HP-003/SC-EC-002 Edit service category name and restore baseline")
@pytest.mark.regression
def test_edit_service_category_name_and_restore(managed_category):

    page = managed_category

    try:
        page.update_category_name(MANAGED_CATEGORY, UPDATED_CATEGORY_NAME)
        page.search_category(UPDATED_CATEGORY_NAME)

        assert page.wait_for_category_row(UPDATED_CATEGORY_NAME).is_displayed()

    finally:
        page.wait_for_list_loaded()
        if page.category_exists(UPDATED_CATEGORY_NAME):
            page.update_category_name(UPDATED_CATEGORY_NAME, MANAGED_CATEGORY)
