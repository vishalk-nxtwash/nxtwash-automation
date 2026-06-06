import json

import pytest

from pages.superadmin.login_page import LoginPage
from pages.superadmin.sidebar import Sidebar
from pages.superadmin.user_roles_page import CreateUserRolePage
from pages.superadmin.user_roles_page import UserRolesPage


ROLE_NAME = "VK carwash role"
USER_ROLES_URL = "https://superadmin.nxtwash.com/user-roles"


@pytest.fixture
def logged_in_browser(browser):

    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()

    login_page.wait_for_url(
        "https://superadmin.nxtwash.com/"
    )

    return browser


def open_user_roles_page(browser):

    sidebar = Sidebar(browser)
    sidebar.open_user_roles()

    user_roles_page = UserRolesPage(browser)
    user_roles_page.wait_for_loaded()

    return user_roles_page


def upsert_role(browser):

    create_user_role_page = CreateUserRolePage(browser)
    create_user_role_page.upsert_role_with_api(ROLE_NAME)


def get_saved_role(browser):

    create_user_role_page = CreateUserRolePage(browser)
    response_body = create_user_role_page.get_role_permissions_with_api(
        ROLE_NAME
    )

    return json.loads(response_body)["data"]


def assert_saved_permissions_are_correct(saved_role):

    assert saved_role["roleName"] == ROLE_NAME
    assert saved_role["isActive"] is True

    for menu in saved_role["userRolesMenuAccess"]:
        assert menu["isEnabled"] is True

        for submenu in menu["subMenuAccessList"]:
            if (
                menu["menuName"] == "Companies"
                and submenu["subMenuName"] == "Create Company"
            ):
                assert submenu["isEnabled"] is False
            else:
                assert submenu["isEnabled"] is True

            assert submenu["subMenuItemAccessList"] == []


def test_create_vk_carwash_role_with_all_permissions_except_create_company(
    logged_in_browser
):

    open_user_roles_page(logged_in_browser)

    upsert_role(logged_in_browser)

    logged_in_browser.get(USER_ROLES_URL)
    user_roles_page = UserRolesPage(logged_in_browser)
    user_roles_page.wait_for_loaded()

    assert user_roles_page.role_exists(ROLE_NAME)

    saved_role = get_saved_role(logged_in_browser)
    assert_saved_permissions_are_correct(saved_role)
