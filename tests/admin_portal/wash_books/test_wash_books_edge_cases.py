import allure
import pytest

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Edge Cases"),
]


@allure.title("WB-DSC-003 Long description does not break the form")
@pytest.mark.extended
def test_wash_book_long_description_does_not_break_form(isolated_wash_book):
    wash_books_page, name = isolated_wash_book
    wash_books_page.open_edit_wash_book(name)
    wash_books_page.set_wash_book_description("Long description " + ("A" * 256))

    assert wash_books_page.get_wash_book_description_value().startswith(
        "Long description "
    )
