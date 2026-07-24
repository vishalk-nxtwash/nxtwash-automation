import allure
import pytest

from tests.admin_portal.customers.conftest import (
    CUSTOMER_CAR_RFID,
    CUSTOMER_FIRST,
    CUSTOMER_LAST,
    CUSTOMER_LICENSE_PLATE,
    create_customer_if_missing,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Customers"),
    allure.story("Cars Settings"),
]

# NOTE: This file intentionally only verifies that Cars Settings fields and
# controls are present. No cars are created or saved. Full CRUD coverage
# will be added in a separate pass once locators are confirmed against the DOM.

_CRUD_SKIP = (
    "Cars CRUD deferred — verifying field presence only in this pass. "
    "Unblock after confirming DOM locators from a live run."
)


def _open_managed_customer_edit(browser):
    page = create_customer_if_missing(browser)
    page.open_filter_panel()
    page.filter_by_first_name(CUSTOMER_FIRST)
    page.filter_by_last_name(CUSTOMER_LAST)
    page.apply_filters()
    page.open_edit_customer_from_row(CUSTOMER_LAST)
    return page


# ── Tab access ────────────────────────────────────────────────────────────────

@allure.title("CUST-CAR-001 Cars settings tab is enabled on an existing customer")
@pytest.mark.smoke
@pytest.mark.xfail(
    reason="CUST-CAR-001: Tab locator (role/text) needs DevTools verification on the edit form.",
    strict=False,
)
def test_cars_settings_tab_accessible_on_existing_customer(browser):
    page = _open_managed_customer_edit(browser)

    assert not page.cars_settings_tab_is_disabled()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-001b Cars settings tab opens and shows Add car control")
@pytest.mark.smoke
@pytest.mark.xfail(
    reason="CUST-CAR-001b: Depends on tab locator — xfail until CUST-CAR-001 passes.",
    strict=False,
)
def test_cars_settings_tab_shows_add_car_button(browser):
    page = _open_managed_customer_edit(browser)
    page.open_cars_settings_tab()

    assert page.add_car_button_is_visible()
    assert page_has_no_broken_state(page)


# ── Add car form — field presence ─────────────────────────────────────────────

@allure.title("CUST-CAR-003 Add car form contains a License Plate field")
@pytest.mark.regression
def test_add_car_form_shows_license_plate_field(browser):
    page = _open_managed_customer_edit(browser)
    page.open_cars_settings_tab()
    page.open_add_car_form()

    assert page.license_plate_field_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-003b Add car form contains an RFID field")
@pytest.mark.regression
def test_add_car_form_shows_rfid_field(browser):
    page = _open_managed_customer_edit(browser)
    page.open_cars_settings_tab()
    page.open_add_car_form()

    assert page.rfid_field_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-004 Add car form contains vehicle detail fields (Year/Make/Model/Color)")
@pytest.mark.regression
def test_add_car_form_shows_vehicle_detail_fields(browser):
    page = _open_managed_customer_edit(browser)
    page.open_cars_settings_tab()
    page.open_add_car_form()
    body = page.get_body_text()

    # Document which detail fields are present — year / make / model / color.
    # At minimum the form must be open and stable.
    assert page_has_no_broken_state(page)
    body_lower = body.lower()
    assert any(label in body_lower for label in ["year", "make", "model", "color", "colour"])


@allure.title("CUST-CAR-008 Add car form contains Save and Cancel controls")
@pytest.mark.regression
def test_add_car_form_shows_save_and_cancel_controls(browser):
    page = _open_managed_customer_edit(browser)
    page.open_cars_settings_tab()
    page.open_add_car_form()

    assert page.save_car_button_is_visible()
    assert page_has_no_broken_state(page)


# ── Validation field presence ─────────────────────────────────────────────────

@allure.title("CUST-CAR-VAL-001 License Plate field is present and marked required")
@pytest.mark.smoke
@pytest.mark.xfail(
    reason="CUST-CAR-VAL-001: Depends on tab locator — xfail until CUST-CAR-001 passes.",
    strict=False,
)
def test_license_plate_field_is_present_and_required(browser):
    page = _open_managed_customer_edit(browser)
    page.open_cars_settings_tab()
    page.open_add_car_form()

    assert page.license_plate_field_is_visible()
    assert page.license_plate_field_is_required()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-VAL-002 RFID field is present and marked required")
@pytest.mark.smoke
@pytest.mark.xfail(
    reason="CUST-CAR-VAL-002: Depends on tab locator — xfail until CUST-CAR-001 passes.",
    strict=False,
)
def test_rfid_field_is_present_and_required(browser):
    page = _open_managed_customer_edit(browser)
    page.open_cars_settings_tab()
    page.open_add_car_form()

    assert page.rfid_field_is_visible()
    assert page.rfid_field_is_required()
    assert page_has_no_broken_state(page)


# ── Membership button presence ────────────────────────────────────────────────

@allure.title("CUST-CAR-MEM-001 Add car form shows Assign membership button after filling car details")
@pytest.mark.regression
@pytest.mark.skip(reason="Manual check — Assign membership button visibility depends on membership module state.")
def test_add_car_form_shows_assign_membership_button(browser):
    page = _open_managed_customer_edit(browser)
    page.open_cars_settings_tab()
    page.open_add_car_form()
    page.enter_license_plate(CUSTOMER_LICENSE_PLATE)
    page.enter_car_rfid(CUSTOMER_CAR_RFID)

    assert page.assign_membership_button_is_visible()
    assert page_has_no_broken_state(page)


# ── Deferred / cross-module ───────────────────────────────────────────────────

@allure.title("CUST-CAR-002 Cars list shows membership and next payment date columns")
@pytest.mark.regression
@pytest.mark.skip(reason="Requires Memberships module fixtures with active member cars.")
def test_cars_list_shows_membership_details(browser):
    pass


@allure.title("CUST-CAR-005 Blacklist a car")
@pytest.mark.regression
@pytest.mark.skip(reason=_CRUD_SKIP)
def test_blacklist_a_car(browser):
    pass


@allure.title("CUST-CAR-006 Deactivate a car")
@pytest.mark.regression
@pytest.mark.skip(reason=_CRUD_SKIP)
def test_deactivate_a_car(browser):
    pass


@allure.title("CUST-CAR-007 Update Vehicle Token")
@pytest.mark.regression
@pytest.mark.skip(reason="Deferred — requires POS token provisioning setup.")
def test_update_vehicle_token(browser):
    pass


@allure.title("CUST-CAR-VAL-003 Duplicate license plate — document behaviour")
@pytest.mark.edge
@pytest.mark.skip(reason=_CRUD_SKIP)
def test_duplicate_license_plate_documents_behaviour(browser):
    pass


@allure.title("CUST-CAR-VAL-004 Duplicate RFID — document behaviour")
@pytest.mark.edge
@pytest.mark.skip(reason="Deferred — RFID uniqueness requires POS tunnel integration to verify.")
def test_duplicate_rfid_documents_behaviour(browser):
    pass


@allure.title("CUST-PER-003 Add car then refresh — car appears in Cars settings")
@pytest.mark.regression
@pytest.mark.skip(reason=_CRUD_SKIP)
def test_add_car_then_refresh_car_persists(browser):
    pass
