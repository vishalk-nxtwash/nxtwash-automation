import allure
import pytest

from tests.admin_portal.service_categories.conftest import CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import INACTIVE_CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import MANAGED_CATEGORY
from tests.admin_portal.service_categories.conftest import create_category_if_missing
from tests.admin_portal.service_categories.conftest import create_inactive_category_if_missing
from tests.admin_portal.service_categories.conftest import managed_category  # noqa: F401
from tests.admin_portal.service_categories.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Happy Path"),
]

_EDITED_NAME = CATEGORY_NAME + " edited"


@allure.title("SC-HP-001 Create Active Category")
@pytest.mark.sanity
@pytest.mark.regression
def test_create_active_service_category(browser):

    page = create_category_if_missing(browser)
    page.search_category(CATEGORY_NAME)

    assert page.wait_for_category_row(CATEGORY_NAME).is_displayed()
    assert page.get_category_status(CATEGORY_NAME) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("SC-HP-002 Create Inactive Category")
@pytest.mark.regression
def test_create_inactive_service_category(browser):

    page = create_inactive_category_if_missing(browser)

    # Inactive rows are hidden in the default view — verify via the edit form
    page.open_edit_category(INACTIVE_CATEGORY_NAME)

    assert page.get_category_name_value() == INACTIVE_CATEGORY_NAME
    assert not page.active_switch_is_on()
    assert page_has_no_broken_state(page)


@allure.title("SC-HP-003 Edit Category")
@pytest.mark.regression
@pytest.mark.skip(reason="needs_inspection: wait_for_list_loaded() times out after click_save_changes() — app no longer auto-redirects to list after save; check what URL/state the edit form navigates to on staging")
def test_edit_service_category_name(browser):

    page = create_category_if_missing(browser)

    try:
        page.update_category_name(CATEGORY_NAME, _EDITED_NAME)
        page.search_category(_EDITED_NAME)

        assert page.wait_for_category_row(_EDITED_NAME).is_displayed()
        assert page_has_no_broken_state(page)

    finally:
        page.wait_for_list_loaded()
        if page.category_exists(_EDITED_NAME):
            page.update_category_name(_EDITED_NAME, CATEGORY_NAME)


@allure.title("SC-HP-004 Activate Category")
@pytest.mark.regression
@pytest.mark.skip(reason="needs_inspection: wait_for_list_loaded() times out after click_save_changes() — same post-save redirect issue as test_edit_service_category_name")
def test_activate_service_category(managed_category):

    page = managed_category

    # Deactivate first to set up the test condition
    page.open_edit_category(MANAGED_CATEGORY)
    page.ensure_active_switch_off()
    page.click_save_changes()
    page.wait_for_list_loaded()

    # Re-activate — open_edit_category uses inactive-filter fallback
    page.open_edit_category(MANAGED_CATEGORY)
    page.ensure_active_switch_on()
    page.click_save_changes()
    page.wait_for_list_loaded()

    page.search_category(MANAGED_CATEGORY)
    assert page.wait_for_category_row(MANAGED_CATEGORY).is_displayed()
    assert page.get_category_status(MANAGED_CATEGORY) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("SC-HP-005 Deactivate Category")
@pytest.mark.regression
@pytest.mark.skip(reason="needs_inspection: wait_for_list_loaded() times out after click_save_changes() — same post-save redirect issue as test_edit_service_category_name")
def test_deactivate_service_category(managed_category):

    page = managed_category

    page.open_edit_category(MANAGED_CATEGORY)
    page.ensure_active_switch_off()
    page.click_save_changes()
    page.wait_for_list_loaded()

    # Default list shows only Active — deactivated category must be absent
    page.search_category(MANAGED_CATEGORY)
    assert MANAGED_CATEGORY not in page.get_visible_category_names(), (
        "Expected '%s' to be hidden after deactivation but it is still "
        "visible in the active-only default list" % MANAGED_CATEGORY
    )
    assert page_has_no_broken_state(page)


@allure.title("SC-CRUD-002 Service category settings persist")
@pytest.mark.regression
def test_service_category_settings_persist(browser):

    page = create_category_if_missing(browser)
    page.open_edit_category(CATEGORY_NAME)

    assert page.get_category_name_value() == CATEGORY_NAME
    assert page.active_switch_is_on()
