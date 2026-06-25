import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC

from tests.admin_portal.wash_books.conftest import open_wash_books_page
from tests.admin_portal.wash_books.conftest import open_customer_wash_books_page
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("UI and List"),
]


@allure.title("WB-LST-001 Wash books page loads with primary controls")
@pytest.mark.smoke
def test_wash_books_page_loads_with_primary_controls(browser):

    page = open_wash_books_page(browser)
    body_text = page.get_body_text()

    assert "Wash books" in body_text
    # Use wait.until so the element has time to render (avoid NoSuchElementException)
    assert page.wait.until(
        EC.visibility_of_element_located(page.SEARCH_INPUT)
    ).is_displayed()
    assert page.wait.until(
        EC.visibility_of_element_located(page.FILTER_BUTTON)
    ).is_displayed()
    assert page.download_button_is_clickable()
    assert page.wait.until(
        EC.visibility_of_element_located(page.ADD_WASH_BOOK_BUTTON)
    ).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("WB-LST-002 Wash books grid columns are visible")
@pytest.mark.regression
def test_wash_books_grid_columns_are_visible(browser):

    page = open_wash_books_page(browser)
    body_text = page.get_body_text()

    assert "ID" in body_text
    assert "Wash book name" in body_text
    assert "Washes number" in body_text
    assert "Price" in body_text
    assert "Status" in body_text


@allure.title("WB-LST-003 Customer wash books tab and its listing are accessible")
@pytest.mark.smoke
def test_customer_wash_books_tab_is_accessible(browser):

    # Verify tab label is present inside the WB list iframe
    wb_page = open_wash_books_page(browser)
    assert "Customer wash books" in wb_page.get_body_text()

    # Navigate directly to CWB URL to confirm the tab target loads without error
    cwb_page = open_customer_wash_books_page(browser)
    assert "Customer wash books" in cwb_page.get_body_text()
    assert page_has_no_broken_state(cwb_page)


@allure.title("Add wash book form loads with required fields")
@pytest.mark.smoke
def test_add_wash_book_form_loads(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    body_text = page.get_body_text()

    assert "Add new wash book" in body_text
    assert "Wash book name" in body_text
    assert "Number of washes" in body_text
    assert "Global price" in body_text


@allure.title("WB-EXP-001 Export button is clickable (deferred: content validation)")
@pytest.mark.export
@pytest.mark.xfail(
    reason=(
        "WB-EXP-001: File content validation requires browser download-directory "
        "configuration and CSV/XLS parser utilities. Deferred."
    ),
    strict=False,
)
def test_wash_books_export_file_validation(browser):

    page = open_wash_books_page(browser)
    assert page.download_button_is_clickable()
    raise AssertionError("Download file/content validation is not implemented.")
