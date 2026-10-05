import allure
import pytest

from tests.admin_portal.service_categories.conftest import MANAGED_CATEGORY
from tests.admin_portal.service_categories.conftest import MANAGED_CATEGORY_EDITED
from tests.admin_portal.service_categories.conftest import managed_category  # noqa: F401


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("CRUD"),
]


@allure.title("SC-HP-003/SC-EC-002 Edit service category name and restore baseline")
@pytest.mark.regression
def test_edit_service_category_name_and_restore(managed_category):
    """Rename the managed category and verify it persists, then restore it.

    Renames specifically to MANAGED_CATEGORY_EDITED (not an arbitrary data-
    driven name) because reset_managed_category()'s own self-heal logic
    checks for that exact name on every setup. If this test gets killed
    mid-run before its own `finally` restores the baseline name, the next
    run's fixture setup recognizes and recovers it automatically — renaming
    to a name the fixture doesn't watch for would leave the managed record
    permanently stuck under that name until someone fixes it by hand.
    """
    page = managed_category

    try:
        page.update_category_name(MANAGED_CATEGORY, MANAGED_CATEGORY_EDITED)
        page.search_category(MANAGED_CATEGORY_EDITED)

        assert page.wait_for_category_row(MANAGED_CATEGORY_EDITED).is_displayed()

    finally:
        page.wait_for_list_loaded()
        if page.category_exists(MANAGED_CATEGORY_EDITED):
            page.update_category_name(MANAGED_CATEGORY_EDITED, MANAGED_CATEGORY)
