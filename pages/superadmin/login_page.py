from urllib.parse import urlparse

from selenium.webdriver.common.by import By

from pages.common.base_page import BasePage
from core.config_manager import ConfigManager


class LoginPage(BasePage):

    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")

    # Overview page title
    OVERVIEW_TITLE = (By.XPATH,"//div[text()='Overview']")

    # Header gear menu → "Log out" (an <li>, not a button/link)
    SETTINGS_MENU_BUTTON = (
        By.XPATH, "//button[.//*[name()='svg' and contains(@class,'lucide-settings')]]"
    )
    LOGOUT_ITEM = (By.XPATH, "//li[normalize-space()='Log out']")

    # Backend rejection message (the API answers HTTP 200 with statusCode 401)
    INVALID_CREDENTIALS_TEXT = "User login/password is incorrect."

    def __init__(self, driver):

        super().__init__(driver)

        # Load configuration data.
        self.config = ConfigManager()

    def open(self):

        # Open SuperAdmin login page.
        self.driver.get(
            self.config.get_url("superadmin")
        )

    def enter_email(self, email):

        # Enter email address.
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):

        # Enter password.
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):

        # Click login button.
        self.click(self.LOGIN_BUTTON)

    def get_overview_text(self):
        # Get Overview page title text.
        return self.get_text(self.OVERVIEW_TITLE)

    def login(self, attempts=3):
        """Log in with the configured superadmin account.

        A submit that lands before the React form is ready leaves the browser
        sitting on /login with no error (seen on CI). Confirm the redirect and
        retry from a fresh /login instead of letting the caller time out.
        """
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.support.ui import WebDriverWait

        for attempt in range(attempts):
            print("Entering email...")
            self.enter_email(
            self.config.get_username("superadmin")
        )

            print("Entering password...")
            self.enter_password(
            self.config.get_password("superadmin")
        )

            print("Clicking login button...")
            self.click_login()

            try:
                WebDriverWait(self.driver, 20).until(
                    lambda d: "/login" not in d.current_url
                )
                return
            except TimeoutException:
                if attempt == attempts - 1:
                    return  # caller's own wait reports the failure
                print("Still on /login after submit — retrying login...")
                self.open()

    def base_url(self):
        """SuperAdmin origin (scheme + host) for the active environment."""
        parsed = urlparse(self.config.get_url("superadmin"))
        return "%s://%s" % (parsed.scheme, parsed.netloc)

    def wait_for_overview(self, timeout=60):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.OVERVIEW_TITLE)
        )

    def is_login_successful(self):

        current_url = self.driver.current_url

        overview_text = self.get_overview_text()

        return (
            current_url.rstrip("/") == self.base_url()
            and overview_text == "Overview"
    )

    # ── Session / negative-path helpers ───────────────────────────────────────

    def login_with(self, email, password):
        """Submit arbitrary credentials once (no retry — for negative tests)."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def is_on_login_page(self):
        return "/login" in self.driver.current_url

    def stays_on_login(self, seconds=5):
        """True if the browser is still on /login after ``seconds`` — i.e. the
        submit did not authenticate."""
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.support.ui import WebDriverWait
        try:
            WebDriverWait(self.driver, seconds).until(lambda d: "/login" not in d.current_url)
            return False
        except TimeoutException:
            return True

    def wait_for_page_text(self, text, timeout=10):
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.support.ui import WebDriverWait
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: text in d.find_element(By.TAG_NAME, "body").text
            )
            return True
        except TimeoutException:
            return False

    def email_field_is_valid(self):
        """HTML5 constraint validity of the email input (type=email)."""
        el = self.driver.find_element(*self.EMAIL_INPUT)
        return self.driver.execute_script("return arguments[0].validity.valid;", el)

    def has_session_token(self):
        return bool(self.driver.execute_script(
            "try { return !!JSON.parse(JSON.parse(localStorage.getItem('persist:root'))"
            ".authSessionReducer).accessToken; } catch (e) { return false; }"
        ))

    def logout(self):
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        self.click(self.SETTINGS_MENU_BUTTON)
        self.click(self.LOGOUT_ITEM)
        WebDriverWait(self.driver, 15).until(EC.url_contains("/login"))
        # The persisted session is cleared asynchronously after the redirect;
        # wait for it so callers observe the final logged-out state.
        WebDriverWait(self.driver, 10).until(lambda d: not self.has_session_token())
