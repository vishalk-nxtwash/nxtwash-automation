from datetime import datetime

import pytest

from pages.superadmin.companies_page import CompaniesPage
from pages.superadmin.edit_company_page import EditCompanyPage
from pages.superadmin.login_page import LoginPage
from pages.superadmin.sidebar import Sidebar


COMPANY_NAME = "vktestcompany"


@pytest.fixture
def edit_company_page(browser):

    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()

    login_page.wait_for_url(
        "https://superadmin.nxtwash.com/"
    )

    sidebar = Sidebar(browser)
    sidebar.open_companies()

    companies_page = CompaniesPage(browser)
    companies_page.filter_by_company_name(COMPANY_NAME)
    companies_page.open_company_edit(COMPANY_NAME)

    edit_page = EditCompanyPage(browser)
    edit_page.wait_for_loaded(COMPANY_NAME)

    return edit_page


def test_open_edit_company_page(browser, edit_company_page):

    assert "/companies/" in browser.current_url
    assert edit_company_page.get_company_name() == COMPANY_NAME
    assert edit_company_page.get_terms_condition() is not None


def test_cancel_discards_terms_condition_changes(browser, edit_company_page):

    original_terms = edit_company_page.get_terms_condition()
    draft_terms = (
        f"{original_terms}\n\nAutomation cancel draft - not saved"
    ).strip()

    edit_company_page.set_terms_condition(draft_terms)
    edit_company_page.click_cancel()
    edit_company_page.confirm_yes()
    edit_company_page.wait_for_confirmation_closed()

    companies_page = CompaniesPage(browser)
    companies_page.filter_by_company_name(COMPANY_NAME)
    companies_page.open_company_edit(COMPANY_NAME)

    reopened_edit_page = EditCompanyPage(browser)
    reopened_edit_page.wait_for_loaded(COMPANY_NAME)

    assert reopened_edit_page.get_terms_condition() == original_terms


def test_update_terms_condition_and_restore_original(browser, edit_company_page):

    original_terms = edit_company_page.get_terms_condition()
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    updated_terms = (
        f"{original_terms}\n\nAutomation update check {timestamp}"
    ).strip()

    assert updated_terms != original_terms

    try:
        edit_company_page.set_terms_condition(updated_terms)
        edit_company_page.click_save_changes()
        edit_company_page.confirm_yes()
        edit_company_page.wait_for_confirmation_closed()
        edit_company_page.wait_for_terms_condition(updated_terms)

        browser.refresh()
        edit_company_page.wait_for_loaded(COMPANY_NAME)

        assert edit_company_page.get_terms_condition() == updated_terms

    finally:
        edit_company_page.set_terms_condition(original_terms)
        edit_company_page.click_save_changes()
        edit_company_page.confirm_yes()
        edit_company_page.wait_for_confirmation_closed()
        edit_company_page.wait_for_terms_condition(original_terms)

        browser.refresh()
        edit_company_page.wait_for_loaded(COMPANY_NAME)

        assert edit_company_page.get_terms_condition() == original_terms
