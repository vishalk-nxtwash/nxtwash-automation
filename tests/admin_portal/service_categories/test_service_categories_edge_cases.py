import allure
import pytest

from tests.admin_portal.service_categories.conftest import create_category_if_missing
from tests.admin_portal.service_categories.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Edge Cases"),
]


@allure.title("SC-EDGE-001 Long service category name does not break form")
@pytest.mark.regression
def test_service_category_long_name_does_not_break_form(browser):

    page = create_category_if_missing(browser)
    page.open_create_category()
    page.enter_category_name("VK " + ("C" * 128))

    assert page_has_no_broken_state(page)
    assert "Category name" in page.get_body_text()
