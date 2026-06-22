from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:

    # Resolve the chromedriver binary once per process and reuse the path.
    # With a function-scoped browser fixture this otherwise runs a version
    # check / download on every single test; cache it so each xdist worker
    # pays the cost at most once.
    _driver_path = None

    @classmethod
    def _chromedriver_path(cls):
        if cls._driver_path is None:
            cls._driver_path = ChromeDriverManager().install()
        return cls._driver_path

    @classmethod
    def get_driver(cls, headless=False, detach=True):

        options = webdriver.ChromeOptions()

        if headless:
            # Headless flags suited for CI / servers without a display.
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-ipc-flooding-protection")
            options.add_argument("--disable-hang-monitor")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-translate")
            options.add_argument("--metrics-recording-only")
            options.add_argument("--mute-audio")
            options.add_argument("--no-first-run")
            options.add_argument("--safebrowsing-disable-auto-update")
        elif detach:
            # Keep the browser open after script execution (local debugging).
            options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(
            service=Service(cls._chromedriver_path()),
            options=options
        )

        if not headless:
            driver.maximize_window()

        return driver
