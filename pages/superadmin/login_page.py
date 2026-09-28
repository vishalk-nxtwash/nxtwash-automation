from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage
from core.config_manager import ConfigManager


class LoginPage(BasePage):

    EMAIL_INPUT    = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON   = (By.XPATH, "//button[@type='submit']")
    OVERVIEW_TITLE = (By.XPATH, "//div[text()='Overview']")

    # ── UI element locators ──────────────────────────────────────────────────
    LOGO = (By.XPATH,
        "//img[contains(@alt,'NxtWash') or contains(@alt,'logo')"
        " or contains(@alt,'nxtwash') or contains(@src,'logo')]")
    HEADING = (By.XPATH,
        "//*[normalize-space()='Log in'"
        " or normalize-space()='Login'"
        " or normalize-space()='Sign in']")
    EMAIL_LABEL = (By.XPATH, "//label[contains(normalize-space(),'Email')]")
    PASSWORD_LABEL = (By.XPATH,
        "//label[contains(normalize-space(),'Password')"
        " and not(contains(normalize-space(),'Confirm'))]")
    FOOTER_COPYRIGHT = (By.XPATH,
        "//*[contains(text(),'NxtWash')"
        " and (contains(text(),'LLC') or contains(text(),'©'))]")
    AUTH_ERROR = (By.XPATH,
        "//*[@role='alert' and string-length(normalize-space())>0]")

    # Header gear menu → "Log out" (an <li>, not a button/link)
    SETTINGS_MENU_BUTTON = (
        By.XPATH, "//button[.//*[name()='svg' and contains(@class,'lucide-settings')]]"
    )
    LOGOUT_ITEM = (By.XPATH, "//li[normalize-space()='Log out']")

    # Backend rejection message (the API answers HTTP 200 with statusCode 401)
    INVALID_CREDENTIALS_TEXT = "User login/password is incorrect."

    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigManager()

    def open(self):
        """Open the SuperAdmin login page.

        On a shared EC2 host, several shards start ~12 Chrome instances at
        once and the first navigation of a fresh browser can exceed the page
        load timeout ("Timed out receiving message from renderer"). Stop the
        stalled load and retry once instead of failing the test.
        """
        from selenium.common.exceptions import TimeoutException

        url = self.config.get_url("superadmin")
        try:
            self.driver.get(url)
        except TimeoutException:
            print("Login page load timed out — retrying once...")
            try:
                self.driver.execute_script("window.stop();")
            except Exception:  # noqa: BLE001 — renderer may still be busy
                pass
            self.driver.get(url)

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_email_native(self, email):
        """Enter email via native send_keys — triggers browser-level type=email validation."""
        el = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.EMAIL_INPUT)
        )
        el.clear()
        el.send_keys(email)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(self.LOGIN_BUTTON)

    def login_with_enter_key(self, email=None, password=None):
        """Fill credentials and submit by pressing Enter on the password field."""
        email    = email    or self.config.get_username("superadmin")
        password = password or self.config.get_password("superadmin")
        self.enter_email(email)
        el = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PASSWORD_INPUT)
        )
        el.clear()
        el.send_keys(password)
        el.send_keys(Keys.RETURN)

    def login(self, attempts=3):
        """Log in with the configured superadmin account.

        A submit that lands before the React form is ready leaves the browser
        sitting on /login with no error (seen on CI). Confirm the redirect and
        retry from a fresh /login instead of letting the caller time out.
        """
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.support.ui import WebDriverWait

        for attempt in range(attempts):
            self.enter_email(self.config.get_username("superadmin"))
            self.enter_password(self.config.get_password("superadmin"))
            self.click_login()

            try:
                WebDriverWait(self.driver, 20).until(
                    lambda d: "/login" not in d.current_url
                )
                return
            except TimeoutException:
                if attempt == attempts - 1:
                    return  # caller's own wait reports the failure
                self.open()

    # ── Navigation helpers ────────────────────────────────────────────────────

    def get_overview_text(self):
        return self.get_text(self.OVERVIEW_TITLE)

    def base_url(self):
        parsed = urlparse(self.config.get_url("superadmin"))
        return "%s://%s" % (parsed.scheme, parsed.netloc)

    def wait_for_overview(self, timeout=60):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.OVERVIEW_TITLE)
        )

    def wait_for_loaded(self, timeout=20):
        """Wait for the login form to be fully rendered (submit button clickable)."""
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )

    def is_on_login_page(self):
        return "/login" in self.driver.current_url

    def is_login_successful(self):
        return (
            self.driver.current_url.rstrip("/") == self.base_url()
            and self.get_overview_text() == "Overview"
        )

    # ── Session / negative-path helpers ───────────────────────────────────────

    def login_with(self, email, password):
        """Submit arbitrary credentials once (no retry — for negative tests)."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def stays_on_login(self, seconds=5):
        """True if the browser is still on /login after ``seconds`` — submit did not authenticate."""
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

    # ── Body text helpers ─────────────────────────────────────────────────────

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def body_contains(self, text):
        return text.lower() in self.get_body_text().lower()

    # ── UI visibility helpers ─────────────────────────────────────────────────

    def logo_is_visible(self):
        els = self.driver.find_elements(*self.LOGO)
        return any(e.is_displayed() for e in els)

    def heading_is_visible(self):
        els = self.driver.find_elements(*self.HEADING)
        return any(e.is_displayed() for e in els)

    def get_heading_text(self):
        els = [e for e in self.driver.find_elements(*self.HEADING) if e.is_displayed()]
        return els[0].text.strip() if els else ""

    def email_input_is_visible(self):
        els = self.driver.find_elements(*self.EMAIL_INPUT)
        return any(e.is_displayed() for e in els)

    def email_label_is_visible(self):
        els = self.driver.find_elements(*self.EMAIL_LABEL)
        return any(e.is_displayed() for e in els)

    def password_input_is_visible(self):
        els = self.driver.find_elements(*self.PASSWORD_INPUT)
        return any(e.is_displayed() for e in els)

    def password_label_is_visible(self):
        els = self.driver.find_elements(*self.PASSWORD_LABEL)
        return any(e.is_displayed() for e in els)

    def login_button_is_visible_and_enabled(self):
        els = self.driver.find_elements(*self.LOGIN_BUTTON)
        if not els:
            return False
        btn = els[0]
        return btn.is_displayed() and btn.is_enabled()

    def password_is_masked(self):
        el = self.driver.find_element(*self.PASSWORD_INPUT)
        return el.get_attribute("type") == "password"

    def password_is_revealed(self):
        el = self.driver.find_element(*self.PASSWORD_INPUT)
        return el.get_attribute("type") == "text"

    def footer_is_visible(self):
        els = self.driver.find_elements(*self.FOOTER_COPYRIGHT)
        return any(e.is_displayed() for e in els)

    def get_footer_text(self):
        els = [e for e in self.driver.find_elements(*self.FOOTER_COPYRIGHT) if e.is_displayed()]
        return els[0].text.strip() if els else ""

    def get_email_placeholder(self):
        el = self.driver.find_element(*self.EMAIL_INPUT)
        return el.get_attribute("placeholder") or ""

    # ── Error helpers ─────────────────────────────────────────────────────────

    def auth_error_is_visible(self):
        els = self.driver.find_elements(*self.AUTH_ERROR)
        return any(e.is_displayed() and e.text.strip() for e in els)

    def get_auth_error_text(self):
        els = [e for e in self.driver.find_elements(*self.AUTH_ERROR)
               if e.is_displayed() and e.text.strip()]
        return els[0].text.strip() if els else ""

    def wait_for_auth_error(self, timeout=10):
        """Wait for a server-side auth error after submitting bad credentials."""
        _error_kws = ("invalid", "incorrect", "unauthorized", "error", "wrong")
        WebDriverWait(self.driver, timeout).until(
            lambda d: (
                any(
                    e.is_displayed() and e.text.strip()
                    for e in d.find_elements(*self.AUTH_ERROR)
                )
                or any(
                    kw in d.find_element(By.TAG_NAME, "body").text.lower()
                    for kw in _error_kws
                )
            )
        )
