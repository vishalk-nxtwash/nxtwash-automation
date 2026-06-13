import allure
import pytest

from tests.admin_portal.discounts.conftest import MISSING_DISCOUNT
from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Negative"),
]


@allure.title("DIS-NG-001 Missing discount is not returned")
@pytest.mark.regression
def test_missing_discount_is_not_returned(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.search_discount(MISSING_DISCOUNT)

    assert MISSING_DISCOUNT not in discounts_page.get_body_text()
    assert page_has_no_broken_state(discounts_page)


@allure.title("DIS-NG-002 Special-character discount search remains stable")
@pytest.mark.regression
def test_discounts_special_character_search_stays_usable(browser):

    discounts_page = open_discounts_page(browser)
    discounts_page.search_discount("%%%___###")

    assert page_has_no_broken_state(discounts_page)
    assert discounts_page.driver.find_element(*discounts_page.SEARCH_INPUT).is_displayed()
