from tests.admin_portal.test_discounts import (
    DISCOUNT_AMOUNT,
    DISCOUNT_NAME,
    EXISTING_DISCOUNT,
    MISSING_DISCOUNT,
    REQUESTED_SERVICE_CATEGORY,
    SERVICE_CATEGORY,
    START_DAY,
    START_TIME,
    START_VALUE,
    create_discount_if_missing,
    open_discounts_page,
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
