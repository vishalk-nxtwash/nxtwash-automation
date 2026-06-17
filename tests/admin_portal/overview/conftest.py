import pytest

from pages.admin_portal.overview_page import AdminOverviewPage
from tests.admin_portal.admin_session import ensure_admin_logged_in


@pytest.fixture
def overview_page(browser):
    ensure_admin_logged_in(browser)
    page = AdminOverviewPage(browser)
    page.wait_for_loaded()
    return page
