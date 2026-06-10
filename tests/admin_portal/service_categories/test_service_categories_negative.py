from tests.admin_portal.service_categories.conftest import CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import MISSING_CATEGORY
from tests.admin_portal.service_categories.conftest import create_category_if_missing
from tests.admin_portal.service_categories.conftest import open_service_categories_page


def test_missing_service_category_is_not_returned(browser):

    page = open_service_categories_page(browser)
    page.search_category(MISSING_CATEGORY)

    assert MISSING_CATEGORY not in page.get_body_text()


def test_create_service_category_is_idempotent(browser):

    page = create_category_if_missing(browser)
    page.search_category(CATEGORY_NAME)

    assert page.wait_for_category_row(CATEGORY_NAME).is_displayed()
