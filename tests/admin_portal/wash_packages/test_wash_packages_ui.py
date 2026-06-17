from tests.admin_portal.wash_packages.conftest import open_wash_packages_page
from tests.admin_portal.wash_packages.conftest import page_has_no_broken_state


def test_wash_packages_page_loads_with_primary_controls(browser):

    page = open_wash_packages_page(browser)
    body_text = page.get_body_text()

    assert "Wash package name" in body_text
    assert "Price" in body_text
    assert "Status" in body_text
    assert "Add new wash package" in body_text
    assert page_has_no_broken_state(page)


def test_wash_packages_filter_panel_shows_controls(browser):

    page = open_wash_packages_page(browser)
    body_text = page.get_body_text()

    assert "Wash package name" in body_text
    assert "Status" in body_text
    assert page_has_no_broken_state(page)


def test_add_wash_package_form_loads(browser):

    page = open_wash_packages_page(browser)
    page.open_create_package()

    assert "Service name" in page.get_body_text()
    assert "Global price" in page.get_body_text()
    assert page.active_switch_is_on()
