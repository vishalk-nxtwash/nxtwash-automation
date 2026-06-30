import allure
import pytest

from tests.admin_portal.sites.conftest import open_create_site_page
from tests.admin_portal.sites.conftest import page_has_no_broken_state
from tests.admin_portal.sites.conftest import site_data_for_number


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Sites / Locations"),
    allure.story("Validation"),
]


@allure.title("SL-VAL-001 Blank required fields block save and page stays on create form")
@pytest.mark.smoke
def test_create_site_validation_blocks_empty_required_fields(
    logged_in_admin_browser
):
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.click_save_new()

    assert "create" in logged_in_admin_browser.current_url
    assert page_has_no_broken_state(create_page)
    assert "New" in create_page.get_body_text()


@allure.title("SL-VAL-011 Invalid email format blocks save")
@pytest.mark.edge
@pytest.mark.xfail(
    reason=(
        "Framework blocker: the pay-week React-select option is unstable in "
        "this validation path, so the test does not consistently reach email "
        "validation."
    ),
    strict=False,
)
@pytest.mark.parametrize("email", ["abc", "abc@", "abc@yopmail"])
def test_create_site_validation_invalid_email_formats(
    logged_in_admin_browser,
    email
):
    site_data = site_data_for_number(98)
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.fill_general_settings(**site_data)
    create_page.enter_email(email)
    create_page.click_save_new()

    assert "create" in logged_in_admin_browser.current_url


@allure.title("SL-VAL-012/013 Invalid tax values (negative, alpha, above 100%) block save")
@pytest.mark.edge
@pytest.mark.parametrize("tax_field,value", [
    ("state_sales_tax", "-1"),
    ("city_sales_tax", "-1"),
    ("state_sales_tax", "abc"),
    ("city_sales_tax", "abc"),
    ("state_sales_tax", "101"),
    ("city_sales_tax", "101"),
])
def test_create_site_validation_invalid_tax_values(
    logged_in_admin_browser,
    tax_field,
    value
):
    site_data = site_data_for_number(97)
    site_data[tax_field] = value
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.fill_general_settings(**site_data)
    create_page.click_save_new()

    assert "create" in logged_in_admin_browser.current_url
