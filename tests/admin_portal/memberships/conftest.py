from tests.admin_portal.test_create_membership import (
    FIRST_LOCATION_COMMISSION,
    FIRST_LOCATION_PRICE,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    MEMBERSHIP_NAME,
    PREPAID_MONTHS,
    REDEEM_AS_SERVICE,
    VISIBLE_PRICE,
    create_membership_if_missing,
)
from tests.admin_portal.test_memberships import (
    EXISTING_MEMBERSHIP,
    MISSING_MEMBERSHIP,
    open_memberships_page,
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
