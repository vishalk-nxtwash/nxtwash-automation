import allure
import pytest

from tests.admin_portal.tunnel_settings.conftest import (
    open_tunnel_list,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Tunnel Settings"),
    allure.story("UI"),
]


@allure.title("TUN-UI-001 Tunnel settings list loads with primary controls")
@pytest.mark.prod_smoke
def test_tunnel_settings_page_loads_with_primary_controls(browser):
    page = open_tunnel_list(browser)
    body = page.get_body_text()

    assert "Tunnel" in body, "Page heading 'Tunnel' not found"
    assert page.driver.find_element(*page.ADD_TUNNEL_BUTTON).is_displayed(), (
        "Add new tunnel button not visible"
    )
    assert page_has_no_broken_state(page)


@allure.title("TUN-UI-002 Tunnel settings grid shows required column headers")
@pytest.mark.prod_smoke
def test_tunnel_settings_grid_columns_are_visible(browser):
    page = open_tunnel_list(browser)
    body = page.get_body_text()

    assert "Tunnel name" in body, "Column 'Tunnel name' not found"
    assert "Status" in body, "Column 'Status' not found"
    assert "Edit" in body, "Column 'Edit' not found"
    assert page_has_no_broken_state(page)
