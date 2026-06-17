from tests.admin_portal.wash_extras.conftest import open_wash_extras_page
from tests.admin_portal.wash_extras.conftest import page_has_no_broken_state


def test_wash_extras_page_loads_with_primary_controls(browser):

    page = open_wash_extras_page(browser)
    body_text = page.get_body_text()

    assert "Wash extra name" in body_text
    assert "Price" in body_text
    assert "Status" in body_text
    assert "Add new wash extra" in body_text
    assert page_has_no_broken_state(page)


def test_wash_extras_filter_panel_shows_controls(browser):

    page = open_wash_extras_page(browser)
    body_text = page.get_body_text()

    assert "Wash extra name" in body_text
    assert "Status" in body_text
    assert page_has_no_broken_state(page)


def test_add_wash_extra_form_loads(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()

    assert "Service name" in page.get_body_text()
    assert "Global price" in page.get_body_text()
    assert page.active_switch_is_on()
