from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.config_manager import ConfigManager
from pages.common.base_page import BasePage


class LoginPage(BasePage):

    PORTAL = "superadmin"

    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    LOGO_IMAGE = (By.XPATH, "//img[@alt='logo']")
    LOGIN_TITLE = (By.XPATH, "//*[normalize-space()='Log in']")
    EMAIL_LABEL = (By.XPATH, "//*[normalize-space()='Email']")
    PASSWORD_LABEL = (By.XPATH, "//*[normalize-space()='Password']")
    FOOTER_TEXT = (By.XPATH, "//*[contains(normalize-space(),'NxtWash LLC')]")
    PASSWORD_VISIBILITY_BUTTON = (
        By.XPATH,
        "//input[@name='password']/following::div["
        ".//*[local-name()='svg' and contains(@class,'lucide-eye')]][1]",
    )
    OVERVIEW_TITLE = (By.XPATH, "//*[normalize-space()='Overview']")

    ERROR_TEXTS = [
        "invalid",
        "incorrect",
        "unauthorized",
        "required",
        "email",
        "password",
    ]

    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigManager()

    # ── Navigation ───────────────────────────────────────────────────────────

    def open(self):
        """Open the Superadmin login page."""
        self.driver.get(self.config.get_url(self.PORTAL))

    def open_protected_url(self):
        """Navigate directly to the Superadmin root without auth."""
        self.driver.get(self.base_url() + "/")

    def open_login_url(self):
        """Navigate directly to the Superadmin login URL."""
        self.driver.get(self.config.get_url(self.PORTAL))

    def base_url(self):
        """Superadmin origin (scheme + host) for the active environment."""
        parsed = urlparse(self.config.get_url(self.PORTAL))
        return "%s://%s" % (parsed.scheme, parsed.netloc)

    # ── Waits ────────────────────────────────────────────────────────────────

    def wait_for_loaded(self):
        """Wait until the Superadmin login form is fully rendered."""
        long_wait = WebDriverWait(self.driver, 60)
        long_wait.until(lambda d: "/login" in d.current_url)
        long_wait.until(EC.visibility_of_element_located(self.LOGIN_TITLE))
        long_wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        long_wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        long_wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))

    def wait_for_overview(self):
        """Wait until the Superadmin overview page is visible after login."""
        long_wait = WebDriverWait(self.driver, 60)
        long_wait.until(lambda d: "/login" not in d.current_url)
        long_wait.until(EC.visibility_of_element_located(self.OVERVIEW_TITLE))

    def wait_for_login_failure(self):
        """Confirm the driver is still on the login page after a failed attempt."""
        WebDriverWait(self.driver, 10).until(
            lambda d: "/login" in d.current_url
        )

    def wait_for_auth_error(self, timeout=10):
        """Wait until a server-side authentication error message is visible."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: bool(self.visible_error_text())
        )

    def wait_until_redirected_away_from_login(self):
        """Wait until the browser has left the login page."""
        WebDriverWait(self.driver, 60).until(
            lambda d: "/login" not in d.current_url
        )

    # ── State checks ─────────────────────────────────────────────────────────

    def is_login_page(self):
        """Return True when the browser is on the Superadmin login page."""
        return "/login" in self.driver.current_url

    def is_login_successful(self):
        """Return True when the post-login overview is visible."""
        return (
            "/login" not in self.driver.current_url
            and self.get_overview_text() == "Overview"
        )

    # ── Interactions ─────────────────────────────────────────────────────────

    def enter_email(self, email):
        """Type into the email field."""
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        """Type into the password field."""
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Click the login submit button."""
        self.click(self.LOGIN_BUTTON)

    def login_with(self, email, password):
        """Submit the login form with the given credentials."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def login(self):
        """Log in using the configured Superadmin credentials."""
        self.login_with(
            self.config.get_username(self.PORTAL),
            self.config.get_password(self.PORTAL),
        )

    def submit_with_enter(self, email, password):
        """Submit the login form using the Enter key from the password field."""
        self.enter_email(email)
        self.enter_password(password)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(Keys.ENTER)

    def toggle_password_visibility(self):
        """Click the password eye-toggle icon."""
        self.click(self.PASSWORD_VISIBILITY_BUTTON)

    # ── Field + page inspection ───────────────────────────────────────────────

    def get_body_text(self):
        """Return all visible text from the page body."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_overview_text(self):
        """Return the Superadmin overview page title text."""
        return self.get_text(self.OVERVIEW_TITLE)

    def get_footer_text(self):
        """Return the login page footer text."""
        return self.get_text(self.FOOTER_TEXT)

    def get_email_placeholder(self):
        """Return the email field placeholder attribute."""
        return self.driver.find_element(*self.EMAIL_INPUT).get_attribute("placeholder")

    def email_field_is_visible(self):
        return self.driver.find_element(*self.EMAIL_INPUT).is_displayed()

    def email_field_is_enabled(self):
        return self.driver.find_element(*self.EMAIL_INPUT).is_enabled()

    def password_field_is_visible(self):
        return self.driver.find_element(*self.PASSWORD_INPUT).is_displayed()

    def password_field_is_enabled(self):
        return self.driver.find_element(*self.PASSWORD_INPUT).is_enabled()

    def login_button_is_visible(self):
        return self.driver.find_element(*self.LOGIN_BUTTON).is_displayed()

    def login_button_is_enabled(self):
        return self.driver.find_element(*self.LOGIN_BUTTON).is_enabled()

    def email_label_is_visible(self):
        return self.driver.find_element(*self.EMAIL_LABEL).is_displayed()

    def password_label_is_visible(self):
        return self.driver.find_element(*self.PASSWORD_LABEL).is_displayed()

    def logo_is_visible(self):
        """Return True if the NxtWash logo image is visible on the login page."""
        try:
            el = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.LOGO_IMAGE)
            )
            return el.is_displayed()
        except Exception:
            return False

    def get_logo_src(self):
        """Return the logo image src attribute."""
        return self.driver.find_element(*self.LOGO_IMAGE).get_attribute("src")

    def password_input_type(self):
        """Return the password field type attribute ('password' or 'text')."""
        return self.driver.find_element(*self.PASSWORD_INPUT).get_attribute("type")

    def password_visibility_toggle_exists(self):
        """Return True if a password eye-toggle button is present in the DOM."""
        return len(self.driver.find_elements(*self.PASSWORD_VISIBILITY_BUTTON)) > 0

    def visible_error_text(self):
        """Return visible page text if any known auth-error keyword is present."""
        try:
            body = self.get_body_text().lower()
            if any(kw in body for kw in self.ERROR_TEXTS):
                return body[:600]
        except Exception:
            pass
        return ""

    def authenticated_session_is_stored(self):
        """Return True if localStorage holds an active authenticated session."""
        return self.driver.execute_script(
            """
            const root = window.localStorage.getItem('persist:root');
            if (!root) return false;
            try {
                const persisted = JSON.parse(root);
                const auth = JSON.parse(persisted.authSessionReducer || '{}');
                return auth.isAuthorized === true && Boolean(auth.accessToken);
            } catch (e) {
                return false;
            }
            """
        )
