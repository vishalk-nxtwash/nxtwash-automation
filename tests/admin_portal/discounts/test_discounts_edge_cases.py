import allure
import pytest

from tests.admin_portal.discounts.conftest import create_discount_if_missing


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Edge Cases"),
]


@allure.title("DIS-EC-001 Long discount name does not break form")
@pytest.mark.regression
def test_discount_long_name_does_not_break_form(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.open_create_discount()
    discounts_page.enter_discount_name("VK " + ("D" * 128))

    assert discounts_page.get_discount_name_value().startswith("VK ")
    assert "Discount name" in discounts_page.get_body_text()
