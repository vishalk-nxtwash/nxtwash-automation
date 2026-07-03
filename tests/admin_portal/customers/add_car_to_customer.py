"""
One-time setup: adds car "vk test car 7" (plate=07, rfid=VK-CAR7) to the managed
test customer.  Run once after create_test_customer.py.

  venv/bin/pytest tests/admin_portal/customers/add_car_to_customer.py -v -s
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.admin_portal.customers.conftest import (
    CUSTOMER_FIRST,
    CUSTOMER_LAST,
    CUSTOMER_LICENSE_PLATE,
    CUSTOMER_CAR_RFID,
    create_customer_if_missing,
    open_customers_page,
)

CAR_NAME = "vk test car 7"    # informational label only (no dedicated name field)
PLATE = CUSTOMER_LICENSE_PLATE  # "07"
RFID = CUSTOMER_CAR_RFID        # "VK-CAR7"


def test_add_car_to_managed_customer(browser):
    create_customer_if_missing(browser)
    page = open_customers_page(browser)

    # 1. Find and open the managed customer for edit.
    page.open_filter_panel()
    page.filter_by_first_name(CUSTOMER_FIRST)
    page.filter_by_last_name(CUSTOMER_LAST)
    page.apply_filters()
    page.open_edit_customer_from_row(CUSTOMER_LAST)

    # 2. Open the Cars settings tab.
    page.open_cars_settings_tab()

    # 3. Check whether this car already exists (idempotent).
    body = page.get_body_text()
    if PLATE in body:
        print(f"\n[INFO] Car with plate '{PLATE}' already exists — skipping creation.")
        return

    # 4. Click '+ Add car' — opens /cars/new iframe.
    page.open_add_car_form()

    # 5. Fill in the required fields using the JS React setter so onChange fires.
    plate_el = page.wait.until(EC.visibility_of_element_located(page.LICENSE_PLATE_INPUT))
    page._set_input_value(plate_el, PLATE)
    rfid_el = page.wait.until(EC.visibility_of_element_located(page.CAR_RFID_INPUT))
    page._set_input_value(rfid_el, RFID)

    # Confirm values were accepted before submitting.
    plate_val = plate_el.get_attribute("value")
    rfid_val = rfid_el.get_attribute("value")
    print(f"\n[DEBUG] plate input value={plate_val!r}  rfid input value={rfid_val!r}")
    assert plate_val == PLATE, f"Plate input not set — got {plate_val!r}"
    assert rfid_val == RFID,   f"RFID input not set — got {rfid_val!r}"

    # 6. Save.
    page.click_save_car()

    # 7. Verify the car appears in the cars list (back in the edit iframe).
    page.open_cars_settings_tab()
    body = page.get_body_text()
    assert PLATE in body, (
        f"Car with plate '{PLATE}' not found in Cars list after saving.\n"
        f"Body:\n{body[:500]}"
    )
    print(f"\n[OK] Car '{CAR_NAME}' (plate={PLATE}, rfid={RFID}) added successfully.")
