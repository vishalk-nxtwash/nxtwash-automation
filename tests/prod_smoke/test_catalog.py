import allure
import pytest

from pages.admin_portal.bank_drop_page import BankDropPage
from pages.admin_portal.coupon_packages_page import CouponPackagesPage
from pages.admin_portal.discounts_page import DiscountsPage
from pages.admin_portal.gift_cards_page import GiftCardsPage
from pages.admin_portal.memberships_page import MembershipsPage
from pages.admin_portal.service_categories_page import ServiceCategoriesPage
from pages.admin_portal.wash_books_page import WashBooksPage
from pages.admin_portal.wash_extras_page import WashExtrasPage
from pages.admin_portal.wash_packages_page import WashPackagesPage
from tests.admin_portal.admin_session import open_admin_path
from tests.prod_smoke.conftest import page_is_up


pytestmark = [
    allure.epic("Production Smoke"),
    allure.feature("Services Catalog"),
    pytest.mark.prod_smoke,
]


@allure.title("PSMO-SVC-001 Wash Packages page loads")
@pytest.mark.prod_smoke
def test_wash_packages_loads(browser):
    open_admin_path(browser, "/services/washPackages")
    page = WashPackagesPage(browser)
    page.wait_for_loaded(allow_readonly=True)

    assert page_is_up(browser)


@allure.title("PSMO-SVC-002 Service Categories page loads")
@pytest.mark.prod_smoke
def test_service_categories_loads(browser):
    open_admin_path(browser, "/services/serviceCategories")
    page = ServiceCategoriesPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-SVC-003 Memberships page loads")
@pytest.mark.prod_smoke
def test_memberships_loads(browser):
    open_admin_path(browser, "/services/memberships")
    page = MembershipsPage(browser)
    page.wait_for_loaded(allow_readonly=True)

    assert page_is_up(browser)


@allure.title("PSMO-SVC-004 Discounts page loads")
@pytest.mark.prod_smoke
def test_discounts_loads(browser):
    open_admin_path(browser, "/services/discounts")
    page = DiscountsPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-SVC-005 Wash Books page loads")
@pytest.mark.prod_smoke
def test_wash_books_loads(browser):
    open_admin_path(browser, "/services/washBooks")
    page = WashBooksPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-SVC-006 Wash Extras page loads")
@pytest.mark.prod_smoke
def test_wash_extras_loads(browser):
    open_admin_path(browser, "/services/washExtras")
    page = WashExtrasPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-SVC-007 Gift Cards page loads")
@pytest.mark.prod_smoke
def test_gift_cards_loads(browser):
    open_admin_path(browser, "/services/giftCards")
    page = GiftCardsPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-SVC-008 Coupon Packages page loads")
@pytest.mark.prod_smoke
def test_coupon_packages_loads(browser):
    open_admin_path(browser, "/services/couponPackages")
    page = CouponPackagesPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-SVC-009 Bank Drop page loads")
@pytest.mark.prod_smoke
def test_bank_drop_loads(browser):
    open_admin_path(browser, "/services/bankDrop")
    page = BankDropPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)
