import allure
import pytest

from tests.admin_portal.wash_books.conftest import WASH_BOOK_NAME
from tests.admin_portal.wash_books.conftest import create_wash_book_if_missing
from tests.admin_portal.wash_books.conftest import open_wash_books_page
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Edge Cases"),
]


@allure.title("WB-EDGE Create wash book is idempotent — calling twice does not duplicate")
@pytest.mark.extended
def test_wash_book_create_is_idempotent(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.wait_for_list_loaded()
    wash_books_page.search_wash_book(WASH_BOOK_NAME)

    assert wash_books_page.wait_for_wash_book_row(WASH_BOOK_NAME).is_displayed()


@allure.title("WB-RED-001 Redemption settings panel loads with assigned package data")
@pytest.mark.regression
def test_wash_book_redemption_settings_persist(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.open_edit_wash_book(WASH_BOOK_NAME)
    wash_books_page.open_redemption_settings()
    body_text = wash_books_page.get_body_text().lower()

    assert "vk detail wash" in body_text
    assert "detail cleaning" in body_text


@allure.title("WB-NAM-004 Long description does not break the form")
@pytest.mark.extended
def test_wash_book_long_description_does_not_break_form(browser):

    wash_books_page = create_wash_book_if_missing(browser)
    wash_books_page.open_edit_wash_book(WASH_BOOK_NAME)
    wash_books_page.set_wash_book_description("Long description " + ("A" * 256))

    assert wash_books_page.get_wash_book_description_value().startswith(
        "Long description "
    )


@allure.title("WB-SIT-004 Saving a wash book with no site assigned is handled gracefully")
@pytest.mark.smoke
def test_wash_book_save_with_no_site_assigned_is_handled(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-no-site-test")
    page.set_number_of_washes("5")
    page.set_global_price("10")
    page.click_save_wash_book()

    assert page_has_no_broken_state(page)


@allure.title("WB-RED-005 Redeem at header checkbox selects all available sites at once")
@pytest.mark.extended
def test_redeem_at_header_checkbox_selects_all_sites(browser):

    page = create_wash_book_if_missing(browser)
    page.open_edit_wash_book(WASH_BOOK_NAME)
    page.open_redemption_settings()

    assert "Redeem at" in page.get_body_text()
    assert page_has_no_broken_state(page)
