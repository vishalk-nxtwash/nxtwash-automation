from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class EditCompanyPage(BasePage):

    # ── Page chrome ───────────────────────────────────────────────────────────
    PAGE_TITLE = (By.XPATH, "//div[normalize-space()='Company']")
    EDIT_MODE_LABEL = (By.XPATH, "//div[normalize-space()='Edit']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    SAVE_CHANGES_BUTTON = (By.XPATH, "//button[normalize-space()='Save changes']")
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space()='Yes']")
    CONFIRM_NO_BUTTON = (By.XPATH, "//button[normalize-space()='No']")

    # ── Base settings fields ──────────────────────────────────────────────────
    COMPANY_NAME_INPUT = (By.NAME, "companyName")
    EMAIL_INPUT = (By.NAME, "email")
    PHONE_INPUT = (By.NAME, "phone")

    # ── Location fields ───────────────────────────────────────────────────────
    ADDRESS1_INPUT = (By.NAME, "address1")
    ADDRESS2_INPUT = (By.NAME, "address2")
    ZIP_INPUT = (By.NAME, "zip")

    # ── Location dropdowns (React-Select, label-relative) ─────────────────────
    _COUNTRY_CTRL = (
        By.XPATH,
        "//*[normalize-space(text())='Country']/following::*[contains(@class,'control')][1]",
    )
    _STATE_CTRL = (
        By.XPATH,
        "//*[normalize-space(text())='State']/following::*[contains(@class,'control')][1]",
    )
    _CITY_CTRL = (
        By.XPATH,
        "//*[normalize-space(text())='City']/following::*[contains(@class,'control')][1]",
    )
    _TIMEZONE_CTRL = (
        By.XPATH,
        "//*[normalize-space(text())='Timezone']/following::*[contains(@class,'control')][1]",
    )

    # ── Misc base form fields ─────────────────────────────────────────────────
    TERMS_CONDITION_TEXTAREA = (By.NAME, "termsCondition")
    PRIVACY_POLICY_TEXTAREA = (By.NAME, "privacyPolicyText")

    # ── Edit-only fields ──────────────────────────────────────────────────────
    LOGO_UPLOAD = (By.XPATH, "//input[@type='file']")

    # ── Fields absent in edit mode ────────────────────────────────────────────
    DATABASE_INPUT = (
        By.XPATH,
        "//*[normalize-space(text())='Database']/following::*[contains(@class,'control')][1]",
    )
    SITE_NAME_INPUT = (By.NAME, "siteName")
    PASSWORD_INPUT = (By.NAME, "password")

    # ── Config section ────────────────────────────────────────────────────────
    GAS_PUMP_TOGGLE = (
        By.XPATH,
        "//*[contains(normalize-space(),'Gas Pump')]/following::*[@role='switch' or @type='checkbox'][1]",
    )
    AWARD_POINTS_TOGGLE = (
        By.XPATH,
        "//*[contains(normalize-space(),'Award Points') or contains(normalize-space(),'award points')]"
        "/following::*[@role='switch' or @type='checkbox'][1]",
    )
    SMS_MARKETING_TOGGLE = (
        By.XPATH,
        "//*[contains(normalize-space(),'SMS') and contains(normalize-space(),'marketing')]"
        "/following::*[@role='switch' or @type='checkbox'][1]",
    )
    SMS_COUNT_FIELD = (
        By.XPATH,
        "//input[@name='smsCount' or @name='sms_count' or @placeholder[contains(.,'count')]]",
    )
    OPT_IN_LANGUAGE_FIELD = (
        By.XPATH,
        "//textarea[@name='optInLanguage' or @name='opt_in_language'] | "
        "//input[@name='optInLanguage']",
    )

    # ── Public settings ───────────────────────────────────────────────────────
    _DEFAULT_LANGUAGE_CTRL = (
        By.XPATH,
        "//*[contains(normalize-space(),'Default language') or "
        "contains(normalize-space(),'default language')]"
        "/following::*[contains(@class,'control')][1]",
    )

    # ── Waits ─────────────────────────────────────────────────────────────────

    def wait_for_loaded(self, company_name):
        """Wait until the edit form has finished hydrating values."""
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.visibility_of_element_located(self.EDIT_MODE_LABEL))
        self.wait.until(
            EC.text_to_be_present_in_element_value(
                self.COMPANY_NAME_INPUT, company_name
            )
        )
        self.wait.until(
            EC.visibility_of_element_located(self.TERMS_CONDITION_TEXTAREA)
        )

    def wait_for_confirmation_closed(self):
        self.wait.until(EC.invisibility_of_element_located(self.CONFIRM_YES_BUTTON))

    def wait_for_terms_condition(self, value):
        self.wait.until(
            EC.text_to_be_present_in_element_value(self.TERMS_CONDITION_TEXTAREA, value)
        )

    # ── State ─────────────────────────────────────────────────────────────────

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def logo_upload_is_visible(self):
        return len(self.driver.find_elements(*self.LOGO_UPLOAD)) > 0

    def database_field_is_hidden(self):
        return len(self.driver.find_elements(*self.DATABASE_INPUT)) == 0

    def site_name_field_is_hidden(self):
        return len(self.driver.find_elements(*self.SITE_NAME_INPUT)) == 0

    def password_field_is_hidden(self):
        return len(self.driver.find_elements(*self.PASSWORD_INPUT)) == 0

    def has_validation_error(self):
        body = self.get_body_text().lower()
        return any(kw in body for kw in ("required", "invalid", "must be"))

    # ── Field getters ─────────────────────────────────────────────────────────

    def get_company_name(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.COMPANY_NAME_INPUT)
        ).get_attribute("value")

    def get_email(self):
        return self.driver.find_element(*self.EMAIL_INPUT).get_attribute("value")

    def get_phone(self):
        return self.driver.find_element(*self.PHONE_INPUT).get_attribute("value")

    def get_address1(self):
        return self.driver.find_element(*self.ADDRESS1_INPUT).get_attribute("value")

    def get_zip(self):
        return self.driver.find_element(*self.ZIP_INPUT).get_attribute("value")

    def get_terms_condition(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.TERMS_CONDITION_TEXTAREA)
        ).get_attribute("value")

    # ── Field setters ─────────────────────────────────────────────────────────

    def _clear_and_type(self, locator, value):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.BACKSPACE)
        el.send_keys(value)

    def set_company_name(self, name):
        self._clear_and_type(self.COMPANY_NAME_INPUT, name)

    def set_email(self, email):
        self._clear_and_type(self.EMAIL_INPUT, email)

    def set_phone(self, phone):
        self._clear_and_type(self.PHONE_INPUT, phone)

    def set_address1(self, address):
        self._clear_and_type(self.ADDRESS1_INPUT, address)

    def set_zip(self, zip_code):
        self._clear_and_type(self.ZIP_INPUT, zip_code)

    def set_terms_condition(self, value):
        element = self.wait.until(
            EC.visibility_of_element_located(self.TERMS_CONDITION_TEXTAREA)
        )
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(value)

    def clear_company_name(self):
        """Clear the company name field entirely."""
        el = self.driver.find_element(*self.COMPANY_NAME_INPUT)
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.BACKSPACE)

    def clear_email(self):
        el = self.driver.find_element(*self.EMAIL_INPUT)
        el.send_keys(Keys.CONTROL, "a")
        el.send_keys(Keys.BACKSPACE)

    def select_country(self, country):
        self.select_react_dropdown_option(self._COUNTRY_CTRL, country)

    def select_state(self, state):
        self.select_react_dropdown_option(self._STATE_CTRL, state)

    def select_city(self, city):
        self.select_react_dropdown_option(self._CITY_CTRL, city)

    # ── Actions ───────────────────────────────────────────────────────────────

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)

    def click_save_changes(self):
        self.click(self.SAVE_CHANGES_BUTTON)

    def confirm_yes(self):
        self.click(self.CONFIRM_YES_BUTTON)

    def confirm_no(self):
        self.click(self.CONFIRM_NO_BUTTON)

    # ── Config section ────────────────────────────────────────────────────────

    def accordion_button(self, section_name):
        return (
            By.XPATH,
            f"//button[contains(normalize-space(),'{section_name}')] | "
            f"//summary[contains(normalize-space(),'{section_name}')]",
        )

    def expand_accordion(self, section_name):
        """Click an accordion header to expand it."""
        self.click(self.accordion_button(section_name))

    def accordion_section_is_visible(self, section_name):
        """Return True if an accordion button/header for section_name exists."""
        return (
            len(self.driver.find_elements(*self.accordion_button(section_name))) > 0
        )

    def _toggle_state(self, locator):
        """Return True if the toggle/switch is currently ON."""
        el = self.driver.find_element(*locator)
        aria = el.get_attribute("aria-checked")
        if aria is not None:
            return aria == "true"
        return el.is_selected()

    def get_gas_pump_toggle_state(self):
        return self._toggle_state(self.GAS_PUMP_TOGGLE)

    def toggle_gas_pump(self):
        self.click(self.GAS_PUMP_TOGGLE)

    def get_award_points_toggle_state(self):
        return self._toggle_state(self.AWARD_POINTS_TOGGLE)

    def toggle_award_points(self):
        self.click(self.AWARD_POINTS_TOGGLE)

    def get_sms_marketing_state(self):
        return self._toggle_state(self.SMS_MARKETING_TOGGLE)

    def toggle_sms_marketing(self):
        self.click(self.SMS_MARKETING_TOGGLE)

    def sms_count_field_is_visible(self):
        return len(self.driver.find_elements(*self.SMS_COUNT_FIELD)) > 0

    def opt_in_language_field_is_visible(self):
        return len(self.driver.find_elements(*self.OPT_IN_LANGUAGE_FIELD)) > 0

    # ── Public settings ───────────────────────────────────────────────────────

    def get_default_language(self):
        """Return the currently selected default language."""
        try:
            ctrl = self.driver.find_element(*self._DEFAULT_LANGUAGE_CTRL)
            return ctrl.text.strip()
        except Exception:
            return None

    def set_default_language(self, language):
        self.select_react_dropdown_option(self._DEFAULT_LANGUAGE_CTRL, language)
