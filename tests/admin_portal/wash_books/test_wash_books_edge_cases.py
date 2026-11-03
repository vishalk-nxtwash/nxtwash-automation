import allure
import pytest

from tests.admin_portal.wash_books.conftest import MANAGED_WASH_BOOK_2


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Edge Cases"),
]


@allure.title("WB-DSC-003 Long description does not break the form")
@pytest.mark.extended
def test_wash_book_long_description_does_not_break_form(managed_wash_book_2):

    page = managed_wash_book_2
    page.open_edit_wash_book(MANAGED_WASH_BOOK_2)
    page.set_wash_book_description("Long description " + ("A" * 256))

    assert page.get_wash_book_description_value().startswith(
        "Long description "
    )
