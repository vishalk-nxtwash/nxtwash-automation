import allure
import pytest

from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page
from tests.admin_portal.coupon_packages.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Coupon Packages"),
    allure.story("Customer Coupon Packages"),
]


@allure.title("CCP-LST-001 Customer coupon packages tab loads without errors")
@pytest.mark.smoke
def test_customer_coupon_packages_tab_loads(browser):

    page = open_coupon_packages_page(browser)
    page.click_customer_coupon_packages_tab()

    assert page_has_no_broken_state(page)


@allure.title("CCP-LST-002 Customer coupon packages grid columns are visible")
@pytest.mark.regression
def test_customer_coupon_packages_grid_columns_visible(browser):

    page = open_coupon_packages_page(browser)
    page.click_customer_coupon_packages_tab()
    body_text = page.get_body_text()

    assert page_has_no_broken_state(page)
    assert body_text != ""


@allure.title("CCP-SRH-001 Search by exact coupon code")
@pytest.mark.regression
@pytest.mark.skip(reason="Requires POS-generated coupon code data — deferred until POS dependency is available")
def test_customer_coupon_exact_search(browser):
    pass


@allure.title("CCP-SRH-002 Search by partial coupon code")
@pytest.mark.extended
@pytest.mark.skip(reason="Requires POS-generated coupon code data — deferred until POS dependency is available")
def test_customer_coupon_partial_search(browser):
    pass


@allure.title("CCP-SRH-003 Search non-existing code shows empty state")
@pytest.mark.extended
@pytest.mark.skip(reason="Requires POS-generated coupon code data — deferred until POS dependency is available")
def test_customer_coupon_missing_search(browser):
    pass


@allure.title("CCP-FLT-001 Filter by Is used = Used shows only redeemed coupons")
@pytest.mark.regression
@pytest.mark.skip(reason="Requires POS-generated coupon code data — deferred until POS dependency is available")
def test_customer_coupon_filter_used(browser):
    pass


@allure.title("CCP-FLT-002 Filter by Is used = Not used shows only unredeemed coupons")
@pytest.mark.regression
@pytest.mark.skip(reason="Requires POS-generated coupon code data — deferred until POS dependency is available")
def test_customer_coupon_filter_not_used(browser):
    pass


@allure.title("CCP-FLT-003 Filter Is used = All shows all coupons")
@pytest.mark.extended
@pytest.mark.skip(reason="Requires POS-generated coupon code data — deferred until POS dependency is available")
def test_customer_coupon_filter_all(browser):
    pass


@allure.title("CCP-FLT-004 Active coupon code filter shows active only")
@pytest.mark.regression
@pytest.mark.skip(reason="Requires POS-generated coupon code data — deferred until POS dependency is available")
def test_customer_coupon_filter_active(browser):
    pass


@allure.title("CCP-FLT-005 Combined Is used + Active filter narrows results correctly")
@pytest.mark.extended
@pytest.mark.skip(reason="Requires POS-generated coupon code data — deferred until POS dependency is available")
def test_customer_coupon_combined_filter(browser):
    pass


@allure.title("CCP-FLT-006 Reset all restores full customer coupon list")
@pytest.mark.extended
@pytest.mark.skip(reason="Requires POS-generated coupon code data — deferred until POS dependency is available")
def test_customer_coupon_reset_filters(browser):
    pass


@allure.title("CCP-DEP-001 Generated coupon code is unique per customer")
@pytest.mark.regression
@pytest.mark.skip(reason="Requires POS integration — deferred")
def test_customer_coupon_code_is_unique(browser):
    pass


@allure.title("CCP-DEP-002 Expired coupon code is marked as inactive")
@pytest.mark.regression
@pytest.mark.skip(reason="Requires POS integration — deferred")
def test_expired_coupon_code_is_inactive(browser):
    pass
