import allure
import pytest

from tests.admin_portal.users.conftest import (
    open_users_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Users"),
    allure.story("Export"),
]


@allure.title("USR-EXP-001 Export button is clickable and does not break the page")
@pytest.mark.edge
def test_users_export_button_clickable(browser):
    page = open_users_page(browser)
    page.click_export_button()
    page.wait_for_loaded()

    assert page_has_no_broken_state(page)
