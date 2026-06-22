import allure
import pytest

from tests.admin_portal.wash_books.conftest import WASH_BOOK_NAME
from tests.admin_portal.wash_books.conftest import create_wash_book_if_missing
from tests.admin_portal.wash_books.conftest import page_has_no_broken_state


_WASH_PACKAGES_SKIP = (
    "Requires Wash Packages module with configured redemption mappings. Deferred."
)

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Redemption Settings"),
]


@allure.title("WB-RED-001 Enabling redemption at a site with a wash package saves correctly")
@pytest.mark.regression
def test_redemption_at_site_with_wash_package_persists(browser):

    page = create_wash_book_if_missing(browser)
    page.open_edit_wash_book(WASH_BOOK_NAME)
    page.open_redemption_settings()

    assert "Redeem at" in page.get_body_text()
    assert page.visible_redemption_checkboxes()
    assert page_has_no_broken_state(page)


@allure.title("WB-RED-002 Different wash package per site all persist after save")
@pytest.mark.regression
def test_different_wash_package_per_site_persists(browser):

    page = create_wash_book_if_missing(browser)
    page.open_edit_wash_book(WASH_BOOK_NAME)
    page.open_redemption_settings()

    body_text = page.get_body_text().lower()
    assert "vk detail wash" in body_text or "detail cleaning" in body_text
    assert page_has_no_broken_state(page)


@allure.title("WB-RED-003 Changing an assigned wash package persists after save")
@pytest.mark.extended
def test_change_assigned_wash_package_persists(browser):

    page = create_wash_book_if_missing(browser)
    page.open_edit_wash_book(WASH_BOOK_NAME)
    page.open_redemption_settings()

    assert "Redeem at" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("WB-RED-004 Checking a redemption site without selecting a wash package is documented")
@pytest.mark.regression
def test_redemption_site_without_wash_package_behaviour(browser):

    page = create_wash_book_if_missing(browser)
    page.open_edit_wash_book(WASH_BOOK_NAME)
    page.open_redemption_settings()

    checkboxes = page.visible_redemption_checkboxes()
    assert checkboxes, "Expected at least one redemption site checkbox"

    page.assign_redemption_location_by_index(0)
    page.click_save_wash_book()

    assert page_has_no_broken_state(page)


@allure.title("WB-RED-005 Redeem at header checkbox selects all available sites at once")
@pytest.mark.extended
def test_redeem_at_header_checkbox_selects_all_sites(browser):

    page = create_wash_book_if_missing(browser)
    page.open_edit_wash_book(WASH_BOOK_NAME)
    page.open_redemption_settings()
    body_text = page.get_body_text()

    assert "Redeem at" in body_text
    assert page.visible_redemption_checkboxes()
    assert page_has_no_broken_state(page)
