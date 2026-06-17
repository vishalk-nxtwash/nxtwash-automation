import allure
import pytest

from tests.admin_portal.service_categories.conftest import CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import MISSING_CATEGORY
from tests.admin_portal.service_categories.conftest import create_category_if_missing
from tests.admin_portal.service_categories.conftest import open_service_categories_page


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Negative"),
]


@allure.title("SC-RG-006 Missing service category is not returned")
@pytest.mark.regression
def test_missing_service_category_is_not_returned(browser):

    page = open_service_categories_page(browser)
    page.search_category(MISSING_CATEGORY)

    assert MISSING_CATEGORY not in page.get_body_text()


@allure.title("SC-CRUD-004 Create service category is idempotent")
@pytest.mark.regression
def test_create_service_category_is_idempotent(browser):

    page = create_category_if_missing(browser)
    page.search_category(CATEGORY_NAME)

    assert page.wait_for_category_row(CATEGORY_NAME).is_displayed()
