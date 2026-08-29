import allure
import pytest

from tests.admin_portal.custom_services.conftest import (
    ASSIGNMENT_SITE,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    SERVICE_CATEGORY,
    SERVICE_NAME,
    create_service_if_missing,
    open_custom_services_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Custom Services"),
    allure.story("Dependency"),
]


@allure.title("CS-DEP-001 Assigned site appears in the site assignment grid after save")
@pytest.mark.regression
def test_assigned_site_appears_in_site_grid_after_save(browser):

    create_service_if_missing(browser)
    page = open_custom_services_page(browser)
    page.open_edit_service(SERVICE_NAME)

    row = page.get_site_row(ASSIGNMENT_SITE)
    assert row.is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("CS-DEP-002 Custom service appears in POS service selection after assignment")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Manual: verifying service visibility on the POS terminal requires "
        "a physical or emulated POS device that is not available in the automation environment."
    )
)
def test_service_appears_in_pos_after_assignment(browser):
    pass


@allure.title("CS-DEP-003 Inactive custom service is hidden from the POS service list")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Manual: verifying POS visibility for inactive services requires "
        "a POS device and is not automatable in the current test setup."
    )
)
def test_inactive_service_hidden_from_pos(browser):
    pass


@allure.title("CS-DEP-004 Deleting a custom service removes it from all POS terminals")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Manual: delete functionality is not exposed in the admin list UI; "
        "POS impact must be verified manually against a live terminal."
    )
)
def test_delete_service_removes_from_pos(browser):
    pass


@allure.title("CS-EXP-001 Export download button triggers a file download")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Manual: automating file download verification in headless Chrome requires "
        "download-directory interception which is out of scope for this test suite."
    )
)
def test_export_download_button_triggers_download(browser):
    pass
