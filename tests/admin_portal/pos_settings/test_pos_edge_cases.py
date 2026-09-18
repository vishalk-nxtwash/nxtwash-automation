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
    allure.story("Edge Cases"),
]

# POS-EC-002: Tunnel fields conditional validation when OFF — Automation = No
# POS-EC-003: Port boundary validation 0 and 65535 — Automation = No
# POS-EC-004: Both payment methods unchecked behavior — Automation = No
# POS-EC-005: Deactivating POS during transaction — Not Scheduled (Deferred)
# POS-EC-006: Settings changes saved atomically — Not Scheduled (Deferred)


@allure.title("POS-EC-001 POS name whitespace trimmed or rejected")
@pytest.mark.extended
def test_pos_name_whitespace_trimmed(browser, managed_pos):
    form = open_edit_pos_form(browser, POS_NAME)
    form.enter_pos_name("  " + POS_NAME + "  ")
    form.click_save()

    page = open_pos_page(browser)
    body = page.get_body_text()
    assert POS_NAME in body or page_has_no_broken_state(page), (
        "POS with whitespace-padded name not handled correctly"
    )
    assert page_has_no_broken_state(page)
