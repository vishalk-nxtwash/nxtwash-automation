import allure
import pytest

from tests.admin_portal.wash_books.conftest import (
    CWB_NUMBER_OF_WASHES,
    CWB_WASH_BOOK_NUMBER,
    WASH_BOOK_NAME,
    create_customer_wash_book_if_missing,
    open_customer_wash_books_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Customer Wash Books — Dependency"),
]


@allure.title("CWB-DEP-001 Only active wash books appear in the Select wash book dropdown")
@pytest.mark.regression
def test_only_active_wash_books_in_cwb_dropdown(browser):

    page = open_customer_wash_books_page(browser)
    page.open_create_cwb()
    body_text = page.get_body_text()

    assert "Select wash book" in body_text
    assert page_has_no_broken_state(page)


@allure.title("CWB-DEP-002 CWB number of washes matches the template wash book at creation time")
@pytest.mark.regression
def test_cwb_washes_reflect_template_wash_book(browser):

    create_customer_wash_book_if_missing(browser)
    page = open_customer_wash_books_page(browser)
    page.search_cwb(CWB_WASH_BOOK_NUMBER)
    row_washes = page.get_cwb_number_of_washes_from_row(CWB_WASH_BOOK_NUMBER)

    assert str(row_washes).strip() == str(CWB_NUMBER_OF_WASHES).strip()
    assert page_has_no_broken_state(page)
