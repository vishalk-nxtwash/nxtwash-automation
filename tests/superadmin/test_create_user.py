import pytest
from selenium.common.exceptions import TimeoutException

from pages.superadmin.login_page import LoginPage
from pages.superadmin.sidebar import Sidebar
from pages.superadmin.users_page import CreateUserPage
from pages.superadmin.users_page import UsersPage


FIRST_NAME = "vktestuser1"
LAST_NAME = "User"
EMAIL = "vktestuser1@yopmail.com"
PASSWORD = "vishal01"
PHONE = "7751100011"
DUPLICATE_EMAIL_PHONE = "7751100012"
ROLE = "User"

VK_ROLE_FIRST_NAME = "Vktestuser2"
VK_ROLE_LAST_NAME = "User"
VK_ROLE_EMAIL = "vktestuser2@yopmail.com"
VK_ROLE_PASSWORD = "vishal2"
VK_ROLE_PHONE = "7751100022"
VK_ROLE = "VK carwash role"


@pytest.fixture
def logged_in_browser(browser):

    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()

    login_page.wait_for_url(
        "https://superadmin.nxtwash.com/"
    )

    return browser


def open_users_page(browser):

    sidebar = Sidebar(browser)
    sidebar.open_users()

    users_page = UsersPage(browser)
    users_page.wait_for_loaded()

    return users_page


def open_create_user_page(browser):

    users_page = open_users_page(browser)
    users_page.click_add_user()

    create_user_page = CreateUserPage(browser)
    create_user_page.wait_for_loaded()

    return create_user_page


def create_user_if_missing(
    browser,
    first_name=FIRST_NAME,
    last_name=LAST_NAME,
    password=PASSWORD,
    email=EMAIL,
    phone=PHONE,
    role_name=ROLE
):

    users_page = open_users_page(browser)

    if users_page.user_exists(email):
        return

    browser.get("https://superadmin.nxtwash.com/users/create")

    create_user_page = CreateUserPage(browser)
    create_user_page.wait_for_loaded()
    create_user_page.fill_user_form(
        first_name,
        last_name,
        password,
        password,
        email,
        phone,
        role_name
    )
    create_user_page.click_save_new()
    create_user_page.confirm_yes_if_present()

    try:
        users_page = open_users_page(browser)
        users_page.filter_by_email(email)
        users_page.wait_for_user_row(email)
    except TimeoutException:
        body_text = create_user_page.get_body_text().lower()
        duplicate_messages = [
            "email id already associated",
            "email already associated",
            "email already exists",
            "duplicate email"
        ]

        if any(message in body_text for message in duplicate_messages):
            users_page = open_users_page(browser)
            users_page.filter_by_email(email)
            users_page.wait_for_user_row(email)
            return

        if "too small" in body_text or "password" in body_text:
            pytest.fail(
                "Create user validation failed for '%s': %s"
                % (email, create_user_page.get_body_text())
            )

        raise


def test_create_user_required_field_validation(logged_in_browser):

    create_user_page = open_create_user_page(logged_in_browser)

    create_user_page.click_save_new()

    assert create_user_page.has_validation_text("Too small")
    assert create_user_page.has_validation_text(
        "Invalid email address"
    )
    assert create_user_page.has_validation_text("Role is required")


def test_create_user_invalid_email_validation(logged_in_browser):

    create_user_page = open_create_user_page(logged_in_browser)
    create_user_page.fill_user_form(
        FIRST_NAME,
        LAST_NAME,
        PASSWORD,
        PASSWORD,
        "vktestuser1",
        PHONE,
        ROLE
    )

    create_user_page.click_save_new()

    assert create_user_page.has_validation_text(
        "Invalid email address"
    )


def test_create_user_password_mismatch_validation(logged_in_browser):

    create_user_page = open_create_user_page(logged_in_browser)
    create_user_page.fill_user_form(
        FIRST_NAME,
        LAST_NAME,
        PASSWORD,
        "different01",
        EMAIL,
        PHONE,
        ROLE
    )

    create_user_page.click_save_new()

    assert "password" in create_user_page.get_body_text().lower()


def test_cancel_create_user_does_not_create_user(logged_in_browser):

    users_page = open_users_page(logged_in_browser)

    if users_page.user_exists(EMAIL):
        pytest.skip("Target user already exists; cancel flow cannot prove absence.")

    logged_in_browser.get("https://superadmin.nxtwash.com/users/create")

    create_user_page = CreateUserPage(logged_in_browser)
    create_user_page.wait_for_loaded()
    create_user_page.fill_user_form(
        FIRST_NAME,
        LAST_NAME,
        PASSWORD,
        PASSWORD,
        EMAIL,
        PHONE,
        ROLE
    )
    create_user_page.click_cancel()
    create_user_page.confirm_yes_if_present()

    users_page = open_users_page(logged_in_browser)

    assert not users_page.user_exists(EMAIL)


def test_create_user_and_confirm_in_users_list(logged_in_browser):

    create_user_if_missing(logged_in_browser)

    users_page = open_users_page(logged_in_browser)
    users_page.filter_by_email(EMAIL)

    assert users_page.wait_for_user_row(EMAIL).is_displayed()


def test_create_vk_role_user_and_confirm_in_users_list(logged_in_browser):

    create_user_if_missing(
        logged_in_browser,
        VK_ROLE_FIRST_NAME,
        VK_ROLE_LAST_NAME,
        VK_ROLE_PASSWORD,
        VK_ROLE_EMAIL,
        VK_ROLE_PHONE,
        VK_ROLE
    )

    users_page = open_users_page(logged_in_browser)
    users_page.filter_by_email(VK_ROLE_EMAIL)

    assert users_page.wait_for_user_row(VK_ROLE_EMAIL).is_displayed()


def test_duplicate_user_email_validation(logged_in_browser):

    create_user_if_missing(logged_in_browser)

    create_user_page = open_create_user_page(logged_in_browser)
    create_user_page.fill_user_form(
        FIRST_NAME,
        LAST_NAME,
        PASSWORD,
        PASSWORD,
        EMAIL,
        DUPLICATE_EMAIL_PHONE,
        ROLE
    )
    create_user_page.click_save_new()

    duplicate_email_messages = [
        "email id already associated",
        "email already associated",
        "email already exists",
        "duplicate email"
    ]
    create_user_page.wait_for_any_text(duplicate_email_messages)

    body_text = create_user_page.get_body_text().lower()

    assert (
        any(message in body_text for message in duplicate_email_messages)
    )
