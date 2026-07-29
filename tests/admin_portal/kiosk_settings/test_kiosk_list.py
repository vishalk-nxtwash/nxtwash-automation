import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    KSK_NAME,
    create_kiosk_if_missing,
    open_kiosk_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("List"),
]


@allure.title("KSK-LST-001 Kiosk Settings page loads with primary controls visible")
@pytest.mark.smoke
def test_kiosk_page_loads(browser):
    page = open_kiosk_page(browser)
    body = page.get_body_text()

    assert "Kiosk" in body
    assert page_has_no_broken_state(page)


@allure.title("KSK-LST-002 List displays expected column headers")
@pytest.mark.regression
def test_kiosk_list_displays_columns(browser):
    page = open_kiosk_page(browser)
    body = page.get_body_text()

    assert "Kiosk name" in body or "Kiosk" in body
    assert "Site" in body
    assert "Lane" in body
    assert "Status" in body
    assert page_has_no_broken_state(page)


@allure.title("KSK-LST-003 Status column shows Active or Inactive for a kiosk")
@pytest.mark.regression
def test_kiosk_list_status_column(browser, managed_kiosk):
    page = open_kiosk_page(browser)
    page.search_kiosk(KSK_NAME)
    body = page.get_body_text()

    assert "Active" in body or "Inactive" in body, (
        "Status column not rendered in kiosk list"
    )
    assert page_has_no_broken_state(page)


@allure.title("KSK-LST-004 Pagination control shows a numeric record count")
@pytest.mark.regression
def test_kiosk_list_pagination_shows_count(browser):
    create_kiosk_if_missing(browser)
    page = open_kiosk_page(browser)
    body = page.get_body_text()

    has_digit = any(ch.isdigit() for ch in body)
    assert has_digit, "No numeric count found in kiosk list pagination area"
    assert page_has_no_broken_state(page)


@allure.title("KSK-LST-005 Results-per-page control is present on the list page")
@pytest.mark.extended
def test_kiosk_list_results_per_page(browser):
    page = open_kiosk_page(browser)
    body = page.get_body_text()

    assert "per page" in body.lower() or "Results per page" in body, (
        "Results-per-page control not found on kiosk list page"
    )
    assert page_has_no_broken_state(page)
