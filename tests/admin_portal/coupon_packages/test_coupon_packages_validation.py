from tests.admin_portal.coupon_packages.conftest import open_coupon_packages_page
from tests.admin_portal.coupon_packages.conftest import page_has_no_broken_state


def test_coupon_package_required_name_validation(browser):

    page = open_coupon_packages_page(browser)
    page.open_create_coupon_package()
    page.click_save_coupon_package()

    assert not page.coupon_package_name_input_is_valid()
    assert page.get_coupon_package_name_validation_message() != ""


def test_coupon_package_blank_required_form_stays_on_form(browser):

    page = open_coupon_packages_page(browser)
    page.open_create_coupon_package()
    page.click_save_coupon_package()

    assert "Coupon package name" in page.get_body_text()
    assert page_has_no_broken_state(page)
