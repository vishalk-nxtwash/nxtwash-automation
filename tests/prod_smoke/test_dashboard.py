import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.overview_page import AdminOverviewPage
from pages.admin_portal.sidebar import AdminSidebar
from tests.admin_portal.admin_session import open_admin_path
from tests.prod_smoke.conftest import page_is_up


pytestmark = [
    allure.epic("Production Smoke"),
    allure.feature("Dashboard & Navigation"),
    pytest.mark.prod_smoke,
]


@pytest.fixture
def overview_page(browser):
    open_admin_path(browser, "/")
    page = AdminOverviewPage(browser)
    page.wait_for_loaded()
    return page


@allure.title("PSMO-NAV-001 Overview page loads at root path without errors")
@pytest.mark.prod_smoke
def test_overview_page_loads(overview_page):
    assert page_is_up(overview_page.driver)


@allure.title("PSMO-NAV-002 Overview title element is visible after load")
@pytest.mark.prod_smoke
def test_overview_title_visible(overview_page):
    body = overview_page.get_body_text()
    assert "Overview" in body, "Overview heading not found in page body"


@allure.title("PSMO-NAV-003 Sidebar top-level navigation links are present")
@pytest.mark.prod_smoke
def test_sidebar_top_level_links_visible(browser):
    open_admin_path(browser, "/")
    sidebar = AdminSidebar(browser)

    assert WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located(sidebar.OVERVIEW_LINK)
    ), "Overview sidebar link not found"
    assert browser.find_elements(*sidebar.SITES_LOCATIONS_LINK), "Sites / Locations link missing"
    assert browser.find_elements(*sidebar.CUSTOMERS_LINK), "Customers link missing"
    assert browser.find_elements(*sidebar.SERVICES_BUTTON), "Services button missing"


@allure.title("PSMO-NAV-004 Services submenu expands and shows all catalog links")
@pytest.mark.prod_smoke
def test_services_submenu_expands(browser):
    open_admin_path(browser, "/")
    sidebar = AdminSidebar(browser)
    sidebar.open_memberships()

    assert browser.find_elements(*sidebar.WASH_PACKAGES_LINK), "Wash Packages link missing"
    assert browser.find_elements(*sidebar.MEMBERSHIPS_LINK), "Memberships link missing"
    assert browser.find_elements(*sidebar.DISCOUNTS_LINK), "Discounts link missing"
    assert browser.find_elements(*sidebar.GIFT_CARDS_LINK), "Gift Cards link missing"


@allure.title("PSMO-NAV-005 Navigating to a deep link does not bounce to login")
@pytest.mark.prod_smoke
def test_deep_link_does_not_bounce(browser):
    open_admin_path(browser, "/customers")
    assert "/login" not in browser.current_url, (
        "Deep link /customers redirected to /login — session may not persist on prod"
    )
    assert page_is_up(browser)
