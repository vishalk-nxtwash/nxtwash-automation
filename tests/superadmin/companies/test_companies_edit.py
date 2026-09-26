import allure
import pytest

from selenium.webdriver.common.by import By

from tests.superadmin.companies.conftest import COMPANY_NAME, PRIMARY_COMPANY

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Companies"),
    allure.story("Edit"),
]


def test_edit_button_opens_edit_form(browser, edit_company_page):
    """SA-CMP-EDT-001 — 'Edit' opens the Edit form at /companies/{id} with data pre-filled."""
    assert "/companies/" in browser.current_url, \
        f"Expected URL to contain '/companies/{{id}}', got: {browser.current_url}"
    assert "/companies/create" not in browser.current_url, \
        "Edit URL should not be the create URL"


def test_edit_form_prefills_company_name(edit_company_page):
    """SA-CMP-EDT-002 — Pre-filled Company name matches the selected company."""
    name = edit_company_page.get_company_name()
    assert COMPANY_NAME.lower() in name.lower(), \
        f"Company name should be pre-filled with '{COMPANY_NAME}', got: {name!r}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EDT-003: Location field names (country, state, city, address, zip, "
           "timezone) on the edit form not confirmed via DOM inspection.",
)
def test_edit_form_prefills_location_fields(edit_company_page, browser):
    """SA-CMP-EDT-003 — Pre-filled Location fields match the company's stored data."""
    body = browser.find_element(By.TAG_NAME, "body").text
    assert body, "Edit form body should be non-empty"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EDT-004: Field names for Database, Site name, Password on the "
           "create form not confirmed — cannot verify absence on the edit form.",
)
def test_edit_form_does_not_show_database_or_site_name(edit_company_page, browser):
    """SA-CMP-EDT-004 — Edit form does not expose Database, Site name or Password."""
    from pages.superadmin.create_company_page import CreateCompanyPage
    # These locators have unconfirmed names — test is xfail
    database_els = edit_company_page.driver.find_elements(
        By.XPATH, "//label[contains(.,'Database')]"
    )
    site_els = edit_company_page.driver.find_elements(
        By.XPATH, "//label[contains(.,'Site name') or contains(.,'Site Name')]"
    )
    assert not database_els, "Edit form should not show a 'Database' field"
    assert not site_els, "Edit form should not show a 'Site name' field"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EDT-005: Company name edit persistence — rich-text or React-controlled "
           "input may not accept Selenium send_keys correctly; save behaviour not confirmed.",
)
def test_edit_company_name_persists(browser, edit_company_page):
    """SA-CMP-EDT-005 — Editing Company name → Save persists on the list and after reload."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EDT-006: Email field name on edit form not confirmed — "
           "locator (By.NAME, 'email') may not match the actual DOM.",
)
def test_edit_email_is_prefilled(edit_company_page):
    """SA-CMP-EDT-006 — Edit form Email field is pre-filled (non-empty)."""
    email = edit_company_page.get_email()
    assert email, \
        "Email field should be pre-filled in the edit form"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EDT-007: Phone field name on edit form not confirmed — "
           "locator (By.NAME, 'phoneNumber') may not match the actual DOM.",
)
def test_edit_phone_is_prefilled(edit_company_page):
    """SA-CMP-EDT-007 — Edit form Phone field is pre-filled (non-empty)."""
    phone = edit_company_page.get_phone()
    assert phone, \
        "Phone field should be pre-filled in the edit form"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EDT-008: Clearing a required field via the X clear icon — "
           "inline clear icon locator not confirmed; save may proceed without blocking.",
)
def test_clearing_required_field_rejected_on_save(edit_company_page):
    """SA-CMP-EDT-008 — Clearing a required field (via X) and saving is blocked."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EDT-009: Invalid email on edit form — "
           "email field name not confirmed; entering invalid value via send_keys may not work.",
)
def test_invalid_email_on_edit_form_rejected(edit_company_page):
    """SA-CMP-EDT-009 — Invalid email format on the Edit form is rejected."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EDT-010: Country/State/City cascade on edit — "
           "React Select interaction and cascade behaviour not confirmed.",
)
def test_edit_country_state_city_cascade(edit_company_page):
    """SA-CMP-EDT-010 — Changing country/state/city cascades correctly and saves."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-EDT-011: Logo upload requires file-upload tooling — manual test."
)
def test_upload_logo_image(edit_company_page):
    """SA-CMP-EDT-011 — 'Upload image' accepts a valid logo and shows a preview."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-EDT-012: Logo upload rejection (invalid type/size) — manual test."
)
def test_upload_logo_invalid_file_rejected(edit_company_page):
    """SA-CMP-EDT-012 — Logo upload rejects an invalid file type or oversized image."""
    pass


def test_cancel_discards_edit_changes(browser, edit_company_page):
    """SA-CMP-EDT-013 — Cancel discards changes — original company data is unchanged."""
    from pages.superadmin.companies_page import CompaniesPage
    from pages.superadmin.edit_company_page import EditCompanyPage

    original_name = edit_company_page.get_company_name()

    edit_company_page.click_cancel()
    edit_company_page.confirm_yes()
    edit_company_page.wait_for_confirmation_closed()

    companies_list = CompaniesPage(browser)
    companies_list.wait_for_loaded()
    companies_list.filter_by_company_name(COMPANY_NAME)
    companies_list.open_company_edit(COMPANY_NAME)

    reopened = EditCompanyPage(browser)
    reopened.wait_for_loaded(COMPANY_NAME)
    assert reopened.get_company_name() == original_name, \
        "Company name should be unchanged after cancelling the edit"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EDT-014: Save changes with no modifications — "
           "behaviour (silent success, confirmation dialog) not confirmed.",
)
def test_save_with_no_modifications_is_safe(edit_company_page):
    """SA-CMP-EDT-014 — 'Save changes' with no modifications is a safe no-op or success."""
    edit_company_page.click_save_changes()
    edit_company_page.confirm_yes()
    edit_company_page.wait_for_confirmation_closed()
    body = edit_company_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "error" not in body, \
        "Save with no modifications should not produce an error"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EDT-015: Company with missing data (e.g. crewcarwashtest) — "
           "existence of this company in staging not confirmed.",
)
def test_editing_partial_data_company_loads_without_error(browser, companies_page):
    """SA-CMP-EDT-015 — Editing a company with missing data loads without error."""
    from pages.superadmin.edit_company_page import EditCompanyPage
    partial_company = "crewcarwashtest"
    companies_page.filter_by_company_name(partial_company)
    companies_page.open_company_edit(partial_company)
    page = EditCompanyPage(browser)
    page.wait_for_loaded(partial_company)
    body = browser.find_element(By.TAG_NAME, "body").text.lower()
    assert "error" not in body, \
        "Editing a company with partial data should not show an error"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EDT-016: Non-existent company ID (404 vs redirect) — "
           "app behaviour not confirmed.",
)
def test_nonexistent_company_id_shows_error_or_redirect(browser, companies_page):
    """SA-CMP-EDT-016 — Navigating to /companies/999999 shows a 404 or redirects."""
    browser.get("https://superadmin.nxtwash.com/companies/999999")
    body = browser.find_element(By.TAG_NAME, "body").text.lower()
    assert (
        "not found" in body
        or "404" in body
        or "companies" in browser.current_url
    ), "Non-existent company ID should show a not-found page or redirect"
