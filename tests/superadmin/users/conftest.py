import pytest

from pages.superadmin.login_page import LoginPage
from pages.superadmin.sidebar import Sidebar
from pages.superadmin.users_page import CreateUserPage, EditUserPage, UsersPage

# ── Known active roles in staging (used by create/dropdown tests) ─────────────
# These constants drive SA-USR-CRT-019 and SA-USR-CRT-022–025.
# The users themselves do NOT need to exist — only the roles do.
TEST_USERS = [
    {
        "first_name": "VK",
        "last_name": "User 1 Company Owner",
        "email": "vksauser1@yopmail.com",
        "phone": "9900000001",
        "password": "Vk@auto2025!",
        "role": "Company Owner",
    },
    {
        "first_name": "VK",
        "last_name": "User 2 POS Super User1",
        "email": "vksauser2@yopmail.com",
        "phone": "9900000002",
        "password": "Vk@auto2025!",
        "role": "POS Super User1",
    },
    {
        "first_name": "VK",
        "last_name": "User 3 POS User8",
        "email": "vksauser3@yopmail.com",
        "phone": "9900000003",
        "password": "Vk@auto2025!",
        "role": "POS User8",
    },
    {
        "first_name": "VK",
        "last_name": "User 4 User",
        "email": "vksauser4@yopmail.com",
        "phone": "9900000004",
        "password": "Vk@auto2025!",
        "role": "User",
    },
    {
        "first_name": "VK",
        "last_name": "User 5 VK Carwash",
        "email": "vksauser5@yopmail.com",
        "phone": "9900000005",
        "password": "Vk@auto2025!",
        "role": "VK carwash role",
    },
]

# Pre-existing staging user — never created by automation.
# first_name/last_name/phone MUST match the actual values in staging for
# edit-form prefill tests to pass. Update these if they differ.
PRIMARY_USER = {
    "first_name": "VK",
    "last_name": "AutoTest1",
    "email": "vkautotest1@yopmail.com",
    "phone": "9900000010",
    "password": "Vk@auto2025!",
    "role": "User",
}


# ── Per-test fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def users_page(browser):
    """Log in to Superadmin and return a loaded Users list page."""
    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()
    login_page.wait_for_overview()

    Sidebar(browser).open_users()

    page = UsersPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def create_user_page(users_page, browser):
    """Navigate from Users list to the Create User form."""
    users_page.click_add_user()

    page = CreateUserPage(browser)
    page.wait_for_loaded()
    return page


@pytest.fixture
def edit_user_page(users_page, browser):
    """Navigate to the edit form for the primary test user (User role)."""
    users_page.open_user_edit(PRIMARY_USER["email"])

    page = EditUserPage(browser)
    page.wait_for_loaded()
    return page
