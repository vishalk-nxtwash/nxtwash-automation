import allure
import pytest

from tests.admin_portal.service_categories.conftest import open_service_categories_page


@allure.epic("Admin Portal")
@allure.feature("Service Categories")
@allure.story("Business Rules")
@allure.title("SC-BURU advanced business rules require product/API contract")
@pytest.mark.regression
@pytest.mark.xfail(
    reason=(
        "Business-rule scenarios in the sheet are generic and need concrete "
        "rules/expected outcomes before executable automation can be written."
    ),
    strict=True,
)
def test_service_categories_business_rules_contract_blocker(browser):
    page = open_service_categories_page(browser)
    assert page.add_category_button_is_clickable()
    raise AssertionError("Business-rule contract coverage is not implemented.")

