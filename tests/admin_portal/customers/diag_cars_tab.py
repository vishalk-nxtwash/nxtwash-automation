"""
Diagnostic — opens add car form, switches to the /cars/new iframe, dumps fields.
Run:  venv/bin/pytest tests/admin_portal/customers/diag_cars_tab.py -v -s
"""
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.admin_portal.customers.conftest import (
    CUSTOMER_FIRST,
    CUSTOMER_LAST,
    create_customer_if_missing,
    open_customers_page,
)


def test_dump_car_form_iframe(browser):
    create_customer_if_missing(browser)
    page = open_customers_page(browser)
    page.open_filter_panel()
    page.filter_by_first_name(CUSTOMER_FIRST)
    page.filter_by_last_name(CUSTOMER_LAST)
    page.apply_filters()
    page.open_edit_customer_from_row(CUSTOMER_LAST)

    wait = WebDriverWait(browser, 20)

    # Click Cars settings tab
    cars_tab = wait.until(EC.element_to_be_clickable(page.CARS_SETTINGS_TAB))
    browser.execute_script("arguments[0].click();", cars_tab)
    time.sleep(1.5)

    # Click '+ Add car'
    add_car_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[contains(normalize-space(),'Add') and contains(normalize-space(),'car')"
        " and not(contains(normalize-space(),'settings'))]",
    )))
    browser.execute_script("arguments[0].click();", add_car_btn)
    time.sleep(2)

    # Switch back to top level and find the new iframe
    browser.switch_to.default_content()
    iframes = browser.find_elements(By.TAG_NAME, "iframe")
    print(f"\n=== IFRAMES AFTER CLICKING + ADD CAR ({len(iframes)} found) ===")
    for i, f in enumerate(iframes):
        print(f"  [{i}] src={f.get_attribute('src')!r}")

    # Switch to the /cars/new iframe
    car_frame = None
    for f in iframes:
        src = f.get_attribute("src") or ""
        if "/cars/new" in src or "/cars/" in src:
            car_frame = f
            break

    if not car_frame and iframes:
        car_frame = iframes[0]

    browser.switch_to.frame(car_frame)
    time.sleep(1)

    print("\n=== BODY IN CAR FORM IFRAME ===")
    print(browser.find_element(By.TAG_NAME, "body").text[:3000])

    inputs = browser.find_elements(By.TAG_NAME, "input")
    print(f"\n=== INPUTS ({len(inputs)} found) ===")
    for inp in inputs:
        try:
            print(f"  name={inp.get_attribute('name')!r}  "
                  f"type={inp.get_attribute('type')!r}  "
                  f"placeholder={inp.get_attribute('placeholder')!r}  "
                  f"required={inp.get_attribute('required')!r}  "
                  f"visible={inp.is_displayed()}")
        except Exception:
            pass

    buttons = browser.find_elements(By.TAG_NAME, "button")
    print(f"\n=== BUTTONS ({len(buttons)} found) ===")
    for b in buttons:
        try:
            if b.is_displayed():
                print(f"  text={b.text.strip()!r}  type={b.get_attribute('type')!r}")
        except Exception:
            pass

    assert True
