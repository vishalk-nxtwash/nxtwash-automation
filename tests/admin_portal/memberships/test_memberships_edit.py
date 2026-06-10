from tests.admin_portal.memberships.conftest import MEMBERSHIP_NAME
from tests.admin_portal.memberships.conftest import create_membership_if_missing


POINTS_AWARDED = "5"
APPLICABLE_DISCOUNT = "Plus discount"


def test_edit_membership_loyalty_points_and_discount(browser):

    memberships_page = create_membership_if_missing(browser)
    memberships_page.update_loyalty_points_and_discount(
        MEMBERSHIP_NAME,
        POINTS_AWARDED,
        APPLICABLE_DISCOUNT
    )

    memberships_page.open_edit_membership(MEMBERSHIP_NAME)

    assert memberships_page.get_points_awarded_value() == POINTS_AWARDED

    memberships_page.open_discount_settings()

    assert memberships_page.discount_is_selected(APPLICABLE_DISCOUNT)
