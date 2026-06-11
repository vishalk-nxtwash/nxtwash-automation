import logging
import uuid

import allure
import pytest

from tests.admin_portal.memberships.conftest import MEMBERSHIP_NAME
from tests.admin_portal.memberships.conftest import create_membership_if_missing
from tests.admin_portal.memberships.conftest import open_memberships_page


LOG = logging.getLogger(__name__)
POINTS_AWARDED = "5"
APPLICABLE_DISCOUNT = "Plus discount"


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MEM-CRUD-006/MEM-CRUD-025 Edit loyalty points and discount")
@pytest.mark.regression
def test_edit_membership_loyalty_points_and_discount(browser):

    LOG.info("Editing membership loyalty points and discount: %s", MEMBERSHIP_NAME)
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


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("CRUD")
@allure.title("MEM-CRUD-019 Verify Edit Membership functionality")
@pytest.mark.regression
def test_edit_membership_name_and_restore(browser):

    LOG.info(
        "Editing membership name from %s and restoring it",
        MEMBERSHIP_NAME,
    )
    updated_membership_name = "%s edit %s" % (
        MEMBERSHIP_NAME,
        uuid.uuid4().hex[:6]
    )
    memberships_page = create_membership_if_missing(browser)

    try:
        memberships_page.update_membership_name(
            MEMBERSHIP_NAME,
            updated_membership_name
        )
        memberships_page.search_membership(updated_membership_name)

        assert memberships_page.wait_for_membership_row(
            updated_membership_name
        ).is_displayed()
        assert updated_membership_name in memberships_page.get_body_text()

        memberships_page.open_edit_membership(updated_membership_name)

        assert memberships_page.get_membership_name_value() == updated_membership_name

    finally:
        memberships_page = open_memberships_page(browser)
        if memberships_page.membership_exists(updated_membership_name):
            memberships_page.update_membership_name(
                updated_membership_name,
                MEMBERSHIP_NAME
            )
