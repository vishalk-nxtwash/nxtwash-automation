import allure
import pytest

from tests.admin_portal.wash_books.conftest import (
    CWB_WASH_BOOK_NUMBER,
    create_customer_wash_book_if_missing,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Books"),
    allure.story("Customer Wash Books — Create"),
    pytest.mark.xdist_group(name="managed_cwb"),
]


@allure.title("CWB-CRT-001 Valid customer wash book creates and appears in the listing")
@pytest.mark.smoke
def test_create_customer_wash_book(browser):

    page = create_customer_wash_book_if_missing(browser)
    page.search_cwb(CWB_WASH_BOOK_NUMBER)

    assert page.wait_for_cwb_row(CWB_WASH_BOOK_NUMBER).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("CWB-CRT-002 Creating with a site selection persists site association")
@pytest.mark.regression
@pytest.mark.skip(
    reason="CWB-CRT-002: Requires a Select site dropdown that is bound to real site data. "
    "Deferred until site fixtures for CWB form are established."
)
def test_create_cwb_with_site_selection(browser):
    pass


@allure.title("CWB-CRT-005 Creating with a future expiration date persists the date")
@pytest.mark.extended
@pytest.mark.skip(
    reason="CWB-CRT-005: Date-time picker interaction requires additional page object "
    "support. Deferred."
)
def test_create_cwb_with_expiration_date(browser):
    pass


@allure.title("CWB-CRT-007 Customer wash book is created as Active by default")
@pytest.mark.regression
@pytest.mark.skip(reason="needs_inspection: data-props-id='isActive' no longer exists on CWB grid — check Customer Wash Books grid HTML for the Active/status column's new data-props-id value")
def test_create_cwb_is_active_by_default(browser):

    page = create_customer_wash_book_if_missing(browser)
    page.search_cwb(CWB_WASH_BOOK_NUMBER)

    assert page.get_cwb_status(CWB_WASH_BOOK_NUMBER) == "Active"
    assert page_has_no_broken_state(page)
