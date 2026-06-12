import logging

import allure
import pytest

from tests.admin_portal.service_categories.conftest import MANAGED_CATEGORY


LOG = logging.getLogger("nxtwash")


@allure.epic("Admin Portal")
@allure.feature("Service Categories")
@allure.story("Managed Data")
@allure.title("SC-MADA managed category baseline is available")
@pytest.mark.sanity
def test_service_category_managed_data_baseline(managed_category):
    LOG.info("Verifying managed Service Category baseline data")
    page = managed_category

    assert page.category_exists(MANAGED_CATEGORY)
    assert page.get_category_status(MANAGED_CATEGORY) == "Active"

