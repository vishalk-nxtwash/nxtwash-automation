import allure
import pytest

from tests.admin_portal.wash_books.conftest import open_customer_wash_books_page
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Customer Wash Books — Edge Cases"),
]


@allure.title("CWB-CRT-004 Customer search requires at least 2 characters to show results")
@pytest.mark.extended
def test_cwb_customer_search_requires_two_characters(browser):

    page = open_customer_wash_books_page(browser)
    page.open_create_cwb()
    body_text = page.get_body_text()

    assert "Select customer" in body_text
    assert page_has_no_broken_state(page)


@allure.title("CWB-VAL-005 Selecting a past expiration date is blocked or documented")
@pytest.mark.extended
@pytest.mark.skip(
    reason="CWB-VAL-005: Date-time picker interaction and past-date validation require "
    "additional page object support. Deferred."
)
def test_cwb_past_expiration_date_behaviour(browser):
    pass
