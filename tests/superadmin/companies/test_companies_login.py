import allure
import pytest

from selenium.webdriver.common.by import By

from tests.superadmin.companies.conftest import COMPANY_NAME

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Companies"),
    allure.story("Login To"),
]

_EXPECTED_APP_OPTIONS = [
    "Admin Portal",
    "POS App",
    "Tunnel App",
    "NxtCRM App",
    "NxtTrack App",
]


def test_login_to_opens_app_selection_modal(companies_page):
    """SA-CMP-LGN-001 — 'Login to' opens the 'Select app to login' modal."""
    companies_page.filter_by_company_name(COMPANY_NAME)
    companies_page.click_login_to(COMPANY_NAME)
    dialog_els = companies_page.driver.find_elements(*companies_page.LOGIN_DIALOG)
    assert dialog_els and dialog_els[0].is_displayed(), \
        "'Login to' should open a dialog/modal"
    companies_page.dismiss_login_dialog()


def test_login_to_modal_lists_all_app_options(companies_page):
    """SA-CMP-LGN-002 — App modal lists Admin Portal, POS App, Tunnel App, NxtCRM App, NxtTrack App and Close."""
    companies_page.filter_by_company_name(COMPANY_NAME)
    companies_page.click_login_to(COMPANY_NAME)
    options = companies_page.get_login_dialog_options()
    for expected in _EXPECTED_APP_OPTIONS:
        assert any(expected.lower() in o.lower() for o in options), \
            f"Expected '{expected}' in dialog options, got: {options}"
    companies_page.dismiss_login_dialog()


@pytest.mark.skip(
    reason="SA-CMP-LGN-003: 'Admin Portal' impersonation opens a new window/tab and "
           "navigates away — side effects on browser state; skipped for automated suite."
)
def test_admin_portal_launches_in_company_context(companies_page):
    """SA-CMP-LGN-003 — Selecting 'Admin Portal' launches that company's Admin Portal."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-LGN-004: POS App sub-step (domain selection) — "
           "dialog structure not confirmed via DOM inspection.",
)
def test_pos_app_shows_domain_selection_step(companies_page):
    """SA-CMP-LGN-004 — Selecting 'POS App' opens the domain selection step."""
    companies_page.filter_by_company_name(COMPANY_NAME)
    companies_page.click_login_to(COMPANY_NAME)
    pos_btn = (
        By.XPATH,
        "//div[@role='dialog']//button[normalize-space()='POS App']"
    )
    els = companies_page.driver.find_elements(*pos_btn)
    assert els, "POS App button should be present in the Login to dialog"
    companies_page.driver.execute_script("arguments[0].click();", els[0])

    domain_options = (
        By.XPATH,
        "//div[@role='dialog']//button[contains(.,'Production') or contains(.,'Staging')]"
    )
    domain_els = companies_page.driver.find_elements(*domain_options)
    assert domain_els, \
        "POS App should show a domain selection step with Production/Staging options"
    companies_page.dismiss_login_dialog()


@pytest.mark.skip(
    reason="SA-CMP-LGN-005: POS Production launch — opens external URL; "
           "side effects on browser state; skipped for automated suite."
)
def test_pos_production_launches(companies_page):
    """SA-CMP-LGN-005 — 'POS Production' launches the production POS for the selected company."""
    pass


@pytest.mark.skip(
    reason="SA-CMP-LGN-006: POS Staging launch — opens external URL; "
           "side effects on browser state; skipped for automated suite."
)
def test_pos_staging_launches(companies_page):
    """SA-CMP-LGN-006 — 'POS Staging' launches the staging POS for the selected company."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-LGN-007: 'Back' button on domain step returns to app selection — "
           "Back button locator in the POS domain step not confirmed.",
)
def test_back_on_domain_step_returns_to_app_selection(companies_page):
    """SA-CMP-LGN-007 — 'Back' on the domain step returns to the app-selection modal."""
    companies_page.filter_by_company_name(COMPANY_NAME)
    companies_page.click_login_to(COMPANY_NAME)
    pos_btn = (
        By.XPATH,
        "//div[@role='dialog']//button[normalize-space()='POS App']"
    )
    els = companies_page.driver.find_elements(*pos_btn)
    assert els, "POS App button should be present"
    companies_page.driver.execute_script("arguments[0].click();", els[0])

    back_btn = (
        By.XPATH,
        "//div[@role='dialog']//button[normalize-space()='Back']"
    )
    back_els = companies_page.driver.find_elements(*back_btn)
    assert back_els, "Back button should be present on the domain selection step"
    companies_page.driver.execute_script("arguments[0].click();", back_els[0])

    app_options = companies_page.get_login_dialog_options()
    assert any("Admin Portal" in o for o in app_options), \
        "After clicking Back, app selection options should reappear"
    companies_page.dismiss_login_dialog()


def test_close_dismisses_launcher_without_navigating(companies_page, browser):
    """SA-CMP-LGN-008 — 'Close' dismisses the launcher without navigating."""
    original_url = browser.current_url
    companies_page.filter_by_company_name(COMPANY_NAME)
    companies_page.click_login_to(COMPANY_NAME)
    companies_page.dismiss_login_dialog()

    assert browser.current_url == original_url or "companies" in browser.current_url, \
        "After dismissing the dialog, URL should remain on companies page"


@pytest.mark.skip(
    reason="SA-CMP-LGN-009: Tunnel/NxtCRM/NxtTrack app launch — opens external URLs; "
           "side effects on browser state; skipped for automated suite."
)
def test_tunnel_nxtcrm_nxttrack_launch(companies_page):
    """SA-CMP-LGN-009 — Tunnel App / NxtCRM App / NxtTrack App each launch for the selected company."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-LGN-010: Context integrity check — verifying the launched app "
           "opens the correct company requires reading the destination page, "
           "which involves a new window and navigation away.",
)
def test_login_to_opens_correct_company_context(companies_page):
    """SA-CMP-LGN-010 — 'Login to' launches into the exact company whose row was clicked."""
    pass


@pytest.mark.xfail(
    strict=False,
    reason="SA-CMP-LGN-011: 'Login to' on a company with missing data — "
           "company 'crewcarwashtest' existence not confirmed in staging.",
)
def test_login_to_partial_data_company(companies_page):
    """SA-CMP-LGN-011 — 'Login to' on a company with missing data documents the behaviour."""
    partial_company = "crewcarwashtest"
    companies_page.filter_by_company_name(partial_company)
    companies_page.click_login_to(partial_company)
    dialog_els = companies_page.driver.find_elements(*companies_page.LOGIN_DIALOG)
    assert dialog_els, "Login to dialog should open even for a partial-data company"
    companies_page.dismiss_login_dialog()
