import allure
import pytest

from tests.admin_portal.service_categories.conftest import create_category_if_missing
from tests.admin_portal.service_categories.conftest import open_service_categories_page
from tests.admin_portal.service_categories.conftest import page_has_no_broken_state


@allure.epic("Admin Portal")
@allure.feature("Service Categories")
@allure.story("Edge Cases")
@allure.title("SC-EDCA long service category name does not break form")
@pytest.mark.regression
def test_service_category_long_name_does_not_break_form(browser):

    page = create_category_if_missing(browser)
    page.open_create_category()
    page.enter_category_name("VK " + ("C" * 128))

    assert page_has_no_broken_state(page)
    assert "Category name" in page.get_body_text()


@allure.epic("Admin Portal")
@allure.feature("Service Categories")
@allure.story("Edge Cases")
@allure.title("SC-EDCA advanced edge cases require infrastructure harnesses")
@pytest.mark.regression
@pytest.mark.xfail(
    reason=(
        "Advanced edge cases need large-data, multi-session, network, audit, "
        "and environment-control harnesses."
    ),
    strict=True,
)
def test_service_categories_advanced_edge_case_harness_blocker(browser):
    page = open_service_categories_page(browser)
    assert "Service categories" in page.get_body_text()
    raise AssertionError("Advanced edge-case harnesses are not implemented.")
