import allure
import pytest

from tests.admin_portal.service_categories.conftest import CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import MANAGED_CATEGORY
from tests.admin_portal.service_categories.conftest import MANAGED_CATEGORY_EDITED
from tests.admin_portal.service_categories.conftest import create_category_if_missing
from tests.admin_portal.service_categories.conftest import managed_category  # noqa: F401
from tests.admin_portal.service_categories.conftest import open_service_categories_page
from tests.admin_portal.service_categories.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Edge Cases"),
]


@allure.title("SC-EDGE-001 Long service category name does not break form")
@pytest.mark.regression
def test_service_category_long_name_does_not_break_form(browser):

    page = create_category_if_missing(browser)
    page.open_create_category()
    page.enter_category_name("VK " + ("C" * 128))

    assert page_has_no_broken_state(page)
    assert "Category name" in page.get_body_text()


@allure.title("SC-EC-003 Activate-Deactivate-Activate cycle")
@pytest.mark.regression
def test_activate_deactivate_activate_cycle(managed_category):

    page = managed_category

    page.open_edit_category(MANAGED_CATEGORY)
    page.ensure_active_switch_off()
    page.click_save_changes()
    page.wait_for_list_loaded()

    page.open_edit_category(MANAGED_CATEGORY)
    page.ensure_active_switch_on()
    page.click_save_changes()
    page.wait_for_list_loaded()

    page.search_category(MANAGED_CATEGORY)
    assert page.wait_for_category_row(MANAGED_CATEGORY).is_displayed()
    assert page.get_category_status(MANAGED_CATEGORY) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("SC-EC-005 Edit inactive category saves changes")
@pytest.mark.regression
def test_edit_inactive_category_saves_changes(managed_category):
    """Deactivate the managed category, then edit it while inactive.

    Renames to MANAGED_CATEGORY_EDITED so the fixture teardown
    (reset_managed_category) can locate and restore it automatically.
    """
    page = managed_category

    page.open_edit_category(MANAGED_CATEGORY)
    page.ensure_active_switch_off()
    page.click_save_changes()
    page.wait_for_list_loaded()

    page.open_edit_category(MANAGED_CATEGORY)
    page.enter_category_name(MANAGED_CATEGORY_EDITED)
    page.ensure_active_switch_off()
    page.click_save_changes()
    page.wait_for_list_loaded()

    page._show_inactive_categories()
    page.search_category(MANAGED_CATEGORY_EDITED)
    assert page.wait_for_category_row(MANAGED_CATEGORY_EDITED).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("SC-EC-006 Deactivated category is findable via inactive filter")
@pytest.mark.regression
def test_deactivated_category_findable_via_filter(managed_category):

    page = managed_category

    page.open_edit_category(MANAGED_CATEGORY)
    page.ensure_active_switch_off()
    page.click_save_changes()
    page.wait_for_list_loaded()

    page.search_category(MANAGED_CATEGORY)
    assert MANAGED_CATEGORY not in page.get_visible_category_names(), (
        "Expected '%s' to be absent from the default active-only list after "
        "deactivation" % MANAGED_CATEGORY
    )

    page._show_inactive_categories()
    page.search_category(MANAGED_CATEGORY)
    assert page.wait_for_category_row(MANAGED_CATEGORY).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("SC-EC-007 Cancel add new does not create a category")
@pytest.mark.regression
def test_cancel_add_new_does_not_create_category(browser):

    cancel_name = "VK AUTOTEST CANCEL NEW"
    page = open_service_categories_page(browser)

    page.open_create_category()
    page.enter_category_name(cancel_name)
    page.click_cancel()
    page.wait_for_list_loaded()

    assert not page.category_exists(cancel_name), (
        "Expected category '%s' not to exist after cancelling creation" % cancel_name
    )
    assert page_has_no_broken_state(page)


@allure.title("SC-EC-008 Cancel edit does not save changes")
@pytest.mark.regression
def test_cancel_edit_does_not_save_changes(browser):

    ghost_name = CATEGORY_NAME + " ghost edit"
    page = create_category_if_missing(browser)

    page.open_edit_category(CATEGORY_NAME)
    page.enter_category_name(ghost_name)
    page.click_cancel()
    page.wait_for_list_loaded()

    page.search_category(CATEGORY_NAME)
    assert page.wait_for_category_row(CATEGORY_NAME).is_displayed()
    assert not page.category_exists(ghost_name), (
        "Expected ghost name '%s' not to exist after cancelling edit" % ghost_name
    )
    assert page_has_no_broken_state(page)
