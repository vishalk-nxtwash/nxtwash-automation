import allure
import pytest

from tests.admin_portal.gas_pump_settings.conftest import (
    open_gas_pump_list,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gas Pump Settings"),
    allure.story("UI"),
]


@allure.title("GPS-UI-001 Gas pump settings list loads with primary controls")
@pytest.mark.prod_smoke
def test_gas_pump_settings_page_loads_with_primary_controls(browser):
    page = open_gas_pump_list(browser)
    body = page.get_body_text()

    assert "Gas Pump" in body, "Page heading 'Gas Pump' not found"
    assert page.driver.find_element(*page.ADD_PUMP_BUTTON).is_displayed(), (
        "Add gas pump button not visible"
    )
    assert page_has_no_broken_state(page)


@allure.title("GPS-UI-002 Gas pump settings grid shows required column headers")
@pytest.mark.prod_smoke
def test_gas_pump_settings_grid_columns_are_visible(browser):
    page = open_gas_pump_list(browser)
    body = page.get_body_text()

    assert "Gas pump name" in body, "Column 'Gas pump name' not found"
    assert "Status" in body, "Column 'Status' not found"
    assert "Edit" in body, "Column 'Edit' not found"
    assert page_has_no_broken_state(page)
