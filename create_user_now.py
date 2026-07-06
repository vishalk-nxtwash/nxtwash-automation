"""Create vkuser02@yopmail.com in staging using confirmed field names."""
import os
import sys
import time

os.environ.setdefault("TEST_ENV", "staging")
sys.path.insert(0, os.path.dirname(__file__))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from core.driver_factory import DriverFactory
from tests.admin_portal.admin_session import ensure_admin_logged_in, open_admin_path
from pages.admin_portal.users_page import AdminUsersPage, AdminUserFormPage

EMPLOYEE_NAME = "test user 2"
USER_PASSWORD  = "test"
USER_EMAIL     = "vkuser02@yopmail.com"
USER_PHONE     = "1234567890"
USER_ROLE      = "VK UR01"


def main():
    driver = DriverFactory.get_driver(headless=False)
    driver.set_page_load_timeout(60)
    try:
        ensure_admin_logged_in(driver)

        # Navigate to fresh users list (no filter applied)
        open_admin_path(driver, "/users/users")
        page = AdminUsersPage(driver)
        page.wait_for_loaded()          # switches into LIST_FRAME

        # Click + Add user  (we're inside the list iframe)
        add_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(normalize-space(),'Add user')]"))
        )
        driver.execute_script("arguments[0].click();", add_btn)
        print("Clicked + Add user")

        # Switch to outer page and wait for the create-form iframe
        driver.switch_to.default_content()
        WebDriverWait(driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[contains(@src,'users/users/new') or contains(@src,'users/users/create')]")
            )
        )
        print("Create form iframe loaded")
        time.sleep(1)

        # Instantiate form page (driver is now inside the create iframe)
        form = AdminUserFormPage(driver)

        # 1. Employee
        print("Selecting employee:", EMPLOYEE_NAME)
        form.select_employee(EMPLOYEE_NAME)

        # 2. Password  (name='pass')
        print("Entering password")
        pwd = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='pass' or @name='password']"))
        )
        pwd.click()
        pwd.send_keys(Keys.COMMAND + "a")
        pwd.send_keys(Keys.BACKSPACE)
        pwd.send_keys(USER_PASSWORD)

        # 3. Confirm password  (name='confirmPass')
        print("Entering confirm password")
        cpwd = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@name='confirmPass' or @name='confirmPassword']"))
        )
        cpwd.click()
        cpwd.send_keys(Keys.COMMAND + "a")
        cpwd.send_keys(Keys.BACKSPACE)
        cpwd.send_keys(USER_PASSWORD)

        # 4. Email  (name='emailId')
        print("Entering email:", USER_EMAIL)
        form.enter_email(USER_EMAIL)

        # 5. Phone  (name='phoneNumber')
        print("Entering phone:", USER_PHONE)
        form.enter_phone(USER_PHONE)

        # 6. Role
        print("Selecting role:", USER_ROLE)
        form.select_role(USER_ROLE)

        # 7. Ensure active
        form.ensure_active_switch_on()

        # Print form state before saving
        time.sleep(1)
        body_before = driver.find_element(By.TAG_NAME, "body").text
        print("\n=== Form body before save ===")
        print(body_before[:800])

        # Check input values
        for inp in driver.find_elements(By.XPATH, "//input"):
            print("  input name=%r value=%r" % (
                inp.get_attribute("name"),
                inp.get_attribute("value"),
            ))

        # 8. Save
        print("\nClicking Save user...")
        save_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save user']"))
        )
        driver.execute_script("arguments[0].click();", save_btn)

        time.sleep(4)
        print("URL after save:", driver.current_url)

        # Print form body after save attempt to see validation errors
        try:
            body_after = driver.find_element(By.TAG_NAME, "body").text
            print("\n=== Form body after save ===")
            print(body_after[:800])
        except Exception:
            print("(frame navigated away — save likely succeeded)")

        # Verify on list
        driver.switch_to.default_content()
        open_admin_path(driver, "/users/users")
        page2 = AdminUsersPage(driver)
        page2.wait_for_loaded()
        if page2.user_exists(USER_EMAIL):
            print("\nSUCCESS — user %s created." % USER_EMAIL)
        else:
            print("\nWARNING — user not visible in list (may be inactive or email filter issue).")
            # Check raw body
            driver.switch_to.default_content()
            fr = driver.find_elements("xpath", "//iframe[contains(@src,'users/users')]")
            if fr:
                driver.switch_to.frame(fr[0])
                body = driver.find_element(By.TAG_NAME, "body").text
                if USER_EMAIL in body:
                    print("  (Email IS in page body — filter issue only)")
                else:
                    print("  Email NOT in body. Save may have failed.")
                    print("  Body:", body[:400])

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
