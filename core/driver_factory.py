from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:

    @staticmethod
    def get_driver(headless=False, detach=True):

        options = webdriver.ChromeOptions()

        if headless:
            # Headless flags suited for CI / servers without a display.
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
        elif detach:
            # Keep the browser open after script execution (local debugging).
            options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=options
        )

        if not headless:
            driver.maximize_window()

        return driver
