import logging

import allure
import pytest

from tests.admin_portal.service_categories.conftest import MANAGED_CATEGORY
from tests.admin_portal.service_categories.conftest import MANAGED_CATEGORY_EDITED


LOG = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Managed data"),
]


@allure.title("SC-MANAGED-001 Managed category starts at baseline")
@pytest.mark.sanity
def test_managed_category_provided_at_baseline(managed_category):
    """The fixture hands over a dedicated record already at baseline name."""
    page = managed_category

    assert page.category_exists(MANAGED_CATEGORY)
    assert not page.category_exists(MANAGED_CATEGORY_EDITED)
    assert page.get_category_status(MANAGED_CATEGORY) == "Active"


@allure.title("SC-MANAGED-002 Rename is reverted on teardown")
@pytest.mark.regression
def test_managed_category_rename_is_reset_on_teardown(managed_category):
    """Rename the category; the fixture teardown restores the baseline name."""
    page = managed_category

    LOG.info("Renaming managed category to %s", MANAGED_CATEGORY_EDITED)
    page.update_category_name(MANAGED_CATEGORY, MANAGED_CATEGORY_EDITED)

    assert page.category_exists(MANAGED_CATEGORY_EDITED)
    # On teardown the fixture renames it back to MANAGED_CATEGORY, so the next
    # test (and the next run) sees the baseline name without manual cleanup.
