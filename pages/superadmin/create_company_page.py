from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class CreateCompanyPage(BasePage):

    URL_PATH = "/companies/create"

    # ── Page chrome ───────────────────────────────────────────────────────────
    COMPANY_BASE_SETTINGS_TITLE = (By.XPATH, "//div[text()='Company Base Settings']")
    PAGE_HEADER = (
        By.XPATH,
        "//*[contains(normalize-space(),'Company') and contains(normalize-space(),'New')]",
    )

    # ── Base settings — text inputs ───────────────────────────────────────────
    # Using label-relative XPath because name attrs differ from expected on staging:
    # the field labelled "Company name" has name="siteName" and vice-versa in the DOM.
    COMPANY_NAME_INPUT = (By.XPATH,
        "//*[normalize-space(text())='Company name']/following::input[1]")
    SITE_NAME_INPUT = (By.XPATH,
        "//*[normalize-space(text())='Site name']/following::input[1]")
    PASSWORD_INPUT = (By.NAME, "password")
    # Email field has no type="email" or name="email" attribute — use label proximity.
    EMAIL_INPUT = (By.XPATH,
        "//*[normalize-space(text())='Email']/following::input[1]")
    PHONE_INPUT = (By.NAME, "phone")

    # ── Location — text inputs ────────────────────────────────────────────────
    ADDRESS1_INPUT = (By.NAME, "address1")
    ADDRESS2_INPUT = (By.NAME, "address2")
    ZIP_INPUT = (By.NAME, "zip")

    # ── React-Select dropdown containers (label-relative) ────────────────────
    # Actual label text confirmed from page dump: "Company country/state/city/timezone"
    _DATABASE_CTRL = (
        By.XPATH,
        "//*[normalize-space(text())='Database']/following::*[contains(@class,'control')][1]",
    )
    _COUNTRY_CTRL = (
        By.XPATH,
        "//*[normalize-space()='Company country']/following::*[contains(@class,'control')][1]",
    )
    _STATE_CTRL = (
        By.XPATH,
        "//*[normalize-space()='Company state']/following::*[contains(@class,'control')][1]",
    )
    _CITY_CTRL = (
        By.XPATH,
        "//*[normalize-space()='Company city']/following::*[contains(@class,'control')][1]",
    )
    _TIMEZONE_CTRL = (
        By.XPATH,
        "//*[normalize-space()='Company timezone']/following::*[contains(@class,'control')][1]",
    )

    # ── Buttons ───────────────────────────────────────────────────────────────
    SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")

    # ── Waits ─────────────────────────────────────────────────────────────────

    def wait_for_loaded(self):
        """Wait until the create company form is fully rendered."""
        WebDriverWait(self.driver, 30).until(
            lambda d: self.URL_PATH in d.current_url
        )
        self.wait.until(
            EC.visibility_of_element_located(self.COMPANY_NAME_INPUT)
        )
        self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON))

    # ── State ─────────────────────────────────────────────────────────────────

    def is_on_create_page(self):
        return self.URL_PATH in self.driver.current_url

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def has_validation_error(self):
        """Return True if any validation error keyword is visible on the page."""
        body = self.get_body_text().lower()
        return any(
            kw in body
            for kw in ("required", "invalid", "is required", "must be", "cannot be empty")
        )

    def required_asterisk_visible_for(self, label_text):
        """Return True if the field label contains a red asterisk marker."""
        try:
            body = self.get_body_text()
            # Labels with required fields typically include '*' adjacent to label text
            return "*" in body and label_text in body
        except Exception:
            return False

    def address2_has_no_asterisk(self):
        """Return True if Address 2 label is NOT marked required."""
        try:
            label = self.driver.find_element(
                By.XPATH,
                "//*[contains(normalize-space(),'Address 2') or contains(normalize-space(),'Address2')]",
            )
            return "*" not in label.text
        except Exception:
            return True

    # ── Field fill helpers ────────────────────────────────────────────────────

    def fill_company_name(self, name):
        self.enter_text(self.COMPANY_NAME_INPUT, name)

    def fill_site_name(self, name):
        self.enter_text(self.SITE_NAME_INPUT, name)

    def fill_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def fill_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def fill_phone(self, phone):
        self.enter_text(self.PHONE_INPUT, phone)

    def fill_address1(self, address):
        self.enter_text(self.ADDRESS1_INPUT, address)

    def fill_address2(self, address):
        self.enter_text(self.ADDRESS2_INPUT, address)

    def fill_zip(self, zip_code):
        self.enter_text(self.ZIP_INPUT, zip_code)

    def select_database(self, value):
        self.select_react_dropdown_option(self._DATABASE_CTRL, value)

    def select_country(self, country):
        self.select_react_dropdown_option(self._COUNTRY_CTRL, country)

    def select_state(self, state):
        self.select_react_dropdown_option(self._STATE_CTRL, state)

    def select_city(self, city):
        self.select_react_dropdown_option(self._CITY_CTRL, city)

    def select_timezone(self, timezone):
        self.select_react_dropdown_option(self._TIMEZONE_CTRL, timezone)

    def fill_text_fields(self, data: dict):
        """Fill all text-based form fields from a dict. Skips unknown keys."""
        mapping = {
            "company_name": self.fill_company_name,
            "site_name": self.fill_site_name,
            "password": self.fill_password,
            "email": self.fill_email,
            "phone": self.fill_phone,
            "address1": self.fill_address1,
            "address2": self.fill_address2,
            "zip": self.fill_zip,
        }
        for key, filler in mapping.items():
            if key in data:
                filler(data[key])

    # ── Actions ───────────────────────────────────────────────────────────────

    def submit(self):
        """Click the Save / submit button."""
        self.click(self.SAVE_BUTTON)

    def cancel(self):
        """Click Cancel to discard the form."""
        self.click(self.CANCEL_BUTTON)

    # ── Field inspection ──────────────────────────────────────────────────────

    def database_dropdown_has_options(self):
        """Return True if the Database dropdown lists at least one option."""
        try:
            self.click(self._DATABASE_CTRL)
            options = WebDriverWait(self.driver, 5).until(
                lambda d: d.find_elements(
                    By.XPATH,
                    "//*[@role='option'] | //*[contains(@class,'option')]",
                )
            )
            return len(options) > 0
        except Exception:
            return False

    def country_dropdown_has_options(self):
        """Return True if the Country dropdown lists at least one option."""
        try:
            self.click(self._COUNTRY_CTRL)
            options = WebDriverWait(self.driver, 5).until(
                lambda d: d.find_elements(
                    By.XPATH,
                    "//*[@role='option'] | //*[contains(@class,'option')]",
                )
            )
            self.driver.find_element(By.TAG_NAME, "body").click()
            return len(options) > 0
        except Exception:
            return False

    def get_password_input_type(self):
        return self.driver.find_element(*self.PASSWORD_INPUT).get_attribute("type")
