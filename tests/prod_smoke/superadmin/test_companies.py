import allure
import pytest

from pages.superadmin.companies_page import CompaniesPage
from tests.prod_smoke.conftest import page_is_up


pytestmark = [
    allure.epic("Production Smoke"),
    allure.feature("Superadmin Companies"),
    pytest.mark.prod_smoke,
]


@pytest.fixture
def companies_page(superadmin_session, sidebar):
    sidebar.open_companies()
    page = CompaniesPage(superadmin_session)
    page.wait_for_loaded()
    return page


@allure.title("SA-PSMO-CMP-001 Companies list loads with title and at least one row")
@pytest.mark.prod_smoke
def test_companies_list_loads(companies_page):
    assert companies_page.get_page_title() == "Companies"
    assert companies_page.get_visible_row_count() >= 1, \
        "Expected at least one company row on the live list"
    assert page_is_up(companies_page.driver)


@allure.title("SA-PSMO-CMP-002 Companies list shows column headers and pagination info")
@pytest.mark.prod_smoke
def test_companies_list_columns_and_pagination(companies_page):
    assert companies_page.get_column_headers(), \
        "Companies table should render column headers"
    assert companies_page.get_pagination_text(), \
        "Pagination info should be visible on the Companies list"


@allure.title("SA-PSMO-CMP-003 'Login to' opens the app-selection dialog and can be dismissed")
@pytest.mark.prod_smoke
def test_login_to_dialog_opens_and_dismisses(companies_page):
    # Never target a specific company by name here — use whichever row is
    # first on the live list, and never select an app inside the dialog.
    buttons = companies_page.driver.find_elements(*companies_page.LOGIN_TO_BUTTON)
    assert buttons, "Expected at least one 'Login to' button on the Companies list"

    companies_page.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", buttons[0]
    )
    companies_page.driver.execute_script("arguments[0].click();", buttons[0])

    options = companies_page.get_login_dialog_options()
    assert options, "'Login to' dialog should list at least one app option"

    companies_page.dismiss_login_dialog()
