import allure
import pytest

from tests.admin_portal.employees.conftest import (
    open_shift_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Employees"),
    allure.story("Shift — Export"),
]


@allure.title("EMP-SH-EXP-001 Shift export button is clickable and does not break the page")
@pytest.mark.edge
def test_shift_export_button_clickable(browser):
    page = open_shift_page(browser)
    page.click_export_button()

    assert page_has_no_broken_state(page), (
        "Shift page entered an error state after clicking Export"
    )
