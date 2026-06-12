import allure
import pytest

from tests.admin_portal.service_categories.conftest import open_service_categories_page


@allure.epic("Admin Portal")
@allure.feature("Service Categories")
@allure.story("Permissions")
@allure.title("SC-PE role-specific permission coverage requires role fixtures")
@pytest.mark.permissions
@pytest.mark.xfail(
    reason="Permission coverage requires non-admin role fixtures and credentials.",
    strict=True,
)
def test_service_categories_permission_matrix_blocker(browser):
    page = open_service_categories_page(browser)
    assert "Service categories" in page.get_body_text()
    raise AssertionError("Role-specific permission coverage is not implemented.")

