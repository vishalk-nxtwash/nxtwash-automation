from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage


class SubscribersPage(BasePage):

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Webhook Subscribers']")
    ADD_BUTTON = (By.XPATH, "//button[contains(.,'Add Webhook Subscriber')]")

    def wait_for_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON))

    def click_add_subscriber(self):
        self.click(self.ADD_BUTTON)

    def get_column_headers(self):
        headers = self.driver.find_elements(
            By.XPATH, "//th | //thead//td | //div[@role='columnheader']"
        )
        return [h.text.strip() for h in headers if h.text.strip()]

    def get_visible_row_count(self):
        rows = self.driver.find_elements(By.XPATH, "//tbody/tr[td]")
        return len(rows) if rows else len(
            self.driver.find_elements(By.XPATH, "//tbody/tr")
        )

    def get_records_count_text(self):
        els = self.driver.find_elements(
            By.XPATH, "//*[contains(.,'out of') and contains(.,'records')]"
        )
        return els[0].text.strip() if els else ""

    def has_no_filter_button(self):
        return not bool(self.driver.find_elements(
            By.XPATH, "//button[contains(.,'Filter by')]"
        ))

    def has_no_export_button(self):
        return not bool(self.driver.find_elements(
            By.XPATH, "//button[.//svg[contains(@class,'lucide-download')]]"
        ))

    def prev_page_button_is_disabled(self):
        btn_loc = (
            By.XPATH,
            "//button[.//svg[contains(@class,'lucide-chevron-left') "
            "and not(contains(@class,'lucide-chevrons-left'))]]"
        )
        els = self.driver.find_elements(*btn_loc)
        return els[0].get_attribute("disabled") is not None if els else True

    def get_row_locator(self, name):
        return (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[.//button[normalize-space()='Edit']][1]" % name
        )

    def wait_for_row(self, name):
        return self.wait.until(
            EC.visibility_of_element_located(self.get_row_locator(name))
        )

    def row_exists(self, name, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.get_row_locator(name))
            )
            return True
        except TimeoutException:
            return False

    def open_edit(self, name):
        row = self.wait_for_row(name)
        btn = row.find_element(By.XPATH, ".//button[normalize-space()='Edit']")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", btn
        )
        btn.click()

    def get_row_actions(self, name):
        row = self.wait_for_row(name)
        btns = row.find_elements(By.XPATH, ".//button")
        return [b.text.strip() for b in btns if b.text.strip()]


class CreateSubscriberPage(BasePage):

    # Input name attributes are best guesses; confirmed after DOM inspection
    NAME_INPUT = (By.NAME, "name")
    ABBREVIATION_INPUT = (By.NAME, "abbreviation")
    # Hidden checkbox following the 'Active Subscriber' label — same pattern as other modules
    ACTIVE_TOGGLE = (
        By.XPATH,
        "//div[normalize-space()='Active Subscriber']"
        "/following-sibling::label//input[@type='checkbox'] | "
        "//div[normalize-space()='Active Subscriber']/..//input[@type='checkbox']"
    )
    SAVE_NEW_BUTTON = (By.XPATH, "//button[normalize-space()='Save new']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space()='Yes']")

    def wait_for_loaded(self):
        self.wait.until(EC.url_contains("/third-party/subscribers"))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_NEW_BUTTON))

    def enter_name(self, name):
        self.enter_text(self.NAME_INPUT, name)

    def enter_abbreviation(self, abbr):
        self.enter_text(self.ABBREVIATION_INPUT, abbr)

    def get_active_toggle_state(self):
        els = self.driver.find_elements(*self.ACTIVE_TOGGLE)
        return els[0].is_selected() if els else None

    def set_active_toggle(self, state):
        current = self.get_active_toggle_state()
        if current is None or current == state:
            return
        label_loc = (
            By.XPATH,
            "//div[normalize-space()='Active Subscriber']/following-sibling::label[1]"
        )
        els = self.driver.find_elements(*label_loc)
        if els:
            self.driver.execute_script("arguments[0].click();", els[0])

    def click_save_new(self):
        self.click(self.SAVE_NEW_BUTTON)

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)

    def confirm_yes_if_present(self, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.CONFIRM_YES_BUTTON)
            ).click()
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.CONFIRM_YES_BUTTON)
            )
        except TimeoutException:
            return

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def has_validation_text(self, text):
        return text.lower() in self.get_body_text().lower()


class EditSubscriberPage(CreateSubscriberPage):

    SAVE_CHANGES_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save changes' or normalize-space()='Update']"
    )
    # Inline X clear buttons confirmed by spec: "Both fields expose an inline clear (X)"
    # Exact locator unconfirmed — best guess using sibling/parent button patterns
    NAME_CLEAR_BUTTON = (
        By.XPATH,
        "//input[@name='name']/following-sibling::button[1] | "
        "//input[@name='name']/..//button[contains(@class,'clear') or @type='button'][1]"
    )
    ABBREVIATION_CLEAR_BUTTON = (
        By.XPATH,
        "//input[@name='abbreviation']/following-sibling::button[1] | "
        "//input[@name='abbreviation']/..//button[contains(@class,'clear') or @type='button'][1]"
    )

    def wait_for_loaded(self, expected_name=None):
        self.wait.until(EC.url_contains("/third-party/subscribers/"))
        self.wait.until(
            lambda d: "/create" not in d.current_url
        )
        self.wait.until(EC.visibility_of_element_located(self.SAVE_CHANGES_BUTTON))
        if expected_name:
            self.wait.until(
                lambda d: (
                    d.find_elements(*self.NAME_INPUT)
                    and d.find_element(*self.NAME_INPUT).get_attribute("value") == expected_name
                )
            )

    def get_name(self):
        el = self.driver.find_element(*self.NAME_INPUT)
        return el.get_attribute("value") or ""

    def get_abbreviation(self):
        el = self.driver.find_element(*self.ABBREVIATION_INPUT)
        return el.get_attribute("value") or ""

    def set_name(self, value):
        el = self.wait.until(EC.element_to_be_clickable(self.NAME_INPUT))
        self.driver.execute_script(
            "arguments[0].value='';"
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
            el
        )
        if value:
            el.send_keys(value)

    def set_abbreviation(self, value):
        el = self.wait.until(EC.element_to_be_clickable(self.ABBREVIATION_INPUT))
        self.driver.execute_script(
            "arguments[0].value='';"
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
            el
        )
        if value:
            el.send_keys(value)

    def click_name_clear(self):
        els = self.driver.find_elements(*self.NAME_CLEAR_BUTTON)
        if els:
            els[0].click()

    def click_abbreviation_clear(self):
        els = self.driver.find_elements(*self.ABBREVIATION_CLEAR_BUTTON)
        if els:
            els[0].click()

    def click_save_changes(self):
        self.click(self.SAVE_CHANGES_BUTTON)
