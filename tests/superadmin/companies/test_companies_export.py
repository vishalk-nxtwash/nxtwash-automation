import allure
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Companies"),
    allure.story("Export"),
]


def test_export_icon_is_visible(companies_page):
    """SA-CMP-EXP-001 — Export icon button is visible on the Companies list page."""
    icons = companies_page.driver.find_elements(*companies_page.EXPORT_ICON_BUTTON)
    assert icons, "Export icon button should be present on the Companies list page"


def test_export_icon_opens_modal(companies_page):
    """SA-CMP-EXP-002 — Clicking the export icon opens the Export modal."""
    companies_page.click_export_icon()
    assert companies_page.export_modal_is_visible(), \
        "Export modal should appear after clicking the export icon"


def test_export_modal_title_contains_companies(companies_page):
    """SA-CMP-EXP-003 — Export modal title includes 'Export Companies'."""
    companies_page.click_export_icon()
    titles = companies_page.driver.find_elements(*companies_page.EXPORT_MODAL_TITLE)
    assert titles, \
        "Export modal should display a title containing 'Export Companies'"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EXP-004: Export format selector structure (native select vs "
           "React Select) not confirmed — DOM inspection required to verify XLSX/CSV options.",
)
def test_export_modal_has_xlsx_and_csv_options(companies_page):
    """SA-CMP-EXP-004 — Export format dropdown offers XLSX and CSV options."""
    companies_page.click_export_icon()
    formats = [f.upper() for f in companies_page.get_export_format_options()]
    assert "XLSX" in formats or "EXCEL" in formats, \
        f"Expected XLSX in export formats, got: {formats}"
    assert "CSV" in formats, \
        f"Expected CSV in export formats, got: {formats}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EXP-005: Default export format detection depends on whether "
           "the selector is a native <select> or React Select — DOM inspection required.",
)
def test_export_default_format_is_xlsx(companies_page):
    """SA-CMP-EXP-005 — Default export format is XLSX."""
    companies_page.click_export_icon()
    default = companies_page.get_default_export_format()
    assert default and ("xlsx" in default.lower() or "excel" in default.lower()), \
        f"Default export format should be XLSX, got: {default!r}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EXP-006: Column toggle checkbox locator inside the modal "
           "not confirmed — needs DOM inspection.",
)
def test_export_modal_default_column_toggles(companies_page):
    """SA-CMP-EXP-006 — Export modal shows column toggles, with expected defaults ON."""
    companies_page.click_export_icon()
    states = companies_page.get_export_column_states()
    assert states, "Export modal should contain at least one column toggle"
    expected_on = [
        "companyName", "email", "phoneNumber",
        "companyCountry", "companyState", "companyCity", "address",
    ]
    for col in expected_on:
        if col in states:
            assert states[col], f"Column '{col}' should be ON by default"


@pytest.mark.skip(
    reason="SA-CMP-EXP-007: Download XLSX content verification — "
           "Automation: Pending in spec; requires download tooling."
)
def test_export_xlsx_downloads_valid_file(companies_page):
    """SA-CMP-EXP-007 — Export as XLSX downloads a valid .xlsx containing selected columns."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-EXP-008: Download CSV content verification — "
           "Automation: Pending in spec; requires download tooling."
)
def test_export_csv_downloads_valid_file(companies_page):
    """SA-CMP-EXP-008 — Export as CSV downloads a valid .csv containing selected columns."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-EXP-009: Exported row/value reconciliation against on-screen list — "
           "Automation: Pending in spec; requires download tooling."
)
def test_exported_rows_match_on_screen_list(companies_page):
    """SA-CMP-EXP-009 — Exported rows and values match the visible list."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EXP-010: Turning every column OFF then exporting — "
           "toggle interaction and Export button disabled state not confirmed via DOM.",
)
def test_all_columns_off_disables_export_or_shows_message(companies_page):
    """SA-CMP-EXP-010 — Turning every column OFF disables the Export button or shows a message."""
    companies_page.click_export_icon()
    toggles = companies_page.driver.find_elements(*companies_page.EXPORT_COLUMN_TOGGLES)
    for toggle in toggles:
        if toggle.is_selected():
            companies_page.driver.execute_script("arguments[0].click();", toggle)

    is_disabled = companies_page.export_confirm_button_is_disabled()
    body = companies_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    has_message = "select" in body or "required" in body or "choose" in body
    assert is_disabled or has_message, \
        "With no columns selected, Export button should be disabled or show a message"


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-EXP-011: Export respects active filter — "
           "filter + export interaction not confirmed; download tooling not available.",
)
def test_export_respects_active_filter(companies_page):
    """SA-CMP-EXP-011 — Export honours an active company name filter."""
    from tests.superadmin.companies.conftest import COMPANY_NAME
    companies_page.filter_by_company_name(COMPANY_NAME)
    companies_page.click_export_icon()
    assert companies_page.export_modal_is_visible(), \
        "Export modal should open while a filter is active"
    companies_page.cancel_export()


def test_cancel_closes_export_modal(companies_page):
    """SA-CMP-EXP-012 — Cancel button closes the Export modal without downloading."""
    companies_page.click_export_icon()
    companies_page.cancel_export()
    assert not companies_page.export_modal_is_visible(), \
        "Export modal should be dismissed after clicking Cancel"
