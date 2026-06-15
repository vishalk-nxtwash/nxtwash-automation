import logging

import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from tests.admin_portal.memberships.conftest import open_memberships_page


LOG = logging.getLogger(__name__)


def completed_downloads(download_dir):
    """Return completed downloaded files."""
    return [
        path
        for path in download_dir.iterdir()
        if path.is_file() and not path.name.endswith(".crdownload")
    ]


def wait_for_membership_download(browser, download_dir, memberships_page):
    """Click download and return newly completed files."""
    before_files = set(completed_downloads(download_dir))
    memberships_page.click_download_memberships()

    LOG.info("Waiting for membership export download")
    WebDriverWait(browser, 20).until(
        lambda driver: len(set(completed_downloads(download_dir)) - before_files) > 0
    )

    return set(completed_downloads(download_dir)) - before_files


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Download")
@allure.title("MB-EXP-001 Verify Download Memberships button functionality")
@pytest.mark.export
def test_download_memberships_starts_file_download(browser, tmp_path):

    LOG.info("Configuring Chrome download directory: %s", tmp_path)
    browser.execute_cdp_cmd(
        "Page.setDownloadBehavior",
        {
            "behavior": "allow",
            "downloadPath": str(tmp_path),
        }
    )

    memberships_page = open_memberships_page(browser)
    downloaded_files = wait_for_membership_download(browser, tmp_path, memberships_page)

    assert downloaded_files
    assert all(file.stat().st_size > 0 for file in downloaded_files)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Download")
@allure.title("MEM-DL-002 Verify downloaded file format")
@pytest.mark.export
def test_download_memberships_file_format(browser, tmp_path):

    LOG.info("Verifying membership export file format")
    browser.execute_cdp_cmd(
        "Page.setDownloadBehavior",
        {
            "behavior": "allow",
            "downloadPath": str(tmp_path),
        }
    )

    memberships_page = open_memberships_page(browser)
    downloaded_files = wait_for_membership_download(browser, tmp_path, memberships_page)

    assert downloaded_files
    assert any(
        file.suffix.lower() in {".csv", ".xlsx", ".xls"}
        for file in downloaded_files
    )
