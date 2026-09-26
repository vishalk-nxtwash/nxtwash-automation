import allure
import pytest

from pages.superadmin.users_page import UsersPage
from tests.prod_smoke.conftest import page_is_up


pytestmark = [
    allure.epic("Production Smoke"),
    allure.feature("Superadmin Users"),
    pytest.mark.prod_smoke,
]


@pytest.fixture
def users_page(superadmin_session, sidebar):
    sidebar.open_users()
    page = UsersPage(superadmin_session)
    page.wait_for_loaded()
    return page


@allure.title("SA-PSMO-USR-001 Users list loads with title and at least one row")
@pytest.mark.prod_smoke
def test_users_list_loads(users_page):
    assert users_page.get_text(users_page.PAGE_TITLE) == "Users"
    assert users_page.get_visible_row_count() >= 1, \
        "Expected at least one user row on the live list"
    assert page_is_up(users_page.driver)


@allure.title("SA-PSMO-USR-002 Users list shows column headers and pagination info")
@pytest.mark.prod_smoke
def test_users_list_columns_and_pagination(users_page):
    assert users_page.get_column_headers(), \
        "Users table should render column headers"
    assert users_page.pagination_controls_present(), \
        "Pagination info should be visible on the Users list"
