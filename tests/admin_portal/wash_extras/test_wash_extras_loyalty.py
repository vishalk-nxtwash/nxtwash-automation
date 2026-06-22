import allure
import pytest

from tests.admin_portal.wash_extras.conftest import GLOBAL_PRICE
from tests.admin_portal.wash_extras.conftest import open_wash_extras_page
from tests.admin_portal.wash_extras.conftest import page_has_no_broken_state


_LOYALTY_SKIP = (
    "Requires Loyalty module integration to verify points are awarded/redeemed. Deferred."
)

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Extras"),
    allure.story("Loyalty Settings"),
]


@allure.title("WE-LTY-001 Valid points awarded saves correctly (deferred: end-to-end verification)")
@pytest.mark.extended
@pytest.mark.skip(reason=_LOYALTY_SKIP)
def test_valid_points_awarded_saves(browser):
    pass


@allure.title("WE-LTY-002 Valid points to redeem saves correctly (deferred: end-to-end verification)")
@pytest.mark.extended
@pytest.mark.skip(reason=_LOYALTY_SKIP)
def test_valid_points_to_redeem_saves(browser):
    pass


@allure.title("WE-LTY-003 Entering 0 for Points awarded is accepted as a valid value")
@pytest.mark.extended
def test_zero_points_awarded_accepted(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK EWA2-zero-pts-awarded-test")
    page.set_points_awarded("0")

    assert page.get_points_awarded_value() == "0"
    assert page_has_no_broken_state(page)


@allure.title("WE-LTY-004 Negative loyalty points is rejected on save")
@pytest.mark.extended
def test_negative_loyalty_points_rejected(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK EWA2-neg-pts-test")
    page.set_points_awarded("-1")

    assert page_has_no_broken_state(page)


@allure.title("WE-LTY-005 Saving without loyalty points succeeds — fields are optional")
@pytest.mark.extended
def test_save_without_loyalty_points(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK EWA2-no-pts-test")
    page.set_global_price(GLOBAL_PRICE)

    assert page_has_no_broken_state(page)


@allure.title("WE-LTY-006 Info tooltip icon is visible next to Points awarded")
@pytest.mark.extended
def test_info_tooltip_visible_for_points_awarded(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    body_text = page.get_body_text()

    assert "Points awarded" in body_text
    assert page_has_no_broken_state(page)


@allure.title("WE-LTY-007 Info tooltip icon is visible next to Points to redeem")
@pytest.mark.extended
def test_info_tooltip_visible_for_points_to_redeem(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    body_text = page.get_body_text()

    assert "Points to redeem" in body_text
    assert page_has_no_broken_state(page)
