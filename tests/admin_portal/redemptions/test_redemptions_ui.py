import allure
import pytest

from tests.admin_portal.redemptions.conftest import (
    open_rdm_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Redemptions"),
    allure.story("UI"),
]


@allure.title("RDM-UI-001 Redemptions page loads and filter modal opens automatically")
@pytest.mark.prod_smoke
def test_redemptions_page_loads_and_modal_opens(browser):
    page = open_rdm_page(browser)

    assert page.modal_is_open(), "Filter modal did not open automatically on page load"
    assert page_has_no_broken_state(page)


@allure.title("RDM-UI-002 Redemptions filter modal contains site and date controls")
@pytest.mark.prod_smoke
def test_redemptions_filter_modal_has_site_and_date_controls(browser):
    page = open_rdm_page(browser)

    assert page.driver.find_element(*page.SITE_MULTISELECT).is_displayed(), (
        "Site multiselect not visible in filter modal"
    )
    assert page.driver.find_element(*page.DATE_PRESET_COMBOBOX).is_displayed(), (
        "Date preset combobox not visible in filter modal"
    )
    assert page.driver.find_element(*page.APPLY_BUTTON).is_displayed(), (
        "Apply button not visible in filter modal"
    )
    assert page_has_no_broken_state(page)
