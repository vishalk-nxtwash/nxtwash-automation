import allure
import pytest

from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal.discounts.conftest import DISCOUNT_NAME
from tests.admin_portal.discounts.conftest import MANAGED_DISCOUNT
from tests.admin_portal.discounts.conftest import create_discount_if_missing
from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Persistence"),
]


@allure.title("DS-PER-002 Created discount persists after re-login")
@pytest.mark.regression
def test_discount_persists_after_relogin(browser):

    create_discount_if_missing(browser)

    browser.execute_script("window.localStorage.clear();")
    discounts_page = open_discounts_page(browser)
    discounts_page.search_discount(DISCOUNT_NAME)

    assert discounts_page.wait_for_discount_row(DISCOUNT_NAME).is_displayed()
    assert page_has_no_broken_state(discounts_page)


@allure.title("DS-PER-003 Edited discount persists after page refresh")
@pytest.mark.regression
def test_discount_edit_persists_after_refresh(managed_discount):

    page = managed_discount
    new_amount = "7"

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.set_discount_amount(new_amount)
    page.click_save_discount()
    page.wait_for_list_loaded()

    open_admin_path(page.driver, "/services/discounts")
    page.wait_for_list_loaded()
    page.open_edit_discount(MANAGED_DISCOUNT)

    assert page.get_discount_amount_value() == new_amount
    assert page_has_no_broken_state(page)


@allure.title("DS-PER-004 Deactivated discount persists after page refresh")
@pytest.mark.regression
def test_discount_deactivation_persists_after_refresh(managed_discount):

    page = managed_discount

    page.open_edit_discount(MANAGED_DISCOUNT)
    page.ensure_active_switch_off()
    page.click_save_discount()
    page.wait_for_list_loaded()

    open_admin_path(page.driver, "/services/discounts")
    page.wait_for_list_loaded()
    page.search_discount(MANAGED_DISCOUNT)

    assert page.get_discount_status(MANAGED_DISCOUNT) == "Inactive"
    assert page_has_no_broken_state(page)
