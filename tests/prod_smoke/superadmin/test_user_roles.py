import allure
import pytest

from pages.superadmin.user_roles_page import UserRolesPage
from tests.prod_smoke.conftest import page_is_up


pytestmark = [
    allure.epic("Production Smoke"),
    allure.feature("Superadmin User Roles"),
    pytest.mark.prod_smoke,
]


@pytest.fixture
def user_roles_page(superadmin_session, sidebar):
    sidebar.open_user_roles()
    page = UserRolesPage(superadmin_session)
    page.wait_for_loaded()
    return page


@allure.title("SA-PSMO-UR-001 User Roles list loads with title and at least one row")
@pytest.mark.prod_smoke
def test_user_roles_list_loads(user_roles_page):
    assert user_roles_page.get_visible_row_count() >= 1, \
        "Expected at least one role row on the live list"
    assert page_is_up(user_roles_page.driver)


@allure.title("SA-PSMO-UR-002 User Roles list shows column headers and pagination info")
@pytest.mark.prod_smoke
def test_user_roles_list_columns_and_pagination(user_roles_page):
    assert user_roles_page.get_column_headers(), \
        "User Roles table should render column headers"
    assert user_roles_page.get_pagination_text(), \
        "Pagination info should be visible on the User Roles list"
