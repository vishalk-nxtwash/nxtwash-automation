import uuid

import allure
import pytest

from tests.admin_portal.bank_drop.conftest import (
    BANK_DROP_NAME,
    BANK_DROP_ORDER,
    EDIT_BANK_DROP_NAME,
    EDIT_BANK_DROP_UPDATED_NAME,
    SECOND_BANK_DROP_NAME,
    SECOND_BANK_DROP_ORDER,
    VISIBLE_BANK_DROP_ORDER,
    create_bank_drop_if_missing,
    managed_bank_drop,
    managed_edit_bank_drop,
    open_bank_drop_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Bank Drop"),
    allure.story("Edit"),
]


@allure.title("BD-EDT-001 Edit bank drop name persists after save")
@pytest.mark.regression
def test_edit_bank_drop_name_persists(managed_edit_bank_drop, browser):

    page = managed_edit_bank_drop
    page.open_edit(EDIT_BANK_DROP_NAME)
    page.enter_name(EDIT_BANK_DROP_UPDATED_NAME)
    page.click_save()
    page.wait_for_list_loaded()  # confirm save committed before fresh navigation
    page = open_bank_drop_page(browser)

    assert page.wait_for_bank_drop_row(EDIT_BANK_DROP_UPDATED_NAME).is_displayed()


@allure.title("BD-EDT-002 Edit order value persists after save")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "BD-EDT-002: parallel worker race — managed_bank_drop restore on another gw "
        "reverts order to the original value between save and re-read under -n 3. "
        "Fix: per-worker bank-drop isolation."
    ),
)
def test_edit_bank_drop_order_persists(managed_bank_drop):

    new_order = "5"
    page = managed_bank_drop
    page.open_edit(BANK_DROP_NAME)
    page.enter_order(new_order)
    page.click_save()
    page.wait_for_list_loaded()

    page.open_edit(BANK_DROP_NAME)
    assert page.get_order_value() == new_order
    assert page_has_no_broken_state(page)


@allure.title("BD-EDT-003 Activate an inactive bank drop updates its status to Active")
@pytest.mark.smoke
def test_activate_inactive_bank_drop(browser, request):

    inactive_name = "VK act-%s" % uuid.uuid4().hex[:6]

    def _teardown():
        try:
            open_bank_drop_page(browser).deactivate_bank_drop(inactive_name)
        except Exception:  # noqa: BLE001
            pass  # best-effort; item may not be visible if staging has >100 records

    request.addfinalizer(_teardown)

    page = open_bank_drop_page(browser)
    page.open_create()
    page.enter_name(inactive_name)
    page.enter_order("97")
    page.ensure_active_off()
    page.click_save()
    page.wait_for_list_loaded()

    page.open_edit(inactive_name)
    page.ensure_active_on()
    page.click_save()
    page.wait_for_list_loaded()

    assert page.wait_for_bank_drop_row(inactive_name).is_displayed()
    assert page.get_bank_drop_status(inactive_name) == "Active"


@allure.title("BD-EDT-004 Deactivate an active bank drop hides it from the default list")
@pytest.mark.regression
def test_deactivate_active_bank_drop(browser):

    temp_name = "VK deact-%s" % uuid.uuid4().hex[:6]
    page = open_bank_drop_page(browser)
    page.create_bank_drop(temp_name, "96")

    page.open_edit(temp_name)
    page.ensure_active_off()
    page.click_save()
    page.wait_for_list_loaded()

    assert temp_name not in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("BD-EDT-005 Edit form pre-populates existing name and order values")
@pytest.mark.regression
def test_edit_form_prepopulates_existing_values(browser):

    create_bank_drop_if_missing(browser)
    page = open_bank_drop_page(browser)
    page.open_edit(BANK_DROP_NAME)

    assert page.get_name_value() == BANK_DROP_NAME
    assert page.get_order_value() == BANK_DROP_ORDER
    assert page.active_bank_drop_is_on()
    assert page_has_no_broken_state(page)


@allure.title("BD-EDT-006 Cancel out of edit form discards changes")
@pytest.mark.regression
def test_cancel_out_of_edit_form(browser):

    create_bank_drop_if_missing(browser)
    page = open_bank_drop_page(browser)
    page.open_edit(BANK_DROP_NAME)
    page.enter_name("VK should-not-save")
    page.click_cancel()
    page.wait_for_list_loaded()

    assert page.wait_for_bank_drop_row(BANK_DROP_NAME).is_displayed()
    assert "VK should-not-save" not in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("BD-PER-002 Edited bank drop changes persist after page reload")
@pytest.mark.regression
def test_edited_bank_drop_persists_after_reload(managed_bank_drop):

    new_order = "4"
    page = managed_bank_drop
    page.open_edit(BANK_DROP_NAME)
    page.enter_order(new_order)
    page.click_save()
    page.wait_for_list_loaded()

    page = open_bank_drop_page(managed_bank_drop.driver)
    page.open_edit(BANK_DROP_NAME)
    assert page.get_order_value() == new_order
    assert page_has_no_broken_state(page)


@allure.title("BD-ORD-001 Bank drop list is sorted by order value ascending")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Manual: the admin list sorts by creation time, not order value; "
        "the order field controls display sequence on the customer portal, not admin list order."
    )
)
def test_bank_drop_list_sorted_by_order(browser):

    create_bank_drop_if_missing(browser, BANK_DROP_NAME, BANK_DROP_ORDER)
    create_bank_drop_if_missing(browser, SECOND_BANK_DROP_NAME, SECOND_BANK_DROP_ORDER)
    page = open_bank_drop_page(browser)
    orders = page.get_visible_row_orders()

    assert len(orders) >= 2
    assert orders == sorted(orders), "Grid rows are not sorted by order value"
    assert page_has_no_broken_state(page)
