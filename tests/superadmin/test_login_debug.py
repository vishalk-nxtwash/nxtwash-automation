from selenium.webdriver.common.by import By
import time

from core.driver_factory import DriverFactory
from core.config_manager import ConfigManager


def test_login_debug():

    config = ConfigManager()

    driver = DriverFactory.get_driver()

    # Open SuperAdmin Login Page
    driver.get(config.get_url("superadmin"))

    print(f"Login Page URL: {driver.current_url}")

    # Enter Email
    driver.find_element(By.NAME, "email").send_keys(
        config.get_username("superadmin")
    )

    # Enter Password
    driver.find_element(By.NAME, "password").send_keys(
        config.get_password("superadmin")
    )

    # Click Login
    driver.find_element(
        By.XPATH,
        "//button[@type='submit']"
    ).click()

    # Wait and observe
    time.sleep(10)

    # Print current URL after login
    print(f"Current URL: {driver.current_url}")

    # Keep browser open
    input("Press Enter to close browser...")

    driver.quit()