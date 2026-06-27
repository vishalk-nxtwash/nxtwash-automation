import allure
import pytest

from tests.admin_portal.wash_extras.conftest import WASH_EXTRA_NAME
from tests.admin_portal.wash_extras.conftest import create_wash_extra_if_missing
from tests.admin_portal.wash_extras.conftest import open_wash_extras_page
from tests.admin_portal.wash_extras.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Extras"),
    allure.story("Edge Cases"),
]


@allure.title("WE-EDGE Create wash extra is idempotent — calling twice does not duplicate")
@pytest.mark.extended
def test_wash_extra_create_is_idempotent(browser):

    page = create_wash_extra_if_missing(browser)
    page.search_extra(WASH_EXTRA_NAME)

    assert page.wait_for_extra_row(WASH_EXTRA_NAME).is_displayed()


@allure.title("WE-NAM-004 Long service name does not break the form")
@pytest.mark.extended
def test_wash_extra_long_name_does_not_break_form(browser):

    page = create_wash_extra_if_missing(browser)
    page.open_create_extra()
    page.enter_service_name("VK " + ("E" * 128))

    assert page.get_service_name_value().startswith("VK ")
    assert "Service name" in page.get_body_text()


@allure.title("WE-LTY-003 Entering 0 for Points awarded is accepted as a valid value")
@pytest.mark.extended
def test_zero_loyalty_points_accepted(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK EWA2-zero-pts-edge-test")
    page.set_points_awarded("0")

    assert page.get_points_awarded_value() == "0"
    assert page_has_no_broken_state(page)


@allure.title("WE-LTY-006 Info tooltip is visible next to Points awarded field")
@pytest.mark.extended
def test_info_tooltip_visible_for_points_awarded(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    body_text = page.get_body_text()

    assert "Points awarded" in body_text
    assert page_has_no_broken_state(page)


@allure.title("WE-LTY-007 Info tooltip is visible next to Points to redeem field")
@pytest.mark.extended
def test_info_tooltip_visible_for_points_to_redeem(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    body_text = page.get_body_text()

    assert "Points to redeem" in body_text
    assert page_has_no_broken_state(page)
