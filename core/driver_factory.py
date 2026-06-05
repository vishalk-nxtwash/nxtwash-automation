from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:

    @staticmethod
    def get_driver():

        options = webdriver.ChromeOptions()

        # Keep browser open after script execution.
        options.add_experimental_option(
            "detach",
            True
        )

        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=options
        )

        driver.maximize_window()

        return driver