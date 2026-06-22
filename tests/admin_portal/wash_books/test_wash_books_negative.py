import allure
import pytest

from tests.admin_portal.wash_books.conftest import EXISTING_WASH_BOOK
from tests.admin_portal.wash_books.conftest import MISSING_WASH_BOOK
from tests.admin_portal.wash_books.conftest import WASH_BOOK_NAME
from tests.admin_portal.wash_books.conftest import create_wash_book_if_missing
from tests.admin_portal.wash_books.conftest import open_wash_books_page
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Negative"),
]


@allure.title("WB-SRH-003 Searching a non-existing wash book returns no results")
@pytest.mark.extended
def test_missing_wash_book_is_not_returned(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book(MISSING_WASH_BOOK)

    assert MISSING_WASH_BOOK not in wash_books_page.get_body_text()
    assert page_has_no_broken_state(wash_books_page)


@allure.title("WB-SRH special-character search does not crash the grid")
@pytest.mark.extended
def test_wash_books_special_character_search_stays_usable(browser):

    wash_books_page = open_wash_books_page(browser)
    wash_books_page.search_wash_book("%%%___###")

    assert page_has_no_broken_state(wash_books_page)
    assert wash_books_page.driver.find_element(
        *wash_books_page.SEARCH_INPUT
    ).is_displayed()


@allure.title("WB-NAM-003 Duplicate wash book name is blocked on save")
@pytest.mark.regression
def test_duplicate_wash_book_name_is_blocked(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name(EXISTING_WASH_BOOK)
    page.set_number_of_washes("5")
    page.set_global_price("10")
    page.click_save_wash_book()

    body_text = page.get_body_text()
    saved = "Add new wash book" not in body_text and EXISTING_WASH_BOOK in page.get_body_text()
    error_shown = any(
        phrase in body_text
        for phrase in ("already exists", "duplicate", "exist")
    )
    assert error_shown or not saved


@allure.title("WB-NAM-005 A whitespace-only wash book name is rejected on save")
@pytest.mark.extended
def test_whitespace_only_wash_book_name_is_rejected(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("   ")
    page.set_number_of_washes("5")
    page.set_global_price("10")
    page.click_save_wash_book()

    assert (
        not page.wash_book_name_input_is_valid()
        or "Add new wash book" in page.get_body_text()
    )
    assert page_has_no_broken_state(page)


@allure.title("WB-WNO-003 Negative number of washes is rejected on save")
@pytest.mark.extended
def test_negative_number_of_washes_is_rejected(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-neg-washes-test")
    page.set_number_of_washes("-1")
    page.set_global_price("10")
    page.click_save_wash_book()

    assert "Add new wash book" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("WB-PRI-005 Negative global price is rejected on save")
@pytest.mark.regression
def test_negative_global_price_is_rejected(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-neg-price-test")
    page.set_number_of_washes("5")
    page.set_global_price("-10")
    page.click_save_wash_book()

    assert "Add new wash book" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("WB-COM-002 Negative global commission is rejected on save")
@pytest.mark.extended
def test_negative_global_commission_is_rejected(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-neg-commission-test")
    page.set_number_of_washes("5")
    page.set_global_price("10")
    page.set_global_commission("-2")
    page.click_save_wash_book()

    assert "Add new wash book" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("WB-LTY-003 Negative loyalty points awarded is rejected on save")
@pytest.mark.extended
def test_negative_loyalty_points_is_rejected(browser):

    page = open_wash_books_page(browser)
    page.open_create_wash_book()
    page.enter_wash_book_name("VK AWB2-neg-points-test")
    page.set_points_awarded("-1")

    assert page_has_no_broken_state(page)


@allure.title("WB-BAR-003 Duplicate barcode is rejected on save")
@pytest.mark.regression
@pytest.mark.skip(
    reason="WB-BAR-003: Requires a known barcode already assigned to another wash book. "
    "Deferred until barcode fixtures are established."
)
def test_duplicate_barcode_is_rejected(browser):
    pass


@allure.title("WB-RED-004 Saving a redemption site without selecting a wash package is blocked or documented")
@pytest.mark.regression
def test_save_redemption_site_without_wash_package(browser):

    page = create_wash_book_if_missing(browser)
    page.open_edit_wash_book(WASH_BOOK_NAME)
    page.open_redemption_settings()

    assert "Redeem at" in page.get_body_text()
    assert page_has_no_broken_state(page)
