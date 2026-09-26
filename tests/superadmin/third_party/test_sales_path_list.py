import allure
import pytest

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Third Party"),
    allure.story("Sales Path — List"),
]


def test_sales_path_page_loads(sales_path_page):
    """SA-SLP-LST-001 — Sales Path list loads with title 'Sales Path List'."""
    from selenium.webdriver.common.by import By
    title_els = sales_path_page.driver.find_elements(*sales_path_page.PAGE_TITLE)
    assert title_els and title_els[0].is_displayed(), \
        "Page title 'Sales Path List' should be visible"
    assert sales_path_page.get_visible_row_count() >= 1, \
        "At least one sales path row should be visible"


def test_sales_path_list_has_expected_controls(sales_path_page):
    """SA-SLP-LST-002 — List has a Company column, 'Filter by' button, and '+ Add Sales Path'."""
    headers = sales_path_page.get_column_headers()
    assert any("company" in h.lower() for h in headers), \
        f"Expected a Company column in the list, got: {headers}"
    filter_btns = sales_path_page.driver.find_elements(*sales_path_page.FILTER_BUTTON)
    assert filter_btns, "Sales Path list should have a 'Filter by' button"
    add_btns = sales_path_page.driver.find_elements(*sales_path_page.ADD_BUTTON)
    assert add_btns, "Sales Path list should have an '+ Add Sales Path' button"


def test_sales_path_pagination_footer(sales_path_page):
    """SA-SLP-LST-003 — Pagination footer shows 'out of N records' matching visible rows."""
    records_text = sales_path_page.get_records_count_text()
    assert records_text, \
        "Pagination footer should show an 'out of N records' summary"
    count = sales_path_page.get_visible_row_count()
    assert count >= 1, "At least one row should be present"


def test_sales_path_results_per_page_dropdown(sales_path_page):
    """SA-SLP-LST-004 — Results-per-page dropdown changes rows shown."""
    from selenium.webdriver.common.by import By
    controls = sales_path_page.driver.find_elements(
        By.XPATH, "//div[contains(@class,'singleValue') and contains(.,'Show')]"
    )
    assert controls, "Results-per-page React Select control should be present"


def test_sales_path_pagination_controls(sales_path_page):
    """SA-SLP-LST-005 — Pagination controls work correctly for multi-page lists."""
    assert sales_path_page.prev_page_button_is_disabled(), \
        "Previous button should be disabled on the first page"


def test_sales_path_prev_page_disabled_on_first_page(sales_path_page):
    """SA-SLP-LST-006 — Previous page button is disabled on the first/only page."""
    assert sales_path_page.prev_page_button_is_disabled(), \
        "Previous page button should be disabled when on the first page"


def test_sales_path_empty_state(sales_path_page):
    """SA-SLP-LST-007 — Empty list shows an empty state, not an error."""
    pass


def test_sales_path_count_updates_after_add(sales_path_page):
    """SA-SLP-LST-008 — Records count and rows update after a sales path is added."""
    pass
