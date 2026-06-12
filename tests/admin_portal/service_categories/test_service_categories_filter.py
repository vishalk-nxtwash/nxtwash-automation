import allure
import pytest

from tests.admin_portal.service_categories.conftest import open_service_categories_page


@allure.epic("Admin Portal")
@allure.feature("Service Categories")
@allure.story("Filter")
@allure.title("SC-FI filter behavior requires stable filter-panel contract")
@pytest.mark.regression
@pytest.mark.xfail(
    reason=(
        "Service Categories filter behavior cannot be marked covered until "
        "the filter panel fields and expected active/inactive fixture data are "
        "formalized."
    ),
    strict=True,
)
def test_service_categories_filter_behavior_blocker(browser):
    page = open_service_categories_page(browser)
    assert page.filter_button_is_clickable()
    raise AssertionError("Filter behavior coverage is not implemented.")

