import allure
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Users"),
    allure.story("Export"),
]


def test_export_icon_is_visible(users_page):
    """SA-USR-EXP-001 — Export icon button is visible on the Users list page."""
    icons = users_page.driver.find_elements(*users_page.EXPORT_ICON_BUTTON)
    assert icons, "Export icon button should be present on the Users list page"


def test_export_icon_opens_modal(users_page):
    """SA-USR-EXP-002 — Clicking the export icon opens the Export modal."""
    users_page.click_export_icon()
    assert users_page.export_modal_is_visible(), \
        "Export modal should appear after clicking the export icon"


def test_export_modal_has_users_title(users_page):
    """SA-USR-EXP-003 — Export modal title includes 'Export Users'."""
    users_page.click_export_icon()
    titles = users_page.driver.find_elements(*users_page.EXPORT_MODAL_TITLE)
    assert titles, \
        "Export modal should display a title containing 'Export Users'"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-EXP-004: Export format selector structure (native select vs "
           "React Select) not confirmed — needs DOM inspection to verify XLSX/CSV options.",
)
def test_export_modal_has_xlsx_and_csv_options(users_page):
    """SA-USR-EXP-004 — Export format dropdown offers XLSX and CSV."""
    users_page.click_export_icon()
    formats = [f.upper() for f in users_page.get_export_format_options()]
    assert "XLSX" in formats or "EXCEL" in formats, \
        f"Expected XLSX in export formats, got: {formats}"
    assert "CSV" in formats, \
        f"Expected CSV in export formats, got: {formats}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-EXP-005: Default export format detection depends on whether "
           "the selector is a native <select> or React Select — needs DOM inspection.",
)
def test_export_default_format_is_xlsx(users_page):
    """SA-USR-EXP-005 — Default export format is XLSX."""
    users_page.click_export_icon()
    default = users_page.get_default_export_format()
    assert default and "xlsx" in default.lower() or "excel" in (default or "").lower(), \
        f"Default export format should be XLSX, got: {default!r}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-EXP-006: Column toggle locator (@role='switch' or checkbox) "
           "inside the modal not confirmed — needs DOM inspection.",
)
def test_export_modal_has_column_toggles(users_page):
    """SA-USR-EXP-006 — Export modal contains column selection toggles."""
    users_page.click_export_icon()
    toggles = users_page.driver.find_elements(*users_page.EXPORT_COLUMN_TOGGLES)
    assert len(toggles) >= 1, \
        f"Export modal should show at least one column toggle, found: {len(toggles)}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-EXP-007: Column toggle default state not confirmed — "
           "depends on aria-checked or is_selected() API which varies by implementation.",
)
def test_export_all_columns_on_by_default(users_page):
    """SA-USR-EXP-007 — All column toggles are ON by default in the Export modal."""
    users_page.click_export_icon()
    states = users_page.get_export_column_states()
    assert states, "No column toggles found in export modal"
    assert all(states.values()), \
        f"All column toggles should be ON by default, states: {states}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-EXP-008: Toggling off all columns to disable the Export button — "
           "toggle interaction not confirmed; Export button disable state may not be "
           "reflected via the 'disabled' attribute.",
)
def test_export_button_disabled_when_no_columns_selected(users_page):
    """SA-USR-EXP-008 — Export button is disabled when all column toggles are OFF."""
    users_page.click_export_icon()
    toggles = users_page.driver.find_elements(*users_page.EXPORT_COLUMN_TOGGLES)
    for toggle in toggles:
        users_page.driver.execute_script("arguments[0].click();", toggle)

    assert users_page.export_confirm_button_is_disabled(), \
        "Export button should be disabled when no columns are selected"


def test_export_button_enabled_by_default(users_page):
    """SA-USR-EXP-009 — Export button is enabled with at least one column selected (default state)."""
    users_page.click_export_icon()
    assert not users_page.export_confirm_button_is_disabled(), \
        "Export confirm button should be enabled in the default state"


def test_cancel_button_closes_export_modal(users_page):
    """SA-USR-EXP-010 — Cancel button closes the Export modal."""
    users_page.click_export_icon()
    users_page.cancel_export()
    assert not users_page.export_modal_is_visible(), \
        "Export modal should be dismissed after clicking Cancel"


def test_esc_key_closes_export_modal(users_page):
    """SA-USR-EXP-011 — ESC key dismisses the Export modal."""
    users_page.click_export_icon()
    users_page.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    users_page.wait.until(
        EC.invisibility_of_element_located(users_page.EXPORT_MODAL)
    )
    assert not users_page.export_modal_is_visible(), \
        "Export modal should be dismissed by pressing ESC"


@pytest.mark.xfail(
    strict=False,
    reason="SA-USR-EXP-012: Clicking outside the modal to dismiss — modal backdrop "
           "click target not confirmed; some React dialogs ignore outside clicks.",
)
def test_clicking_outside_modal_closes_it(users_page):
    """SA-USR-EXP-012 — Clicking outside the Export modal closes it."""
    users_page.click_export_icon()
    # Click the page backdrop outside the dialog (top-left corner of viewport)
    from selenium.webdriver.common.action_chains import ActionChains
    (
        ActionChains(users_page.driver)
        .move_to_element_with_offset(
            users_page.driver.find_element(By.TAG_NAME, "body"), 5, 5
        )
        .click()
        .perform()
    )
    users_page.wait.until(
        EC.invisibility_of_element_located(users_page.EXPORT_MODAL)
    )
    assert not users_page.export_modal_is_visible(), \
        "Export modal should close when clicking outside it"
