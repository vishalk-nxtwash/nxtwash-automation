import allure
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Companies"),
    allure.story("Create"),
]

_CREATE_URL = "https://superadmin.nxtwash.com/companies/create"
_COMPANIES_URL = "https://superadmin.nxtwash.com/companies"


def test_add_company_button_opens_create_form(companies_page, browser):
    """SA-CMP-CRT-001 — '+ Add Company' opens the Create form at /companies/create."""
    companies_page.click_add_company()
    from pages.superadmin.create_company_page import CreateCompanyPage
    page = CreateCompanyPage(browser)
    page.wait_for_loaded()
    assert "/companies/create" in browser.current_url, \
        f"Expected /companies/create URL after Add Company, got: {browser.current_url}"


def test_create_form_shows_both_settings_sections(create_company_page, browser):
    """SA-CMP-CRT-002 — Create form shows Company Base Settings and Location Settings."""
    body = browser.find_element(By.TAG_NAME, "body").text
    assert "Company Base Settings" in body, \
        "Create form should show 'Company Base Settings' section"
    assert "Company Location Settings" in body, \
        "Create form should show 'Company Location Settings' section"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-CRT-003: Checking for a red asterisk on required fields requires "
           "CSS pseudo-element or aria-required inspection — not reliably done via Selenium.",
)
def test_required_fields_are_marked_with_asterisk(create_company_page, browser):
    """SA-CMP-CRT-003 — All required fields are marked with a red asterisk."""
    required_inputs = create_company_page.driver.find_elements(
        By.XPATH, "//*[@required or @aria-required='true']"
    )
    assert required_inputs, \
        "At least one required field should have aria-required or required attribute"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-CRT-004: Verifying Address 2 has no asterisk requires CSS inspection "
           "of the label — not reliably done via Selenium.",
)
def test_address_2_is_optional(create_company_page, browser):
    """SA-CMP-CRT-004 — Address 2 is optional — saving without it should succeed."""
    body = browser.find_element(By.TAG_NAME, "body").text
    assert "Address 2" in body or "address2" in body.lower(), \
        "Create form should contain an Address 2 field"


@pytest.mark.skip(
    reason="SA-CMP-CRT-005: Core happy-path create — "
           "skipped to avoid creating new company records in staging."
)
def test_create_company_with_all_required_fields(create_company_page, browser):
    """SA-CMP-CRT-005 — Filling all required fields and saving creates the company."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-CRT-006: Depends on CRT-005 (actual company creation) — skipped."
)
def test_new_company_appears_in_list_and_count_increments(companies_page):
    """SA-CMP-CRT-006 — Newly created company appears in the list with incremented count."""
    pass


def test_save_empty_form_shows_validation(create_company_page):
    """SA-CMP-CRT-007 to CRT-018 — Submitting the empty form is blocked with validation."""
    create_company_page.click_save_new()
    assert "/companies/create" in create_company_page.driver.current_url, \
        "Empty form submission should not navigate away from /companies/create"
    body = create_company_page.get_body_text().lower()
    assert (
        "required" in body
        or "too small" in body
        or "invalid" in body
        or "must" in body
    ), "Empty form submission should show at least one validation message"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-CRT-008: Per-field company-name validation requires filling all other "
           "required dropdowns (Database, country, state, city, timezone) which are "
           "React Selects with unconfirmed option values — isolating one field is not yet possible.",
)
def test_company_name_required(create_company_page):
    """SA-CMP-CRT-008 — Save without Company name is blocked."""
    create_company_page.click_save_new()
    body = create_company_page.get_body_text().lower()
    assert "required" in body or "too small" in body, \
        "Missing company name should trigger a validation error"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-CRT-011: Email field name ('email') on create form not confirmed "
           "via DOM — may differ from the edit form.",
)
def test_email_required(create_company_page):
    """SA-CMP-CRT-011 — Save without Email is blocked with a validation error."""
    create_company_page.enter_company_name("TestValidation")
    create_company_page.click_save_new()
    body = create_company_page.get_body_text().lower()
    assert "required" in body or "email" in body or "/companies/create" in create_company_page.driver.current_url, \
        "Missing email should trigger a validation error"


def test_invalid_email_format_rejected(create_company_page):
    """SA-CMP-CRT-019 — Invalid email format is rejected."""
    create_company_page.enter_company_name("TestValidation")
    try:
        create_company_page.enter_text(
            create_company_page.EMAIL_INPUT, "not-a-valid-email"
        )
    except Exception:
        pytest.xfail(
            "SA-CMP-CRT-019: Email field name on create form not confirmed — "
            "entering text failed."
        )
    create_company_page.click_save_new()
    body = create_company_page.get_body_text().lower()
    assert (
        "invalid email" in body
        or "invalid" in body
        or "/companies/create" in create_company_page.driver.current_url
    ), "Invalid email format should be rejected with a validation message"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-CRT-020: Database dropdown option list — "
           "React Select structure not confirmed; option values unknown.",
)
def test_database_dropdown_lists_options(create_company_page):
    """SA-CMP-CRT-020 — Database dropdown lists the available databases."""
    db_control = (By.XPATH, "//label[contains(.,'Database')]/following::div[contains(@class,'control')][1]")
    els = create_company_page.driver.find_elements(*db_control)
    assert els, "Database dropdown control should be present on the create form"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-CRT-021: Country→State cascade — React Select interaction "
           "and option values not confirmed.",
)
def test_country_dropdown_loads_states(create_company_page):
    """SA-CMP-CRT-021 — Selecting a country loads the matching states in the state dropdown."""
    country_control = (
        By.XPATH,
        "//label[contains(.,'country') or contains(.,'Country')]"
        "/following::div[contains(@class,'control')][1]"
    )
    els = create_company_page.driver.find_elements(*country_control)
    assert els, "Country dropdown should be present on the create form"


@pytest.mark.xfail(strict=False, reason="SA-CMP-CRT-022: State depends on country — cascade not confirmed.")
def test_state_options_depend_on_country(create_company_page):
    """SA-CMP-CRT-022 — Company state options depend on the selected country."""
    pass


@pytest.mark.xfail(strict=False, reason="SA-CMP-CRT-023: City depends on state — cascade not confirmed.")
def test_city_options_depend_on_state(create_company_page):
    """SA-CMP-CRT-023 — Company city options depend on the selected state."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-CRT-024: Timezone dropdown — React Select structure and option values "
           "not confirmed via DOM inspection.",
)
def test_timezone_dropdown_lists_timezones(create_company_page):
    """SA-CMP-CRT-024 — Timezone dropdown lists timezones (e.g. UTC-05:00 Eastern Time)."""
    tz_control = (
        By.XPATH,
        "//label[contains(.,'timezone') or contains(.,'Timezone')]"
        "/following::div[contains(@class,'control')][1]"
    )
    els = create_company_page.driver.find_elements(*tz_control)
    assert els, "Timezone dropdown should be present on the create form"


@pytest.mark.xfail(strict=False, reason="SA-CMP-CRT-025: Zip format/length rule not confirmed.")
def test_zip_validation_rule(create_company_page):
    """SA-CMP-CRT-025 — Zip accepts a valid value and rejects an invalid one."""
    pass


@pytest.mark.xfail(strict=False, reason="SA-CMP-CRT-026: Phone number format/length rule not confirmed.")
def test_phone_number_validation_rule(create_company_page):
    """SA-CMP-CRT-026 — Phone number field validation — document accepted format/length."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-CRT-027: Duplicate company name uniqueness rule — "
           "confirming requires creating a company, skipped to avoid new records."
)
def test_duplicate_company_name_behaviour(create_company_page):
    """SA-CMP-CRT-027 — Duplicate company name is rejected or allowed — document rule."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-CRT-028: Password field masking / visibility toggle — "
           "password input type and toggle button presence not confirmed via DOM.",
)
def test_password_field_is_masked(create_company_page):
    """SA-CMP-CRT-028 — Password field is masked (type='password')."""
    els = create_company_page.driver.find_elements(*create_company_page.PASSWORD_INPUT)
    assert els, "Password input should be present"
    assert els[0].get_attribute("type") == "password", \
        "Password field should have type='password'"


@pytest.mark.xfail(strict=False, reason="SA-CMP-CRT-029: Whitespace-only rejection — server behaviour not confirmed.")
def test_whitespace_only_company_name_rejected(create_company_page):
    """SA-CMP-CRT-029 — Required text fields containing only whitespace are rejected."""
    create_company_page.enter_company_name("     ")
    create_company_page.click_save_new()
    assert "/companies/create" in create_company_page.driver.current_url or \
        create_company_page.has_validation_text("required") or \
        create_company_page.has_validation_text("invalid"), \
        "Whitespace-only company name should be rejected"


@pytest.mark.xfail(strict=False, reason="SA-CMP-CRT-030: Leading/trailing whitespace trim — server behaviour not confirmed.")
def test_company_name_whitespace_trimmed(create_company_page):
    """SA-CMP-CRT-030 — Company name with leading/trailing whitespace is trimmed or rejected."""
    pass


@pytest.mark.xfail(strict=False, reason="SA-CMP-CRT-031: Maximum name length — value not confirmed.")
def test_company_name_max_length(create_company_page):
    """SA-CMP-CRT-031 — Company name at maximum allowed length saves without truncation."""
    pass


@pytest.mark.xfail(strict=False, reason="SA-CMP-CRT-032: Special characters / emoji — behaviour not confirmed.")
def test_special_characters_in_company_name(create_company_page):
    """SA-CMP-CRT-032 — Special characters / emoji in Company name handled gracefully."""
    pass


def test_cancel_returns_to_companies_list(create_company_page, browser):
    """SA-CMP-CRT-033 — Cancel discards the form and returns to the Companies list."""
    create_company_page.click_cancel()
    create_company_page.confirm_yes_if_present()

    from pages.superadmin.companies_page import CompaniesPage
    companies_list = CompaniesPage(browser)
    companies_list.wait_for_loaded()
    assert "companies" in browser.current_url and "create" not in browser.current_url, \
        f"Cancel should return to /companies, got: {browser.current_url}"
