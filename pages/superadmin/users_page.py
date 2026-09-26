from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class UsersPage(BasePage):

    PAGE_TITLE = (By.XPATH, "//div[normalize-space()='Users']")
    ADD_USER_BUTTON = (By.XPATH, "//button[contains(.,'Add User')]")
    FILTER_BUTTON = (By.XPATH, "//button[contains(.,'Filter by')]")

    FIRST_NAME_FILTER = (By.NAME, "firstName")
    LAST_NAME_FILTER = (By.NAME, "lastName")
    EMAIL_FILTER = (By.NAME, "emailId")
    PHONE_FILTER = (By.NAME, "phoneNumber")
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']"
    )
    RESET_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Reset filters']"
    )

    NO_RECORDS_TEXT = (By.XPATH, "//*[contains(.,'out of 0 records')]")

    # lucide-download SVG is the export icon — no aria-label on the button
    EXPORT_ICON_BUTTON = (
        By.XPATH,
        "//button[.//svg[contains(@class,'lucide-download')]]"
    )
    EXPORT_MODAL = (
        By.XPATH,
        "//div[@role='dialog'] | //div[contains(@class,'modal') and contains(.,'Export')]"
    )
    EXPORT_MODAL_TITLE = (
        By.XPATH,
        "//div[@role='dialog']//*[contains(.,'Export Users')] | "
        "//div[contains(@class,'modal')]//*[contains(.,'Export Users')]"
    )
    # Hidden checkboxes (opacity-0) inside labels in the export modal; is_selected() works
    EXPORT_COLUMN_TOGGLES = (
        By.XPATH,
        "//div[@role='dialog']//label//input[@type='checkbox']"
    )

    def wait_for_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_USER_BUTTON))

    def click_add_user(self):
        self.click(self.ADD_USER_BUTTON)

    def open_filters(self):
        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.EMAIL_FILTER))

    def filter_panel_is_open(self):
        els = self.driver.find_elements(*self.EMAIL_FILTER)
        return bool(els) and els[0].is_displayed()

    def apply_filters(self):
        self.click(self.APPLY_FILTERS_BUTTON)

    def reset_filters(self):
        self.click(self.RESET_FILTERS_BUTTON)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//tbody")))

    def close_filter_panel(self):
        # lucide-x SVG is the close icon — no aria-label on the button
        close_btn = (By.XPATH, "//button[.//svg[contains(@class,'lucide-x')]]")
        els = self.driver.find_elements(*close_btn)
        if els:
            self.driver.execute_script("arguments[0].click();", els[0])

    def filter_by_email(self, email):
        self.open_filters()
        self.enter_text(self.EMAIL_FILTER, email)
        self.click(self.APPLY_FILTERS_BUTTON)

    def filter_by_first_name(self, name):
        self.open_filters()
        self.enter_text(self.FIRST_NAME_FILTER, name)
        self.click(self.APPLY_FILTERS_BUTTON)

    def filter_by_last_name(self, name):
        self.open_filters()
        self.enter_text(self.LAST_NAME_FILTER, name)
        self.click(self.APPLY_FILTERS_BUTTON)

    def filter_by_phone(self, phone):
        self.open_filters()
        self.enter_text(self.PHONE_FILTER, phone)
        self.click(self.APPLY_FILTERS_BUTTON)

    def get_filter_value(self, locator):
        el = self.driver.find_element(*locator)
        return el.get_attribute("value") or ""

    def get_user_row_locator(self, email):
        return (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[.//button[normalize-space()='Edit']][1]"
            % email
        )

    def wait_for_user_row(self, email):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_user_row_locator(email)
            )
        )

    def user_exists(self, email):
        self.filter_by_email(email)
        try:
            self.wait_for_user_row(email)
            return True
        except TimeoutException:
            return False

    def open_user_edit(self, email):
        self.filter_by_email(email)
        row = self.wait_for_user_row(email)
        edit_btn = row.find_element(
            By.XPATH, ".//button[normalize-space()='Edit']"
        )
        edit_btn.click()

    def get_column_headers(self):
        headers = self.driver.find_elements(
            By.XPATH, "//th | //thead//td | //div[@role='columnheader']"
        )
        return [h.text.strip() for h in headers if h.text.strip()]

    def get_visible_row_count(self):
        rows = self.driver.find_elements(By.XPATH, "//tbody/tr[td]")
        if rows:
            return len(rows)
        return len(self.driver.find_elements(By.XPATH, "//tbody/tr"))

    def get_visible_user_emails(self):
        cells = self.driver.find_elements(
            By.XPATH, "//tbody/tr/td[contains(.,'@')]"
        )
        return [c.text.strip() for c in cells if "@" in c.text]

    def get_visible_user_first_names(self):
        rows = self.driver.find_elements(By.XPATH, "//tbody/tr[td]")
        names = []
        for row in rows:
            cells = row.find_elements(By.XPATH, ".//td")
            if cells:
                names.append(cells[0].text.strip())
        return names

    def pagination_controls_present(self):
        locators = [
            (By.XPATH, "//*[contains(.,'Page') and contains(.,' of ')]"),
            (By.XPATH, "//nav[contains(.,'Page')]"),
        ]
        for loc in locators:
            if self.driver.find_elements(*loc):
                return True
        return False

    def get_pagination_text(self):
        locators = [
            (By.XPATH, "//*[contains(.,'Page') and contains(.,' of ')]"),
            (By.XPATH, "//nav[contains(.,'Page')] | //div[contains(@class,'pagination')]"),
        ]
        for loc in locators:
            els = self.driver.find_elements(*loc)
            if els:
                return els[0].text.strip()
        return ""

    def prev_page_button_is_disabled(self):
        # lucide-chevron-left = prev; lucide-chevrons-left = first-page (different icon)
        btn_loc = (
            By.XPATH,
            "//button[.//svg[contains(@class,'lucide-chevron-left') "
            "and not(contains(@class,'lucide-chevrons-left'))]]"
        )
        els = self.driver.find_elements(*btn_loc)
        if els:
            return els[0].get_attribute("disabled") is not None
        return True

    def get_results_per_page_options(self):
        # React Select — click the singleValue div to open, then read role='option' items
        control_loc = (By.XPATH, "//div[contains(@class,'singleValue') and contains(.,'Show')]")
        controls = self.driver.find_elements(*control_loc)
        if controls:
            try:
                controls[0].click()
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@role='option']"))
                )
                opts = self.driver.find_elements(By.XPATH, "//*[@role='option']")
                result = [o.text.strip() for o in opts if o.text.strip()]
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                return result
            except Exception:
                pass
        return []

    # ── Export methods ────────────────────────────────────────────────────────

    def click_export_icon(self):
        self.click(self.EXPORT_ICON_BUTTON)

    def export_modal_is_visible(self):
        els = self.driver.find_elements(*self.EXPORT_MODAL)
        return bool(els) and els[0].is_displayed()

    def get_export_format_options(self):
        # React Select inside the export modal — click to open, read role='option' items
        control_loc = (
            By.XPATH,
            "//div[@role='dialog']//div[contains(@class,'singleValue')]"
        )
        controls = self.driver.find_elements(*control_loc)
        if controls:
            try:
                controls[0].click()
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@role='dialog']//*[@role='option']")
                    )
                )
                opts = self.driver.find_elements(
                    By.XPATH, "//div[@role='dialog']//*[@role='option']"
                )
                result = [o.text.strip() for o in opts if o.text.strip()]
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                return result
            except Exception:
                pass
        return []

    def get_default_export_format(self):
        # React Select singleValue div shows the current selection
        els = self.driver.find_elements(
            By.XPATH, "//div[@role='dialog']//div[contains(@class,'singleValue')]"
        )
        if els:
            return els[0].text.strip()
        return None

    def get_export_column_states(self):
        # Each checkbox has name="firstName" / "lastName" etc.; is_selected() reads state
        toggles = self.driver.find_elements(*self.EXPORT_COLUMN_TOGGLES)
        states = {}
        for i, toggle in enumerate(toggles):
            name = toggle.get_attribute("name") or f"column_{i}"
            states[name] = toggle.is_selected()
        return states

    def export_confirm_button_is_disabled(self):
        # Defensive — export confirm button locator needs DOM confirmation
        locators = [
            (By.XPATH,
             "//div[@role='dialog']//button[contains(.,'Export') "
             "and not(contains(.,'Cancel'))]"),
            (By.XPATH,
             "//div[@role='dialog']//button[contains(@class,'primary') or "
             "contains(@class,'confirm')]"),
        ]
        for loc in locators:
            els = self.driver.find_elements(*loc)
            if els:
                btn = els[0]
                return (
                    btn.get_attribute("disabled") is not None
                    or btn.get_attribute("aria-disabled") == "true"
                )
        return False

    def cancel_export(self):
        self.click((
            By.XPATH,
            "//div[@role='dialog']//button[normalize-space()='Cancel'] | "
            "//div[contains(@class,'modal')]//button[normalize-space()='Cancel']"
        ))


class CreateUserPage(BasePage):

    PAGE_TITLE = (By.XPATH, "//div[normalize-space()='User']")
    NEW_MODE_LABEL = (By.XPATH, "//div[normalize-space()='New']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    SAVE_NEW_BUTTON = (By.XPATH, "//button[normalize-space()='Save new']")

    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    PASSWORD_INPUT = (By.NAME, "password")
    CONFIRM_PASSWORD_INPUT = (By.NAME, "confirmPassword")
    EMAIL_INPUT = (By.NAME, "emailId")
    PHONE_INPUT = (By.NAME, "phoneNumber")
    ROLE_ID_INPUT = (By.NAME, "roleId")
    ROLE_CONTROL = (
        By.XPATH,
        "//input[@name='roleId']/preceding-sibling::div"
    )

    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space()='Yes']")
    CONFIRM_NO_BUTTON = (By.XPATH, "//button[normalize-space()='No']")

    def wait_for_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.visibility_of_element_located(self.NEW_MODE_LABEL))
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))

    def enter_first_name(self, first_name):
        self.enter_text(self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name):
        self.enter_text(self.LAST_NAME_INPUT, last_name)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def enter_confirm_password(self, confirm_password):
        self.enter_text(self.CONFIRM_PASSWORD_INPUT, confirm_password)

    def enter_email(self, email):
        self.enter_text(self.EMAIL_INPUT, email)

    def enter_phone(self, phone):
        self.enter_text(self.PHONE_INPUT, phone)

    def select_role(self, role_name):
        self.click(self.ROLE_CONTROL)
        role_option = (
            By.XPATH,
            "//*[@role='option' and normalize-space()='%s']" % role_name
        )
        try:
            self.click(role_option)
        except TimeoutException:
            raise AssertionError(
                "Role '%s' was not available in the user role dropdown."
                % role_name
            )
        role_id_input = self.wait.until(
            EC.presence_of_element_located(self.ROLE_ID_INPUT)
        )
        self.wait.until(
            lambda driver: role_id_input.get_attribute("value") != ""
        )

    def get_role_dropdown_options(self):
        self.click(self.ROLE_CONTROL)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@role='option']"))
            )
            options = self.driver.find_elements(By.XPATH, "//*[@role='option']")
            result = [opt.text.strip() for opt in options if opt.text.strip()]
        except TimeoutException:
            result = []
        try:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except Exception:
            pass
        return result

    def fill_user_form(
        self,
        first_name,
        last_name,
        email,
        phone,
        password,
        role_name,
        confirm_password=None,
    ):
        if confirm_password is None:
            confirm_password = password
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_email(email)
        self.enter_phone(phone)
        self.enter_password(password)
        self.enter_confirm_password(confirm_password)
        self.select_role(role_name)

    def click_save_new(self):
        self.click(self.SAVE_NEW_BUTTON)

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)

    def confirm_yes_if_present(self, timeout=5):
        short_wait = WebDriverWait(self.driver, timeout)
        try:
            short_wait.until(
                EC.element_to_be_clickable(self.CONFIRM_YES_BUTTON)
            ).click()
            short_wait.until(
                EC.invisibility_of_element_located(self.CONFIRM_YES_BUTTON)
            )
        except TimeoutException:
            return

    def confirm_no(self):
        self.click(self.CONFIRM_NO_BUTTON)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.CONFIRM_NO_BUTTON)
            )
        except TimeoutException:
            pass

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def has_validation_text(self, text):
        return text in self.get_body_text()

    def wait_for_any_text(self, *texts, timeout=15):
        texts_lower = [t.lower() for t in texts]
        WebDriverWait(self.driver, timeout).until(
            lambda d: any(
                text in d.find_element(By.TAG_NAME, "body").text.lower()
                for text in texts_lower
            )
        )


class EditUserPage(BasePage):

    PAGE_TITLE = (By.XPATH, "//div[normalize-space()='User']")
    EDIT_MODE_LABEL = (By.XPATH, "//div[normalize-space()='Edit']")

    FIRST_NAME_INPUT = (By.NAME, "firstName")
    LAST_NAME_INPUT = (By.NAME, "lastName")
    EMAIL_INPUT = (By.NAME, "emailId")
    PHONE_INPUT = (By.NAME, "phoneNumber")

    SAVE_CHANGES_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save changes' or normalize-space()='Update']"
    )
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space()='Yes']")
    CONFIRM_NO_BUTTON = (By.XPATH, "//button[normalize-space()='No']")

    def wait_for_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME_INPUT))
        self.wait.until(lambda d: "/users/create" not in d.current_url)
        self.wait.until(
            lambda d: d.find_element(*self.FIRST_NAME_INPUT).get_attribute("value") not in (None, "")
        )

    def _get_input_value(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        return el.get_attribute("value") or ""

    def _js_set_value(self, locator, value):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script(
            "arguments[0].value = ''; "
            "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));",
            el
        )
        if value:
            el.send_keys(value)

    def get_first_name(self):
        return self._get_input_value(self.FIRST_NAME_INPUT)

    def get_last_name(self):
        return self._get_input_value(self.LAST_NAME_INPUT)

    def get_email(self):
        return self._get_input_value(self.EMAIL_INPUT)

    def get_phone(self):
        return self._get_input_value(self.PHONE_INPUT)

    def set_first_name(self, value):
        self._js_set_value(self.FIRST_NAME_INPUT, value)

    def set_last_name(self, value):
        self._js_set_value(self.LAST_NAME_INPUT, value)

    def set_phone(self, value):
        self._js_set_value(self.PHONE_INPUT, value)

    def click_save_changes(self):
        self.click(self.SAVE_CHANGES_BUTTON)

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)

    def confirm_yes_if_present(self, timeout=5):
        short_wait = WebDriverWait(self.driver, timeout)
        try:
            short_wait.until(
                EC.element_to_be_clickable(self.CONFIRM_YES_BUTTON)
            ).click()
            short_wait.until(
                EC.invisibility_of_element_located(self.CONFIRM_YES_BUTTON)
            )
        except TimeoutException:
            return

    def confirm_no(self):
        self.click(self.CONFIRM_NO_BUTTON)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.CONFIRM_NO_BUTTON)
            )
        except TimeoutException:
            pass

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def has_validation_error(self):
        body = self.get_body_text().lower()
        return (
            "required" in body
            or "invalid" in body
            or "too small" in body
        )

    def wait_for_any_text(self, *texts, timeout=15):
        texts_lower = [t.lower() for t in texts]
        WebDriverWait(self.driver, timeout).until(
            lambda d: any(
                text in d.find_element(By.TAG_NAME, "body").text.lower()
                for text in texts_lower
            )
        )
