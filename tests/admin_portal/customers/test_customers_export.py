import allure
import pytest

from tests.admin_portal.customers.conftest import (
    CUSTOMER_FIRST,
    CUSTOMER_LAST,
    CUSTOMER_SITE,
    open_customers_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Customers"),
    allure.story("Export"),
]


@allure.title("CUST-EXP-001 Export button triggers customer list download")
@pytest.mark.export
@pytest.mark.skip(
    reason=(
        "Deferred — export verification requires download interception or a file-system "
        "check which is not yet set up in the test harness."
    )
)
def test_export_button_triggers_customer_list_download(browser):
    pass
