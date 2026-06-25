import allure
import pytest

from tests.admin_portal.wash_extras.conftest import open_wash_extras_page
from tests.admin_portal.wash_extras.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Extras"),
    allure.story("UI and List"),
]


@allure.title("WE-LST-001 Wash extras page loads with all primary controls")
@pytest.mark.smoke
def test_wash_extras_page_loads_with_primary_controls(browser):

    page = open_wash_extras_page(browser)
    body_text = page.get_body_text()

    assert "Wash extra name" in body_text
    assert "Price" in body_text
    assert "Status" in body_text
    assert "Add new wash extra" in body_text
    assert page_has_no_broken_state(page)


@allure.title("WE-LST-002 Wash extras grid columns — Wash extra name, Price, Status are visible")
@pytest.mark.regression
def test_wash_extras_grid_columns_are_visible(browser):

    page = open_wash_extras_page(browser)
    body_text = page.get_body_text()

    assert "Wash extra name" in body_text
    assert "Price" in body_text
    assert "Status" in body_text


@allure.title("Filter panel shows expected controls")
@pytest.mark.regression
def test_wash_extras_filter_panel_shows_controls(browser):

    page = open_wash_extras_page(browser)
    body_text = page.get_body_text()

    assert "Wash extra name" in body_text
    assert "Status" in body_text
    assert page_has_no_broken_state(page)


@allure.title("Add wash extra form loads with required fields and default active switch")
@pytest.mark.smoke
def test_add_wash_extra_form_loads(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()

    assert "Service name" in page.get_body_text()
    assert "Global price" in page.get_body_text()
    assert page.active_switch_is_on()


@allure.title("WE-EXP-001 Export button is clickable (deferred: content validation)")
@pytest.mark.export
@pytest.mark.xfail(
    reason=(
        "WE-EXP-001: File content validation requires browser download-directory "
        "configuration and CSV/XLS parser utilities. Deferred."
    ),
    strict=False,
)
def test_wash_extras_export_file_validation(browser):

    page = open_wash_extras_page(browser)
    assert page.download_button_is_clickable()
    raise AssertionError("Download file/content validation is not implemented.")
