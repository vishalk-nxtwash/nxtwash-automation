import allure
import pytest

from tests.admin_portal.discounts.conftest import DISCOUNT_AMOUNT
from tests.admin_portal.discounts.conftest import DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import REQUESTED_SERVICE_CATEGORY
from tests.admin_portal.discounts.conftest import SERVICE_CATEGORY
from tests.admin_portal.discounts.conftest import START_DAY
from tests.admin_portal.discounts.conftest import START_TIME
from tests.admin_portal.discounts.conftest import create_discount_if_missing


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Edit Flow"),
]


@allure.title("DS-HP-005 Edit discount value and reapply expected settings")
@pytest.mark.regression
def test_edit_discount_reapplies_expected_settings(browser):

    discounts_page = create_discount_if_missing(browser)
    discounts_page.update_discount(
        DISCOUNT_NAME,
        REQUESTED_SERVICE_CATEGORY,
        DISCOUNT_AMOUNT,
        START_DAY,
        START_TIME,
        SERVICE_CATEGORY
    )

    discounts_page.open_edit_discount(DISCOUNT_NAME)

    assert discounts_page.get_discount_name_value() == DISCOUNT_NAME
    assert discounts_page.amount_discount_type_is_selected()
    assert discounts_page.get_discount_amount_value() == DISCOUNT_AMOUNT
    assert discounts_page.active_switch_is_on()
