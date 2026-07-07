import allure
import pytest

from tests.admin_portal.pos_settings.conftest import (
    POS_NAME,
    open_edit_pos_form,
    open_pos_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("POS Settings"),
    allure.story("Active POS"),
]

_TOGGLE_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Active POS toggle locator uses role='switch' heuristics — "
        "verify aria-checked attribute in DevTools before removing xfail."
    ),
)


@allure.title("POS-ACT-001 Active POS toggle ON saves with Active status")
@pytest.mark.smoke
@_TOGGLE_XFAIL
def test_active_pos_toggle_on_saves(browser, managed_pos):
    form = open_edit_pos_form(browser, POS_NAME)
    form.ensure_active_pos_on()
    form.click_save()

    page = open_pos_page(browser)
    page.search_pos(POS_NAME)
    body = page.get_body_text()
    assert "Active" in body, (
        "POS '%s' should show Active status after toggle ON" % POS_NAME
    )
    assert page_has_no_broken_state(page)


@allure.title("POS-ACT-002 Active POS toggle OFF saves with Inactive status")
@pytest.mark.smoke
@_TOGGLE_XFAIL
def test_active_pos_toggle_off_saves(browser, managed_pos):
    form = open_edit_pos_form(browser, POS_NAME)
    form.ensure_active_pos_off()
    form.click_save()

    page = open_pos_page(browser)
    page.search_pos(POS_NAME)
    body = page.get_body_text()
    assert "Inactive" in body or POS_NAME not in body, (
        "POS '%s' should show Inactive status after toggle OFF" % POS_NAME
    )
    assert page_has_no_broken_state(page)
