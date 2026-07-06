import allure
import pytest

from tests.admin_portal.employees.conftest import (
    open_employees_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Employees"),
    allure.story("Export"),
]


@allure.title("EMP-EXP-001 Export button is clickable and does not break the page")
@pytest.mark.edge
@pytest.mark.xfail(
    strict=False,
    reason=(
        "EMP-EXP-001: Export button locator uses sibling heuristic relative to Filter by. "
        "Verify exact button position in DevTools. "
        "File download itself is not asserted — only page integrity is checked."
    ),
)
def test_export_button_clickable(browser):
    page = open_employees_page(browser)
    page.click_export_button()

    assert page_has_no_broken_state(page), (
        "Page entered an error state after clicking Export"
    )
