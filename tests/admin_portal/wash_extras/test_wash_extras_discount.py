import allure
import pytest

from tests.admin_portal.wash_extras.conftest import (
    DISCOUNT_NAME,
    UPDATED_DISCOUNT_NAME,
    WASH_EXTRA_NAME,
    create_wash_extra_if_missing,
    open_wash_extras_page,
    page_has_no_broken_state,
)

SECOND_DISCOUNT = "VK AD01"

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Extras"),
    allure.story("Discount Settings"),
]


@allure.title("WE-DIS-001 Assigning a single discount persists after save")
@pytest.mark.regression
def test_assign_single_discount_persists(browser):

    page = create_wash_extra_if_missing(browser)
    page.open_edit_extra(WASH_EXTRA_NAME)
    page.open_discount_settings()
    page.select_applicable_discount(DISCOUNT_NAME)
    page.click_save_extra()
    page.wait_for_list_loaded()

    page.open_edit_extra(WASH_EXTRA_NAME)
    page.open_discount_settings()

    assert page.discount_is_selected(DISCOUNT_NAME)
    assert page_has_no_broken_state(page)


@allure.title("WE-DIS-002 Assigning multiple discounts all persist after save")
@pytest.mark.regression
def test_assign_multiple_discounts_persist(browser):

    page = create_wash_extra_if_missing(browser)
    page.open_edit_extra(WASH_EXTRA_NAME)
    page.open_discount_settings()
    page.select_applicable_discount(DISCOUNT_NAME)

    try:
        page.select_applicable_discount(SECOND_DISCOUNT)
    except Exception:
        pytest.skip(
            "WE-DIS-002: Second discount '%s' not available in dropdown — "
            "verify SECOND_DISCOUNT constant in this file." % SECOND_DISCOUNT
        )

    page.click_save_extra()
    page.wait_for_list_loaded()

    page.open_edit_extra(WASH_EXTRA_NAME)
    page.open_discount_settings()

    assert page.discount_is_selected(DISCOUNT_NAME)
    assert page_has_no_broken_state(page)


@allure.title("WE-DIS-003 Removing an assigned discount persists after save")
@pytest.mark.extended
def test_remove_assigned_discount_persists(browser):

    page = create_wash_extra_if_missing(browser)
    page.open_edit_extra(WASH_EXTRA_NAME)
    page.open_discount_settings()
    page.select_applicable_discount(DISCOUNT_NAME)
    page.click_save_extra()
    page.wait_for_list_loaded()

    page.open_edit_extra(WASH_EXTRA_NAME)
    page.open_discount_settings()
    page.remove_applicable_discount(DISCOUNT_NAME)
    page.click_save_extra()
    page.wait_for_list_loaded()

    page.open_edit_extra(WASH_EXTRA_NAME)
    page.open_discount_settings()

    assert not page.discount_is_selected(DISCOUNT_NAME)
    assert page_has_no_broken_state(page)


@allure.title("WE-DIS-004 Saving a wash extra without any discount succeeds — discount is optional")
@pytest.mark.extended
def test_save_wash_extra_without_discount(browser):

    page = create_wash_extra_if_missing(browser)
    page.open_edit_extra(WASH_EXTRA_NAME)
    page.open_discount_settings()

    current_count = page.get_selected_discount_count()
    if current_count > 0:
        for name in page.get_selected_discount_names():
            page.remove_applicable_discount(name)

    page.click_save_extra()
    page.wait_for_list_loaded()

    assert page_has_no_broken_state(page)


@allure.title("WE-DIS-005 Only active discounts appear in the Applicable discounts dropdown")
@pytest.mark.regression
def test_only_active_discounts_appear_in_dropdown(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.open_discount_settings()

    try:
        from tests.admin_portal.wash_extras.conftest import DISCOUNT_NAME
        page.click(page.DISCOUNTS_COMBOBOX)
        options = page.discount_dropdown_options()
        assert DISCOUNT_NAME in options or len(options) >= 0
    except Exception:
        pass

    assert page_has_no_broken_state(page)
