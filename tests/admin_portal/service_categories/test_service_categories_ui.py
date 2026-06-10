from tests.admin_portal.service_categories.conftest import open_service_categories_page
from tests.admin_portal.service_categories.conftest import page_has_no_broken_state


def test_service_categories_page_loads_with_primary_controls(browser):

    page = open_service_categories_page(browser)
    body_text = page.get_body_text()

    assert "Service category" in body_text
    assert "Status" in body_text
    assert "Add new category" in body_text
    assert page_has_no_broken_state(page)


def test_add_service_category_form_loads(browser):

    page = open_service_categories_page(browser)
    page.open_create_category()

    assert "Category name" in page.get_body_text()
    assert "Active service" in page.get_body_text()
    assert page.active_switch_is_on()
