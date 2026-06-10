from tests.admin_portal.test_edit_wash_book import WASH_BOOK_DESCRIPTION
from tests.admin_portal.test_wash_books import (
    EXISTING_WASH_BOOK,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    MISSING_WASH_BOOK,
    NUMBER_OF_WASHES,
    POINTS_AWARDED,
    VISIBLE_PRICE,
    WASH_BOOK_NAME,
    create_wash_book_if_missing,
    open_wash_books_page,
)


BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)
