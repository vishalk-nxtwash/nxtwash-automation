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


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Download")
@allure.title("MEM-DL-001 Verify Download Memberships button functionality")
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
    before_files = set(completed_downloads(tmp_path))
    memberships_page.click_download_memberships()

    LOG.info("Waiting for membership export download")
    WebDriverWait(browser, 20).until(
        lambda driver: len(set(completed_downloads(tmp_path)) - before_files) > 0
    )

    downloaded_files = set(completed_downloads(tmp_path)) - before_files

    assert downloaded_files
    assert all(file.stat().st_size > 0 for file in downloaded_files)
