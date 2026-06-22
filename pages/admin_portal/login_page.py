from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.config_manager import ConfigManager
from pages.common.base_page import BasePage


class AdminLoginPage(BasePage):

    PORTAL = "admin_portal"

    EMAIL_OR_PHONE_INPUT = (By.NAME, "emailOrPhone")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    LOGO_IMAGE = (By.XPATH, "//img[@alt='logo']")
    FOOTER_TEXT = (
        By.XPATH,
        "//*[contains(normalize-space(),'NxtWash LLC')]"
    )
    PASSWORD_VISIBILITY_BUTTON = (
        By.XPATH,
        "//input[@name='password']/following::div["
        ".//*[local-name()='svg' and contains(@class,'lucide-eye')]][1]"
    )
    OVERVIEW_TITLE = (By.XPATH, "//*[normalize-space()='Overview']")
    LOGIN_TITLE = (By.XPATH, "//*[normalize-space()='Log in']")
    EMAIL_LABEL = (By.XPATH, "//*[normalize-space()='Email']")
    PASSWORD_LABEL = (By.XPATH, "//*[normalize-space()='Password']")
    ERROR_TEXTS = [
        "invalid",
        "incorrect",
        "unauthorized",
        "required",
        "emailorphone",
        "email address",
        "password"
    ]

    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigManager()

    def open(self):
        """Open Admin Portal."""
        self.driver.get(self.config.get_url(self.PORTAL))

    def wait_for_loaded(self):
        """Wait until the Admin login form is visible."""
        long_wait = WebDriverWait(self.driver, 30)

        long_wait.until(lambda driver: "/login" in driver.current_url)
        long_wait.until(EC.visibility_of_element_located(self.LOGIN_TITLE))
        long_wait.until(
            EC.visibility_of_element_located(self.EMAIL_OR_PHONE_INPUT)
        )
        long_wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        long_wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))

    def get_body_text(self):
        """Get visible page text."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def is_login_page(self):
        """Return whether the browser is on the login page."""
        return "/login" in self.driver.current_url

    def logo_is_visible(self):
        """Return whether the logo image is visible."""
        elements = self.driver.find_elements(*self.LOGO_IMAGE)
        return bool(elements) and elements[0].is_displayed()

    def get_logo_src(self):
        """Return login logo image source."""
        return self.driver.find_element(*self.LOGO_IMAGE).get_attribute("src")

    def email_label_is_visible(self):
        """Return whether the email field label is visible."""
        return self.driver.find_element(*self.EMAIL_LABEL).is_displayed()

    def password_label_is_visible(self):
        """Return whether the password field label is visible."""
        return self.driver.find_element(*self.PASSWORD_LABEL).is_displayed()

    def email_field_is_visible(self):
        """Return whether the email or phone field is visible."""
        return self.driver.find_element(*self.EMAIL_OR_PHONE_INPUT).is_displayed()

    def email_field_is_enabled(self):
        """Return whether the email or phone field is enabled."""
        return self.driver.find_element(*self.EMAIL_OR_PHONE_INPUT).is_enabled()

    def password_field_is_visible(self):
        """Return whether the password field is visible."""
        return self.driver.find_element(*self.PASSWORD_INPUT).is_displayed()

    def password_field_is_enabled(self):
        """Return whether the password field is enabled."""
        return self.driver.find_element(*self.PASSWORD_INPUT).is_enabled()

    def login_button_is_visible(self):
        """Return whether the login button is visible."""
        return self.driver.find_element(*self.LOGIN_BUTTON).is_displayed()

    def login_button_is_enabled(self):
        """Return whether the login button is enabled."""
        return self.driver.find_element(*self.LOGIN_BUTTON).is_enabled()

    def get_footer_text(self):
        """Return footer text."""
        return self.get_text(self.FOOTER_TEXT)

    def get_browser_title(self):
        """Return current browser title."""
        return self.driver.title

    def get_email_placeholder(self):
        """Return email or phone field placeholder."""
        return self.driver.find_element(
            *self.EMAIL_OR_PHONE_INPUT
        ).get_attribute("placeholder")

    def get_password_placeholder(self):
        """Return password field placeholder."""
        return self.driver.find_element(
            *self.PASSWORD_INPUT
        ).get_attribute("placeholder")

    def focus_email_field(self):
        """Move focus to email or phone field."""
        self.click(self.EMAIL_OR_PHONE_INPUT)

    def active_element_name(self):
        """Return the focused element name attribute."""
        return self.driver.switch_to.active_element.get_attribute("name")

    def active_element_type(self):
        """Return the focused element type attribute."""
        return self.driver.switch_to.active_element.get_attribute("type")

    def press_tab(self):
        """Press Tab from the currently focused element."""
        self.driver.switch_to.active_element.send_keys(Keys.TAB)

    def enter_email_or_phone(self, email_or_phone):
        """Enter Admin email or phone."""
        self.enter_text(self.EMAIL_OR_PHONE_INPUT, email_or_phone)

    def enter_password(self, password):
        """Enter Admin password."""
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_login(self):
        """Submit Admin login form."""
        self.click(self.LOGIN_BUTTON)

    def login_with(self, email_or_phone, password):
        """Login with supplied credentials."""
        self.enter_email_or_phone(email_or_phone)
        self.enter_password(password)
        self.click_login()

    def login(self):
        """Login with configured Admin credentials."""
        self.login_with(
            self.config.get_username(self.PORTAL),
            self.config.get_password(self.PORTAL)
        )

    def submit_with_enter(self, email_or_phone, password):
        """Submit login form using Enter from password field."""
        self.enter_email_or_phone(email_or_phone)
        self.enter_password(password)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(Keys.ENTER)

    def get_email_value(self):
        """Return email or phone field value."""
        return self.driver.find_element(
            *self.EMAIL_OR_PHONE_INPUT
        ).get_attribute("value")

    def get_password_value(self):
        """Return password field value."""
        return self.driver.find_element(*self.PASSWORD_INPUT).get_attribute(
            "value"
        )

    def get_email_validation_message(self):
        """Return native email field validation message."""
        element = self.driver.find_element(*self.EMAIL_OR_PHONE_INPUT)
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def get_password_validation_message(self):
        """Return native password field validation message."""
        element = self.driver.find_element(*self.PASSWORD_INPUT)
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def visible_error_text(self):
        """Return visible login validation/error text if present."""
        body_text = self.get_body_text()
        lower_body = body_text.lower()
        if any(text in lower_body for text in self.ERROR_TEXTS):
            return body_text
        return ""

    def wait_for_login_failure(self):
        """Wait until login remains on login page after a failed attempt."""
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: "/login" in driver.current_url)

    def wait_for_auth_error(self, timeout=10):
        """Wait until a server-side login error message is visible."""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: bool(self.visible_error_text())
        )

    def password_input_type(self):
        """Return password input type."""
        return self.driver.find_element(*self.PASSWORD_INPUT).get_attribute("type")

    def password_visibility_toggle_exists(self):
        """Return whether a password visibility toggle exists."""
        return len(self.driver.find_elements(*self.PASSWORD_VISIBILITY_BUTTON)) > 0

    def toggle_password_visibility(self):
        """Click password visibility toggle."""
        self.click(self.PASSWORD_VISIBILITY_BUTTON)

    def open_protected_overview(self):
        """Open the protected Admin Overview URL directly.

        Intentionally identical to open() — the portal root is the overview
        page. The distinction is semantic: this method is called after clearing
        auth state to verify the redirect-to-login guard.
        """
        self.driver.get(self.config.get_url(self.PORTAL))

    def open_login_url(self):
        """Open login URL directly."""
        self.driver.get(self.config.get_url(self.PORTAL).rstrip("/") + "/login")

    def open_overview_in_new_tab(self):
        """Open protected Admin Overview in a second browser tab."""
        overview_url = self.config.get_url(self.PORTAL)
        self.driver.execute_script("window.open(arguments[0], '_blank');", overview_url)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def local_storage_auth_keys(self):
        """Return localStorage keys related to auth/session."""
        return self.driver.execute_script(
            """
            return Object.keys(window.localStorage)
                .filter(key => /auth|token|session/i.test(key));
            """
        )

    def authenticated_session_is_stored(self):
        """Return whether persisted localStorage has an authorized session."""
        return self.driver.execute_script(
            """
            const root = window.localStorage.getItem('persist:root');
            if (!root) return false;
            try {
                const persisted = JSON.parse(root);
                const auth = JSON.parse(persisted.authSessionReducer || '{}');
                return auth.isAuthorized === true && Boolean(auth.accessToken);
            } catch (error) {
                return false;
            }
            """
        )

    def wait_for_overview(self):
        """Wait until Admin Portal overview is visible.

        60s (not 30s) so the post-login redirect+render survives a loaded CI
        runner where several headless Chrome instances compete for CPU.
        """
        long_wait = WebDriverWait(self.driver, 60)

        long_wait.until(
            lambda driver: driver.current_url == self.config.get_url(self.PORTAL)
        )
        long_wait.until(EC.visibility_of_element_located(self.OVERVIEW_TITLE))

    def get_overview_text(self):
        """Get Admin overview title text."""
        return self.get_text(self.OVERVIEW_TITLE)

    def wait_until_redirected_away_from_login(self):
        """Wait until browser is no longer on login page."""
        long_wait = WebDriverWait(self.driver, 30)
        long_wait.until(lambda driver: "/login" not in driver.current_url)
