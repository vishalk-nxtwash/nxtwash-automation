from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page
from tests.admin_portal.coupon_packages.conftest import page_has_no_broken_state


def test_coupon_packages_page_loads_with_primary_controls(browser):

    page = open_coupon_packages_page(browser)
    body_text = page.get_body_text()

    assert "Coupon package name" in body_text
    assert "Discount assigned" in body_text
    assert "Services assigned" in body_text
    assert "Status" in body_text
    assert "Add new coupon package" in body_text
    assert page_has_no_broken_state(page)


def test_add_coupon_package_form_loads(browser):

    page = open_coupon_packages_page(browser)
    page.open_create_coupon_package()

    assert "Coupon package name" in page.get_body_text()
    assert "Assign discount" in page.get_body_text()
    assert page.active_switch_is_on()
