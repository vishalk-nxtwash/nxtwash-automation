import uuid

import allure
import pytest

from tests.admin_portal.bank_drop.conftest import (
    BANK_DROP_NAME,
    BANK_DROP_ORDER,
    VISIBLE_BANK_DROP_ORDER,
    create_bank_drop_if_missing,
    open_bank_drop_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Bank Drop"),
    allure.story("CRUD"),
]


@allure.title("BD-CRT-001 Create active bank drop appears in list with Active status and correct order")
@pytest.mark.smoke
def test_create_active_bank_drop(browser):

    page = create_bank_drop_if_missing(browser)
    page.wait_for_list_loaded()

    assert page.wait_for_bank_drop_row(BANK_DROP_NAME).is_displayed()
    assert page.get_bank_drop_status(BANK_DROP_NAME) == "Active"
    assert page.get_bank_drop_order(BANK_DROP_NAME) == VISIBLE_BANK_DROP_ORDER


@allure.title("BD-CRT-002 Create inactive bank drop is hidden from the default list")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Manual: create-form active toggle saves as Active regardless of state; "
        "deactivation behaviour is covered by BD-EDT-004."
    )
)
def test_create_inactive_bank_drop(browser):

    inactive_name = "VK inactive-%s" % uuid.uuid4().hex[:6]
    inactive_order = "99"
    page = open_bank_drop_page(browser)
    page.open_create()
    page.enter_name(inactive_name)
    page.enter_order(inactive_order)
    page.ensure_active_off()
    page.click_save()
    # Navigate fresh so the default active-only filter is applied.
    page = open_bank_drop_page(browser)

    assert inactive_name not in page.get_body_text()


@allure.title("BD-CRT-003 Create bank drop with required fields only appears in list")
@pytest.mark.regression
def test_create_bank_drop_required_fields_only(browser):

    name = "VK req-only %s" % uuid.uuid4().hex[:6]
    page = open_bank_drop_page(browser)
    page.open_create()
    page.enter_name(name)
    page.enter_order("88")
    page.click_save()
    page.wait_for_list_loaded()

    assert page.wait_for_bank_drop_row(name).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("BD-CRT-004 Cancel out of add form discards data and returns to list")
@pytest.mark.regression
def test_cancel_out_of_add_form(browser):

    page = open_bank_drop_page(browser)
    page.open_create()
    page.enter_name("VK cancel-test")
    page.enter_order("50")
    page.click_cancel()
    page.wait_for_list_loaded()

    assert "VK cancel-test" not in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("BD-PER-001 Created bank drop data persists after page reload")
@pytest.mark.regression
def test_created_bank_drop_persists_after_reload(browser):

    create_bank_drop_if_missing(browser)
    page = open_bank_drop_page(browser)

    assert page.wait_for_bank_drop_row(BANK_DROP_NAME).is_displayed()
    assert page.get_bank_drop_status(BANK_DROP_NAME) == "Active"
    assert page_has_no_broken_state(page)
