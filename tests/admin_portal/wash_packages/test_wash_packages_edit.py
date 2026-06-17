from tests.admin_portal.wash_packages.conftest import APPLICABLE_DISCOUNT
from tests.admin_portal.wash_packages.conftest import EXISTING_PACKAGE
from tests.admin_portal.wash_packages.conftest import open_wash_packages_page


def test_wash_package_discount_settings_tab_loads(browser):

    page = open_wash_packages_page(browser)
    page.open_edit_package(EXISTING_PACKAGE)
    page.open_discount_settings()

    assert "Applicable discounts" in page.get_body_text()


def test_wash_package_discount_can_be_selected_on_form(browser):

    page = open_wash_packages_page(browser)
    page.open_edit_package(EXISTING_PACKAGE)
    page.open_discount_settings()
    page.select_applicable_discount(APPLICABLE_DISCOUNT)

    assert page.discount_is_selected(APPLICABLE_DISCOUNT)
