import allure
import pytest

from tests.admin_portal.sites.conftest import PAY_WEEK_START_DAY
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


@allure.title("SL-VAL-002 Filling basic info only without address section blocks save")
@pytest.mark.edge
def test_create_site_missing_address_blocks_save(logged_in_admin_browser):
    site_data = site_data_for_number(92)
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.enter_basic_information(
        site_data["site_name"], site_data["site_code"], site_data["email"]
    )
    create_page.select_pay_week_start_day(PAY_WEEK_START_DAY)
    create_page.enter_tax_settings(site_data["state_sales_tax"], site_data["city_sales_tax"])
    create_page.enter_site_contact_email(site_data["site_contact_email"])
    create_page.click_save_new()

    assert "create" in logged_in_admin_browser.current_url
    assert page_has_no_broken_state(create_page)


@allure.title("SL-VAL-003 Blank site name with otherwise complete form blocks save")
@pytest.mark.edge
def test_create_site_blank_name_with_complete_form_blocks_save(logged_in_admin_browser):
    site_data = site_data_for_number(91)
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.fill_general_settings(
        site_name="",
        site_code=site_data["site_code"],
        email=site_data["email"],
        street_address=site_data["street_address"],
        zip_code=site_data["zip_code"],
        state=site_data["state"],
        city=site_data["city"],
        time_zone=site_data["time_zone"],
        state_sales_tax=site_data["state_sales_tax"],
        city_sales_tax=site_data["city_sales_tax"],
        site_contact_email=site_data["site_contact_email"],
        pay_week_start_day=site_data["pay_week_start_day"],
    )
    create_page.click_save_new()

    assert "create" in logged_in_admin_browser.current_url
    assert page_has_no_broken_state(create_page)


@allure.title("SL-VAL-009 Special characters in site name do not crash the create form")
@pytest.mark.edge
def test_create_site_special_chars_in_name_do_not_break_form(logged_in_admin_browser):
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.enter_basic_information(
        "VK SPEC &<>\"'%", "SPEC01", "spec01@yopmail.com"
    )

    assert page_has_no_broken_state(create_page)


@allure.title("SL-VAL-010 Very long site name (200+ chars) does not crash the create form")
@pytest.mark.edge
def test_create_site_very_long_name_does_not_crash_form(logged_in_admin_browser):
    long_name = "VK LONG " + ("X" * 200)
    create_page = open_create_site_page(logged_in_admin_browser)
    create_page.enter_basic_information(long_name, "LONG01", "long01@yopmail.com")

    assert page_has_no_broken_state(create_page)
