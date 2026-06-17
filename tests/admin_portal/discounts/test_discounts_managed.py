import logging

import allure
import pytest

from tests.admin_portal.discounts.conftest import DISCOUNT_AMOUNT
from tests.admin_portal.discounts.conftest import MANAGED_DISCOUNT


LOG = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Managed data"),
]

UPDATED_AMOUNT = "8"


@allure.title("DS-FRM-001 Managed discount starts at baseline")
@pytest.mark.sanity
def test_managed_discount_provided_at_baseline(managed_discount):
    """The fixture hands over a dedicated record already reset to baseline."""
    page = managed_discount

    page.open_edit_discount(MANAGED_DISCOUNT)

    assert page.get_discount_name_value() == MANAGED_DISCOUNT
    assert page.get_discount_amount_value() == DISCOUNT_AMOUNT


@allure.title("DS-FRM-002 Managed discount mutation resets on teardown")
@pytest.mark.regression
def test_managed_discount_mutation_is_reset_on_teardown(managed_discount):
    """Mutate the discount amount; the fixture teardown resets it to baseline."""
    page = managed_discount

    LOG.info("Mutating managed discount amount to %s", UPDATED_AMOUNT)
    page.open_edit_discount(MANAGED_DISCOUNT)
    page.set_discount_amount(UPDATED_AMOUNT)
    page.click_save_discount()
    page.wait_for_list_loaded()

    page.open_edit_discount(MANAGED_DISCOUNT)
    assert page.get_discount_amount_value() == UPDATED_AMOUNT
    # On teardown the fixture resets the amount back to DISCOUNT_AMOUNT, so the
    # next test (and the next run) sees a clean record without manual cleanup.
