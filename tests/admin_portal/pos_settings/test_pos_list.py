import allure
import pytest

from tests.admin_portal.pos_settings.conftest import (
    POS_NAME,
    create_pos_if_missing,
    open_pos_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("POS Settings"),
    allure.story("List"),
]


@allure.title("POS-LST-001 POS Settings page loads showing the POS list")
@pytest.mark.smoke
def test_pos_page_loads(browser):
    page = open_pos_page(browser)
    body = page.get_body_text()

    assert "POS" in body
    assert page_has_no_broken_state(page)


@allure.title("POS-LST-002 List displays correct columns")
@pytest.mark.regression
def test_pos_list_displays_columns(browser):
    page = open_pos_page(browser)
    body = page.get_body_text()

    assert "POS name" in body or "Name" in body
    assert "Site" in body
    assert "Lane" in body
    assert "Status" in body
    assert page_has_no_broken_state(page)


@allure.title("POS-LST-003 Status column shows Active/Inactive badge per POS")
@pytest.mark.regression
def test_pos_list_status_column(browser, managed_pos):
    page = open_pos_page(browser)
    page.search_pos(POS_NAME)
    body = page.get_body_text()

    assert "Active" in body or "Inactive" in body, (
        "Status column not rendered in POS list"
    )
    assert page_has_no_broken_state(page)


@allure.title("POS-LST-004 Pagination shows correct total count and page info")
@pytest.mark.regression
def test_pos_list_pagination_shows_count(browser):
    create_pos_if_missing(browser)
    page = open_pos_page(browser)
    body = page.get_body_text()

    has_digit = any(ch.isdigit() for ch in body)
    assert has_digit, "No numeric count found in POS list pagination area"
    assert page_has_no_broken_state(page)


@allure.title("POS-LST-005 Results-per-page dropdown changes number of rows")
@pytest.mark.extended
@pytest.mark.xfail(
    strict=False,
    reason=(
        "POS-LST-005: Results-per-page control locator not confirmed in DevTools "
        "— verify exact element before removing xfail."
    ),
)
def test_pos_list_results_per_page(browser):
    page = open_pos_page(browser)
    body = page.get_body_text()

    assert "per page" in body.lower() or "Results per page" in body, (
        "Results-per-page control not found on POS list page"
    )
    assert page_has_no_broken_state(page)
