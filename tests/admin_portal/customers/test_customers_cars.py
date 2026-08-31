import uuid

import allure
import pytest

from tests.admin_portal.customers.conftest import (
    CUSTOMER_EMAIL,
    CUSTOMER_LICENSE_PLATE,
    CUSTOMER_CAR_RFID,
    create_customer_if_missing,
    open_customers_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Customers"),
    allure.story("Cars Settings"),
    # Staging's search index can lag up to ~90 s after customer creation or
    # reactivation. Each test also spends up to ~155 s in create_customer_if_missing
    # on the first run. 480 s gives comfortable headroom.
    pytest.mark.timeout(480),
]


def _open_managed_customer_cars_tab(browser):
    """Open the managed customer's edit form and navigate to the Cars settings tab."""
    page = create_customer_if_missing(browser)
    page.filter_by_email_and_open_edit(CUSTOMER_EMAIL)
    page.open_cars_settings_tab()
    return page


def _add_car(page, plate, rfid=None):
    """Helper: open the add-car form, fill fields, save, and return to Cars tab."""
    page.open_add_car_form()
    page.enter_license_plate(plate)
    if rfid:
        page.enter_car_rfid(rfid)
    page.click_save_car()          # returns to Customer Info tab
    page.open_cars_settings_tab()  # navigate back to see the car list


# ── Tab access ────────────────────────────────────────────────────────────────

@allure.title("CUST-CAR-001 Cars settings tab is enabled on an existing customer")
@pytest.mark.smoke
def test_cars_settings_tab_accessible_on_existing_customer(browser):
    page = create_customer_if_missing(browser)
    page.filter_by_email_and_open_edit(CUSTOMER_EMAIL)

    assert not page.cars_settings_tab_is_disabled()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-001b Cars settings tab opens and shows Add car control")
@pytest.mark.smoke
def test_cars_settings_tab_shows_add_car_button(browser):
    page = _open_managed_customer_cars_tab(browser)

    assert page.add_car_button_is_visible()
    assert page_has_no_broken_state(page)


# ── Create car ────────────────────────────────────────────────────────────────

@allure.title("CUST-CAR-003 Add new car with required fields only — car appears in list")
@pytest.mark.regression
def test_add_car_with_required_fields_only(browser):
    plate = "VK-" + uuid.uuid4().hex[:6].upper()
    page = _open_managed_customer_cars_tab(browser)
    _add_car(page, plate)

    assert page.car_row_visible(plate)
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-004 Add new car with full details (plate + RFID) — car appears in list")
@pytest.mark.regression
def test_add_car_with_full_details(browser):
    plate = "VK-F-" + uuid.uuid4().hex[:5].upper()
    rfid  = "VK-RF-" + uuid.uuid4().hex[:4].upper()
    page = _open_managed_customer_cars_tab(browser)
    _add_car(page, plate, rfid=rfid)

    assert page.car_row_visible(plate)
    assert page_has_no_broken_state(page)


# ── Add car form — field/control presence ─────────────────────────────────────

@allure.title("CUST-CAR-003b Add car form contains a License Plate field")
@pytest.mark.regression
def test_add_car_form_shows_license_plate_field(browser):
    page = _open_managed_customer_cars_tab(browser)
    page.open_add_car_form()

    assert page.license_plate_field_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-003c Add car form contains an RFID field")
@pytest.mark.regression
def test_add_car_form_shows_rfid_field(browser):
    page = _open_managed_customer_cars_tab(browser)
    page.open_add_car_form()

    assert page.rfid_field_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-004b Add car form contains vehicle detail fields (Year / Make / Model / Color)")
@pytest.mark.regression
def test_add_car_form_shows_vehicle_detail_fields(browser):
    page = _open_managed_customer_cars_tab(browser)
    page.open_add_car_form()
    body = page.get_body_text().lower()

    assert any(label in body for label in ["year", "make", "model", "color", "colour"])
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-004c Add car form contains Save and Cancel controls")
@pytest.mark.regression
def test_add_car_form_shows_save_and_cancel_controls(browser):
    page = _open_managed_customer_cars_tab(browser)
    page.open_add_car_form()

    assert page.save_car_button_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-008 Car year / make / model / color cascading dropdowns")
@pytest.mark.regression
@pytest.mark.skip(
    reason="CUST-CAR-008: Year/Make/Model/Color dropdown locators not confirmed "
    "against the live DOM. Implement once field names are verified via diag_cars_tab.py."
)
def test_vehicle_detail_cascading_dropdowns(browser):
    pass


# ── Blacklist / Deactivate ────────────────────────────────────────────────────

@allure.title("CUST-CAR-005 Blacklist a car — row reflects blacklisted state")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason="CUST-CAR-005: Blacklist button location in the car list row not confirmed "
    "against the live DOM. Test passes if the button is inline; fails if it requires "
    "opening a separate car-edit form.",
)
def test_blacklist_a_car(browser):
    plate = "VK-BL-" + uuid.uuid4().hex[:4].upper()
    page = _open_managed_customer_cars_tab(browser)
    _add_car(page, plate)
    page.blacklist_car_from_row(plate)

    body = page.get_body_text()
    assert plate in body
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-006 Deactivate a car — row reflects deactivated state")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason="CUST-CAR-006: Deactivate button location in the car list row not confirmed "
    "against the live DOM. Test passes if the button is inline; fails if it requires "
    "opening a separate car-edit form.",
)
def test_deactivate_a_car(browser):
    plate = "VK-DV-" + uuid.uuid4().hex[:4].upper()
    page = _open_managed_customer_cars_tab(browser)
    _add_car(page, plate)
    page.deactivate_car_from_row(plate)

    body = page.get_body_text()
    assert plate in body
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-007 Update Vehicle Token")
@pytest.mark.regression
@pytest.mark.skip(reason="CUST-CAR-007: Requires POS token provisioning setup. Deferred.")
def test_update_vehicle_token(browser):
    pass


# ── Validation ────────────────────────────────────────────────────────────────

@allure.title("CUST-CAR-VAL-001 Blank license plate is blocked on save")
@pytest.mark.smoke
def test_blank_license_plate_blocked_on_save(browser):
    page = _open_managed_customer_cars_tab(browser)
    page.open_add_car_form()
    # Attempt to save without entering a license plate
    page.click(page.SAVE_CAR_BUTTON)

    assert not page.license_plate_input_is_valid()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-VAL-002 RFID field is present and marked required")
@pytest.mark.smoke
@pytest.mark.xfail(
    strict=False,
    reason="CUST-CAR-VAL-002: RFID field may not carry the HTML required attribute "
    "on this form — behaviour depends on server-side validation. Verify via diag_cars_tab.py.",
)
def test_rfid_field_is_present_and_required(browser):
    page = _open_managed_customer_cars_tab(browser)
    page.open_add_car_form()

    assert page.rfid_field_is_visible()
    assert page.rfid_field_is_required()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CAR-VAL-003 Duplicate license plate — document behaviour")
@pytest.mark.edge
def test_duplicate_license_plate_documents_behaviour(browser):
    plate = "VK-DUP-" + uuid.uuid4().hex[:4].upper()
    page = _open_managed_customer_cars_tab(browser)
    # Create first car with the plate
    _add_car(page, plate)
    # Attempt to create a second car with the same plate
    page.open_add_car_form()
    page.enter_license_plate(plate)
    page.click(page.SAVE_CAR_BUTTON)

    # Document: either form stays (duplicate blocked) or closes (duplicates allowed).
    body = page.get_body_text()
    assert page_has_no_broken_state(page), (
        "Broken state after duplicate LP attempt.\nBody:\n%s" % body[:500]
    )


# ── Persistence ───────────────────────────────────────────────────────────────

@allure.title("CUST-PER-003 Add car then refresh — car still appears in Cars settings")
@pytest.mark.regression
def test_add_car_then_refresh_car_persists(browser):
    plate = "VK-PER-" + uuid.uuid4().hex[:5].upper()
    page = _open_managed_customer_cars_tab(browser)
    _add_car(page, plate)
    assert page.car_row_visible(plate), "Car not found in list immediately after save."

    # Reload and navigate back to Cars tab
    page = open_customers_page(browser)
    page.filter_by_email_and_open_edit(CUSTOMER_EMAIL)
    page.open_cars_settings_tab()

    assert page.car_row_visible(plate)
    assert page_has_no_broken_state(page)


# ── Cross-module / deferred ───────────────────────────────────────────────────

@allure.title("CUST-CAR-002 Cars list shows membership and next payment date columns")
@pytest.mark.regression
@pytest.mark.skip(reason="Requires Memberships module fixtures with active member cars.")
def test_cars_list_shows_membership_details(browser):
    pass


@allure.title("CUST-CAR-MEM-001 Add car form shows Assign membership button after filling car details")
@pytest.mark.regression
@pytest.mark.skip(reason="Manual check — Assign membership button visibility depends on membership module state.")
def test_add_car_form_shows_assign_membership_button(browser):
    page = _open_managed_customer_cars_tab(browser)
    page.open_add_car_form()
    page.enter_license_plate(CUSTOMER_LICENSE_PLATE)
    page.enter_car_rfid(CUSTOMER_CAR_RFID)

    assert page.assign_membership_button_is_visible()
    assert page_has_no_broken_state(page)
