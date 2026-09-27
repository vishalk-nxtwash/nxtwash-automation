import re
import warnings

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.superadmin.login_page import LoginPage
from pages.superadmin.sidebar import Sidebar
from pages.superadmin.user_roles_page import CreateUserRolePage, EditUserRolePage, UserRolesPage

# ── Test role constants ────────────────────────────────────────────────────────
# Only ONE custom role is created and maintained in staging to avoid clutter.
TEST_ROLE_NAME = "VK Auto Test Role"
PREDEFINED_ROLE_NAME = "Company Owner"

_BASE_URL = "https://superadmin.nxtwash.com"


# Names the edit test gives the role ("<name> Edited <6 hex>"). If a run dies
# before its teardown restore, the role keeps that name; recover it by id here,
# otherwise the name-based upsert below would POST a duplicate role.
_EDITED_TEST_ROLE = re.compile(r"^%s Edited [0-9a-f]{6}$" % re.escape(TEST_ROLE_NAME))


def _recover_renamed_test_role(api):
    roles = api._role_api_call("GET") or []
    if any(r["roleName"] == TEST_ROLE_NAME for r in roles):
        return
    leftovers = [r for r in roles if _EDITED_TEST_ROLE.match(r["roleName"])]
    if leftovers:
        snapshot = api.get_role_by_id_with_api(leftovers[0]["superAdminUserRoleId"])
        snapshot["roleName"] = TEST_ROLE_NAME
        api.restore_role_with_api(snapshot)


@pytest.fixture(scope="session", autouse=True)
def ensure_test_roles_exist(request):
    """Create active and inactive automation test roles before any test runs.

    Uses the API upsert so the fixture is idempotent across re-runs.
    """
    from core.driver_factory import DriverFactory

    headless = request.config.getoption("--headless", default=False)
    driver = DriverFactory.get_driver(headless=headless, detach=False)
    driver.set_page_load_timeout(60)

    try:
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login()
        login_page.wait_for_url("https://superadmin.nxtwash.com/")

        driver.get(f"{_BASE_URL}/user-roles")
        WebDriverWait(driver, 15).until(
            lambda d: "/user-roles" in d.current_url
        )

        api = CreateUserRolePage(driver)
        _recover_renamed_test_role(api)
        api.upsert_role_with_api(TEST_ROLE_NAME, is_active=True, include_create_company=True)

    except Exception as exc:
        warnings.warn(
            f"ensure_test_roles_exist: setup failed — user-roles tests may fail.\n"
            f"Reason: {exc}",
            stacklevel=2,
        )
    finally:
        try:
            driver.set_page_load_timeout(5)
            driver.get("about:blank")
        except Exception:
            pass
        try:
            driver.quit()
        except Exception:
            pass


# ── Per-test fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def user_roles_page(browser):
    """Log in to Superadmin and return a loaded User Roles list page."""
    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()
    login_page.wait_for_url("https://superadmin.nxtwash.com/")

    Sidebar(browser).open_user_roles()

    page = UserRolesPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def create_role_page(user_roles_page, browser):
    """Navigate from the list to the Add User Role create form."""
    user_roles_page.click_add_role()
    page = CreateUserRolePage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def edit_role_page(user_roles_page, browser):
    """Navigate to the edit form for the automation test role."""
    user_roles_page.open_role(TEST_ROLE_NAME)
    page = EditUserRolePage(browser)
    page.wait_for_loaded()
    return page
