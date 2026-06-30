import allure
import pytest

from tests.admin_portal.sites.conftest import open_sites_page
from tests.admin_portal.sites.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Sites / Locations"),
    allure.story("Export"),
]


@allure.title("SL-EXP-001 Export button is clickable and does not break the page")
@pytest.mark.regression
def test_sites_export_button_clickable(logged_in_admin_browser):
    sites_page = open_sites_page(logged_in_admin_browser)

    assert sites_page.download_button_is_clickable()
    assert page_has_no_broken_state(sites_page)


@allure.title("SL-EXP-001 Export file content validation")
@pytest.mark.regression
@pytest.mark.xfail(
    reason=(
        "File/content validation needs browser download-directory configuration "
        "and a CSV/XLS parser. Button clickability is verified above; "
        "full export assertion is deferred."
    ),
    strict=False,
)
def test_sites_export_file_content(logged_in_admin_browser):
    sites_page = open_sites_page(logged_in_admin_browser)
    assert sites_page.download_button_is_clickable()
    raise AssertionError("Download file/content validation is not implemented.")
