import allure
import pytest

from pages.admin_portal.customers_page import CustomersPage
from pages.admin_portal.employees_page import AdminEmployeesPage
from pages.admin_portal.user_roles_page import AdminUserRolesPage
from pages.admin_portal.users_page import AdminUsersPage
from tests.admin_portal.admin_session import open_admin_path
from tests.prod_smoke.conftest import page_is_up


pytestmark = [
    allure.epic("Production Smoke"),
    allure.feature("People"),
    pytest.mark.prod_smoke,
]


@allure.title("PSMO-PPL-001 Customers page loads with grid visible")
@pytest.mark.prod_smoke
def test_customers_page_loads(browser):
    open_admin_path(browser, "/customers")
    page = CustomersPage(browser)
    page.wait_for_list_loaded()

    assert page_is_up(browser)
    body = page.get_body_text()
    assert "Customers" in body, "Customers page title not found"


@allure.title("PSMO-PPL-002 Employees page loads with grid visible")
@pytest.mark.prod_smoke
def test_employees_page_loads(browser):
    open_admin_path(browser, "/users/employees")
    page = AdminEmployeesPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-PPL-003 Users page loads with grid visible")
@pytest.mark.prod_smoke
def test_users_page_loads(browser):
    open_admin_path(browser, "/users/users")
    page = AdminUsersPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-PPL-004 User Roles page loads with grid visible")
@pytest.mark.prod_smoke
def test_user_roles_page_loads(browser):
    open_admin_path(browser, "/users/userRoles")
    page = AdminUserRolesPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)
