import allure
import pytest

from tests.admin_portal.service_categories.conftest import EXISTING_CATEGORY
from tests.admin_portal.service_categories.conftest import MISSING_CATEGORY
from tests.admin_portal.service_categories.conftest import open_service_categories_page
from tests.admin_portal.service_categories.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Search"),
]


@allure.title("SC-SE existing category search")
@pytest.mark.regression
def test_service_categories_existing_search(browser):

    page = open_service_categories_page(browser)
    page.search_category(EXISTING_CATEGORY)

    assert page.wait_for_category_row(EXISTING_CATEGORY).is_displayed()


@allure.title("SC-SE missing category search")
@pytest.mark.regression
def test_service_categories_missing_search(browser):

    page = open_service_categories_page(browser)
    page.search_category(MISSING_CATEGORY)

    assert MISSING_CATEGORY not in page.get_body_text()


@allure.title("SC-SE special character search remains stable")
@pytest.mark.regression
def test_service_categories_special_character_search_stays_usable(browser):

    page = open_service_categories_page(browser)
    page.search_category("' OR 1=1 --")

    assert page_has_no_broken_state(page)
