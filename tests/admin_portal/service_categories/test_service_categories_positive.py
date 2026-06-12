import allure
import pytest

from tests.admin_portal.service_categories.conftest import CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import create_category_if_missing


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("CRUD"),
]


@allure.title("SC-CRUD create active service category")
@pytest.mark.sanity
def test_create_active_service_category(browser):

    page = create_category_if_missing(browser)
    page.search_category(CATEGORY_NAME)

    assert page.wait_for_category_row(CATEGORY_NAME).is_displayed()
    assert page.get_category_status(CATEGORY_NAME) == "Active"


@allure.title("SC-CRUD service category settings persist")
@pytest.mark.regression
def test_service_category_settings_persist(browser):

    page = create_category_if_missing(browser)
    page.open_edit_category(CATEGORY_NAME)

    assert page.get_category_name_value() == CATEGORY_NAME
    assert page.active_switch_is_on()
