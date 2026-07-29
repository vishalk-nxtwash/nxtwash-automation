import logging

import allure
import pytest

from tests.admin_portal.service_categories.conftest import CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import MISSING_CATEGORY
from tests.admin_portal.service_categories.conftest import create_category_if_missing
from tests.admin_portal.service_categories.conftest import open_service_categories_page
from tests.admin_portal.service_categories.conftest import page_has_no_broken_state


LOG = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Search"),
]


@allure.title(
    "SC-RG-001/SC-RG-002 Search variants (exact, partial, case, trim, long, missing) "
    "and clear"
)
@pytest.mark.regression
@pytest.mark.skip(reason="staging data / intermittent — deferred")
def test_service_categories_search_variants_and_clear(browser):
    LOG.info("Verifying Service Categories search variants")
    page = create_category_if_missing(browser)
    original_count = len(page.get_visible_category_names())

    page.search_category(CATEGORY_NAME)
    assert page.wait_for_category_row(CATEGORY_NAME).is_displayed()

    page.search_category(CATEGORY_NAME[:4])
    assert CATEGORY_NAME in page.get_body_text()

    page.search_category(CATEGORY_NAME.upper())
    assert CATEGORY_NAME.lower() in page.get_body_text().lower()

    page.search_category("  %s  " % CATEGORY_NAME)
    assert CATEGORY_NAME.lower() in page.get_body_text().lower()

    page.search_category("x" * 128)
    assert page_has_no_broken_state(page)

    page.search_category(MISSING_CATEGORY)
    assert MISSING_CATEGORY not in page.get_body_text()

    page.clear_category_search()
    assert len(page.get_visible_category_names()) >= min(original_count, 1)


@allure.title("SC-SRCH-002 Special character search remains stable")
@pytest.mark.regression
def test_service_categories_special_character_search_stays_usable(browser):

    page = open_service_categories_page(browser)
    page.search_category("' OR 1=1 --")

    assert page_has_no_broken_state(page)
